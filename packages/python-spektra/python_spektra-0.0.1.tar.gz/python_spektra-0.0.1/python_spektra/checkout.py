import requests

def validate_transaction(token, public_key, secret_key):
    VERIFY_URL = "https://api.spektra.co/wallets/transaction/verify/"
    r = requests.post(
        VERIFY_URL,
        json={
            "token": token,
            "public_key": public_key
        },
        headers={
            "Authorization": "Bearer {0!s}".format(secret_key)
        }
    )
    if r.status_code == 200:
        return True, r.json()
    elif r.status_code == 403:
        return False, "Invalid credentials"
    elif r.status_code == 404:
        return False, "Not found"
    elif r.status_code == 400:
        return False, "a token is required"
    else:
        return False, "Something went wrong"

if __name__ == "__main__":
    PUBLIC_KEY = "jaAI1bWuvE8WKIRweBPA"
    SECRET_KEY = "S60Cxu00B1hvmfalHTw7"
    token = "1yTCFtUYWY9dods02yjgV0xCgcw14us-_yZOIANR44Bm02v8HACQmsmaYr_BwWzKrZ96H3APJXswsWjeWOxPESrBMtoc6tuCYYNg-zQwhOiHIbI2WkcvdVD6oraFyiRn8oxvOarDzmwsXfxiTwqkRu75Ewux-pgtvkXNzW24rw5E4HmQib2j2h-jt8EEUOu76GaybBAAAAAg"
    p = validate_transaction(token=token, public_key=PUBLIC_KEY, secret_key=SECRET_KEY)
