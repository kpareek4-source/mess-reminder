import pdfplumber
import pandas as pd

PDF_PATH = "data/menu.pdf"
CSV_PATH = "data/menu.csv"

days = {
    "YADNOM": "Monday",
    "YADSEUT": "Tuesday",
    "YADSENDEW": "Wednesday",
    "YADSRUHT": "Thursday",
    "YADIRF": "Friday",
    "YADRUTAS": "Saturday",
    "YADNUS": "Sunday"
}

rows = []

with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            for row in table:

                # Skip empty or incomplete rows
                if not row or len(row) < 7:
                    continue

                day = (row[1] or "").strip()

                # Skip header/footer rows
                if day not in days:
                    continue

                day = days[day]

                meals = [
                    ("Breakfast", (row[3] or "").strip()),
                    ("Lunch", (row[4] or "").strip()),
                    ("Snacks", (row[5] or "").strip()),
                    ("Dinner", (row[6] or "").strip()),
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