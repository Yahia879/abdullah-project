import json
import random
import pandas as pd
import re
import os
import uuid
import string

from apis.auth import login_logistics, login_admission, login_shop, login_shop_manual

LOGISTICS_TOKEN = login_logistics()
ADMISSION_TOKEN = login_admission()
# SHOP_TOKEN = login_shop()

# --- MANUAL SHOP COOKIES (FOR ONE USER) ---
# Paste the two parts of the session token here:
COOKIE_PART_0 = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..Y09fw6EUJ-2n9cX6.Pk3dpga9uOMbGMZfsLtw4zy_zlh3FnhKbzKdHBoAEHBz9s6TfsukwW0H4GTgxSezBS0yyac9UcK8Yc-7uEJq5gud0_kDitkd8swBe1I-pAGsGgGnB_53H35cw-QnwfszIDwHyoUhHhhTrVy-reg96PFV60hgKTiehhwnUZfi1Uqcw3OW-pxavHXnt7cpxpVMM-fNLleM1ET1sWtR1bKapg9TTQlSESLTPiZyjABJRRKQi2MULNfZ-9UdDYNZcne7ctIDmNfoMks7eH6LiEVTgSXZFGOQsj1TJCqNNyeOj4Dxdg_7Xq-axuz3R_KBHGutnT-nGx4VPO1szHQ46NTP2rLyw0uyUWzRM7qhTWZxgBX60rj-f7DT-8RcFDpOnXlVEXJlKfXcs3IV79XFJOXAJRCjI_Bpliknvc7Pu9MS8XkA7v7sUP8y1mZOGH39iyhRkHUdT1vGyaATKvs7Dk0gCi3x2EyHdhXNng4S1Jr67sFKa0-OOcL7u_iE5lN4ARC3TiVdOheqLxZeehaRyoBWDEXBrEn6MJBZRsuP7pOCdxRxmHJJHqWnhIjEY5o7zoSL9UyW6az99BAhl7uxIzTvSX6bt_J4nhemp_yoKMr7DiD9o72do8uoUh-CMs7UCgqN3GteYBFOAHlWR7o0dO3bIeinwK0rY1xDOqIWIFtotnB8gwuVjx6241TQwOaKmGqJOeA_4MuN94CFnxAicyrsvvM3Ygq9Rt0CtSESYAYnLGkuRdyjYvNfKnDU6UF30RTgd1iOPFJO5xnDkSWJzf7r4WXNrx9tSIfTd8tNx4IyrT0ysRo0zpe5Vk02D8MWQFkbcLK_SNbygluBM_BAX9b3r2vxOl4bsNxql3BtCzHAy-0AiWHWL0CIsdc3Rr_2lIF-7CDf6QonTHlW6OIEZKunBfE4SXi7gLbB1U2RDjM8SHn4DCL5I1CLktSjB7eJAa2HLVZ_AUxIsWWJYg8LelSLXUtuWh7gTBnFpL0VWXGTgv3dWwQxSWz69X0-_wmvA8LFjJqVAuCO8HOHyAzxnwJpcQ5y_OT0rCiXbMyyJAMpWZ9KoI6_v1Umpgrf_fIEMyICt12zqWlzcprJKueAkxvx0K44rQIQkMDtaEq646Kt-vhba281BrQc0Gr8r5pmLlslOViyyTm1jOVewlpiIPA-fPIV3AbCpUAdZWZRsFyrcAJlDie-lHW_RvHL_3Xzfrimd9aagM4I6Ww1LrlM1D2gS084IiLOdhI6umIH7dcwgmd_pVGaNGCGjfj8FTe1ulDityXSJOeiU6fLcRnh1DXgWfrDQQJ2ZKb_1GAfWDdyAljLG82mmVnPrX59BQumGSIjP7x5Xw_dcllShz1DFkbIurY_l_9dZvkoBTVoXDqdfiLj_aX3bFJyhXnHiyXo_T3-TeOHeyCEiVI2XDz5TSQMI1arXrRwX19VVz4YeM55L5nFKEbeIkYp2GJyL7RICCEBZczzufo1XvRZMWutLXMD_sB9rRUm7MAkmO7n6FQVT-me3osWW2yV8k8VvE9yJPWjIa9bVivjzNLslnMvTkch82lj0wmuZz4kW4FsEnbGDK_dF4YJHji6B1hBbR4V3FGd9-IOImSUCTb_XcwNnkspQn2J8n0BHWc-9FcIsfkF-3UKLd0w_1_Xmq4T-oPHG-g5t0VW-nJcTIoqFcFM8v8aVm1zvs2JmMa7QGbvFHuYeg80gG24KcIM_1AzrGHHbOlhjToJMp1zjSbADihBSfVIYRA-jBUC5b4urTe_V-S6InkM5lmfmCyriM_3jCOZt49DgKUFb8FfhWmYIOAnC_d5xYvEUkb_zbIIcH0V5sUatQkpK2TYPtu0HhiCoMp6wLgv3NG4FdxKJKK3bvdNLwjsKikZVlsIuaKJNZ8PiBoQNgD5HJzqxw2Zd19UZPm_UKa3ZSOZsf59kSfTuWcmaTlzdfFa15_mwAKhkQR1Szv4FkQBiQtqdc-t9FdQq3P7-HW-dkMnu1YVjofrDidRY5cF9V-XKtUeVnHzmHq3tRyfkkmnppYhjzPCIkxDaFXfwQdhsODekmuPCcpvc5HVrMeP8jAxUFDCoq0oiYTHYlzXMPW1FiCSfJr11Pk_Pz-YQq_jcUjD5X3cfvNkIeons58kpRS0boU7pkVAoIu4SgUd7EVebfqfcI8f0IjsUjdibzPMvrtJBO9mZSfsjrT2PSPyOIw6LCZ1WpIQeaLhDkxQFT5Y2RJYvDAKBwY0dEZ9YYsWdpuWY6_e_cs0TfeCGutNqlz6-GyVDsviSEoaDUqHPo9mQFg2MsVXAib1fvT25fLzlgx71ksYqLX3Rpj74fXIpdJ_FStyBrNYBF2mtdPBvIW8E1SobcXKa1abam2JloUcNPkCCQTzRXBEgSkxuiTFipXimemdt_4jJN2e64sZLX69YgLiUeX54q5qLJSr1njlQzUJCsM3fBQAm2PCxxaHmV7WZ_GfLzsGYFB-2iW_XzDURM2qPi6vIXITu468VcF1WNLI10Zoo-w1_-JKcUOYn_ggv-FNLbTSXGHMWMg6GqlIel20cn4NofBwxTovdoDF03kWUd8hIJEnr3g1UIUO-OGj3idzqgi4Yab_VgTei9uYMR3ZBCvWR382Q7B55fUYQHJEk2qyGi0xc3p_C2NAX0D6J01rApslKSTembC7ghmkVdXqRmhifrKJi5pQOolQkozXA5Mldbax9W0mfL75WP-2UzpBo2E60ZTtdZK_r_obVLC-xbqaY1hDg-q1_fDRIJIBhcMxDfE1gE4fzCSJNjakx3iqgw7uJ9IgIo9rLzwLPTAc2fDoAMtTfAfsn8nkfxUV8dB4-Q90i1_dibfA-ZcBrs7WD11rpo8gjEk1NP-IGLmNGPRGMEIQmfhcCM4CyWWKrEzGJN84BQoRGtnHs8jHKBh0KCtlsFg8Fg1RdtnN0aJBJq-KOGFwP4ntCS-KtnyslQgno-gWDgcgoUE77U0OoggooLeDWPWeWupYadvNYEZUYYjPFQKNjqB-ecxx2zjUVZweghLuyfNFMc0sMdEo7t88Od3XR-dAWVnvl5rblEuD3GPGnE_fOHwcVpx5xdqlzO6k9b_G6yHeWNzaPxgzwCjwHYm2mUS-VsYQoW6kMJ0cmKky88OGvk1vggPeW0OdI5a1mmgWzLYegLlSPAIiLwFgq_cBFR0dfrIw62Qw8NfGTbwbgP3hsqUmGxfnGYuzKq0NKxeo-RJX1Mq9c-R9-IPy1RPuF76QodHfe0vforr60J4einjdc8KogRZACJq0B4b-6Mr7GMtvrNQ2GW0RKn1iOfkVS8IocV4JSCrSFOvmqsbCQn7z12peXyFGREFyiLGqnCojbHQ8kcFywcXPI5skG2B3GkQ5vo0qIlKo1Z3-J2rHjFaf0fIXxIObzHW5QDpkel4wP2EL_N9wrJGfy0wxV4JwFO7T5uSQAIQXPN5yg8e40j2kbArTmMEd_vfzKHMd45x4woj6JExHprhQeeq_Bp0Yo7dtIex5EGahdzlrw5ac98iz6wSG9I-vnVxKZrMLKp8O0GLUDODpbKuAOBavpJt-oSLJ-eRqpMbfpgRoOKMAPXLflOEuMWQ0SHAkek3kMqAWM2a1z__hrzzu_kaNmjB-H2BEiGfRAVE0ZSnIzi8WC_y4VMOz2LpNMF8RqBNbxmPSDJaSVaAwNmkz3zX9EnHiEnJZOBZtHhDuz624TLJ7NRiaprnwyGULlxSq5cNOBLj06zTvDw8itrVLMULGp8nJp4Q4vhy5Id0fjNsqIjYT29k5t5yr0qua6Wj8nPGYrtF1E7D1bLkUhFEuxg_oEI4hcmG9MXZw1dGE1ADbj9rTYpGW0c-zX7GHFptwhIR8xQFy6lEy-OGGN3t48pfInnSDoJ1"
COOKIE_PART_1 = "C-KcHvKsyhvSwHr6fZF-c_8_Bku5NKOAnzSs4eNWsCsc_YXugrrCN-tVHS-ARwb6mYaBJnjjaVwoLV0b9ltSP48Pp6oFkUTCyd3mW7Go8ajsZ1Q437MqMAdU1zyF1HhtghXm44SWek98-m0zFruZnA-rUtsM_EMdPsbanXdZE0nmJGjF_JE2kVJnMk7jFZTMI9HR2ugaQaKgvdybfGqwsC2ENsmqSUaQQtUSJfRUplA_o-tR9IW18nBSm73_EdS5gX4SdZBHczmshD1kQ4HWiLXWYHUuJyUYWbDcSfh0cDFmWwXUBXWznmcPwKJMAkfjeAILd8o8uNLxBEQ3EK4jO01i3Mp7qzdxDup9AiEL7wozZiWgFESbr8qbxryC2X6Mfxvuc2lGvxJz6CnPeYPNEnacohAd44MmoCFwuCbTiJTGm7uZDhyy7eNg1kZVBVcrn7orfiMi2re18Q_udpNa9xvd_snmXDUxkuCiU3-xWvUepAHXORCvcPAXl6sOdB2SDn0NoypS5HI5F1MQPz7H42hyEG9WNnmACBhQ0H-85PGap4r3CuEI4cD9hcnYxYc_h_mi-9LClMq7IeFjOSk8VL6G0P3HWgrRR8jvF_hrJHBmxoOQ0ztrzDjOyJL0qqIxa8jDfcTDli_CGKrAzrQ9KO06rNSfu8yUHW7aveazG1B1CZQg8VkM4b8VkuPVsD7bhqAss_U4YxjE7GNqeKLD5zFBlYr-_t83UQaOYXKRicUihS38uVuxDh0kzUu3yG3ZSwNfL-9tl2Ws2HTA0n6jMm6aeqJI-II-PTTbQGUoFOlMm2bsiC9dC3AupBGVMic2VrFFZRPxR6E1CxBSfoc3mrOweffbgIB5vDlf6IbinXKsySU1pu1IYOv-ebEdWSfGXxMVZJhM79VWuB1FqtG16bn42tLESFGMPtY7AI84I3MzissazN64LTw9i94TJm9liXkLLCmNJMRxW7AkMhHLcp9lxvY5coAQIfDsUd4Mu8fy68v-CN1zu84DpEW-IUH1qINy2eMHHzZwuNXsmpyRlCpkKFhfjKsAGUMuzjzX0lts1JtFTzxIggVQhu1Ti3LekmHAiuPEupXm19fbC5XhhAMzcdBhnLo51tubFVr1MQ9DltrQ8uaeA14iDdVuuTzHVgpDO7s1CnLg83-OHGr3jnyqVBgRCA-Uc0I91gk2dB6XEJf3_sbkW49DeM4cLWSH7_UEreTgqIvbv3x1kTtxwrCaisEGfcNA1gpvq4rB6W-469QWi5oo-W8BpGxKvZhFTX3YlFHmh3LqgJT1cbnO2AJzMwn97eXNm7fPq99uCDE7x-82JM_P3WeXczKZfFktSdejDSg.-FfDuZxd1sOX3Xdh1WOD3g"

