import requests

def send_callback(callback_url: str, payload: dict) -> bool:
    """Отправка callback запроса"""
    try:
        response = requests.post(
            callback_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Callback sent to {callback_url}: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending callback to {callback_url}: {e}")
        return False
