import csv, io, datetime, requests, frappe
from frappe.utils import getdate
from cbk_exchange_rate.cbk_exchange_rate.fetch import get_latest_usd_rate
from cbk_exchange_rate.cbk_exchange_rate.logger import logger
def update_usd_rate():
    """Fetch and save the latest USD rate if it's for today and not already present."""
    today_date = getdate().date()

    # Check if rate for today already exists
    if frappe.db.exists(
        "Currency Exchange",
        {"from_currency": "USD", "to_currency": "KES", "date": today_date},
    ):
        logger.info(f"Rate for {today_date} already exists. Skipping update.")
        return

    # Fetch the latest rate if today's rate doesn't exist
    rate_date, rate = get_latest_usd_rate()

    # Save only if the fetched rate is for today
    if rate_date == today_date:
        save_usd_rate(rate_date, rate)
    else:
        logger.info(
            f"Fetched rate is for {rate_date}, not today ({today_date}). Skipping save."
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
                "for_buying": True,
                "for_selling": True,
                "exchange_rate": rate,
                "date": rate_date,
            }
        )
        doc.insert(ignore_permissions=True)
        logger.info(f"CBK rate saved: {rate_date} 1 USD = {rate} KES")
    else:
        logger.info(f"Rate for {rate_date} already exists. Skipping save.")
