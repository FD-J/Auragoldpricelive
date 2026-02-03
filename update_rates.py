import requests
import datetime
import time


# API URLs
G_URL = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
S_URL = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"


# 10 minutes = 600 seconds
INTERVAL = 600


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

    # Bot run time (UNIX timestamp)
    last_run = int(time.time())


    # Get API Data
    gold = get_data(G_URL)
    silver = get_data(S_URL)


    # Prices
    g_buy = f"{float(gold['aura_buy_price']):,.2f}"
    g_sell = f"{float(gold['aura_sell_price']):,.2f}"

    s_buy = f"{float(silver['aura_buy_price']):,.2f}"
    s_sell = f"{float(silver['aura_sell_price']):,.2f}"


    # API Time
    api_time = format_time(gold.get("created_at", ""))


    # HTML Page (Auto Generated)
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<title>FDJ Live Rates</title>

<!-- Website Logo -->
<link rel="icon" type="image/png" href="logo.png">
<link rel="apple-touch-icon" href="logo.png">

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

.timer{{color:#38bdf8;font-weight:500;margin-top:6px}}

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

<div class="timer">
Next refresh in: <span id="countdown">--:--</span>
</div>

</div>

</div>


<!-- Bot Timestamp -->
<div id="botTime" data-time="{last_run}" style="display:none"></div>


<script>

const INTERVAL = {INTERVAL};

const last =
  Number(document.getElementById("botTime").dataset.time);

function updateTimer(){{
    
    const now = Math.floor(Date.now()/1000);

    let left = (last + INTERVAL) - now;

    if(left < 0) left = 0;

    let m = Math.floor(left/60);
    let s = left % 60;

    document.getElementById("countdown").innerText =
        String(m).padStart(2,"0") + ":" +
        String(s).padStart(2,"0");

    if(left === 0){{
        location.reload();
    }}
}}

updateTimer();
setInterval(updateTimer,1000);

</script>

</body>
</html>
"""


    # Save HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


    # Save Heartbeat
    with open("heartbeat.txt", "w") as f:
        f.write(str(last_run))


    print("Updated at:", last_run)


if __name__ == "__main__":
    main()
