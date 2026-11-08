import pdfplumber
import pandas as pd

# Produces a draft only: pdfplumber can merge words (e.g. "KadhaiPaneer")
# and split wrapped dishes, so review data/menu.csv before committing.

PDF_PATH = "data/menu.pdf"
CSV_PATH = "data/menu.csv"

days = {
    "MONDAY": "Monday",
    "TUESDAY": "Tuesday",
    "WEDNESDAY": "Wednesday",
    "THURSDAY": "Thursday",
    "FRIDAY": "Friday",
    "SATURDAY": "Saturday",
    "SUNDAY": "Sunday"
}

rows = []

with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            for row in table:

                # Skip empty or incomplete rows
                if not row or len(row) < 5:
                    continue

                day = (row[0] or "").strip().upper()

                # Skip header/footer rows
                if day not in days:
                    continue

                day = days[day]

                meals = [
                    ("Breakfast", (row[1] or "").strip()),
                    ("Lunch", (row[2] or "").strip()),
                    ("Snacks", (row[3] or "").strip()),
                    ("Dinner", (row[4] or "").strip()),
                ]

                for meal, items in meals:
                    if items:
                        rows.append({
                            "Day": day,
                            "Meal": meal,
                            "Items": items.replace("\n", "; ")
                        })

df = pd.DataFrame(rows)

day_order = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]

meal_order = [
    "Breakfast",
    "Lunch",
    "Snacks",
    "Dinner"
]

df["Day"] = pd.Categorical(df["Day"], categories=day_order, ordered=True)
df["Meal"] = pd.Categorical(df["Meal"], categories=meal_order, ordered=True)

df = df.sort_values(["Day", "Meal"]).reset_index(drop=True)

df.to_csv(CSV_PATH, index=False)

print(df)
print(f"\nSaved to {CSV_PATH}")