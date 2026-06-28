import os, json, random, requests
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8980514283:AAHn_V_zQQV_XRcHv2WZfwBtQ9GjrmKqP1E"
SUPABASE_URL = "https://fcnougrrwxhgbepkbzoi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZjbm91Z3Jyd3hoZ2JlcGtiem9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2NDQxMzEsImV4cCI6MjA5ODIyMDEzMX0.RVxD32m-FQxWE7P1CZfeHvH2vSOZ9uRXuHW0ZRLMPrg"
SB_H = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}
user_sessions = {}
TEAM_STRENGTH = {
    "real madrid":95,"manchester city":94,"barcelona":92,"psg":90,"bayern munich":93,
    "liverpool":91,"arsenal":88,"chelsea":87,"juventus":86,"inter milan":87,
    "ac milan":85,"atletico madrid":88,"borussia dortmund":86,"napoli":84,
    "lyon":80,"marseille":79,"ajax":82,"benfica":81,"porto":82,"sevilla":83,
    "cameroun":72,"senegal":78,"maroc":80,"nigeria":76,"cote d'ivoire":75,
    "ghana":71,"algerie":74,"egypte":75,"afrique du sud":65,"canada":70,
    "france":92,"bresil":91,"argentine":93,"angleterre":90,"espagne":91,
    "allemagne":89,"portugal":88,"belgique":87,"pays-bas":86,"italie":88,
    "lakers":88,"bulls":75,"warriors":90,"celtics":91,"heat":84,
    "nets":82,"bucks":89,"76ers":86,"suns":83,"clippers":85,
    "djokovic":97,"nadal":94,"federer":93,"alcaraz":92,"sinner":91,
    "medvedev":90,"tsitsipas":88,"zverev":89,"swiatek":95,"sabalenka":92,
    "navi":92,"astralis":90,"faze":91,"g2":89,"vitality":88,
    "liquid":86,"ence":84,"heroic":83,"nip":82,"mouz":85,
    "t1":95,"gen.g":90,"jdg":89,"weibo":86,"cloud9":82,
    "fnatic":83,"g2 esports":88,"100 thieves":80,
    "mbappe":95,"ronaldo":93,"messi":97,"neymar":89,"haaland":94,
    "benzema":91,"salah":90,"vinicius":92,"bellingham":91,"osimhen":87,
    "mcgregor":88,"poirier":87,"jones":95,"adesanya":91,"usman":90,
    "ngannou":93,"miocic":89,"shevchenko":90,
    "all blacks":96,"springboks":93,"wallabies":86,"irlande":91,"australie":86,
}
ANALYSES = {
    "Football":[
        ["Domination territoriale attendue de {t1} grâce a un pressing haut intense.","Les stats des 5 derniers matchs favorisent {t1} avec 4 victoires consecutives."],
        ["Match tres serre prevu entre ces deux formations de haut niveau.","Le facteur terrain et la gestion du ballon seront decisifs."],
        ["La forme recente de {t2} est impressionnante avec une serie positive.","{t2} affiche une attaque redoutable et une defense solide cette saison."],
    ],
    "Basketball":[
        ["{t1} a l avantage physique et une profondeur de banc superieure.","La defense de zone de {t1} sera tres difficile a percer ce soir."],
        ["Attendez-vous a un duel serre jusqu au buzzer final.","La victoire se jouera sur les lancers francs et les rebonds offensifs."],
        ["{t2} en excellente forme avec 6 victoires consecutives en NBA.","Le back-court de {t2} est parmi les meilleurs de la conference."],
    ],
    "Tennis":[
        ["{t1} domine parfaitement sur ce type de surface cette saison.","Le service de {t1} a plus de 220 km/h sera une arme decisive."],
        ["Match totalement indecis entre deux joueurs de niveau mondial similaire.","Le tie-break du 3eme set sera tres probablement decisif."],
        ["{t2} est en grande forme avec 4 titres cette saison.","Le revers long de ligne de {t2} est inarretable en ce moment."],
    ],
    "FIFA":[
        ["{t1} maitrise parfaitement les mecaniques du jeu cette saison.","Le build-up play structure de {t1} est tres difficile a contrer."],
        ["Duel de strategies - chaque possession et transition sera cruciale.","Tout peut basculer en quelques secondes dans ce type de rencontre."],
        ["{t2} affiche un meilleur winrate en ligne ce mois-ci.","La creativite offensive et les skills de {t2} sont redoutables."],
    ],
    "CSGO":[
        ["{t1} domine sur cette map avec un winrate impressionnant de 78%.","L IGL de {t1} est reconnu comme le meilleur stratege du circuit."],
        ["Clash de titans - les deux equipes se connaissent parfaitement.","L economie et la gestion des rounds pistolets seront decisifs."],
        ["{t2} sort d un bootcamp tres reussi avec de nouveaux strats.","Le clutch potential de {t2} dans les situations difficiles est impressionnant."],
    ],
    "LoL":[
        ["{t1} possede le meilleur early game de toute la competition.","Le draft de {t1} sera probablement plus adapte a la meta actuelle."],
        ["Meta equilibree - tout dependra du draft et des picks/bans.","Baron Nashor et les objectifs neutres seront la cle de ce match."],
        ["{t2} domine le mid-game avec une macro superieure.","{t2} a une carry en forme absolue depuis le debut de la saison."],
    ],
    "MMA":[
        ["{t1} a l avantage en striking avec +65% de precision de frappe.","Le ground game et la lutte de {t1} sont difficiles a neutraliser."],
        ["Combat tres equilibre sur le papier - les deux ont des chances reelles.","Tout peut se terminer des le premier round - match tres ouvert."],
        ["{t2} sort de 3 KO consecutifs et est en forme absolue.","La portee, la puissance et la vitesse de {t2} donnent un avantage clair."],
    ],
    "Rugby":[
        ["{t1} domine en melee fermee et en touche avec un pack solide.","Le jeu au pied strategique de {t1} sera tres difficile a contrer."],
        ["Test-match tres ouvert entre deux nations de tout premier plan mondial.","La discipline et la gestion des cartons jaunes seront absolument decisives."],
        ["{t2} excelle en contre-attaque rapide avec des ailiers tres rapides.","Le jeu deploye de {t2} sur les grands espaces sera dangereux."],
    ],
}
FACTEURS = {
    "win":["✅ Forme recente superieure (4V/5M)","✅ Meilleur bilan H2H en confrontations directes","✅ Avantage tactique et physique confirme","✅ Attaque la plus prolifique du championnat","✅ Defense solide - moins de 1 but encaisse/match"],
    "draw":["〰️ Equilibre parfait en confrontations directes H2H","〰️ Styles de jeu qui s annulent mutuellement","〰️ Contexte de match aller - prudence tactique"],
    "lose":["⚠️ Blessures importantes dans l effectif titulaire","⚠️ Fatigue due a un calendrier tres charge","⚠️ Difficulte a scorer en dehors de leur domicile"],
}
TIPS = [
    "💡 Ne mise jamais plus de *5%* de ta bankroll sur un seul pari.",
    "💡 Les cotes entre *1.30 et 1.60* sont souvent plus sures pour debuter.",
    "💡 Analyse toujours les *confrontations directes H2H* avant de miser.",
    "💡 Une *HIGH confidence* ne garantit pas la victoire - le sport reste imprevisible !",
    "💡 Combine *2-3 matchs HIGH* pour maximiser ton gain en pari combine.",
    "💡 Les *equipes a domicile* gagnent en moyenne 45% des matchs en football.",
    "💡 Attends les *compositions officielles* avant de miser.",
    "💡 Fixe-toi une *limite de pertes journaliere* et respecte-la.",
    "💡 En eSports, les *patch recents* peuvent changer completement les favoris.",
    "💡 Le meilleur parieur sait *quand ne pas parier*.",
]
NO_DRAW = ["tennis","mma","fifa","cs:go","csgo","lol","esports"]
EMOJIS = {"football":"⚽","basketball":"🏀","tennis":"🎾","fifa":"🎮","cs:go":"🔫","csgo":"🔫","lol":"🧙","mma":"🥊","rugby":"🏉"}

