from ..http.qxbroker import Browser

class Login(Browser):
    """Class for Quotex login resource."""

    async def __call__(self, username, password, email_pass, user_data_dir=None):
        """Method to get Quotex API login http request.
        :param str username: The username of a Quotex server.
        :param str password: The password of a Quotex server.
        :param str email_pass: The password of a Email.
        :param str user_data_dir: The optional value for path userdata.
        :returns: The instance of :class:`playwright.cookies`.
        """
        self.user_data_dir = user_data_dir
        self.username = username
        self.password = password
        self.email_pass = email_pass
        await self.get_cookies_and_ssid()
