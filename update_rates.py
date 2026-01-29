import requests
import datetime


# API URLs
G_URL = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
S_URL = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"


def get_api_data(url):
    try:
        ts = int(datetime.datetime.now().timestamp())

        response = requests.get(
            f"{url}&t={ts}",
            timeout=15,
            headers={"Cache-Control": "no-cache"}
        )

        response.raise_for_status()
        return response.json().get("data", None)

    except Exception as e:
        print("API Error:", e)
        return None


def main():

    gold = get_api_data(G_URL)
    silver = get_api_data(S_URL)

    # Stop if API failed
    if not gold or not silver:
        print("API Failed. File not updated.")
        return


    # Prices
    g_buy = f"{float(gold['aura_buy_price']):,.2f}"
    g_sell = f"{float(gold['aura_sell_price']):,.2f}"

    s_buy = f"{float(silver['aura_buy_price']):,.2f}"
    s_sell = f"{float(silver['aura_sell_price']):,.2f}"


    api_time = gold.get("created_at", "Live")


    # HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>FDJ Live Rates</title>

<meta http-equiv="refresh" content="60">

<style>
body {{
    background:#0f172a;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}}

.card {{
    background:#1e293b;
    padding:25px;
    border-radius:15px;
    width:320px;
}}

h2 {{
    text-align:center;
    color:#fbbf24;
}}

.row {{
    display:flex;
    justify-content:space-between;
    margin:10px 0;
}}

.val {{
    color:#fbbf24;
    font-weight:bold;
}}

.footer {{
    text-align:center;
    font-size:12px;
    margin-top:15px;
    color:#94a3b8;
}}
</style>

</head>

<body>

<div class="card">

<h2>FDJ Live Rates</h2>

<div class="row">
<span>Gold Buy</span>
<span class="val">₹ {g_buy}</span>
</div>

<div class="row">
<span>Gold Sell</span>
<span class="val">₹ {g_sell}</span>
</div>

<hr>

<div class="row">
<span>Silver Buy</span>
<span class="val">₹ {s_buy}</span>
</div>

<div class="row">
<span>Silver Sell</span>
<span class="val">₹ {s_sell}</span>
</div>

<div class="footer">
Updated: {api_time}<br>
Auto Refresh 60s
</div>

</div>

</body>
</html>
"""


    # Write file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("index.html created/updated successfully.")



if __name__ == "__main__":
    main()
