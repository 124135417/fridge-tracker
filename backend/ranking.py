from datetime import date

def get_top10(items):
    today = date.today()

    enriched = []
    for item in items:
        days = (today - item["date_in"]).days
        enriched.append({
            "name": item["name"],
            "days": days,
            "date_in": item["date_in"],
        })

    enriched.sort(key=lambda x: x["days"], reverse=True)
    return enriched[:10]
