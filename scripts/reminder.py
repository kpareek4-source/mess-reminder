import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests

# -------------------------------------------------
# Project setup
# -------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from config import TOPIC

CSV_PATH = ROOT_DIR / "data" / "menu.csv"

TEST_MODE = False

# -------------------------------------------------
# Reminder schedule
# -------------------------------------------------

meal_schedule = {
    (7, 15): "Breakfast",
    (12, 30): "Lunch",
    (16, 45): "Snacks",
    (19, 30): "Dinner"
}

serving_times = {
    "Breakfast": "7:45 AM - 10:15 AM",
    "Lunch": "1:00 PM - 3:00 PM",
    "Snacks": "5:15 PM - 6:45 PM",
    "Dinner": "8:00 PM - 10:15 PM"
}

greetings = {
    "Breakfast": "🌅 Good Morning!",
    "Lunch": "☀️ Hope you're having a great day!",
    "Snacks": "☕ Time for a quick break!",
    "Dinner": "🌙 Good Evening!"
}

meal_tags = {
    "Breakfast": "sunrise",
    "Lunch": "plate_with_cutlery",
    "Snacks": "coffee",
    "Dinner": "crescent_moon"
}

priorities = {
    "Breakfast": "high",
    "Lunch": "high",
    "Snacks": "default",
    "Dinner": "default"
}

# -------------------------------------------------
# Decide today's meal
# -------------------------------------------------

if TEST_MODE:
    today = TEST_DAY
    meal = TEST_MEAL
else:
    now = datetime.now()
    today = now.strftime("%A")
    current_time = (now.hour, now.minute)

    if current_time not in meal_schedule:
        print("Not a reminder time.")
        exit()

    meal = meal_schedule[current_time]

current_date = datetime.now().strftime("%d %B")

# -------------------------------------------------
# Read menu
# -------------------------------------------------

df = pd.read_csv(CSV_PATH)

menu = df[
    (df["Day"] == today) &
    (df["Meal"] == meal)
]

if menu.empty:
    print(f"No {meal} found for {today}")
    exit()

items = menu.iloc[0]["Items"]

# -------------------------------------------------
# Split items
# -------------------------------------------------

food_items = []

for section in items.split(";"):
    for item in section.split(","):
        item = item.strip()

        if item:
            food_items.append(item)

total_items = len(food_items)

# -------------------------------------------------
# Emoji mapping
# -------------------------------------------------

emoji_map = {
    "tea": "🥤",
    "coffee": "🥤",
    "milk": "🥛",
    "bread": "🍞",
    "butter": "🧈",
    "jam": "🍓",
    "cornflakes": "🥣",
    "omelette": "🥚",
    "egg": "🥚",
    "fruit": "🍉",
    "paratha": "🫓",
    "roti": "🫓",
    "rice": "🍚",
    "dal": "🥣",
    "paneer": "🧀",
    "curd": "🥣",
    "idli": "🥞",
    "dosa": "🥞",
    "sambar": "🥣",
    "chutney": "🌿"
}

drink_keywords = [
    "tea",
    "coffee",
    "milk",
    "juice",
    "shake",
    "lassi",
    "chaach"
]

drinks = []
foods = []

for item in food_items:

    lower = item.lower()

    icon = "🍽️"

    for keyword, emoji in emoji_map.items():
        if keyword in lower:
            icon = emoji
            break

    formatted = f"• {item}"

    if any(word in lower for word in drink_keywords):
        drinks.append(formatted)
    else:
        foods.append(formatted)

bullet_list = ""

if drinks:
    bullet_list += "🥤 Drinks\n"
    bullet_list += "\n".join(drinks)
    bullet_list += "\n\n"

if foods:
    bullet_list += "🍛 Food\n"
    bullet_list += "\n".join(foods)

# -------------------------------------------------
# Notification
# -------------------------------------------------

message = f"""{greetings[meal]}

🍽️ {meal} in 30 minutes

📅 {today}, {current_date}

📋 {total_items} items on today's menu

🍴 Today's Menu

{bullet_list}

⏰ Serving Time
{serving_times[meal]}

💡 Don't forget your ID card if it's required.

Enjoy your meal! 😊
"""

print(message)

headers = {
    "Title": f"{meal} Reminder",
    "Tags": meal_tags[meal],
    "Priority": priorities[meal],
    "Markdown": "yes"
}

response = requests.post(
    f"https://ntfy.sh/{TOPIC}",
    headers=headers,
    data=message.encode("utf-8")
)

print(f"\nNotification Status: {response.status_code}")