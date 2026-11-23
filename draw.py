#!/usr/bin/env python3
"""Draw the Monday 23 November 2026 front page (1024x1024 PNG) — v2.

64 stories, denser layout, same code-drawn newspaper format: every
letter is real text rendered by PIL, no AI-generated text, no network,
no randomness, no clock reads -- the same input always writes the same
bytes.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
MUTED = (91, 91, 91)
RED = (180, 35, 24)
BLUE = (30, 64, 175)
GREEN = (22, 101, 52)
ORANGE = (154, 52, 18)
PANEL = (255, 255, 255)
LINE = (180, 174, 158)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

TAG_FILL = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": ORANGE,
            "CLAIM": RED}


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, text, fnt, xy, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns y just below the last line."""
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def chip(d, x, y, label):
    """Small coloured confidence tag; returns width used."""
    fnt = SANS_B(10)
    tw = fnt.getlength(label)
    w, h = int(tw) + 10, 15
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=TAG_FILL[label])
    d.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def rule(d, x0, x1, y, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX, MX1 = 28, 996
    CW = MX1 - MX  # 968 content width

    # ---- kicker bar -------------------------------------------------
    d.rectangle([0, 0, W, 20], fill=INK)
    kf = SANS_B(12)
    d.text((MX, 4), "THE WORLD IN ONE DAY", font=kf, fill=(255, 255, 255))
    mid = "DAY 327 OF 2026"
    d.text(((W - kf.getlength(mid)) / 2, 4), mid, font=kf,
           fill=(255, 255, 255))
    right = "ALL TIMES UTC"
    d.text((MX1 - kf.getlength(right), 4), right, font=kf,
           fill=(255, 255, 255))

    # ---- masthead ---------------------------------------------------
    title = "MONDAY 23 NOVEMBER 2026"
    tf = SERIF_B(42)
    d.text(((W - tf.getlength(title)) / 2, 26), title, font=tf, fill=INK)
    sub = "64 STORIES  ·  9 REGIONS  ·  EVERY ONE DATED"
    sf = SANS(15)
    d.text(((W - sf.getlength(sub)) / 2, 72), sub, font=sf, fill=MUTED)
    rule(d, MX, MX1, 92, fill=INK, width=2)

    # ---- red 3-hook subline -----------------------------------------
    hooks = ("COP31 collapses with no deal   •   Iran strikes US bases in "
             "Bahrain   •   NATO meets on Poland missiles")
    hf = SERIF_B(17)
    d.text(((W - hf.getlength(hooks)) / 2, 98), hooks, font=hf, fill=RED)

    # ---- stats strip ------------------------------------------------
    stats = [("186", "drones fired"), ("161", "drones downed"),
             ("~25", "tankers hit in a week"), ("$7.5bn", "chips diverted"),
             ("720/9", "India's Test total"), ("98.79%", "HK turnout")]
    y0, y1 = 120, 152
    bw = CW / 6
    nf, lf = SERIF_B(23), SANS(10)
    for i, (num, lab) in enumerate(stats):
        x = MX + i * bw
        if i:
            d.line([(x, y0 + 3), (x, y1 - 3)], fill=LINE, width=1)
        d.text((x + (bw - nf.getlength(num)) / 2, y0 + 1), num, font=nf,
               fill=INK)
        d.text((x + (bw - lf.getlength(lab)) / 2, y0 + 25), lab, font=lf,
               fill=MUTED)
    rule(d, MX, MX1, 156, fill=LINE, width=1)

    # ---- region bar -------------------------------------------------
    regions = ("EU 7  ·  ME 7  ·  APAC 22  ·  AMER 12  ·  AFR 5  ·  OCE 2  ·  "
               "SPORT 5  ·  SCI 2  ·  WORLD 2")
    rf = SANS_B(11)
    d.text(((W - rf.getlength(regions)) / 2, 162), regions, font=rf,
           fill=INK)

    # ---- timeline strip ---------------------------------------------
    tl = ("00:00 UTC  Cikande search resumes   ·   00:02 UTC  Lunch, Day 5, "
          "Wellington: NZ 157/4   ·   TODAY  NATO Council meets   ·   TODAY  "
          "Modi-Shah talks   ·   TODAY  Oil futures reopen")
    tlf = SANS(11)
    d.text(((W - tlf.getlength(tl)) / 2, 180), tl, font=tlf, fill=MUTED)
    rule(d, MX, MX1, 198, fill=INK, width=1)

    # ---- section header ---------------------------------------------
    d.text((MX, 204), "THE THREE BIG STORIES", font=SANS_B(13), fill=INK)
    rule(d, MX, MX1, 222, fill=INK, width=1)

    # ---- three leads ------------------------------------------------
    leads = [
        dict(kick="CLIMATE  ·  ANTALYA, TURKEY",
             head="COP31 COLLAPSES — NO DEAL",
             body=("Sunday: the longest climate summit ever ends with no "
                   "deal. The EU, UK and island states reject the "
                   "'Antalya Pact' — it never mentions fossil fuels."),
             tag="CONFIRMED", panel="cop"),
        dict(kick="GULF  ·  BAHRAIN / HORMUZ",
             head="IRAN STRIKES US BASES; TANKER WAR",
             body=("Saturday night: IRGC missiles and drones hit US "
                   "positions in Bahrain; 2 injured. ~25 tankers hit in "
                   "and around the Strait of Hormuz in a week."),
             tag="CONFIRMED", panel="gulf"),
        dict(kick="SECURITY  ·  BRUSSELS, TODAY",
             head="NATO MEETS ON POLAND MISSILES",
             body=("Extraordinary North Atlantic Council session in "
                   "Brussels today after Russian missiles crossed into "
                   "Poland on Friday. All three were Kh-101s, prosecutors "
                   "say."),
             tag="CONFIRMED", panel="nato"),
    ]
    col_w, gap = 314, 13
    for i, lead in enumerate(leads):
        x = MX + i * (col_w + gap)
        d.text((x, 228), lead["kick"], font=SANS_B(10), fill=RED)
        # drawn panel, 56px tall
        px, py, pw, ph = x, 242, col_w, 56
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL,
                    outline=LINE, width=1)
        if lead["panel"] == "cop":
            cx, cy, r = px + 38, py + 28, 20
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE,
                      width=2)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(219, 234,
                                                               254))
            d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=1)
            d.ellipse([cx - 8, cy - r, cx + 8, cy + r], outline=BLUE,
                      width=1)
            d.rectangle([px + 70, py + 13, px + 172, py + 38],
                        outline=RED, width=2)
            d.text((px + 80, py + 18), "NO DEAL", font=SANS_B(15),
                   fill=RED)
            d.text((px + 180, py + 18), "ANTALYA", font=SANS_B(9),
                   fill=MUTED)
            d.text((px + 180, py + 32), "35% by 2035", font=SANS_B(9),
                   fill=MUTED)
            d.text((px + 70, py + 41), "draft kept fossil fuels out",
                   font=SANS(9), fill=MUTED)
        elif lead["panel"] == "gulf":
            d.rectangle([px, py, px + pw, py + 14], fill=(222, 226, 214))
            d.rectangle([px, py + 42, px + pw, py + ph],
                        fill=(222, 226, 214))
            d.rectangle([px, py + 14, px + pw, py + 42], fill=(191, 219,
                                                                254))
            d.text((px + 6, py + 2), "IRAN", font=SANS_B(9), fill=MUTED)
            d.text((px + 6, py + 44), "ARABIAN SEA", font=SANS_B(9),
                   fill=MUTED)
            for sx in (96, 156, 216):
                d.rectangle([px + sx, py + 28, px + sx + 22, py + 34],
                            fill=INK)
                d.rectangle([px + sx + 7, py + 22, px + sx + 10, py + 28],
                            fill=INK)
            for ex, ey in ((px + 137, py + 21), (px + 197, py + 21)):
                d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=RED,
                          outline=(255, 255, 255), width=1)
            d.text((px + 248, py + 2), "HORMUZ", font=SANS_B(9), fill=RED)
            d.text((px + 6, py + 17), "~25 tankers hit", font=SANS_B(9),
                   fill=INK)
        else:
            pts = [(px + 157, py + 3), (px + 200, py + 12),
                   (px + 200, py + 34), (px + 157, py + 53),
                   (px + 114, py + 34), (px + 114, py + 12)]
            d.polygon(pts, fill=(30, 64, 175), outline=(20, 40, 120))
            for k in range(32):
                a = 2 * math.pi * k / 32 - math.pi / 2
                sx = px + 157 + 30 * math.cos(a)
                sy = py + 28 + 20 * math.sin(a)
                d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                          fill=(255, 255, 255))
            d.text((px + 214, py + 40), "32 MEMBERS", font=SANS_B(9),
                   fill=MUTED)
            d.text((px + 8, py + 40), "EASTERN FLANK", font=SANS_B(9),
                   fill=MUTED)
        hf2 = SERIF_B(17)
        y = draw_wrapped(d, lead["head"], hf2, (x, 304), col_w, fill=INK,
                         leading=19)
        y = draw_wrapped(d, lead["body"], SANS(11), (x, y + 2), col_w,
                         fill=INK, leading=13)
        chip(d, x, 389, lead["tag"])

    # ---- the day in twenty ------------------------------------------
    d.text((MX, 412), "THE DAY IN TWENTY", font=SANS_B(13), fill=INK)
    rule(d, MX, MX1, 430, fill=INK, width=1)
    twenty = [
        ("UKRAINE", "Dymer: 3 dead, 14 trapped",
         "A drone flattens a block in Dymer; ~2,700 drones fired in a week.",
         "CONFIRMED"),
        ("NEPAL-INDIA", "Modi-Shah talks today",
         "Nepal PM Balen Shah meets Narendra Modi in Delhi; MoUs on energy and trade.",
         "CONFIRMED"),
        ("INDONESIA", "Cikande search resumes",
         "Search resumes 07:00 Monday: 29 missing, 8 unconfirmed; 24 body bags out.",
         "REPORTED"),
        ("TECH", "$7.5bn chips to China",
         "FT: a network around ex-Megaspeed exec Alice Huang diverted ~240,000 Nvidia chips.",
         "REPORTED"),
        ("MYANMAR", "Rejects ASEAN and ICJ",
         "Army-backed government calls an ASEAN decision 'unfair' and rejects the UN court ruling.",
         "CONFIRMED"),
        ("CRICKET", "LIVE: NZ 157/4",
         "India need 6 wickets on the final day in Wellington; 720/9 is a record Test total in NZ.",
         "CONFIRMED"),
        ("HONG KONG", "Election Committee vote",
         "856 candidates for 723 seats; turnout 98.79%. It picks the next chief executive.",
         "OFFICIAL"),
        ("BOLSONARO", "Surgery call due today",
         "Ex-president, 71, still in intensive care in Brasilia; the surgery call is due today.",
         "CONFIRMED"),
        ("MARKETS", "Asia slides again",
         "Taiex -6%, Kospi -3.8% as the AI rout spreads; Tokyo closed; US futures bounce ~2%.",
         "REPORTED"),
        ("EUROPE", "Lisbon marches",
         "Thousands march in Lisbon over living costs as anger at prices fuels protests.",
         "REPORTED"),
        ("MEXICO", "El Chapo Isidro caught",
         "FBI most-wanted cartel boss captured after firefights in Sinaloa; 11 dead.",
         "CONFIRMED"),
        ("UKRAINE", "14 missing in Kyiv region",
         "Russian drone hits a building in the Kyiv region; 14 people missing, Zelenskiy says.",
         "CONFIRMED"),
        ("BALTIC", "Cargo ship still burning",
         "Russian cargo ship Sparta II still on fire off Finland after an attack.",
         "CONFIRMED"),
        ("USA", "Schumer faces challenge",
         "Senate Democratic leader faces Chris Van Hollen; first contested race since 1994.",
         "CONFIRMED"),
        ("CHINA", "Margin rules eased",
         "Exchanges cut minimum margin ratio to 80% from Nov 30; Shanghai at a 16-month low.",
         "REPORTED"),
        ("USA", "$TRUMP gala tonight",
         "Trump hosts a gala for top holders of his meme coin, now under $1 from a ~$75 peak.",
         "CONFIRMED"),
        ("TECH", "Anthropic IPO slides",
         "Shares fall 8.5% Friday after a 17% first-day pop; bankers chafed at the process.",
         "REPORTED"),
        ("SPORT", "Verstappen wins in Vegas",
         "Max Verstappen wins a chaotic Las Vegas GP by 0.639s from Norris; Russell crashes late.",
         "CONFIRMED"),
        ("SPORT", "Liverpool 4–0 Man Utd",
         "Liverpool thrash Manchester United 4-0 at Anfield in the Premier League.",
         "CONFIRMED"),
        ("FILM", "Hunger Games: $120m",
         "Sunrise on the Reaping opens with $120m in the US and $225m worldwide.",
         "CONFIRMED"),
    ]
    cw20, gap20 = 239, 4
    for i, (region, head, body, tag) in enumerate(twenty):
        col, row = i % 4, i // 4
        x = MX + col * (cw20 + gap20)
        y = 436 + row * 50
        d.rectangle([x, y, x + cw20, y + 48], fill=PANEL, outline=LINE,
                    width=1)
        d.text((x + 6, y + 3), "%d  %s" % (i + 4, region), font=SANS_B(9),
               fill=RED)
        d.text((x + 6, y + 14), head, font=SERIF_B(12), fill=INK)
        draw_wrapped(d, body, SANS(9), (x + 6, y + 28), cw20 - 12,
                     fill=INK, leading=10)

    # ---- bottom: map + also list ------------------------------------
    d.text((MX, 694), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((252, 694), "ALSO ON MONDAY — 41 MORE", font=SANS_B(12),
           fill=INK)
    rule(d, MX, MX1, 712, fill=INK, width=1)
    # simplified world map (rough equirectangular continents)
    mx0, my0, mw, mh = 28, 724, 208, 130

    def ll(lon, lat):
        return (mx0 + (lon + 170) / 360.0 * mw,
                my0 + (75 - lat) / 130.0 * mh)

    continents = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73),
         (-60, 60), (-55, 47), (-70, 42), (-80, 32), (-90, 21),
         (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-150, 60)],
        [(-80, 10), (-60, 8), (-35, -8), (-40, -22), (-55, -35),
         (-70, -52), (-73, -40), (-70, -20), (-80, -5)],
        [(-18, 35), (-10, 30), (10, 37), (30, 31), (43, 12), (51, 11),
         (40, -5), (35, -20), (20, -35), (12, -18), (8, 4), (-8, 5)],
        [(-10, 36), (-9, 43), (-2, 48), (0, 51), (8, 54), (18, 56),
         (28, 60), (30, 70), (40, 68), (45, 60), (30, 46), (20, 40),
         (12, 44), (3, 42)],
        [(40, 68), (60, 70), (90, 75), (120, 73), (150, 70), (178, 66),
         (162, 58), (140, 45), (130, 35), (122, 30), (108, 12),
         (100, 8), (90, 22), (80, 8), (72, 20), (60, 25), (50, 29),
         (43, 12)],
        [(113, -22), (125, -14), (142, -11), (150, -22), (150, -37),
         (140, -38), (130, -32), (115, -35)],
    ]
    for poly in continents:
        d.polygon([ll(lo, la) for lo, la in poly], fill=(203, 213, 225),
                  outline=(120, 130, 145))
    dots = [(30.7, 36.9, "1"), (50.6, 26.2, "2"), (4.35, 50.85, "3"),
            (30.5, 50.45, "4"), (77.2, 28.6, "5"), (106.2, -6.2, "6"),
            (174.8, -41.3, "9"), (114.2, 22.3, "10"),
            (-47.9, -15.8, "11"), (-9.1, 38.7, "13"), (3.4, 6.5, "33"),
            (28.5, 8.0, "34"), (-122.4, 37.8, "26")]
    df = SANS_B(8)
    for lon, lat, num in dots:
        cx, cy = ll(lon, lat)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx - df.getlength(num) / 2, cy - 4), num, font=df,
               fill=(255, 255, 255))
    d.text((MX, 860), "13 sites numbered", font=SANS(9), fill=MUTED)
    d.text((MX, 872), "to the stories above", font=SANS(9), fill=MUTED)

    # also list: 41 items, two columns, one line each
    also = [
        (24, "USA — FBI probes apparent hack of its NCIC database. [REPORTED]"),
        (25, "USA — CISA deadline: patch VMware, Cisco, Apache and SAP flaws."),
        (26, "USA — SF king tides may peak near 9 ft, a record."),
        (27, "India — BJP MP Ramrao Wadkute dies of a cardiac arrest in Delhi."),
        (28, "India — Shah launches Rs 4,000 cr push in Arunachal Pradesh."),
        (29, "India — 9 pilgrims killed as their vehicle rams a truck in Kota."),
        (30, "India — IFFI 2026 hosts a BRICS roundtable on film partnerships."),
        (31, "India — Hyderabad students protest over alleged casteist remarks."),
        (32, "Sport — Anupama retains the IBSF World Women's Snooker title."),
        (33, "Africa — NDLEA Lagos: golfer, chef held over 50 kg cannabis haul."),
        (34, "Africa — South Sudan: rebels kill 24, incl. 7 children. [REPORTED]"),
        (35, "Science — BepiColombo glitch at Mercury entry; craft safe."),
        (36, "Science — JWST finds a possible black hole that outgrew its galaxy."),
        (37, "Gulf — Qatar visited Tehran Friday; Iran demands blockade end."),
        (38, "Gaza — no fresh development reported on Monday."),
        (39, "Oceania — NZ retail sales and Australia flash PMIs due today."),
        (40, "UN — nations agree to keep negotiating lethal AI weapons rules."),
        (41, "UK — Britain to produce Ukrainian drones under a new agreement."),
        (42, "S Korea — education minister quits over AI cheating scandal."),
        (43, "Australia — PM: COP31 failure shows 'difficult times'."),
        (44, "WHO — chief pleads for peace in Ebola-hit DR Congo area."),
        (45, "Sudan — drone strikes hit homes and a UN building in Khartoum."),
        (46, "Israel — Netanyahu, Eisenkot end talks with no government deal."),
        (47, "Nigeria — 35 Fulanis killed in revenge attacks in Kano State."),
        (48, "Saudi — coalition intercepts Houthi missile in the west."),
        (49, "West Bank — Eisenkot condemns settler arson attacks on villages."),
        (50, "Pakistan — 15 terrorists killed in two operations in Mastung."),
        (51, "Pakistan — Imran Khan, Bushra Bibi appeals set for November 25."),
        (52, "India — Modi: 50 crore lifted out of poverty, World Bank says."),
        (53, "India — Modi opens AI centre at IIT Patna, Rs 400 cr park."),
        (54, "India — PM announces Rs 2 lakh aid after Kutch mishap."),
        (55, "India — winter session delayed; monsoon session hits 100 days."),
        (56, "India — Vijayan hits Modi over corporate pay remarks."),
        (57, "India — UP runs air-raid, blackout drills in all 75 districts."),
        (58, "Sport — Newcastle 2–2 Arsenal; Hull 2–0 Brighton on Sunday."),
        (59, "Crypto — Bitcoin holds $60k; ETFs bled $1.25bn last week."),
        (60, "Film — Ramayana crosses Rs 940 cr net in India after Day 18."),
        (61, "USA — Kalshi in court Monday over NY order to shut it down."),
        (62, "Markets — oil reopens Monday, first futures price of tanker war."),
        (63, "Tech — Apple building an AI agent to run your Mac. [REPORTED]"),
        (64, "Kashmir — saffron fields used as dump for 3 years: Mufti."),
    ]
    af = SANS(9)
    afb = SANS_B(9)
    for i, (num, text) in enumerate(also):
        col = 0 if i < 21 else 1
        row = i if i < 21 else i - 21
        x = 252 if col == 0 else 636
        y = 718 + row * 10
        d.text((x, y), "%d." % num, font=afb, fill=RED)
        d.text((x + 20, y), text, font=af, fill=INK)

    # ---- date check -------------------------------------------------
    d.rectangle([MX, 936, MX1, 994], outline=RED, width=2)
    d.text((MX + 8, 940), "DATE CHECK — NOT MONDAY'S NEWS",
           font=SANS_B(10), fill=RED)
    dc = SANS(9)
    dc_lines = [
        "THU 19 NOV — Trump-Xi-Putin summit, Shenzhen · ICJ Myanmar ruling",
        ("FRI 20 NOV — Market rout (S&P -3.7%, Nasdaq -5.3%) · UK-EU "
         "Brexit reset · Denmark expels Russian attaché · Poland incursion "
         "(event) · Bolsonaro admitted"),
        ("SAT 21 NOV — Gaza food-van strike (3 killed) · BepiColombo enters "
         "Mercury orbit · EU-Indonesia trade deal · Cikande fire breaks "
         "out · Sparta II struck"),
        ("SUN 22 NOV — COP31 collapse · Dymer strike · Hong Kong EC "
         "election · NDLEA arrests · Myanmar rejects ASEAN · Verstappen "
         "wins Las Vegas GP · India declare 720/9 (final day is today)"),
    ]
    yy = 954
    for ln in dc_lines:
        d.text((MX + 8, yy), ln, font=dc, fill=INK)
        yy += 10

    # ---- footer -----------------------------------------------------
    ff = SANS(9)
    d.text((MX, 998), "Sources: Reuters · CNN · The Times · FT · Al Jazeera "
           "· AFP · IANS · ANI · ESPNcricinfo · Cricbuzz · ESA · News "
           "Central TV · NDLEA · Finnhub · Cinepals", font=ff, fill=MUTED)
    d.text((MX, 1009), "CONFIRMED = verified by 2+ outlets · OFFICIAL = "
           "government or agency statement · REPORTED = single source · "
           "CLAIM = one side's claim  ·  Wires read up to 00:35 UTC, Mon 23 "
           "Nov 2026 · Drawn by code", font=ff, fill=MUTED)

    out = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                       dither=Image.Dither.NONE)
    out.save("entry.png", optimize=True)
    print("saved entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()
