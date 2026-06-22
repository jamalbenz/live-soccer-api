import undetected_chromedriver as uc
import time
import json

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, version_main=149)
driver.get("https://www.flashscore.com/football/")
time.sleep(12)

try:
    driver.execute_script("""
    [...document.querySelectorAll('button')].forEach(b=>{
      if(b.innerText.includes('Reject All') || b.innerText.includes('I Accept') || b.innerText.includes('Accept')) b.click();
    });
    """)
    time.sleep(4)
except:
    pass

data = driver.execute_script("""
let matches = [];
let rows = [...document.querySelectorAll('[id^="g_1_"]')];

let bigTeams = [
  "real madrid","barcelona","atletico","manchester city","man city",
  "manchester united","man united","liverpool","arsenal","chelsea","tottenham",
  "newcastle","bayern","dortmund","leverkusen","psg","marseille",
  "juventus","inter","milan","napoli","roma","lazio",
  "benfica","porto","sporting","ajax","feyenoord","psv",
  "celtic","rangers","galatasaray","fenerbahce","besiktas",
  "argentina","brazil","france","spain","england","germany",
  "portugal","belgium","netherlands","italy","croatia","uruguay",
  "egypt","morocco","sweden","norway","denmark",
  "malmo","malmö","aik","djurgarden","djurgården","hammarby",
  "ifk goteborg","ifk göteborg","elfsborg","norrkoping","norrköping",
  "hacken","häcken","helsingborg","kalmar","sirius",
  "fc copenhagen","copenhagen","brondby","brøndby","midtjylland",
  "rosenborg","molde","bodo/glimt","bodø/glimt",
  "al nassr","al hilal","al ittihad","al ahli"
];

let blocked = [
  "u23","u21","u20","u19","women","youth","reserve","reserves",
  "kuwait","ethiopia","gambia","mongolia","kyrgyzstan","australia npl",
  "bombada","brikama","falcons","steve biko","dutch lions","hart academy"
];

rows.forEach(row => {
  let txt = row.innerText.trim().split("\\n").filter(Boolean);
  let allText = txt.join(" ").toLowerCase();

  if (blocked.some(b => allText.includes(b))) return;
  if (!bigTeams.some(t => allText.includes(t))) return;

  if (txt.length >= 3) {
    let status = txt[0] || "NS";

    matches.push({
      league: "Premium Football",
      home: txt[1] || "",
      away: txt[2] || "",
      home_logo: "",
      away_logo: "",
      home_score: txt[3] || "",
      away_score: txt[4] || "",
      league_logo: "",
      status: status,
      minute: status,
      is_live: !status.toLowerCase().includes("finished") && !status.match(/^\\d{1,2}:\\d{2}$/)
    });
  }
});

return matches.slice(0, 20);
""")

result = {
    "success": True,
    "count": len(data),
    "matches": data
}

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))
print("matches.json created successfully")

input("Press Enter to close...")
driver.quit()