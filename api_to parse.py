from dotenv import dotenv_values
import requests

# Load environment variables
env_vars = dotenv_values('.env')
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + env_vars['Google_API_KEY']  # Google API key
headers = {"Content-Type": "application/json"}


# Example usage with the provided sample messages
messages = """
⏰ Time Zone: UTC +17
CURRENCY PAIR :USD/CHF 
START TIME; 11: 00;PUT 🟩

CLOSE TIME: 09:05

1st GALE —> TIME FOR 19:10
2nd GALE—> TIME FOR 21:15

[↗️ Tap to access your broker
⭕️](https://broker-qx.pro/sign-up/?lid=468019) Not sure how to trade yet? [Click here](https://t.me/c/1949005573/2083)
"""

data = {"contents": [{"parts": [{"text": """
Answer the following questions from below paragraph the default Duration is 5 Min , also don't mention  (default) & only return question and answer format is 1: Start Time: 09:00

1:Start Time
2:Currency
3:Duration
4:TL-1 
5:TL-2
6:Time Zone
\n\n\n"""
+ messages}]}]}
        # Make the API request
response = requests.post(api_url, headers=headers, json=data)
        # Parse the JSON response and extract the text value
response_data = response.json()
if 'candidates' in response_data and len(response_data['candidates']) > 0 and 'content' in response_data['candidates'][0]:
            content_parts = response_data['candidates'][0]['content']['parts']
            text_value = ' '.join([part['text'] for part in content_parts])
            print(text_value)