def get_upcoming():
    today = datetime.now()
    return [
        {"sport":"Football","t1":"Real Madrid","t2":"Barcelona","date":(today+timedelta(days=1)).strftime("%d/%m"),"ligue":"🇪🇸 La Liga","hot":True},
        {"sport":"Football","t1":"PSG","t2":"Manchester City","date":(today+timedelta(days=2)).strftime("%d/%m"),"ligue":"🏆 Champions League","hot":True},
        {"sport":"Football","t1":"Cameroun","t2":"Senegal","date":(today+timedelta(days=2)).strftime("%d/%m"),"ligue":"🌍 CAN","hot":True},
        {"sport":"Football","t1":"Liverpool","t2":"Arsenal","date":(today+timedelta(days=3)).strftime("%d/%m"),"ligue":"🏴 Premier League","hot":False},
        {"sport":"Basketball","t1":"Lakers","t2":"Warriors","date":(today+timedelta(days=1)).strftime("%d/%m"),"ligue":"🏀 NBA","hot":True},
        {"sport":"Basketball","t1":"Celtics","t2":"Bucks","date":(today+timedelta(days=3)).strftime("%d/%m"),"ligue":"🏀 NBA","hot":False},
        {"sport":"Tennis","t1":"Djokovic","t2":"Alcaraz","date":(today+timedelta(days=2)).strftime("%d/%m"),"ligue":"🎾 Wimbledon","hot":True},
        {"sport":"CSGO","t1":"NAVI","t2":"FaZe","date":(today+timedelta(days=1)).strftime("%d/%m"),"ligue":"🔫 ESL Pro","hot":True},
        {"sport":"LoL","t1":"T1","t2":"Gen.G","date":(today+timedelta(days=2)).strftime("%d/%m"),"ligue":"🧙 LCK","hot":True},
        {"sport":"MMA","t1":"Jones","t2":"Ngannou","date":(today+timedelta(days=5)).strftime("%d/%m"),"ligue":"🥊 UFC","hot":True},
        {"sport":"Rugby","t1":"France","t2":"All Blacks","date":(today+timedelta(days=6)).strftime("%d/%m"),"ligue":"🏉 Test Match","hot":False},
    ]

