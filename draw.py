#!/usr/bin/env python3
"""Draw the Monday 23 November 2026 front page (1024x1024 PNG).

Code-drawn newspaper front page: every letter is real text rendered by
PIL, no AI-generated text, no network, no randomness, no clock reads --
the same input always writes the same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
MUTED = (91, 91, 91)
RED = (180, 35, 24)
DARKRED = (140, 25, 18)
BLUE = (30, 64, 175)
GREEN = (22, 101, 52)
ORANGE = (154, 52, 18)
PANEL = (255, 255, 255)
PANEL_BG = (238, 234, 222)
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
    d.rectangle([0, 0, W, 30], fill=INK)
    kf = SANS_B(14)
    d.text((MX, 7), "THE WORLD IN ONE DAY", font=kf, fill=(255, 255, 255))
    mid = "DAY 327 OF 2026"
    d.text(((W - kf.getlength(mid)) / 2, 7), mid, font=kf,
           fill=(255, 255, 255))
    right = "ALL TIMES UTC"
    d.text((MX1 - kf.getlength(right), 7), right, font=kf,
           fill=(255, 255, 255))

    # ---- masthead ---------------------------------------------------
    title = "MONDAY 23 NOVEMBER 2026"
    tf = SERIF_B(50)
    d.text(((W - tf.getlength(title)) / 2, 40), title, font=tf, fill=INK)
    sub = "30 STORIES  ·  8 REGIONS  ·  EVERY ONE DATED"
    sf = SANS(17)
    d.text(((W - sf.getlength(sub)) / 2, 98), sub, font=sf, fill=MUTED)
    rule(d, MX, MX1, 122, fill=INK, width=2)

    # ---- red 3-hook subline -----------------------------------------
    hooks = ("COP31 collapses with no deal   •   Iran strikes US bases in "
             "Bahrain   •   NATO meets on Poland missiles")
    hf = SERIF_B(19)
    while hf.getlength(hooks) > CW and hf.size > 15:
        hf = SERIF_B(hf.size - 1)
    d.text(((W - hf.getlength(hooks)) / 2, 130), hooks, font=hf, fill=RED)

    # ---- stats strip ------------------------------------------------
    stats = [("186", "drones fired at Ukraine"),
             ("161", "drones downed"),
             ("~25", "tankers hit in a week"),
             ("$7.5bn", "chips diverted to China"),
             ("720/9", "India's record Test total"),
             ("98.79%", "Hong Kong turnout")]
    y0, y1 = 158, 202
    bw = CW / 6
    nf, lf = SERIF_B(25), SANS(10)
    for i, (num, lab) in enumerate(stats):
        x = MX + i * bw
        if i:
            d.line([(x, y0 + 4), (x, y1 - 4)], fill=LINE, width=1)
        d.text((x + (bw - nf.getlength(num)) / 2, y0 + 2), num, font=nf,
               fill=INK)
        for j, ln in enumerate(wrap(lab, lf, bw - 12)):
            d.text((x + (bw - lf.getlength(ln)) / 2, y0 + 30 + j * 12), ln,
                   font=lf, fill=MUTED)
    rule(d, MX, MX1, y1 + 2, fill=LINE, width=1)

    # ---- region bar -------------------------------------------------
    regions = ("EUROPE  ·  MIDDLE EAST  ·  ASIA-PACIFIC  ·  AMERICAS  ·  "
               "AFRICA  ·  OCEANIA  ·  SPORT  ·  SCIENCE")
    rf = SANS_B(13)
    d.text(((W - rf.getlength(regions)) / 2, 210), regions, font=rf,
           fill=INK)

    # ---- timeline strip ---------------------------------------------
    tl = ("00:00 UTC  Cikande search resumes   ·   00:02 UTC  Lunch, Day 5, "
          "Wellington: NZ 157/4   ·   TODAY  NATO Council meets, Brussels"
          "   ·   TODAY  Modi-Shah talks, Delhi")
    tlf = SANS(12)
    d.text(((W - tlf.getlength(tl)) / 2, 232), tl, font=tlf, fill=MUTED)
    rule(d, MX, MX1, 252, fill=INK, width=1)

    # ---- section header ---------------------------------------------
    d.text((MX, 260), "THE THREE BIG STORIES", font=SANS_B(14), fill=INK)
    rule(d, MX, MX1, 280, fill=INK, width=1)

    # ---- three leads ------------------------------------------------
    leads = [
        dict(kick="CLIMATE  ·  ANTALYA, TURKEY",
             head="COP31 COLLAPSES — NO DEAL",
             body=("Sunday: the longest climate summit ever ends with no "
                   "deal. The EU, UK and island states reject the "
                   "'Antalya Pact' — it never mentions fossil fuels. "
                   "Kurum: 'there is no agreement on this text.'"),
             tag="CONFIRMED", panel="cop"),
        dict(kick="GULF  ·  BAHRAIN / HORMUZ",
             head="IRAN STRIKES US BASES; TANKER WAR",
             body=("Saturday night: IRGC missiles and drones hit US "
                   "positions at al-Riffa and Awali in Bahrain; 2 people "
                   "injured. ~25 tankers hit in and around the Strait of "
                   "Hormuz in a week."),
             tag="CONFIRMED", panel="gulf"),
        dict(kick="SECURITY  ·  BRUSSELS, TODAY",
             head="NATO MEETS ON POLAND MISSILES",
             body=("An extraordinary North Atlantic Council session meets "
                   "in Brussels today after Russian missiles crossed "
                   "into Poland on Friday. Prosecutors say all three "
                   "objects were Russian Kh-101s."),
             tag="CONFIRMED", panel="nato"),
    ]
    col_w, gap = 314, 13
    for i, lead in enumerate(leads):
        x = MX + i * (col_w + gap)
        kf2 = SANS_B(11)
        d.text((x, 282), lead["kick"], font=kf2, fill=RED)
        # drawn panel
        px, py, pw, ph = x, 298, col_w, 84
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL,
                    outline=LINE, width=1)
        if lead["panel"] == "cop":
            # globe with a NO DEAL stamp
            cx, cy, r = px + 52, py + 42, 32
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE,
                      width=2)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(219, 234,
                                                               254))
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=BLUE,
                  width=1)
            d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=BLUE,
                  width=1)
            d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=1)
            d.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline=BLUE,
                      width=1)
            d.rectangle([px + 100, py + 22, px + 232, py + 56],
                        outline=RED, width=3)
            sf2 = SANS_B(20)
            d.text((px + 112, py + 28), "NO DEAL", font=sf2, fill=RED)
            d.text((px + 238, py + 64), "ANTALYA", font=SANS_B(10),
                   fill=MUTED)
            d.text((px + 238, py + 26), "35% by 2035", font=SANS_B(10),
                   fill=MUTED)
            d.text((px + 100, py + 62), "draft kept", font=SANS(10),
                   fill=MUTED)
        elif lead["panel"] == "gulf":
            # strait schematic: land, sea, ships, missile arcs
            d.rectangle([px, py, px + pw, py + 24], fill=(222, 226, 214))
            d.rectangle([px, py + 60, px + pw, py + ph],
                        fill=(222, 226, 214))
            d.rectangle([px, py + 24, px + pw, py + 60], fill=(191, 219,
                                                                254))
            d.text((px + 8, py + 5), "IRAN", font=SANS_B(10), fill=MUTED)
            d.text((px + 8, py + 66), "ARABIAN SEA", font=SANS_B(10),
                   fill=MUTED)
            for sx in (96, 156, 216):
                d.rectangle([px + sx, py + 40, px + sx + 26, py + 48],
                            fill=INK)
                d.rectangle([px + sx + 8, py + 32, px + sx + 12, py + 40],
                            fill=INK)
            d.arc([px + 60, py - 12, px + 180, py + 54], 300, 60,
                  fill=RED, width=2)
            d.arc([px + 150, py - 6, px + 260, py + 50], 300, 60,
                  fill=RED, width=2)
            d.text((px + 244, py + 5), "HORMUZ", font=SANS_B(10),
                   fill=RED)
            d.text((px + 8, py + 28), "~25 tankers hit", font=SANS_B(10),
                   fill=INK)
        else:
            # NATO shield with 32 stars
            pts = [(px + 157, py + 6), (px + 218, py + 18),
                   (px + 218, py + 48), (px + 157, py + 80),
                   (px + 96, py + 48), (px + 96, py + 18)]
            d.polygon(pts, fill=(30, 64, 175), outline=(20, 40, 120))
            import math
            for k in range(32):
                a = 2 * math.pi * k / 32 - math.pi / 2
                sx = px + 157 + 42 * math.cos(a)
                sy = py + 43 + 28 * math.sin(a)
                d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                          fill=(255, 255, 255))
            d.text((px + 240, py + 64), "32 MEMBERS", font=SANS_B(10),
                   fill=MUTED)
            d.text((px + 10, py + 64), "EASTERN FLANK", font=SANS_B(10),
                   fill=MUTED)
        hf2 = SERIF_B(19)
        y = draw_wrapped(d, lead["head"], hf2, (x, 388), col_w, fill=INK,
                         leading=21)
        y = draw_wrapped(d, lead["body"], SANS(12), (x, y + 3), col_w,
                         fill=INK, leading=15)
        chip(d, x, 498, lead["tag"])

    # ---- the day in ten ---------------------------------------------
    d.text((MX, 520), "THE DAY IN TEN", font=SANS_B(14), fill=INK)
    rule(d, MX, MX1, 538, fill=INK, width=1)
    ten = [
        ("UKRAINE", "186 drones, 161 downed",
         "A drone flattens a block in Dymer: 3 dead, 14 may be trapped. "
         "~2,700 drones fired in a week.",
         "CONFIRMED"),
        ("NEPAL-INDIA", "Modi-Shah talks today",
         "Nepal PM Balen Shah meets Narendra Modi in Delhi; joint "
         "presser and MoUs on energy and trade.",
         "CONFIRMED"),
        ("INDONESIA", "Cikande search resumes",
         "Search resumes 07:00 Monday: 29 missing, 8 unconfirmed; 24 "
         "body bags removed Sunday; 3 dead.",
         "REPORTED"),
        ("TECH", "$7.5bn chips to China",
         "FT: a network around ex-Megaspeed executive Alice Huang "
         "diverted ~240,000 Nvidia AI chips to China.",
         "REPORTED"),
        ("MYANMAR", "Rejects ASEAN and ICJ",
         "Army-backed government calls an ASEAN decision 'unfair', "
         "rejects the UN court's Rohingya ruling.",
         "CONFIRMED"),
        ("CRICKET", "LIVE: NZ 157/4",
         "India need 6 wickets on the final day in Wellington; 720/9 "
         "is the highest Test total ever in NZ.",
         "CONFIRMED"),
        ("HONG KONG", "Election Committee vote",
         "856 candidates for 723 seats; turnout 98.79%. The body picks "
         "the next chief executive.",
         "OFFICIAL"),
        ("BOLSONARO", "Surgery call due today",
         "Ex-president, 71, still in intensive care in Brasilia with a "
         "blocked bowel; surgery call due today.",
         "CONFIRMED"),
        ("MARKETS", "Asia slides again",
         "Taiex -6%, Kospi -3.8% as the AI rout spreads; Tokyo closed; "
         "US futures bounce ~2%.",
         "REPORTED"),
        ("EUROPE", "Lisbon marches",
         "Thousands march in Lisbon over living costs as anger at "
         "prices fuels protests.",
         "REPORTED"),
    ]
    cw10, gap10 = 190, 4
    for i, (region, head, body, tag) in enumerate(ten):
        col, row = i % 5, i // 5
        x = MX + col * (cw10 + gap10)
        y = 544 + row * 74
        d.rectangle([x, y, x + cw10, y + 70], fill=PANEL, outline=LINE,
                    width=1)
        d.text((x + 6, y + 4), "%d  %s" % (i + 4, region), font=SANS_B(10),
               fill=RED)
        yy = draw_wrapped(d, head, SERIF_B(13), (x + 6, y + 18), cw10 - 12,
                          fill=INK, leading=15)
        draw_wrapped(d, body, SANS(10), (x + 6, yy + 1), cw10 - 12,
                     fill=INK, leading=11)

    # ---- bottom: map + also list ------------------------------------
    d.text((MX, 694), "WHERE IT HAPPENED", font=SANS_B(13), fill=INK)
    d.text((432, 694), "ALSO ON MONDAY", font=SANS_B(13), fill=INK)
    rule(d, MX, MX1, 712, fill=INK, width=1)
    # simplified world map (rough equirectangular continents)
    mx0, my0, mw, mh = 36, 718, 376, 138

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
            (-47.9, -15.8, "11"), (-9.1, 38.7, "13"), (3.4, 6.5, "24"),
            (28.5, 8.0, "25"), (-122.4, 37.8, "17")]
    df = SANS_B(9)
    for lon, lat, num in dots:
        cx, cy = ll(lon, lat)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx - df.getlength(num) / 2, cy - 5), num, font=df,
               fill=(255, 255, 255))
    counts = "EU 4 · ME 3 · APAC 9 · AMER 4 · AFR 2 · OCE 2 · SPORT 2 · SCI 2"
    cf = SANS_B(10)
    d.text(((36 + 412) / 2 - cf.getlength(counts) / 2, 860), counts,
           font=cf, fill=MUTED)

    # also list: 17 items, two columns
    also = [
        (14, "Baltic Sea — Russian cargo ship Sparta II still burning, "
             "drifting into Finnish waters."),
        (15, "USA — FBI probes an apparent hack of its NCIC national "
             "crime database. [REPORTED]"),
        (16, "USA — CISA deadline today: agencies must patch VMware, "
             "Cisco, Apache and SAP flaws."),
        (17, "USA — San Francisco king tides may peak near 9 ft, a "
             "record; no non-essential travel Mon-Wed."),
        (18, "India — BJP MP Ramrao Wadkute dies of a cardiac arrest in "
             "Delhi."),
        (19, "India — Amit Shah launches a Rs 4,000 crore infrastructure "
             "push in Arunachal Pradesh."),
        (20, "India — 9 pilgrims killed as their vehicle rams a truck in "
             "Kota, Rajasthan."),
        (21, "India — IFFI 2026 hosts a BRICS roundtable on film "
             "partnerships."),
        (22, "India — Hyderabad university students protest over alleged "
             "casteist remarks."),
        (23, "Sport — Anupama retains the IBSF World Women's Snooker "
             "title."),
        (24, "Africa — NDLEA Lagos: golfer and chef held over a 50.40 kg "
             "cannabis smuggling attempt."),
        (25, "Africa — South Sudan: rebels kill 24 civilians, incl. 7 "
             "children, in Warrap State. [REPORTED]"),
        (26, "Science — BepiColombo thruster glitch in its Mercury orbit "
             "entry; craft safe, ESA update due today."),
        (27, "Science — JWST finds a possible black hole that outgrew "
             "its host galaxy 12bn years ago."),
        (28, "Gulf — Qatari delegation visited Tehran Friday; Iran "
             "demands the blockade end and assets unfrozen."),
        (29, "Gaza — no fresh development reported on Monday."),
        (30, "Oceania — NZ retail sales and Australia flash PMIs due "
             "today."),
    ]
    af = SANS(10)
    for i, (num, text) in enumerate(also):
        col = 0 if i < 9 else 1
        row = i if i < 9 else i - 9
        x = 432 if col == 0 else 720
        y = 718 + row * 21
        d.text((x, y), "%d." % num, font=SANS_B(10), fill=RED)
        draw_wrapped(d, text, af, (x + 22, y), 254, fill=INK, leading=10)

    # ---- date check -------------------------------------------------
    d.rectangle([MX, 912, MX1, 978], outline=RED, width=2)
    d.text((MX + 8, 917), "DATE CHECK — NOT MONDAY'S NEWS",
           font=SANS_B(11), fill=RED)
    dc = SANS(10)
    dc_lines = [
        "THU 19 NOV — ICJ Myanmar ruling · Trump-Xi-Putin summit, Shenzhen",
        ("FRI 20 NOV — Market rout (S&P -3.7%, Nasdaq -5.3%) · UK-EU "
         "Brexit reset · Denmark expels Russian attaché · Poland incursion "
         "(event) · Bolsonaro admitted"),
        ("SAT 21 NOV — Gaza food-van strike (3 killed) · El Chapo Isidro "
         "captured · BepiColombo enters Mercury orbit · EU-Indonesia trade "
         "deal · Cikande fire breaks out · Sparta II struck"),
        ("SUN 22 NOV — COP31 collapse · Dymer strike · Hong Kong EC "
         "election · NDLEA arrests · Myanmar rejects ASEAN · Verstappen "
         "wins Las Vegas GP · India declare 720/9 (final day is today)"),
    ]
    yy = 934
    for ln in dc_lines:
        d.text((MX + 8, yy), ln, font=dc, fill=INK)
        yy += 11

    # ---- footer -----------------------------------------------------
    ff = SANS(10)
    d.text((MX, 984), "Sources: Reuters · CNN · The Times · FT · Al Jazeera "
           "· AFP · IANS · ANI · ESPNcricinfo · Cricbuzz · info.gov.hk · "
           "ESA · News Central TV · NDLEA", font=ff, fill=MUTED)
    d.text((MX, 996), "CONFIRMED = verified by 2+ outlets · OFFICIAL = "
           "government or agency statement · REPORTED = single source · "
           "CLAIM = one side's claim", font=ff, fill=MUTED)
    d.text((MX, 1008), "Wires read up to 00:20 UTC, Monday 23 November 2026 "
           "· Drawn by code — no AI-generated text", font=ff, fill=MUTED)

    out = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                       dither=Image.Dither.NONE)
    out.save("entry.png", optimize=True)
    print("saved entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()



