app_name = "cbk_exchange_rate"
app_title = "CBK Exchange Rate"
app_publisher = "William Luke"
app_description = "CBK Exchange Rate"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "william@switchedon.world"
app_license = "MIT"

scheduler_events = {
    "hourly": [
        "cbk_exchange_rate.cbk_exchange_rate.tasks.update_usd_rate"
    ]
    # Add other scheduled events here if needed (e.g., daily, weekly)
    # "daily": [ ... ],
    # "all": [ ... ], # Runs every few minutes
}