def get_strength(name):
    key = name.lower().strip()
    if key in TEAM_STRENGTH: return TEAM_STRENGTH[key]
    for k,v in TEAM_STRENGTH.items():
        if k in key or key in k: return v
    return random.randint(60,85)

def predict(t1,t2,sport):
    s1=get_strength(t1); s2=get_strength(t2)
    sk=sport.lower().split()[0]
    no_draw=any(nd in sk for nd in NO_DRAW)
    emoji=EMOJIS.get(sk,"🏆")
    noise=random.randint(-8,8); total=s1+s2
    raw1=(s1/total)*100+noise; raw2=100-raw1
    if no_draw:
        w1=max(10,min(85,int(raw1))); dr=0; w2=100-w1
    else:
        dc=random.randint(10,25) if abs(s1-s2)<10 else random.randint(5,15)
        w1=max(10,min(75,int(raw1*(1-dc/100)))); w2=max(10,min(75,int(raw2*(1-dc/100)))); dr=100-w1-w2
    if w1>w2 and w1>dr: verdict=f"🏆 {t1} gagne"; outcome=0; cote=round(100/w1*random.uniform(0.88,0.95),2)
    elif w2>w1 and w2>dr: verdict=f"🏆 {t2} gagne"; outcome=2; cote=round(100/w2*random.uniform(0.88,0.95),2)
    else: verdict="➖ Match Nul"; outcome=1; cote=round(random.uniform(2.8,3.6),2)
    conf="HIGH" if abs(w1-w2)>20 else "MEDIUM" if abs(w1-w2)>10 else "LOW"
    pk=next((k for k in ANALYSES if k.lower() in sport.lower()),"Football")
    lines=ANALYSES[pk][outcome]
    analyse=" ".join([l.replace("{t1}",t1).replace("{t2}",t2) for l in lines])
    facs=random.sample(FACTEURS["win"],2)+random.sample(FACTEURS["lose"],1) if outcome in [0,2] else random.sample(FACTEURS["draw"],3)
    return {"verdict":verdict,"win1":w1,"draw":dr,"win2":w2,"confidence":conf,"cote":str(cote),"analyse":analyse,"facteurs":facs,"emoji":emoji,"s1":s1,"s2":s2}

def save_pred(uid,uname,sport,t1,t2,verdict,conf,w1,dr,w2,analyse):
    try: requests.post(f"{SUPABASE_URL}/rest/v1/predictions",headers=SB_H,json={"user_id":str(uid),"username":uname,"sport":sport,"team1":t1,"team2":t2,"verdict":verdict,"confidence":conf,"win1":w1,"draw":dr,"win2":w2,"analyse":analyse})
    except: pass

def get_history(uid):
    try:
        r=requests.get(f"{SUPABASE_URL}/rest/v1/predictions?user_id=eq.{uid}&order=created_at.desc&limit=5",headers=SB_H)
        return r.json() if r.status_code==200 else []
    except: return []

