import requests
from my_app.config import YANDEX_CLIENT_ID, YANDEX_REDIRECT_URI, SECRET_YANDEX


async def exchange_code_token(code):
    token_url = "https://oauth.yandex.ru/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": YANDEX_REDIRECT_URI,
        "client_id": YANDEX_CLIENT_ID,
        "client_secret": SECRET_YANDEX,
    }
    response = requests.post(token_url, headers=headers, data=data)
    return response.json()


async def get_user_data(token_data):
    access_token = token_data.get("access_token")
    user_url = "https://login.yandex.ru/info"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_url, headers=headers)
    return user_response.json()