# This will combine them and fetch the real SHOP_TOKEN automatically
SHOP_TOKEN = login_shop_manual(COOKIE_PART_0, COOKIE_PART_1)
# ------------------------------------------
APPSYNC_TOKEN = os.getenv(
    "BLINK_APPSYNC_TOKEN",
    "eyJhbGciOiJSUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzLUJqMGJDcEhqakJnTGhuUFE1cldENmF6SkNNOVFSUGxYX05OcVNSRGpJIn0.eyJleHAiOjE3Nzk0NDkxNzcsImlhdCI6MTc3ODIzOTU3NywianRpIjoib25ydHJvOjljZjBmNzc4LTZhYWItMGU4OC1lMWMzLTg3OWU4OTczZGRjNiIsImlzcyI6Imh0dHBzOi8vZGV2LWlkLmJsaW5rLmdsb2JhbC9yZWFsbXMvYmxpbmstaWQiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMGJkNjAwOTYtZWZkYS00NTllLWJiYmMtMmE4Y2QzMzJiMDRiIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibm9pdHMtYWNjZXNzIiwic2lkIjoiYTZhYjFiZWEtY2E2ZS0zZGY3LThjZTAtZThhNzQ5OWE2OWJmIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2Rldi1zaG9wLmJsaW5rLmdsb2JhbC8iXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLWJsaW5rIGlkIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwiZGVsZXRlLWFjY291bnQiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIGNvZ25pdG86Z3JvdXBzIGN1c3RvbS1hdXRoIiwiY29nbml0bzpncm91cHMiOiJhZG1pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdXRoX3RpbWUiOjE3NzgyMzk1NzcsIm5hbWUiOiJtYW1ob3VkIGFtcGxpZnl1c2VyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWFobW91ZCthbXBsaWZ5ZGV2QGJsaW5rLmdsb2JhbCIsImdpdmVuX25hbWUiOiJtYW1ob3VkIiwiZmFtaWx5X25hbWUiOiJhbXBsaWZ5dXNlciIsImVtYWlsIjoibWFobW91ZCthbXBsaWZ5ZGV2QGJsaW5rLmdsb2JhbCJ9.YjSJmWEmqba3IXc-Mv0oUwqmd0Mfu0lJhBdEU849-Rfi9uQZGKltC6uGSE7EFOCjtWCv9W03yaHPPJMBtnab2ZW-dmONwqv2EH2HWR7uyxUmV4RDPWJ5O4fWFumakQQPUjievC6ywB0VXoGGoIxvt-CGxQxwBi4HG55Daamq7oFy4mJ-KtXfzDueDcURCEKTdX8Op7Y71mfdP8V9SkD_PbTFt3MD4_1WoYTwXzSN0cuYTmP-0GdqvurfDSAt7G69dgMjGrWQ53RiE-2CeXz8G6dqgyqrfVYhJukZO4p_h8zUmiMzuhWY2KRS-f0TnJ6r_7D99DYX32_oniqffeBrKw",
)

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Load test",
    "Authorization": f"Bearer {LOGISTICS_TOKEN}",
    "Origin": "blink.global"
}


