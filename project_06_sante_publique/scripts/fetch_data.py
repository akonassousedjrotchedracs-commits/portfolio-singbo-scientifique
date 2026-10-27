"""Télécharge les indicateurs publics de la Banque mondiale (sources OMS/UNICEF/IGME).

Usage : python scripts/fetch_data.py
Écrit data/indicateurs_bm.csv (format long) ; à relancer pour actualiser.
"""
import csv
import json
import urllib.request
from datetime import date
from pathlib import Path

COUNTRIES = {"BEN": "Bénin", "TGO": "Togo", "NGA": "Nigeria", "BFA": "Burkina Faso", "NER": "Niger", "SSF": "Afrique subsaharienne"}
INDICATORS = {
    "SH.MLR.INCD.P3": "Incidence du paludisme (pour 1 000 personnes à risque)",
    "SH.DYN.MORT": "Mortalité des moins de 5 ans (pour 1 000 naissances vivantes)",
    "SH.IMM.IDPT": "Couverture vaccinale DTC3 (% des 12-23 mois)",
    "SH.IMM.MEAS": "Couverture vaccinale rougeole (% des 12-23 mois)",
}
OUT = Path(__file__).resolve().parents[1] / "data" / "indicateurs_bm.csv"


def fetch(indicator):
    url = (f"https://api.worldbank.org/v2/country/{';'.join(COUNTRIES)}/indicator/{indicator}"
           "?format=json&date=2000:2024&per_page=1000")
    with urllib.request.urlopen(url, timeout=60) as response:
        meta, rows = json.load(response)
    if meta.get("pages", 1) != 1:
        raise RuntimeError(f"{indicator}: pagination inattendue")
    return rows


def main():
    records = []
    for code, label in INDICATORS.items():
        for row in fetch(code):
            if row["value"] is None:
                continue
            records.append({"country_code": row["countryiso3code"], "country": COUNTRIES[row["countryiso3code"]],
                            "indicator_code": code, "indicator": label, "year": int(row["date"]), "value": row["value"]})
    records.sort(key=lambda r: (r["indicator_code"], r["country_code"], r["year"]))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"{len(records)} valeurs écrites dans {OUT.name} (extraction du {date.today().isoformat()})")


if __name__ == "__main__":
    main()
