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

                if not row or len(row) < 5:
                    continue

                day = row[1]

                if day not in days:
                    continue

                day = days[day]

                meals = [
                    ("Breakfast", row[2]),
                    ("Lunch", row[3]),
                    ("Snacks", row[4]),
                    ("Dinner", row[5]),
                ]

                for meal, items in meals:
                    if items:
                        rows.append({
                            "Day": day,
                            "Meal": meal,
                            "Items": items.replace("\n", "; ")
                        })

df = pd.DataFrame(rows)
df.to_csv(CSV_PATH, index=False)

print(df)
print(f"\nSaved to {CSV_PATH}")