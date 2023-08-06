import requests as _requests
import os as _os


def send_line(message, receiver_api_key=None):
    """
    https://qiita.com/iitenkida7/items/576a8226ba6584864d95(How to get api key)
    return requests.post()
    """
    receiver_api_key = receiver_api_key or _os.getenv('umihico_line_api_key')
    url = "https://notify-api.line.me/api/notify"
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": "Bearer " + api_key}
    data = {"message": message}
    response = _requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response
