import os
import re
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from ..http.automail import get_pin
from ..utils.playwright_install import install
from playwright.async_api import Playwright, async_playwright, expect
from playwright_stealth import stealth_async


class Browser(object):
    user_data_dir = None
    base_url = 'qxbroker.com'
    https_base_url = f'https://{base_url}'
    username = None
    # headless=False
    password = None
    email_pass = None
    args = [
        '--disable-web-security',
        '--no-sandbox',
        '--disable-web-security',
        '--aggressive-cache-discard',
        '--disable-cache',
        '--disable-application-cache',
        '--disable-offline-load-stale-cache',
        '--disk-cache-size=0',
        '--disable-background-networking',
        '--disable-default-apps',
        '--disable-extensions',
        '--disable-sync',
        '--disable-translate',
        '--hide-scrollbars',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
        '--ignore-certificate-errors',
        '--ignore-ssl-errors',
        '--ignore-certificate-errors-spki-list',
        '--disable-features=LeakyPeeker',
        '--disable-setuid-sandbox'
    ]

    def __init__(self, api):
        self.api = api

    async def run(self, playwright: Playwright) -> None:
        if self.user_data_dir:
            browser = playwright.firefox
            context = await browser.launch_persistent_context(
                self.user_data_dir,
                headless=False,
            )
            page = context.pages[0]
        else:
            browser = await playwright.firefox.launch(
                headless=False,
            )
            context = await browser.new_context()
            page = await context.new_page()
            await stealth_async(page)
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
        })
        await page.goto(f"{self.https_base_url}/en/sign-in")
        if page.url != f"{self.https_base_url}/en/trade":
            # Click on the input element for email
            await page.click('xpath=/html/body/bdi/div[1]/div/div[2]/div[3]/form/div[1]/input')

            # Fill in the input element for email with the username
            await page.fill('xpath=/html/body/bdi/div[1]/div/div[2]/div[3]/form/div[1]/input', self.username)

            # Click on the input element for password
            await page.click('xpath=/html/body/bdi/div[1]/div/div[2]/div[3]/form/div[2]/input')

            # Fill in the input element for password with the password
            await page.fill('xpath=/html/body/bdi/div[1]/div/div[2]/div[3]/form/div[2]/input', self.password)

            # Click on the button to sign in
            await page.click('xpath=/html/body/bdi/div[1]/div/div[2]/div[3]/form/button')


            
            async with page.expect_navigation():
                await page.wait_for_timeout(10000)
                soup = BeautifulSoup(await page.content(), "html.parser")
                if "Insira o código PIN que acabamos de enviar para o seu e-mail" in soup.get_text():
                    pin_code = await get_pin(self.username, self.email_pass)
                    if pin_code:
                        code = pin_code
                    else:
                        code = input("Insira o código PIN que acabamos de enviar para o seu e-mail: ")
                    """await page.evaluate(
                        f'() => {{ document.querySelector("input[name=\\"code\\"]").value = {int(code)}; }}')"""
                    try:
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").click()
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").fill(code)
                        await page.get_by_role("button", name="Entrar").click()
                    except:
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").click()
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").fill(code)
                        await page.get_by_role("button", name="Entrar").click()
        await page.wait_for_timeout(5000)
        cookies = await context.cookies()
        source = await page.content()
        soup = BeautifulSoup(source, "html.parser")
        user_agent = await page.evaluate("() => navigator.userAgent;")
        self.api.session_data["user_agent"] = user_agent
        script = soup.find_all("script", {"type": "text/javascript"})
        if not script:
            await context.close() if self.user_data_dir else await browser.close()
            return
        settings = script[1].get_text().strip().replace(";", "")
        match = re.sub("window.settings = ", "", settings)
        token = json.loads(match).get("token")
        self.api.session_data["token"] = token
        output_file = Path(os.path.join(self.api.resource_path, "session.json"))
        output_file.parent.mkdir(exist_ok=True, parents=True)
        cookiejar = requests.utils.cookiejar_from_dict({c['name']: c['value'] for c in cookies})
        cookies_string = "_ga=GA1.1.1907095278.1691245340; referer=https%3A%2F%2Fquotexbrokerlogin.com%2F; lang=pt; "
        cookies_string += '; '.join([f'{c.name}={c.value}' for c in cookiejar])
        self.api.session_data["cookies"] = cookies_string
        output_file.write_text(
            json.dumps({"cookies": cookies_string, "token": token, "user_agent": user_agent}, indent=4)
        )
        await context.close() if self.user_data_dir else await browser.close()

    async def main(self) -> None:
        async with async_playwright() as playwright:
            # install(playwright.firefox, with_deps=True)
            await self.run(playwright)

    async def get_cookies_and_ssid(self):
        await self.main()