orgapp_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Load test - OrgApp",
    "Authorization": f"Bearer {LOGISTICS_TOKEN}",
    "Origin": "blink.global",
    "X-App-Type": "org-app"
}

admission_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Load test - Admission",
    "Authorization": f"Bearer {ADMISSION_TOKEN}",
    "Origin": "blink.global",
    "X-App-Type": "admission"
}

shop_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Load test - Shop",
    "Authorization": f"Bearer {SHOP_TOKEN}",
    "Origin": "blink.global",
    "X-App-Type": "shop"
}

appsync_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Load test - AppSync",
    "Authorization": f"Bearer {APPSYNC_TOKEN}",
    "Origin": "blink.global"
}

letters = "qwertyuioplkjhgfdsazxcvbnm"
numbers = "0123456789"
ssoid_list = []
email_list = []
sessions_list = []
badge_qr_codes = []


adjectives = ["happy", "clever", "brave", "bright", "calm", "eager", "fair", "kind", "proud", "wise", 
              "bold", "busy", "cool", "free", "nice", "rich", "safe", "warm", "young", "sweet"]
              
nouns = ["apple", "book", "city", "door", "earth", "field", "game", "house", "island", "journey", 
         "king", "light", "music", "night", "ocean", "paper", "queen", "river", "story", "time"]


