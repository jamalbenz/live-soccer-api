import undetected_chromedriver as uc
import time
import json

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options, version_main=149)
driver.get("https://www.flashscore.com/football/")
time.sleep(12)

try:
    driver.execute_script("""
    [...document.querySelectorAll('button')].forEach(b=>{
      if(b.innerText.includes('Reject All') || b.innerText.includes('I Accept') || b.innerText.includes('Accept')) b.click();
    });
    """)
    time.sleep(3)
except:
    pass

data = driver.execute_script("""
let matches = [];
let rows = [...document.querySelectorAll('[id^="g_1_"]')];

let teams = {
  "real madrid":"LaLiga","barcelona":"LaLiga","atletico":"LaLiga",
  "manchester city":"Premier League","man city":"Premier League","manchester united":"Premier League","man united":"Premier League","liverpool":"Premier League","arsenal":"Premier League","chelsea":"Premier League","tottenham":"Premier League","newcastle":"Premier League",
  "bayern":"Bundesliga","dortmund":"Bundesliga","leverkusen":"Bundesliga",
  "psg":"Ligue 1","marseille":"Ligue 1",
  "juventus":"Serie A","inter":"Serie A","milan":"Serie A","napoli":"Serie A","roma":"Serie A","lazio":"Serie A",
  "benfica":"Primeira Liga","porto":"Primeira Liga","sporting":"Primeira Liga",
  "ajax":"Eredivisie","feyenoord":"Eredivisie","psv":"Eredivisie",
  "argentina":"World Cup","brazil":"World Cup","france":"World Cup","spain":"World Cup","england":"World Cup","germany":"World Cup","portugal":"World Cup","belgium":"World Cup","netherlands":"World Cup","italy":"World Cup","croatia":"World Cup","uruguay":"World Cup","egypt":"World Cup","morocco":"World Cup","sweden":"World Cup","norway":"World Cup","denmark":"World Cup","iraq":"World Cup","austria":"World Cup","new zealand":"World Cup",
  "malmo":"Allsvenskan","malmö":"Allsvenskan","aik":"Allsvenskan","djurgarden":"Allsvenskan","djurgården":"Allsvenskan","hammarby":"Allsvenskan","ifk goteborg":"Allsvenskan","ifk göteborg":"Allsvenskan","elfsborg":"Allsvenskan","norrkoping":"Allsvenskan","norrköping":"Allsvenskan","hacken":"Allsvenskan","häcken":"Allsvenskan","kalmar":"Allsvenskan","sirius":"Allsvenskan",
  "fc copenhagen":"Nordic Football","copenhagen":"Nordic Football","brondby":"Nordic Football","brøndby":"Nordic Football","midtjylland":"Nordic Football","rosenborg":"Nordic Football","molde":"Nordic Football","bodo/glimt":"Nordic Football","bodø/glimt":"Nordic Football",
  "al nassr":"Saudi Pro League","al hilal":"Saudi Pro League","al ittihad":"Saudi Pro League","al ahli":"Saudi Pro League"
};

let blocked = [
  "u23","u21","u20","u19","women","youth","reserve","reserves",
  "kuwait","ethiopia","gambia","mongolia","kyrgyzstan","australia npl",
  "bombada","brikama","falcons","steve biko","dutch lions","hart academy"
];

function leagueLogo(league){
  let map = {
    "World Cup":"https://media.api-sports.io/football/leagues/1.png",
    "Premier League":"https://media.api-sports.io/football/leagues/39.png",
    "LaLiga":"https://media.api-sports.io/football/leagues/140.png",
    "Serie A":"https://media.api-sports.io/football/leagues/135.png",
    "Bundesliga":"https://media.api-sports.io/football/leagues/78.png",
    "Ligue 1":"https://media.api-sports.io/football/leagues/61.png",
    "Champions League":"https://media.api-sports.io/football/leagues/2.png",
    "Europa League":"https://media.api-sports.io/football/leagues/3.png",
    "Allsvenskan":"https://media.api-sports.io/football/leagues/113.png",
    "Saudi Pro League":"https://media.api-sports.io/football/leagues/307.png"
  };
  return map[league] || "";
}

function inferLeague(text){
  text = text.toLowerCase();
  for (let key in teams){
    if(text.includes(key)) return teams[key];
  }
  return "Premium Football";
}

function logoName(name){
  return "https://ui-avatars.com/api/?name=" + encodeURIComponent(name) + "&background=D4AF37&color=000&bold=true";
}

rows.forEach(row => {
  let txt = row.innerText.trim().split("\\n").filter(Boolean);
  let allText = txt.join(" ").toLowerCase();

  if (blocked.some(b => allText.includes(b))) return;

  let league = inferLeague(allText);
  if (league === "Premium Football") return;

  if (txt.length >= 3) {
    let status = txt[0] || "NS";
    let home = txt[1] || "";
    let away = txt[2] || "";

    matches.push({
    id: home.toLowerCase().replaceAll(" ", "-") + "-vs-" + away.toLowerCase().replaceAll(" ", "-"),
    league: league,
    league_logo: leagueLogo(league),
    country: league === "Allsvenskan" ? "Sweden" : "",
    home: home,
    home_logo: logoName(home),
    away: away,
    away_logo: logoName(away),
    home_score: txt[3] || "",
    away_score: txt[4] || "",
    status: status,
    minute: status,
    match_time: status.match(/^\\d{1,2}:\\d{2}$/) ? status : "",
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

driver.quit()