from datetime import datetime
import requests

def get_latest_usd_rate():
    """Grab latest CBK USD→KES ‘Mean’ rate and save it if not already present."""
    url = "https://www.centralbank.go.ke/wp-admin/admin-ajax.php?action=get_wdtable&table_id=193"

    payload = 'draw=9&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=date_r&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=~&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=currency&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=US+DOLLAR&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=ROUND(jx_views_fx_new_rates.mean%2C4)&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=desc&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&sRangeSeparator=~'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    # Parse JSON response
    json_data = response.json()

    # Extract data rows
    data_rows = json_data.get('data', [])

    if not data_rows or len(data_rows) != 1:
        raise Exception(f"Unexpected number of rows: {len(data_rows)}")

    row = data_rows[0]
    if len(row) != 3:
        raise Exception(f"Unexpected number of columns: {len(row)}")
    if row[1].strip().upper() != "US DOLLAR":
        raise Exception(f"Unexpected currency: {row[1]}")
    date_str, _currency, rate = row
    date = datetime.strptime(date_str.strip(), '%d/%m/%Y')
    rate = float(rate.strip())
    return date, rate
