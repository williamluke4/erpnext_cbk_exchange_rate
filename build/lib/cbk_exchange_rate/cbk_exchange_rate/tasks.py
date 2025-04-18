import csv, io, datetime, requests, frappe
from frappe.utils import getdate

CSV_URL = (
    "https://www.centralbank.go.ke/uploads/fx_rates/historical_data.csv"
    # huge file (~3 MB) but fast to stream once a day
)


def save_usd_rate(rate_date: datetime.date, rate: float):
    """Save the given USD rate if not already present for the given date."""
    if not frappe.db.exists(
        "Currency Exchange",
        {"from_currency": "USD", "to_currency": "KES", "date": rate_date},
    ):
        doc = frappe.get_doc(
            {
                "doctype": "Currency Exchange",
                "from_currency": "USD",
                "to_currency": "KES",
                "exchange_rate": rate,
                "date": rate_date,
            }
        )
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info(f"CBK rate saved: {rate_date} 1 USD = {rate} KES")


def fetch_usd_rate_from_cbk():
    """Grab latest CBK USD→KES ‘Mean’ rate and save it if not already present."""
    resp = requests.get(CSV_URL, timeout=30)
    resp.raise_for_status()

    # CSV columns: Date, Currency, Mean, Buy, Sell
    rows = list(csv.DictReader(io.StringIO(resp.text)))
    usd_rows = [r for r in rows if r["Currency"].strip().upper() == "US DOLLAR"]
    latest = usd_rows[-1]  # last line is the most recent day

    rate_date = getdate(latest["Date"])  # e.g. 2025‑04‑17
    rate = float(latest["Mean"])

    save_usd_rate(rate_date, rate)
