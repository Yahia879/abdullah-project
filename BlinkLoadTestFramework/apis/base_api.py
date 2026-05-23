import json
import random
import pandas as pd
import re
import os
import uuid
import string

from apis.auth import login_logistics, login_admission, login_shop

LOGISTICS_TOKEN = login_logistics()
ADMISSION_TOKEN = login_admission()
SHOP_TOKEN = login_shop()
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

