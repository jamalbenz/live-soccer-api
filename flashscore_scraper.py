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

function cleanLeague(text){
  text = text || "";
  text = text.replace("Standings", "").trim();

  if (text.toLowerCase().includes("world championship")) return "World Cup";
  if (text.toLowerCase().includes("champions league")) return "Champions League";
  if (text.toLowerCase().includes("europa league")) return "Europa League";
  if (text.toLowerCase().includes("conference league")) return "Conference League";
  if (text.toLowerCase().includes("premier league")) return "Premier League";
  if (text.toLowerCase().includes("laliga") || text.toLowerCase().includes("la liga")) return "LaLiga";
  if (text.toLowerCase().includes("serie a")) return "Serie A";
  if (text.toLowerCase().includes("bundesliga")) return "Bundesliga";
  if (text.toLowerCase().includes("ligue 1")) return "Ligue 1";
  if (text.toLowerCase().includes("allsvenskan")) return "Allsvenskan";
  if (text.toLowerCase().includes("superettan")) return "Superettan";
  if (text.toLowerCase().includes("saudi")) return "Saudi Pro League";

  return "Premium Football";
}

function getLeague(row){
  let section = row.closest('[class*="event__match"]') || row;
  let p = row.previousElementSibling;
  let tries = 0;

  while(p && tries < 30){
    let txt = (p.innerText || "").trim();

    if (
      txt &&
      txt.length < 140 &&
      !txt.includes("\\n") &&
      (
        txt.toLowerCase().includes("world") ||
        txt.toLowerCase().includes("champions") ||
        txt.toLowerCase().includes("europa") ||
        txt.toLowerCase().includes("conference") ||
        txt.toLowerCase().includes("premier") ||
        txt.toLowerCase().includes("laliga") ||
        txt.toLowerCase().includes("la liga") ||
        txt.toLowerCase().includes("serie a") ||
        txt.toLowerCase().includes("bundesliga") ||
        txt.toLowerCase().includes("ligue 1") ||
        txt.toLowerCase().includes("allsvenskan") ||
        txt.toLowerCase().includes("superettan") ||
        txt.toLowerCase().includes("saudi")
      )
    ) {
      return cleanLeague(txt);
    }

    p = p.previousElementSibling;
    tries++;
  }

  return "Premium Football";
}

rows.forEach(row => {
  let txt = row.innerText.trim().split("\\n").filter(Boolean);
  let allText = txt.join(" ").toLowerCase();

  if (blocked.some(b => allText.includes(b))) return;
  if (!bigTeams.some(t => allText.includes(t))) return;

  if (txt.length >= 3) {
    let status = txt[0] || "NS";
    let league = getLeague(row);

    matches.push({
      league: league,
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