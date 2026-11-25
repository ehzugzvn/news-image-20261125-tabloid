#!/usr/bin/env python3
"""TABLOID variant — news-image-20261125. Draws entry.png (1024x1024).
All art drawn with PIL shapes. All facts from CONTENT.md only."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (17, 17, 20)
WHITE = (255, 255, 255)
YELLOW = (255, 212, 0)
RED = (230, 51, 18)
GREY = (178, 178, 182)
DARK = (32, 32, 38)
PANEL = (24, 24, 30)
LINE = (64, 64, 72)

BASE = os.path.dirname(os.path.abspath(__file__))
_cache = {}


def font(size, bold=True):
    key = (size, bold)
    if key not in _cache:
        name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
        _cache[key] = ImageFont.truetype(os.path.join(BASE, "fonts", name), size)
    return _cache[key]


def tw(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0]


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, f, max_w, color, lh=None):
    lines = wrap(draw, text, f, max_w)
    if lh is None:
        lh = f.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=color)
        y += lh
    return y, len(lines)


def chip(draw, x, y, text, fg=(17, 17, 20), bg=YELLOW, size=13):
    f = font(size)
    w = tw(draw, text, f) + 14
    h = size + 10
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + 7, y + 5), text, font=f, fill=fg)
    return w


def tag_chip(draw, x, y, tag):
    colors = {"C": YELLOW, "O": (0, 200, 120), "R": (255, 170, 0), "F": (120, 180, 255)}
    return chip(draw, x, y, tag, fg=(17, 17, 20), bg=colors.get(tag, YELLOW), size=13)


# ---------------------------------------------------------------- art
def draw_rocket_panel(draw, x, y, w, h):
    # dawn sky bands
    bands = [(26, 18, 40), (64, 28, 46), (150, 62, 32), (232, 122, 30), (255, 170, 60)]
    for i, c in enumerate(bands):
        y0 = y + i * h // 5
        y1 = y + (i + 1) * h // 5
        draw.rectangle([x, y0, x + w, y1], fill=c)
    # sun
    cx, cy, r = x + w - 150, y + h - 26, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 220, 110))
    # horizon ground
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(12, 12, 16))
    # station silhouette (top right)
    sx, sy = x + w - 190, y + 8
    draw.rectangle([sx, sy + 6, sx + 150, sy + 12], fill=(20, 20, 26))
    draw.rectangle([sx + 18, sy, sx + 52, sy + 18], fill=(20, 20, 26))
    draw.rectangle([sx + 96, sy, sx + 130, sy + 18], fill=(20, 20, 26))
    draw.rectangle([sx + 62, sy + 4, sx + 88, sy + 14], fill=(20, 20, 26))
    # stars
    for (sx2, sy2) in [(x + 40, y + 12), (x + 120, y + 26), (x + 260, y + 10),
                       (x + 420, y + 18), (x + 560, y + 8), (x + 700, y + 22)]:
        draw.ellipse([sx2 - 2, sy2 - 2, sx2 + 2, sy2 + 2], fill=WHITE)
    # rocket (left of centre)
    rx = x + 150
    ry = y + 18
    draw.polygon([(rx - 16, ry + 62), (rx - 16, ry + 22), (rx, ry),
                  (rx + 16, ry + 22), (rx + 16, ry + 62)], fill=WHITE)
    draw.polygon([(rx - 16, ry + 22), (rx, ry), (rx - 16, ry + 40)], fill=RED)
    draw.rectangle([rx - 16, ry + 62, rx + 16, ry + 74], fill=(200, 200, 205))
    draw.polygon([(rx - 26, ry + 74), (rx - 14, ry + 62), (rx - 14, ry + 74)], fill=RED)
    draw.polygon([(rx + 26, ry + 74), (rx + 14, ry + 62), (rx + 14, ry + 74)], fill=RED)
    # flame
    draw.polygon([(rx - 10, ry + 74), (rx + 10, ry + 74), (rx, ry + 104)],
                 fill=(255, 200, 40))
    draw.polygon([(rx - 5, ry + 74), (rx + 5, ry + 74), (rx, ry + 92)],
                 fill=(255, 240, 150))
    # smoke
    for i, r2 in enumerate([14, 18, 22]):
        draw.ellipse([rx - 44 - i * 8, ry + 96, rx - 44 - i * 8 + r2 * 2,
                      ry + 96 + r2], fill=(120, 110, 105))
        draw.ellipse([rx + 30 + i * 8, ry + 96, rx + 30 + i * 8 + r2 * 2,
                      ry + 96 + r2], fill=(120, 110, 105))


def draw_gavel_board(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 60, 34))
    for i in range(5):
        draw.line([x + 8, y + 10 + i * 12, x + w - 30, y + 10 + i * 12],
                  fill=(40, 160, 90), width=2)
    for i in range(4):
        cx = x + 20 + i * 36
        draw.rectangle([cx, y + 8, cx + 10, y + 18], fill=(255, 212, 0))
    # gavel
    draw.rectangle([x + 96, y + 12, x + 150, y + 26], fill=(180, 130, 60))
    draw.line([x + 122, y + 26, x + 138, y + h - 8], fill=(180, 130, 60), width=7)
    draw.ellipse([x + 118, y + h - 16, x + 158, y + h - 6], fill=(120, 120, 125))


def draw_grave_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 28, 34))
    bars = [18, 26, 34, 46, 58]
    for i, bh in enumerate(bars):
        bx = x + 14 + i * 30
        draw.rectangle([bx, y + h - 8 - bh, bx + 20, y + h - 8], fill=(150, 150, 158))
    draw.rectangle([x + w - 34, y + 8, x + w - 14, y + 34], fill=(200, 200, 205))
    draw.ellipse([x + w - 34, y + 4, x + w - 14, y + 16], fill=(200, 200, 205))
    draw.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=GREY, width=2)


def draw_chip_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(18, 22, 44))
    # chip
    draw.rectangle([x + 12, y + 14, x + 62, y + 52], fill=(40, 40, 48),
                   outline=YELLOW, width=2)
    draw.rectangle([x + 26, y + 26, x + 48, y + 40], fill=YELLOW)
    for i in range(3):
        draw.line([x + 18 + i * 14, y + 14, x + 18 + i * 14, y + 6],
                  fill=YELLOW, width=2)
        draw.line([x + 18 + i * 14, y + 52, x + 18 + i * 14, y + 60],
                  fill=YELLOW, width=2)
    # falling chart
    pts = [(x + 74, y + 14), (x + 96, y + 22), (x + 118, y + 18),
           (x + 140, y + 38), (x + 162, y + 54)]
    draw.line(pts, fill=RED, width=4)
    draw.polygon([(x + 162, y + 54), (x + 150, y + 50), (x + 158, y + 40)],
                 fill=RED)


def pictogram(draw, kind, x, y, s=34):
    """Small yellow pictogram in a s x s box."""
    draw.rectangle([x, y, x + s, y + s], fill=PANEL, outline=LINE)
    c = YELLOW
    if kind == "bomb":  # Hodeidah: explosion / tower
        draw.rectangle([x + 10, y + 14, x + 24, y + 30], fill=c)
        draw.polygon([(x + 17, y + 4), (x + 12, y + 14), (x + 22, y + 14)], fill=RED)
        draw.line([x + 6, y + 8, x + 12, y + 12], fill=c, width=2)
        draw.line([x + 28, y + 8, x + 22, y + 12], fill=c, width=2)
    elif kind == "shield":  # pact
        draw.polygon([(x + 17, y + 4), (x + 28, y + 9), (x + 28, y + 20),
                      (x + 17, y + 30), (x + 6, y + 20), (x + 6, y + 9)], fill=c)
        draw.line([x + 12, y + 17, x + 16, y + 21], fill=BG, width=2)
        draw.line([x + 16, y + 21, x + 23, y + 12], fill=BG, width=2)
    elif kind == "heart":  # femicide
        draw.ellipse([x + 7, y + 8, x + 17, y + 18], fill=RED)
        draw.ellipse([x + 17, y + 8, x + 27, y + 18], fill=RED)
        draw.polygon([(x + 8, y + 14), (x + 26, y + 14), (x + 17, y + 28)], fill=RED)
    elif kind == "mine":  # Hormuz
        draw.ellipse([x + 10, y + 10, x + 24, y + 24], fill=c)
        for dx, dy in [(0, -8), (0, 8), (-8, 0), (8, 0), (-6, -6), (6, -6),
                       (-6, 6), (6, 6)]:
            draw.line([x + 17, y + 17, x + 17 + dx, y + 17 + dy], fill=c, width=2)
    elif kind == "pct":  # tariffs
        draw.text((x + 7, y + 5), "%", font=font(24), fill=c)
    elif kind == "drone":  # Samara
        draw.rectangle([x + 12, y + 14, x + 22, y + 20], fill=c)
        for cx, cy in [(10, 10), (24, 10), (10, 24), (24, 24)]:
            draw.ellipse([x + cx - 4, y + cy - 4, x + cx + 4, y + cy + 4],
                         outline=c, width=2)
    elif kind == "quake":  # quakes
        draw.line([(x + 4, y + 20), (x + 10, y + 10), (x + 16, y + 24),
                   (x + 22, y + 8), (x + 30, y + 20)], fill=c, width=3)
    elif kind == "gavel":  # Shanghai
        draw.rectangle([x + 8, y + 8, x + 22, y + 16], fill=c)
        draw.line([x + 15, y + 16, x + 24, y + 28], fill=c, width=4)
    elif kind == "shop":  # Cartagena
        draw.rectangle([x + 6, y + 12, x + 28, y + 28], fill=c)
        draw.polygon([(x + 6, y + 12), (x + 10, y + 5), (x + 24, y + 5),
                      (x + 28, y + 12)], fill=RED)
    elif kind == "ship":  # Gulf of Finland
        draw.polygon([(x + 6, y + 18), (x + 28, y + 18), (x + 24, y + 26),
                      (x + 10, y + 26)], fill=c)
        draw.rectangle([x + 14, y + 8, x + 20, y + 18], fill=c)
        draw.line([x + 4, y + 30, x + 30, y + 30], fill=(90, 140, 200), width=2)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = 0

    # Kicker bar
    d.rectangle([0, 0, W, 20], fill=YELLOW)
    d.text((10, 3), "THE WORLD IN ONE DAY", font=font(13), fill=BG)
    r = "WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - 10 - tw(d, r, font(13)), 3), r, font=font(13), fill=BG)
    y = 20

    # Date — largest element
    d.text((12, y + 1), "WEDNESDAY", font=font(16), fill=GREY)
    d.text((10, y + 16), "25 NOVEMBER 2026", font=font(60), fill=YELLOW)
    y += 78
    # strip under date
    d.rectangle([0, y, W, y + 18], fill=PANEL)
    strip = "38 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS WEDNESDAY"
    d.text((10, y + 2), strip, font=font(13), fill=WHITE)
    regs = "Americas 8  ·  Europe 10  ·  Asia-Pacific 5  ·  Middle East 5  ·  Oceania 3  ·  Africa 4  ·  Global 3"
    d.text((W - 10 - tw(d, regs, font(13)), y + 2), regs, font=font(13), fill=YELLOW)
    y += 18

    # ---- GIANT LEAD: Shenzhou-24 (art left, text right)
    lead_h = 104
    draw_rocket_panel(d, 0, y, 380, lead_h)
    d.rectangle([380, y, W, y + lead_h], fill=(10, 10, 12))
    chip(d, 10, y + 5, "1st PAKISTANI ASTRONAUT", bg=YELLOW)
    tag_chip(d, W - 46, y + 5, "C")
    d.text((392, y + 4), "Shenzhou-24 lifts off with", font=font(24), fill=WHITE)
    d.text((392, y + 31), "a Pakistani pilot aboard", font=font(24), fill=YELLOW)
    d.text((392, y + 62),
           "Long March 2F launched from Jiuquan at 00:18 UTC; crew Tang Hongbo, Wu Yi and",
           font=font(13, bold=False), fill=WHITE)
    d.text((392, y + 76),
           "Muhammad Zeeshan Ali — the first Pakistani in orbit. Docked 03:56 UTC.",
           font=font(13, bold=False), fill=WHITE)
    d.text((392, y + 90), "XINHUA · REUTERS · CMSA", font=font(13), fill=GREY)
    y += lead_h

    # ---- 3 stacked leads
    leads = [
        ("Huawei guilty on 10 of 12 counts, and it will appeal",
         "A Brooklyn jury convicted the telecom giant of bank fraud, wire fraud, sanctions violations and "
         "stealing trade secrets after an 11-week trial; acquitted on racketeering and obstruction. "
         "Sentencing 14 Sep 2027.  REUTERS · CNN · WSJ", "C", draw_gavel_board),
        ("Russia's own figures show nearly 500,000 war dead",
         "Leaked Russian government data, analysed by BBC Russian Service, shows ~500,000 excess deaths "
         "among military-age men since the invasion; Moscow has not acknowledged the figures.  "
         "BBC RUSSIAN SERVICE · MEDIAZONA", "R", draw_grave_chart),
        ("Huang apologises to staff as Nvidia shares slide 5.9%",
         "A day after his Trump-backed return as CEO, Jensen Huang told staff he made \u201cterrible mistakes\u201d "
         "and breached the code of conduct; shares fell 5.9%. Senate hearing 3 Dec.  REUTERS · NYT · THE TIMES",
         "C", draw_chip_chart),
    ]
    for headline, summary, tag, art in leads:
        row_h = 56
        art(d, 10, y + 3, 150, row_h - 6)
        tx = 172
        tag_chip(d, W - 46, y + 3, tag)
        d.text((tx, y + 1), headline, font=font(17), fill=WHITE)
        draw_wrapped(d, tx, y + 21, summary, font(13, bold=False), W - 20 - tx, GREY, lh=14)
        y += row_h
        d.line([0, y, W, y], fill=LINE, width=1)

    # ---- Big-number strip
    nums = [
        ("10/12", "Huawei counts convicted"),
        ("\u2248500,000", "Russian war dead"),
        ("47,000", "women killed by partners"),
        ("11", "hurt in Riyadh strike"),
        ("5.9%", "Nvidia shares fell"),
        ("1st", "Pakistani in orbit"),
    ]
    d.rectangle([0, y, W, y + 46], fill=(30, 26, 0))
    col = W // 6
    for i, (n, cap) in enumerate(nums):
        cx = i * col + 8
        d.text((cx, y + 1), n, font=font(22), fill=YELLOW)
        d.text((cx, y + 28), cap, font=font(13, bold=False), fill=WHITE)
        if i:
            d.line([i * col, y + 3, i * col, y + 43], fill=LINE, width=1)
    y += 46

    # ---- Tier-2: 10 cards, 2 columns x 5 rows
    tier2 = [
        ("5", "bomb", "HODEIDAH / RIYADH", "Saudi jets bomb Hodeidah; Houthis hit Riyadh tower, 11 hurt",
         "Second strike on the PIF tower in six days.", "AL JAZEERA · REUTERS", "C"),
        ("6", "shield", "AUSTRALIA–SOLOMONS", "Australia signs sweeping pact with Solomon Islands",
         "Police, ports, schools — to blunt Beijing's reach.", "REUTERS · ABC", "O"),
        ("7", "heart", "FEMICIDE", "UN reports 47,000 women killed by partners or kin in a year",
         "129 a day; Africa's rate highest at 2.9 per 100,000.", "UNODC · UN WOMEN", "O"),
        ("8", "mine", "HORMUZ", "Two tankers hit mines in the Strait of Hormuz, IRGC says",
         "Saudis strike Hodeidah in reply.", "TIMES OF ISRAEL · GULF NEWS", "R"),
        ("9", "pct", "US TARIFFS", "US readies tariffs in 16-nation capacity probe, 15–25%",
         "China, India, Japan and ASEAN targeted.", "REUTERS · HINDUSTAN TIMES", "R"),
        ("10", "drone", "SAMARA", "Ukraine drones hit two Samara oil refineries, 800 km deep",
         "Kremlin rejects four-party talks.", "KYIV INDEPENDENT · AZERNEWS", "R"),
        ("11", "quake", "QUAKES", "M5.9 quakes strike off Baffin Island and near Antarctica",
         "Balleny Islands quake 10 km deep at 04:30 UTC.", "USGS", "O"),
        ("12", "gavel", "SHANGHAI", "Xi's anti-graft drive reaches Shanghai party boss",
         "Chen Jining probed before next year's reshuffle.", "GUARDIAN · CNA", "C"),
        ("13", "shop", "CARTAGENA", "Hostages held in a supermarket on a second day",
         "20 remain inside after a failed armoured-car raid.", "AP · EL TIEMPO", "R"),
        ("14", "ship", "GULF OF FINLAND", "A drone hits a Russian cargo ship in the gulf",
         "Zelenskyy confirmed the strike; Norway urged restraint.", "YLE · REUTERS", "R"),
    ]
    row_h = 44
    for r in range(5):
        for c in range(2):
            num, kind, place, head, summ, src, tag = tier2[r * 2 + c]
            x0 = 10 + c * 502
            pictogram(d, kind, x0, y + 3)
            tx = x0 + 42
            d.text((tx, y + 0), num + ". " + place, font=font(13), fill=YELLOW)
            tag_chip(d, x0 + 502 - 56, y + 0, tag)
            d.text((tx, y + 14), head, font=font(14), fill=WHITE)
            d.text((tx, y + 29), summ + "  " + src, font=font(13, bold=False), fill=GREY)
        y += row_h
        d.line([0, y, W, y], fill=LINE, width=1)

    # ---- World map band
    map_h = 42
    d.rectangle([0, y, W, y + map_h], fill=(14, 16, 24))
    # rough continents (lon/lat -> x/y in band)
    def mx(lon, lat):
        return int((lon + 180) / 360 * W)
    def my(lat):
        return int(y + 8 + (85 - lat) / 145 * (map_h - 12))
    continents = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 62),
         (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-120, 34),
         (-125, 49), (-150, 60), (-168, 66)],
        [(-80, 10), (-60, 8), (-50, 0), (-40, -8), (-48, -22), (-58, -34),
         (-70, -40), (-73, -50), (-70, -20), (-80, -5), (-80, 10)],
        [(-10, 36), (-9, 43), (-2, 48), (3, 51), (8, 57), (12, 55), (18, 56),
         (24, 59), (30, 60), (28, 45), (22, 40), (12, 44), (0, 38), (-10, 36)],
        [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (43, 12),
         (51, 11), (48, 0), (40, -12), (35, -25), (28, -33), (19, -35), (15, -27),
         (12, -18), (9, -1), (-8, 4), (-17, 15)],
        [(30, 70), (45, 68), (60, 70), (75, 73), (100, 77), (130, 72), (160, 70),
         (180, 66), (162, 60), (142, 50), (135, 43), (127, 40), (120, 32),
         (108, 20), (100, 8), (92, 16), (80, 8), (75, 20), (60, 25), (50, 30),
         (44, 39), (36, 36), (30, 42), (30, 70)],
        [(114, -22), (122, -14), (130, -12), (137, -15), (142, -11), (146, -19),
         (150, -23), (153, -27), (150, -37), (140, -38), (132, -32), (124, -33),
         (115, -35), (114, -22)],
    ]
    for poly in continents:
        pts = [(mx(lon, lat), my(lat)) for lon, lat in poly]
        d.polygon(pts, fill=(76, 78, 92))
    d.rectangle([8, y + 1, 172, y + 16], fill=(14, 16, 24))
    d.text((10, y + 2), "WHERE IT HAPPENED", font=font(13), fill=YELLOW)
    pins = [(1, -74, 41), (2, 100, 41), (3, 37, 56), (4, -122, 37),
            (5, 43, 17), (6, 147, -42), (7, 10, 20), (8, 56, 26),
            (9, -77, 39), (10, 50, 53), (11, 155, -66), (12, 121, 31),
            (13, -75, 10), (14, 24, 60)]
    for n, lon, lat in pins:
        px, py = mx(lon, lat), my(lat)
        py = max(y + 11, min(py, y + map_h - 11))
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=1)
        t = str(n)
        d.text((px - tw(d, t, font(13)) // 2, py - 7), t, font=font(13), fill=WHITE)
    y += map_h

    # ---- Briefs 15-38, 2 columns, 17px
    briefs = [
        ("WINDSOR", "Two arrested on William and Kate's estate."),
        ("DAKAR", "Senegal restored as 2025 champions on appeal."),
        ("LOS ANGELES", "Thomas Markle faces a second charge."),
        ("MADRID", "Spain votes Sunday; Vox may enter government."),
        ("NEW DELHI", "Food inflation hits vegetables, pulses, oils."),
        ("TAIPEI", "AI disinfo network targets Taiwan candidates."),
        ("SYDNEY", "Ex-officer Lamarre convicted of double murder."),
        ("BAGHDAD", "Iraq to take over Kurdish-controlled oilfields."),
        ("KUALA LUMPUR", "Malaysia returns Rohingya to Myanmar."),
        ("HAVANA", "WHO chief: end US fuel blockade on Cuba."),
        ("GLOBAL", "Landmine casualties hit a five-year high."),
        ("DEEP SPACE", "ESA's Hera reaches asteroid Dimorphos."),
        ("MOSCOW", "Putin and Brunei Sultan sign joint declaration."),
        ("PARIS", "Champions League: PSG–Roma & Arsenal–BVB."),
        ("BRUSSELS", "NATO chief Rutte meets Trump on security."),
        ("CHICAGO", "O'Hare ground stop & radar outage snarls travel."),
        ("MEXICO CITY", "US Embassy alert on Reforma–Zócalo march."),
        ("BRUSSELS", "90+ leaders: cap €210B frozen Russian assets."),
        ("BENGHAZI", "UN cities hit in drone strike on Russian ship."),
        ("LONDON", "Russia demands UK drop NATO nuclear shield."),
        ("GAZA", "Israeli strike kills Hamas security chief Abu Nahel."),
        ("DOHA", "US Embassy warns of Houthi threats."),
        ("ABUJA", "Tinubu's N65.2T budget; $20.5B loan cleared."),
        ("CAIRO", "Sudan & Egypt reject Red Sea militarisation."),
    ]
    d.text((10, y + 1), "THE REST OF THE DAY — 24 MORE STORIES", font=font(14), fill=YELLOW)
    by = y + 16
    for i, (place, text) in enumerate(briefs):
        col = i % 2
        row = i // 2
        bx = 10 + col * 502
        byy = by + row * 18
        d.text((bx, byy), f"{15 + i}. ", font=font(17), fill=RED)
        nx = bx + tw(d, f"{15 + i}. ", font(17))
        d.text((nx, byy), place + " — ", font=font(17), fill=YELLOW)
        nx += tw(d, place + " — ", font(17))
        d.text((nx, byy), text, font=font(17, bold=False), fill=WHITE)
    y = by + 12 * 18 + 2

    # ---- UTC timeline strip
    tl = [("00:18", "Shenzhou liftoff"), ("01:38", "Baffin quake"),
          ("03:56", "Shenzhou docks"), ("04:30", "Balleny quake"),
          ("MORNING", "Huawei verdict"), ("MIDDAY", "Aus pact"),
          ("AFTERNOON", "Hodeidah/Riyadh"), ("EVENING", "Samara hit"),
          ("NIGHT", "Nvidia −5.9%")]
    d.rectangle([0, y, W, y + 40], fill=PANEL)
    d.line([0, y + 8, W, y + 8], fill=LINE, width=1)
    col = W // 9
    for i, (t, lab) in enumerate(tl):
        cx = i * col + 6
        d.ellipse([cx + 2, y + 3, cx + 12, y + 13], fill=YELLOW)
        d.text((cx, y + 14), t, font=font(13), fill=YELLOW)
        d.text((cx, y + 27), lab, font=font(13, bold=False), fill=WHITE)
    y += 40

    # ---- DATE CHECK strip
    d.rectangle([0, y, W, y + 26], fill=(30, 26, 0))
    dc = ("LEFT OUT AS OTHER DAYS' NEWS — Spain's election (29 Nov, not yet) · US Thanksgiving "
          "(26 Nov, not yet) · Huang's Senate hearing (3 Dec, not yet) · Huawei sentencing (Sep 2027, not yet).")
    draw_wrapped(d, 10, y + 1, dc, font(13), W - 20, YELLOW, lh=12)
    y += 26

    # ---- HOW SURE legend + footer
    leg = "HOW SURE:  C = CONFIRMED by 2+ major outlets  ·  O = OFFICIAL data or statement  ·  R = REPORTED by one outlet or attributed  ·  F = FORECAST / preview"
    d.text((10, y + 1), leg, font=font(13), fill=WHITE)
    y += 15
    foot = "Sources: Reuters · AP · BBC · Al Jazeera · Xinhua · The Guardian · SCMP · USGS · UNODC · NATO — Drawn by an AI agent for make.fun — 25 November 2026."
    d.text((10, y + 0), foot, font=font(13, bold=False), fill=GREY)
    y += 13

    print("final y =", y, "canvas H =", H, "overflow =", y - H)
    img.save(os.path.join(BASE, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