first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
               "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", 
               "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy", "Matthew", "Lisa", 
               "Anthony", "Margaret", "Mark", "Betty", "Donald", "Sandra"]
               
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", 
              "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", 
              "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", 
              "Walker", "Hall", "Allen", "Young", "King", "Wright"]

def load_xlsx_file():
    try:
        
        xlsx_path = "resources/full_users_data.xlsx"
        
        if not os.path.exists(xlsx_path):
            print(f"Warning: {xlsx_path} not found. Trying fallback to ssoid.xlsx")
            xlsx_path = "ssoid.xlsx"
            
        df = pd.read_excel(xlsx_path)
        global ssoid_list, email_list
        
        
        if "Single Sign On ID" in df.columns:
            ssoid_list = df["Single Sign On ID"].tolist()
        elif "ssoid" in df.columns:
            ssoid_list = df["ssoid"].tolist()
        else:
            raise Exception("Single Sign On ID column not found in the Excel file")
            
        if "Email" in df.columns:
            email_list = df["Email"].tolist()
        elif "email" in df.columns:
            email_list = df["email"].tolist()
        else:
            email_list = df.iloc[:, 1].tolist() if len(df.columns) > 1 else []
        
        print(f"Loaded {len(ssoid_list)} ssoIDs and {len(email_list)} emails from {xlsx_path}")
        return True
    except Exception as e:
        print(f"Error loading xlsx file: {e}")
        return False