def get_stats(uid):
    try:
        r=requests.get(f"{SUPABASE_URL}/rest/v1/predictions?user_id=eq.{uid}&select=confidence",headers=SB_H)
        data=r.json() if r.status_code==200 else []; total=len(data); high=sum(1 for p in data if p.get("confidence")=="HIGH")
        return total,high
    except: return 0,0

def bar(p): return "█"*int(p/10)+"░"*(10-int(p/10))
def stars(s): return "⭐"*int(s/20)+"☆"*(5-int(s/20))
def conf_info(c): return {"HIGH":("🔥","HAUTE - Mise recommandee ✅"),"MEDIUM":("⚡","MOYENNE - Mise prudente ⚠️"),"LOW":("⚠️","FAIBLE - Match risque ❌")}.get(c,("⚠️","Indeterminee"))

def nav_kb():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🎯 Prediction"),    KeyboardButton("📅 Matchs a venir")],
        [KeyboardButton("📊 Historique"),    KeyboardButton("📈 Mes stats")],
        [KeyboardButton("💡 Tips paris"),    KeyboardButton("ℹ️ Aide")],
    ],resize_keyboard=True)

def sport_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚽ Football",callback_data="S|Football"),InlineKeyboardButton("🏀 Basketball",callback_data="S|Basketball")],
        [InlineKeyboardButton("🎾 Tennis",callback_data="S|Tennis"),InlineKeyboardButton("🎮 FIFA",callback_data="S|FIFA")],
        [InlineKeyboardButton("🔫 CS:GO",callback_data="S|CSGO"),InlineKeyboardButton("🧙 LoL",callback_data="S|LoL")],
        [InlineKeyboardButton("🥊 MMA",callback_data="S|MMA"),InlineKeyboardButton("🏉 Rugby",callback_data="S|Rugby")],
    ])

async def start(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    u=update.effective_user; total,high=get_stats(u.id)
    await update.message.reply_text(
        f"🎯 *PredixBot v3* - IA Sport & eSports\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Salut *{u.first_name}* ! 👋🏆\n\nJe suis ton robot de predictions sportives IA.\n\n"
        f"📊 Stats: *{total}* predictions | 🔥 *{high}* haute confiance\n\n"
        f"{random.choice(TIPS)}\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n👇 *Utilise le menu ci-dessous*",
        parse_mode="Markdown",reply_markup=nav_kb())

async def run_pred(update,ctx,t1,t2,sport):
    msg=await update.message.reply_text(random.choice(["🔍 Analyse H2H en cours...","📊 Calcul des probabilites...","🧠 Modele IA en execution...","⚡ Traitement des donnees stats..."]))
    res=predict(t1,t2,sport); ce,ct=conf_info(res["confidence"])
    no_draw=any(nd in sport.lower() for nd in NO_DRAW)
    draw_line=f"➖ Nul\n`{bar(res['draw'])}` *{res['draw']}%*\n" if not no_draw else ""
    facs="\n".join([f"  {f}" for f in res["facteurs"]])
    text=(
        f"{res['emoji']} *{t1}* ⚔️ *{t2}*\n🏷️ {sport} | 📅 {datetime.now().strftime('%d/%m/%Y')}\n{'━'*26}\n\n"
        f"💪 *Niveau*\n  {t1}: {stars(res['s1'])} `{res['s1']}/100`\n  {t2}: {stars(res['s2'])} `{res['s2']}/100`\n\n"
        f"📊 *Probabilites*\n✅ {t1}\n`{bar(res['win1'])}` *{res['win1']}%*\n{draw_line}❌ {t2}\n`{bar(res['win2'])}` *{res['win2']}%*\n\n"
        f"{'━'*26}\n🏆 *Verdict:* {res['verdict']}\n💰 *Cote estimee:* `{res['cote']}`\n{ce} *Confiance:* {ct}\n\n"
        f"📝 *Analyse:*\n_{res['analyse']}_\n\n🔍 *Facteurs cles:*\n{facs}\n\n{'━'*26}\n{random.choice(TIPS)}\n\n⚡ _PredixBot v3_"
    )
    kb=[[InlineKeyboardButton("🎯 Autre prediction",callback_data="new"),InlineKeyboardButton("📊 Historique",callback_data="hist")]]
    await msg.edit_text(text,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))
    u=update.effective_user
    save_pred(u.id,u.username or u.first_name,sport,t1,t2,res["verdict"],res["confidence"],res["win1"],res["draw"],res["win2"],res["analyse"])

