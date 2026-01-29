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


def format_time(api_time):

    try:
        # Convert API time to readable format
        dt = datetime.datetime.fromisoformat(api_time.replace("Z", "+00:00"))

        return dt.strftime("%d-%m-%Y  %H:%M")

    except:
        return datetime.datetime.now().strftime("%d-%m-%Y  %H:%M")



def main():

    gold = get_api_data(G_URL)
    silver = get_api_data(S_URL)

    if not gold or not silver:
        print("API Failed. File not updated.")
        return


    # Prices
    g_buy = f"{float(gold['aura_buy_price']):,.2f}"
    g_sell = f"{float(gold['aura_sell_price']):,.2f}"

    s_buy = f"{float(silver['aura_buy_price']):,.2f}"
    s_sell = f"{float(silver['aura_sell_price']):,.2f}"


    # Format Time
    api_time_raw = gold.get("created_at", "")
    api_time = format_time(api_time_raw)


    # HTML
    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<title>FDJ Live Rates</title>

<!-- Auto refresh handled by GitHub bot -->

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">

<style>

* {{
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}}

body {{
    background: linear-gradient(135deg,#020617,#020617,#020617,#020617);
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    color:white;
}}


.card {{
    background: rgba(30,41,59,0.9);
    width:360px;
    padding:28px;
    border-radius:22px;
    box-shadow:0 25px 60px rgba(0,0,0,0.7);
    animation: slideUp 1s ease;
    backdrop-filter: blur(10px);
}}


@keyframes slideUp {{
    from {{
        opacity:0;
        transform:translateY(40px);
    }}
    to {{
        opacity:1;
        transform:translateY(0);
    }}
}}


h2 {{
    text-align:center;
    color:#facc15;
    margin-bottom:25px;
    font-weight:600;
}}


.section {{
    background: rgba(255,255,255,0.04);
    padding:15px;
    border-radius:14px;
    margin-bottom:15px;
    animation: fadeIn 1.3s ease;
}}


@keyframes fadeIn {{
    from {{ opacity:0; }}
    to {{ opacity:1; }}
}}


.label {{
    font-size:13px;
    color:#94a3b8;
    margin-bottom:8px;
}}


.row {{
    display:flex;
    justify-content:space-between;
    margin:6px 0;
    font-size:17px;
}}


.price {{
    color:#facc15;
    font-weight:600;
}}


.footer {{
    text-align:center;
    font-size:12px;
    margin-top:15px;
    color:#94a3b8;
    animation: pulse 2s infinite;
}}


@keyframes pulse {{
    0% {{ opacity:0.6; }}
    50% {{ opacity:1; }}
    100% {{ opacity:0.6; }}
}}


.refresh {{
    font-size:11px;
    margin-top:4px;
    color:#64748b;
}}

</style>

</head>


<body>

<div class="card">

<h2>FDJ Live Rates</h2>


<div class="section">

<div class="label">Gold 24K (1 g)</div>

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

<div class="label">Silver (1 g)</div>

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

<div class="refresh">
Auto Refresh: 10 Minutes
</div>

</div>


</div>

</body>
</html>
"""


    # Write file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("index.html updated successfully.")



if __name__ == "__main__":
    main()