def load_json_file():
    global sessions_list
    try:
        csv_path = "resources/session_ids.csv"
        
        if not os.path.exists(csv_path):
            print(f"Warning: {csv_path} not found. Trying fallback to sessions.json")
            
            with open("sessions.json", "r") as file:
                content = file.read()
                pattern = r'"id"\s*:\s*"([^"]+)"'
                sessions_list = re.findall(pattern, content)
                print(f"Loaded {len(sessions_list)} session IDs from JSON file")
            return True
            
        sessions_df = pd.read_csv(csv_path)
        
        if len(sessions_df.columns) > 0:
            # Get the name of the first column
            first_column = sessions_df.columns[0]
            sessions_list = sessions_df[first_column].tolist()
            print(f"Loaded {len(sessions_list)} session IDs from CSV file")
            return True
        else:
            print("Error: CSV file has no columns")
            return False
    except Exception as e:
        print(f"Error loading session IDs: {e}")
        return False


def load_badge_qr_codes():
    global badge_qr_codes
    try:
        path = "resources/attendees.json"
        with open(path) as f:
            data = json.load(f)
        badge_qr_codes = [a["badgeId"] for a in data if a.get("badgeId")]
        print(f"Loaded {len(badge_qr_codes)} badge QR codes from {path}")
        return True
    except Exception as e:
        print(f"Error loading badge QR codes: {e}")
        return False


load_xlsx_file()
load_json_file()
load_badge_qr_codes()

def generate_email():
    return random.choice(email_list) if email_list else "test@example.com"

def generate_string():
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adj}_{noun}"

def generate_numbers():
    return random.randint(1, 1000000)

def generate_name():
    first = random.choice(first_names)
    last = random.choice(last_names)
    return f"{first} {last}"

def generate_user_id():
    if ssoid_list:
        return random.choice(ssoid_list)
    return 'random-user-id'

def generate_event_id():
    return "112"

def generate_badge_qr_code():
    return random.choice(badge_qr_codes) if badge_qr_codes else "no-qr-code-loaded"

def generate_session_id():
    return random.choice(sessions_list) if sessions_list else "session-123"

def generate_id():
    return str(uuid.uuid4())

def generate_bool():
    return random.choice([True, False])

def generate_url():
    new_url = 'https://linkedin.com/kasjhdkajsd'
    return new_url

def generate_group():
    new_group = '22222'
    return new_group

def generate_list():
    new_list = []
    for i in range(0, 5):
        new_list.append('random')
    return new_list

def generate_email_user_id():
    if not email_list or not ssoid_list:
        return "test@example.com", "random-user-id"
        
    max_index = min(len(email_list), len(ssoid_list)) - 1
    if max_index < 0:
        return "test@example.com", "random-user-id"
        
    random_index = random.randint(0, max_index)
    new_email = email_list[random_index]
    new_user_id = ssoid_list[random_index]
    return new_email, new_user_id

