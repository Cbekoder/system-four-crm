import json
import urllib.parse
import requests


class TelegramService:
    def __init__(self, bot_token):
        self.bot_token = bot_token

    def send_message(self, chat_id, text, app_url=None):
        # encoded_message = urllib.parse.quote(text)
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        try:
            prev_params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
            }
            if app_url:
                prev_params["reply_markup"] = json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "🔗 App ga o'tish",
                                    "url": app_url,
                                }
                            ]
                        ]
                    }
                )
            response = requests.post(
                url=url,
                params=prev_params,
            )
            return response.json()
        except Exception as e:
            print(e)
            return None