async def handle_msg(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    text=update.message.text; uid=update.effective_user.id
    if uid in user_sessions:
        s=user_sessions[uid]
        if s["step"]=="team1":
            s["team1"]=text; s["step"]="team2"; user_sessions[uid]=s
            await update.message.reply_text(f"✅ *{text}* enregistre !\n\n⬇️ Entre maintenant le nom de l *equipe 2 / joueur 2* :",parse_mode="Markdown")
            return
        elif s["step"]=="team2":
            t1=s["team1"]; sport=s["sport"]; del user_sessions[uid]
            await run_pred(update,ctx,t1,text,sport); return
    if text=="🎯 Prediction":
        await update.message.reply_text("🎯 *Nouvelle Prediction*\n\n👇 *Choisis le sport :*",parse_mode="Markdown",reply_markup=sport_kb())
    elif text=="📅 Matchs a venir":
        matches=get_upcoming(); lines=["📅 *Matchs a venir - Clique pour predire !*\n━━━━━━━━━━━━━━━━━━━━━━━━\n"]; kb_rows=[]
        for m in matches:
            hot="🔥 " if m.get("hot") else "   "; emoji=EMOJIS.get(m["sport"].lower(),"🏆")
            lines.append(f"{hot}{emoji} *{m['t1']}* vs *{m['t2']}*\n   {m['ligue']} | 🕐 {m['date']}\n")
            kb_rows.append([InlineKeyboardButton(f"{emoji} {m['t1']} vs {m['t2']}",callback_data=f"Q|{m['sport']}|{m['t1']}|{m['t2']}")])
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━\n💡 _Appuie pour une prediction instantanee !_")
        await update.message.reply_text("\n".join(lines),parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb_rows))
    elif text=="📊 Historique":
        preds=get_history(uid)
        if not preds: await update.message.reply_text("📭 *Aucune prediction encore*\n\nAppuie sur 🎯 *Prediction* pour commencer !",parse_mode="Markdown",reply_markup=nav_kb()); return
        lines=["📊 *Tes 5 dernieres predictions*\n━━━━━━━━━━━━━━━━━━━━━━━━\n"]
        for i,p in enumerate(preds,1):
            ce,_=conf_info(p.get("confidence")); date=p.get("created_at","")[:10]
            lines.append(f"*{i}.* {ce} *{p['team1']}* vs *{p['team2']}*\n   🏷️ {p['sport']} | 📅 {date}\n   ➜ _{p['verdict']}_\n")
        await update.message.reply_text("\n".join(lines),parse_mode="Markdown",reply_markup=nav_kb())
    elif text=="📈 Mes stats":
        u=update.effective_user; total,high=get_stats(u.id); med=total-high
        pct=int(high/total*100) if total>0 else 0
        level="🥉 Debutant" if total<5 else "🥈 Intermediaire" if total<20 else "🥇 Expert" if total<50 else "💎 Legendaire"
        await update.message.reply_text(
            f"📈 *Tes stats PredixBot*\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 *{u.first_name}* | 🏅 {level}\n\n🎯 Total: *{total}*\n🔥 Haute confiance: *{high}*\n⚡ Autres: *{med}*\n\n"
            f"`{bar(pct)}` *{pct}% HIGH*\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n_Continue pour monter de niveau !_ 🚀",
            parse_mode="Markdown",reply_markup=nav_kb())
    elif text=="💡 Tips paris":
        all_tips=["1️⃣ Ne mise jamais plus de *5%* de ta bankroll sur un seul pari.","2️⃣ Les cotes *1.30-1.60* sont plus sures pour debuter.","3️⃣ Analyse toujours les *confrontations directes H2H*.","4️⃣ *HIGH confidence* ne garantit pas la victoire !","5️⃣ Combine *2-3 matchs HIGH* pour maximiser ton gain.","6️⃣ Evite les matchs *LOW confidence* - risque trop eleve.","7️⃣ Les *equipes a domicile* gagnent 45% des matchs en foot.","8️⃣ Attends les *compositions officielles* avant de miser.","9️⃣ Fixe une *limite de pertes journaliere* et respecte-la.","🔟 En eSports, les *patch recents* changent les favoris.","💎 Garde la tete froide - *ne chasse jamais tes pertes*.","🏆 Le meilleur parieur sait *quand ne pas parier*."]
        await update.message.reply_text("💡 *Tips & Conseils Paris Sportifs*\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"+"\n\n".join(all_tips)+"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n⚡ _PredixBot - Paris responsables_ 🙏",parse_mode="Markdown",reply_markup=nav_kb())
    elif text=="ℹ️ Aide":
        await update.message.reply_text(
            "ℹ️ *Guide PredixBot v3*\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Prediction* - Choisis un sport puis entre tes 2 equipes\n"
            "📅 *Matchs a venir* - Clique sur un match pour predire\n"
            "📊 *Historique* - Tes 5 dernieres predictions\n"
            "📈 *Mes stats* - Ton niveau et tes statistiques\n"
            "💡 *Tips paris* - 12 conseils de paris\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "*Commande rapide:*\n`/pred Football PSG vs Real Madrid`\n\n"
            "*Sports:* ⚽🏀🎾🎮🔫🧙🥊🏉",
            parse_mode="Markdown",reply_markup=nav_kb())