def generate_country():
    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia",
        "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
        "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil",
        "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada",
        "Cape Verde", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
        "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
        "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
        "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia",
        "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
        "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
        "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
        "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho",
        "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi",
        "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
        "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
        "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
        "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
        "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
        "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
        "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
        "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan",
        "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
        "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
        "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
        "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
        "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]
    return random.choice(countries)

def generate_company_size():
    company_sizes = [
       "1 - 10 employees (Startup / Small Business)",
        "11 - 50 employees (Small Business)",
        "51 - 250 employees (Medium Business)",
        "251 - 1,000 employees (Large Business)",
        "1,001 - 5,000 employees (Enterprise)",
        "More than 5,000 employees (Global Enterprise)"
    ]
    return random.choice(company_sizes)

def generate_budget_range():
    budget_ranges = [
       "Less than £10000",
        "£10000 - £50000",
        "£50000 - £100000",
        "£100000 - £500000",
        "Over £500000",
        "Prefer not to say"
    ]
    return random.choice(budget_ranges)

def generate_age_group():
    age_groups = [
       "16-17",
        "18-21",
        "21-25",
        "26-35",
        "36-45",
        "46-55",
        "56-65",
        "Over 65"
    ]
    return random.choice(age_groups)

def generate_industry():
    industries = [
            "Accounting",
        "Administrative and Support Services",
        "Advertising Agency",
        "Aerospace & Aviation",
        "Agriculture, Forestry and Mining",
        "Animation and Post-Production",
        "Apparel & Fashion",
        "Appliances, Electrical and Electronics Manufacturing",
        "Architecture and Planning",
        "Artists and Writers",
        "Arts Management",
        "Audio and Video Equipment Manufacturing",
        "Automotive",
        "Banking",
        "Biotechnology Research",
        "Blockchain Services",
        "Book and Periodical Publishing",
        "Broadcast Media Production and Distribution",
        "Business Consulting and Services",
        "Business Intelligence Platforms",
        "Cable and Satellite Programming",
        "Capital Markets",
        "Caterers",
        "Chemical Manufacturing",
        "Cinemas, Theatres and Event Spaces",
        "Civic and Social Organisations",
        "Civil Engineering",
        "Climate Data and Analytics",
        "Climate Technology Product Manufacturing",
        "Computer Games",
        "Computers and Electronics Manufacturing",
        "Construction",
        "Consumer Services",
        "Creative Agency",
        "Cybersecurity & Authentication",
        "Data Infrastructure and Analytics",
        "Design Services",
        "E-Learning Providers",
        "Education",
        "Electric Power",
        "Electrical Equipment Manufacturing",
        "Entertainment Company",
        "Environmental Services",
        "Events",
        "Film & Media Production",
        "Financial Services",
        "Food and Beverage",
        "Fundraising",
        "Furniture & Home",
        "Geospatial Technologies",
        "Governance, Risk and Compliance",
        "Government Administration",
        "Graphic Design",
        "Health and Wellness",
        "Healthcare",
        "Hospitality",
        "Human Resources and Staffing",
        "Import and Export",
        "Information Technology",
        "Insurance",
        "Intellectual Property Services",
        "International Trade and Development",
        "Internet Services",
        "Investment Banking",
        "Jewelry & Watches",
        "Laboratories",
        "Law Firms",
        "Legal Services",
        "Lifestyle",
        "Management Consulting",
        "Manufacturing",
        "Marketing and Advertising",
        "Mass Media",
        "Medical Devices",
        "Music",
        "Nanotechnology",
        "Nonprofit Organization Management",
        "Oil and Energy",
        "Online Media",
        "Outsourcing/Offshoring",
        "Pharmaceuticals",
        "Public Relations and Communications",
        "Publishing",
        "Real Estate",
        "Recycling",
        "Renewable Energy",
        "Restaurants",
        "Retail",
        "Robotics",
        "Social Media",
        "Software Development",
        "Sports",
        "Staffing and Recruiting",
        "Technology",
        "Telecommunications",
        "Textiles",
        "Transportation/Trucking/Railroad",
        "Utilities",
        "Venture Capital and Private Equity",
        "Video Games",
        "Warehousing",
        "Waste Management",
        "Wholesale",
        "Wine and Spirits",
        "Writing and Editing",
        "Youth Development",
        "Zoos and Aquariums",
        "Apparel & Fashion"
    ]
    return random.choice(industries)

