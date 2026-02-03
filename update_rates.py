import requests
import datetime
import time


G_URL = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
S_URL = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"

INTERVAL = 600   # 10 minutes in seconds


def get_data(url):

    ts = int(time.time())

    r = requests.get(
        f"{url}&t={ts}",
        headers={"Cache-Control": "no-cache"},
        timeout=15
    )

    r.raise_for_status()

    return r.json()["data"]


def format_time(t):

    dt = datetime.datetime.fromisoformat(
        t.replace("Z","+00:00")
    )

    return dt.strftime("%d-%m-%Y %H:%M:%S")


def main():

    now = int(time.time())   # current unix time


    gold = get_data(G_URL)
    silver = get_data(S_URL)


    g_buy = f"{float(gold['aura_buy_price']):,.2f}"
    g_sell = f"{float(gold['aura_sell_price']):,.2f}"

    s_buy = f"{float(silver['aura_buy_price']):,.2f}"
    s_sell = f"{float(silver['aura_sell_price']):,.2f}"


    time_str = format_time(gold["created_at"])


    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<title>FDJ Live Rates</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">

<style>

*{{box-sizing:border-box;font-family:'Poppins',sans-serif;}}

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

h2{{text-align:center;color:#facc15;}}

.section{{
    background:rgba(255,255,255,0.05);
    padding:14px;
    border-radius:12px;
    margin:12px 0;
}}

.row{{display:flex;justify-content:space-between;}}

.price{{color:#facc15;font-weight:600;}}

.footer{{text-align:center;font-size:12px;color:#94a3b8;}}

.timer{{color:#38bdf8;font-weight:500;margin-top:6px;}}

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
<b>{time_str}</b>

<div class="timer">
Next refresh in: <span id="countdown"></span>
</div>

</div>

</div>


<!-- Hidden timestamp -->
<div id="lastUpdate" data-time="{now}" style="display:none"></div>


<script>

const INTERVAL = {INTERVAL};

const last =
  Number(document.getElementById("lastUpdate").dataset.time);

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


    with open("index.html","w",encoding="utf-8") as f:
        f.write(html)


    print("Updated at", now)


if __name__ == "__main__":
    main()