async def pred_cmd(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    args=ctx.args
    if not args or len(args)<3 or "vs" not in [a.lower() for a in args]:
        await update.message.reply_text("❌ Format: `/pred Football PSG vs Real Madrid`",parse_mode="Markdown"); return
    sport=args[0]; rest=" ".join(args[1:]); parts=rest.lower().split(" vs ")
    if len(parts)!=2: await update.message.reply_text("❌ Manque le *vs*.",parse_mode="Markdown"); return
    await run_pred(update,ctx,parts[0].strip().title(),parts[1].strip().title(),sport)

async def btn(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); uid=update.effective_user.id
    if q.data.startswith("S|"):
        sport=q.data.split("|")[1]; user_sessions[uid]={"sport":sport,"step":"team1"}
        await q.message.reply_text(f"🏷️ Sport: *{sport}*\n\n⬇️ Entre le nom de l *equipe 1 / joueur 1* :",parse_mode="Markdown")
    elif q.data.startswith("Q|"):
        parts=q.data.split("|"); sport,t1,t2=parts[1],parts[2],parts[3]
        msg=await q.message.reply_text("⚡ Analyse en cours..."); res=predict(t1,t2,sport); ce,ct=conf_info(res["confidence"])
        no_draw=any(nd in sport.lower() for nd in NO_DRAW)
        draw_line=f"➖ Nul\n`{bar(res['draw'])}` *{res['draw']}%*\n" if not no_draw else ""
        facs="\n".join([f"  {f}" for f in res["facteurs"]])
        text=(f"{res['emoji']} *{t1}* ⚔️ *{t2}*\n🏷️ {sport}\n{'━'*26}\n\n💪 *Niveau*\n  {t1}: {stars(res['s1'])} `{res['s1']}/100`\n  {t2}: {stars(res['s2'])} `{res['s2']}/100`\n\n📊 *Probabilites*\n✅ {t1}\n`{bar(res['win1'])}` *{res['win1']}%*\n{draw_line}❌ {t2}\n`{bar(res['win2'])}` *{res['win2']}%*\n\n{'━'*26}\n🏆 *Verdict:* {res['verdict']}\n💰 *Cote:* `{res['cote']}`\n{ce} *Confiance:* {ct}\n\n📝 *Analyse:*\n_{res['analyse']}_\n\n🔍 *Facteurs:*\n{facs}\n\n⚡ _PredixBot v3_")
        kb=[[InlineKeyboardButton("🎯 Autre prediction",callback_data="new"),InlineKeyboardButton("📊 Historique",callback_data="hist")]]
        await msg.edit_text(text,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))
        u=update.effective_user; save_pred(u.id,u.username or u.first_name,sport,t1,t2,res["verdict"],res["confidence"],res["win1"],res["draw"],res["win2"],res["analyse"])
    elif q.data=="new":
        await q.message.reply_text("🎯 *Choisis le sport :*",parse_mode="Markdown",reply_markup=sport_kb())
    elif q.data=="hist":
        preds=get_history(uid)
        if not preds: await q.message.reply_text("📭 Aucune prediction encore.")
        else:
            lines=["📊 *Historique:*\n"]
            for p in preds:
                ce,_=conf_info(p.get("confidence")); lines.append(f"{ce} *{p['team1']}* vs *{p['team2']}* - _{p['verdict']}_\n")
            await q.message.reply_text("\n".join(lines),parse_mode="Markdown")

def main():
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("pred",pred_cmd))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_msg))
    print("🚀 PredixBot v3 Ultra lance !")
    app.run_polling()

if __name__=="__main__":
    main()
