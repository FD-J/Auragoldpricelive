import requests
import datetime
import time


# API URLs
G_URL = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
S_URL = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"


def get_data(url):

    ts = int(time.time())

    r = requests.get(
        f"{url}&t={ts}",
        headers={"Cache-Control": "no-cache"},
        timeout=15
    )

    r.raise_for_status()

    return r.json()["data"]


def format_time(api_time):

    try:
        dt = datetime.datetime.fromisoformat(
            api_time.replace("Z", "+00:00")
        )

        return dt.strftime("%d-%m-%Y %H:%M:%S")

    except:
        return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def main():

    now = int(time.time())


    # Get API Data
    gold = get_data(G_URL)
    silver = get_data(S_URL)


    # Prices
    g_buy = f"{float(gold['aura_buy_price']):,.2f}"
    g_sell = f"{float(gold['aura_sell_price']):,.2f}"

    s_buy = f"{float(silver['aura_buy_price']):,.2f}"
    s_sell = f"{float(silver['aura_sell_price']):,.2f}"


    # Time
    api_time = format_time(gold.get("created_at", ""))


    # HTML Page
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<title>FDJ Live Rates</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">

<style>

*{{font-family:'Poppins',sans-serif;box-sizing:border-box}}

body{{
    margin:0;
    background:#020617;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    color:white;
}}

.card{{
    width:100%;
    max-width:360px;
    background:#1e293b;
    padding:22px;
    border-radius:18px;
}}

h2{{text-align:center;color:#facc15}}

.section{{
    background:rgba(255,255,255,0.05);
    padding:14px;
    border-radius:12px;
    margin:12px 0;
}}

.row{{display:flex;justify-content:space-between}}

.price{{color:#facc15;font-weight:600}}

.footer{{text-align:center;font-size:12px;color:#94a3b8}}

</style>

</head>

<body>

<div class="card">

<h2>FDJ Live Rates</h2>


<div class="section">

<b>Gold 24K (1g)</b>

<div class="row">
<span>Buy</span>
<span class="price">₹ {g_buy}</span>
</div>

<div class="row">
<span>Sell</span>
<span class="price">₹ {g_sell}</span>
</div>

</div>


<div class="section">

<b>Silver (1g)</b>

<div class="row">
<span>Buy</span>
<span class="price">₹ {s_buy}</span>
</div>

<div class="row">
<span>Sell</span>
<span class="price">₹ {s_sell}</span>
</div>

</div>


<div class="footer">

Last Updated<br>
<b>{api_time}</b>

</div>

</div>

</body>
</html>
"""


    # Save HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


    # Save Heartbeat
    with open("heartbeat.txt", "w") as f:
        f.write(str(now))


    print("Updated at:", now)


if __name__ == "__main__":
    main()
