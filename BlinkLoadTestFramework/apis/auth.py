import os
import requests

LOGISTICS_LOGIN_URL = os.getenv(
    "BLINK_LOGISTICS_LOGIN_URL",
    "https://dev-foundation-api-admin.blink.global/api/v2/mobile-logistics/login",
)

LOGISTICS_USERNAME = os.getenv("BLINK_LOGISTICS_USERNAME", "testingtesting")
LOGISTICS_PASSWORD = os.getenv(
    "BLINK_LOGISTICS_PASSWORD",
    "0822dae81bd1c4dd2d4e054ea0cebe31c0eac7ed6210b645bc262db7a0f5cd13",
)
LOGISTICS_DEVICE_ID = os.getenv(
    "BLINK_LOGISTICS_DEVICE_ID",
    "484135f068e22a079c6066751248325c2a64ce2482ded67f56ee72cd0dc406c8",
)

ADMISSION_LOGIN_URL = os.getenv(
    "BLINK_ADMISSION_LOGIN_URL",
    "https://dev-foundation-api-admin.blink.global/api/v3/admission-portal/login",
)

SHOP_SESSION_URL = os.getenv(
    "BLINK_SHOP_SESSION_URL",
    "https://dev-shop.blink.global/api/auth/session",
)


# OrgApp uses mobile-logistics realm; Admission uses admission-portal realm; Shop and AppSync use Keycloak.
def login_logistics():
    resp = requests.post(
        LOGISTICS_LOGIN_URL,
        json={
            "username": LOGISTICS_USERNAME,
            "password": LOGISTICS_PASSWORD,
            "os_name": "android",
            "device_id": LOGISTICS_DEVICE_ID,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["token"]


def login_admission():
    resp = requests.post(
        ADMISSION_LOGIN_URL,
        json={
            "username": LOGISTICS_USERNAME,
            "password": LOGISTICS_PASSWORD,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["token"]


# Pulls a fresh Keycloak access token using manually provided cookies
def login_shop_manual(cookie_0, cookie_1):
    if not cookie_0 or not cookie_1:
        print("[auth] Manual cookies not set — Shop tasks will 401")
        return ""
    try:
        resp = requests.get(
            SHOP_SESSION_URL,
            cookies={
                "__Secure-next-auth.session-token.0": cookie_0,
                "__Secure-next-auth.session-token.1": cookie_1,
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json().get("accessToken", "")
    except Exception as e:
        print(f"[auth] login_shop_manual failed: {e}")
        return ""


# Pulls a fresh Keycloak access token from the dev-shop NextAuth session endpoint
# using browser session cookies. Cookies expire ~30 days; access token refreshes on each call.
def login_shop():
    cookie_0 = os.getenv("BLINK_SHOP_COOKIE_0", "")
    cookie_1 = os.getenv("BLINK_SHOP_COOKIE_1", "")
    if not cookie_0 or not cookie_1:
        print("[auth] BLINK_SHOP_COOKIE_0/1 not set — Shop tasks will 401")
        return ""
    try:
        resp = requests.get(
            SHOP_SESSION_URL,
            cookies={
                "__Secure-next-auth.session-token.0": cookie_0,
                "__Secure-next-auth.session-token.1": cookie_1,
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json().get("accessToken", "")
    except Exception as e:
        print(f"[auth] login_shop failed: {e}")
        return ""
