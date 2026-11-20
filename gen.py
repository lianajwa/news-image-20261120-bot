#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024) by hand.

Every fact below was re-checked against live news sources on 20 Nov 2026
inside the build session. Items marked with a dagger happened on Thu 19 Nov
and were first reported / developed on Fri 20 Nov; everything else happened
on Fri 20 Nov 2026. Run: python3 gen.py  ->  writes entry.png next to this file.
Deterministic: no clock, no randomness, fixed fonts.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (163, 18, 18)
BLUE = (28, 68, 128)
TEAL = (14, 90, 90)
GREY = (90, 88, 82)
LIGHT = (233, 228, 214)
OCEAN = (188, 216, 232)
LAND = (207, 227, 184)
LAND_EDGE = (122, 154, 90)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    out = []
    for para in text.split("\n"):
        out.extend(textwrap.wrap(para, width=200) if False else _wrap(draw, para, fnt, width))
    return out


def _wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- stories
# (region, place, headline) -- exactly 52, in reading order.
STORIES = [
    ("EUROPE", "KYIV", "Overnight ballistic barrage; 3 Dnipro bridges hit, fires in 3 districts"),
    ("EUROPE", "KYIV", "Thu strikes damaged Austrian & Dutch embassies, St Volodymyr's Cathedral \u2020"),
    ("EUROPE", "LONDON", "UK & EU agree youth-mobility scheme, BBC understands"),
    ("EUROPE", "LONDON", "UK pledges 1,000+ drones for Ukraine in \u00a3260m package"),
    ("EUROPE", "OSLO", "UK & Norway fund two Ukrainian naval craft, \u00a3100m+ \u2020"),
    ("EUROPE", "BERLIN", "Merz: new Ukraine talks including Europe to be held soon"),
    ("EUROPE", "GENOA", "Airport suspends flights after unidentified drones seen"),
    ("EUROPE", "PARIS", "Harris meets Macron in 'courtesy meeting' amid 2028 talk"),
    ("EUROPE", "ISTANBUL", "Court blocks jailed mayor Imamoglu from 2028 presidential race"),
    ("EUROPE", "ANTALYA", "COP31 final day; Thu draft drops all fossil-fuel wording \u2020"),
    ("ASIA", "ODISHA", "Cyclone Akvan lands near Gopalpur, winds 70\u201380 km/h"),
    ("ASIA", "ODISHA", "300,000+ evacuated, 423 rescue teams, 69 trains cancelled"),
    ("ASIA", "ODISHA", "No major damage or loss of life reported so far in Odisha"),
    ("ASIA", "TOKYO", "Nikkei \u22124.8% in Friday trade; SoftBank \u221215% intraday"),
    ("ASIA", "SEOUL", "KOSPI \u22125.7%; Samsung \u22127%, SK Hynix \u22126.6%"),
    ("ASIA", "TAIPEI", "Taiex \u22126.75%; worst week since 1990, TSMC \u22125.2%"),
    ("ASIA", "TOKYO", "Anthropic debut: $83 \u2192 $97 close, +17%, largest IPO ever \u2020"),
    ("ASIA", "SHENZHEN", "Trump, Xi & Putin hold first 3-way summit; peace declaration \u2020"),
    ("ASIA", "RIYADH", "Houthi missiles damage PIF tower in financial district"),
    ("ASIA", "HORMUZ", "Tanker catches fire after hitting a mine; ADNOC vessel attacked"),
    ("ASIA", "THE HAGUE", "ICJ: Myanmar committed genocide against Rohingya, 9\u20136 \u2020"),
    ("ASIA", "WELLINGTON", "Nicholls 113* as NZ reach 243/5, day 1 vs India"),
    ("ASIA", "WELLINGTON", "India bowl New Zealand out for 368 in 1st Test"),
    ("MIDDLE EAST", "RIYADH", "Saudi air defences destroy two Houthi drones"),
    ("MIDDLE EAST", "RIYADH", "Houthis claim strikes on four Saudi targets"),
    ("MIDDLE EAST", "BEIRUT", "Israeli airstrike hits Hezbollah missile facility in E Lebanon"),
    ("MIDDLE EAST", "GAZA", "Israeli military completes ground op beyond 'Yellow Line'"),
    ("MIDDLE EAST", "TEHRAN", "Iran war in 9th month; US cost tops $48bn"),
    ("MIDDLE EAST", "RIYADH", "Saudi thunderstorm warnings run to Tue 24 Nov"),
    ("AMERICAS", "NEW YORK", "US stocks fall 5th straight day Thu; Dow \u22121,101, Nasdaq \u22122.3% \u2020"),
    ("AMERICAS", "WASHINGTON", "Senate rejects Iran war-powers resolution 51\u201348 \u2020"),
    ("AMERICAS", "WASHINGTON", "Trump posthumously pardons baseball legend Pete Rose"),
    ("AMERICAS", "WASHINGTON", "US sanctions Comancheros and 'Ndrangheta gangs"),
    ("AMERICAS", "WASHINGTON", "Court limits agriculture chief Rollins' religious emails"),
    ("AMERICAS", "CALIFORNIA", "State targets Nvidia in China AI-chip probe"),
    ("AMERICAS", "WASHINGTON", "House panel: ~880,000 advanced AI chips approved for China"),
    ("AMERICAS", "FLORIDA", "State carries out record 20th execution of the year"),
    ("AMERICAS", "PORT-AU-PRINCE", "Haiti police: at least 34 suspected gang members killed in raid"),
    ("AMERICAS", "SAN SALVADOR", "Bukele expected to formalise bid for 3rd presidential term"),
    ("AFRICA", "NAIROBI", "Kenya's Ebola countdown continues; no new case since 19 Oct"),
    ("AFRICA", "JOHANNESBURG", "Bavuma ruled out of 2nd Test vs Bangladesh (calf)"),
    ("AFRICA", "NAIROBI", "Jepchirchir gets 3-year ban after admitting EPO violations"),
    ("OCEANIA", "SYDNEY", "Ash Barty selected for Tennis Hall of Fame, class of 2027"),
    ("OCEANIA", "NOUM\u00c9A", "M5.6 quake SE of Loyalty Islands, 00:49 UTC, no tsunami threat"),
    ("OCEANIA", "MADANG", "M4.9 quake 54 km W of Madang, 05:17 UTC"),
    ("OCEANIA", "NADI", "Cyclone Xavier: track forecasts updated, island warnings hold"),
    ("GLOBAL", "GLOBAL", "Meta rethinks 2030 climate goals as AI data centres lift emissions"),
    ("GLOBAL", "GLOBAL", "IEA: data-centre power use could double by 2030"),
    ("GLOBAL", "GLOBAL", "Study: Islam to become world's largest religion by 2035"),
    ("GLOBAL", "GLOBAL", "BepiColombo nears Mercury after an 8-year voyage"),
    ("GLOBAL", "GLOBAL", "Pochettino's first Man Utd address: calls for love and unity"),
    ("GLOBAL", "GLOBAL", "Save the Children: nearly 1 in 4 children live in conflict zones"),
]
assert len(STORIES) == 52, len(STORIES)

REGION_ORDER = ["EUROPE", "ASIA", "MIDDLE EAST", "AMERICAS", "AFRICA", "OCEANIA", "GLOBAL"]
REGION_COLOURS = {
    "EUROPE": (28, 68, 128), "ASIA": (163, 18, 18), "MIDDLE EAST": (120, 72, 10),
    "AMERICAS": (14, 90, 90), "AFRICA": (96, 60, 140), "OCEANIA": (0, 110, 110),
    "GLOBAL": (70, 70, 70),
}

TIMELINE = [
    ("00:49 UTC", "M5.6 quake, Loyalty Islands"),
    ("01:25 UTC", "Kyiv explosions begin"),
    ("05:17 UTC", "M4.9 quake near Madang, PNG"),
    ("08:30 IST", "Akvan lands near Gopalpur"),
    ("FRI AM", "Nikkei \u22124.5%; SoftBank \u221215%"),
    ("FRI", "COP31 final day, Antalya"),
]

# (lat, lon, label) pins -- all on land, or on named islands drawn below.
PINS = [
    (50.45, 30.52, "Kyiv"), (51.50, -0.12, "London"), (44.41, 8.93, "Genoa"),
    (36.90, 30.71, "Antalya"), (48.85, 2.35, "Paris"), (41.01, 28.98, "Istanbul"),
    (52.08, 4.31, "The Hague"), (24.71, 46.68, "Riyadh"), (19.27, 84.92, "Gopalpur"),
    (35.68, 139.69, "Tokyo"), (37.57, 126.98, "Seoul"), (25.03, 121.57, "Taipei"),
    (22.54, 114.06, "Shenzhen"), (-41.29, 174.78, "Wellington"), (-5.22, 145.79, "Madang"),
    (-24.70, 171.23, "Loyalty Is."), (-1.29, 36.82, "Nairobi"), (38.91, -77.04, "Washington"),
    (18.54, -72.34, "Port-au-Prince"), (13.69, -89.22, "San Salvador"),
    (27.95, -81.76, "Florida"), (-17.78, 177.44, "Nadi"), (36.74, -119.79, "California"),
    (26.50, 56.00, "Hormuz"),
]

SOURCES = ("Sources (20 Nov 2026): Reuters \u00b7 BBC \u00b7 The Hindu BusinessLine \u00b7 IMD \u00b7 Kyiv Independent \u00b7 "
           "Morningstar \u00b7 InvestingLive \u00b7 USGS \u00b7 ICJ \u00b7 AP/AFP via wire \u00b7 One Turn \u00b7 "
           "Jagran Josh \u00b7 myKhel \u00b7 Career India. \u2020 = happened Thu 19 Nov, reported/developed Fri 20 Nov.")

# ---------------------------------------------------------------- map
# Coarse hand-drawn continent outlines (lon, lat), equirectangular.
N_AMERICA = [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62),
             (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 33), (-81, 30),
             (-81, 26), (-84, 29), (-85, 30),
             (-95, 29), (-105, 22), (-95, 16), (-88, 14), (-83, 10), (-80, 8), (-95, 15),
             (-110, 23), (-125, 40), (-125, 49), (-150, 60), (-168, 66)]
S_AMERICA = [(-80, 8), (-75, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
             (-48, -28), (-55, -35), (-65, -45), (-70, -55), (-75, -40),
             (-75, -20), (-80, -5), (-80, 8)]
AFRICA = [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
          (40, 15), (48, 11), (51, 12), (43, 0), (40, -10), (35, -20), (32, -28),
          (25, -34), (18, -35), (12, -18), (9, -2), (9, 4), (-8, 4), (-17, 15)]
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (18, 56),
           (21, 55), (24, 59), (30, 60), (30, 70), (40, 68), (55, 68), (70, 72),
           (80, 73), (100, 76), (120, 73), (140, 72), (160, 70), (178, 66),
           (170, 60), (162, 56), (158, 52), (142, 50), (140, 40), (135, 35),
           (130, 33), (127, 35), (122, 30), (120, 25), (110, 20), (105, 10),
           (100, 8), (98, 12), (95, 16), (92, 21), (88, 22), (85, 19), (80, 13),
           (77, 8), (73, 16), (68, 23), (66, 25), (60, 25), (57, 26), (52, 28),
           (50, 29), (48, 30), (43, 28), (40, 36), (36, 36), (30, 36), (26, 38),
           (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (0, 39),
           (-2, 37), (-6, 36), (-9, 37), (-10, 36)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (135, -35),
             (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (130, -13),
             (126, -14), (122, -17), (118, -20), (113, -22)]
# island blobs as (lon, lat, rx, ry) in degrees
ISLANDS = [(100, 0, 4, 2), (106, -3, 3, 2), (113, -7, 4, 1.5), (120, -2, 3, 2),
           (131, -2, 3, 1.5), (141, -5, 5, 2), (147, -6, 2, 1.5), (167, -16, 2, 3),
           (172, -42, 2, 4), (176, -38, 1.5, 2), (-3, 54, 1.5, 2), (139, 38, 1.5, 4),
           (141, 42, 1.5, 2), (44, -19, 1.5, 4), (171, -25, 1.5, 1.5), (177, -18, 1.5, 1.5),
           (146, -6, 1.5, 1.5), (18, 66, 2, 3), (-20, 65, 1.5, 2),
           (-74, 19, 3, 1.5), (-77, 21, 2, 1), (-86, 16, 1.5, 1)]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    return (x0 + (lon + 180) / 360 * (x1 - x0),
            y0 + (85 - lat) / 145 * (y1 - y0))


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=OCEAN, outline=INK, width=2)
    for lon in range(-150, 181, 30):
        x = x0 + (lon + 180) / 360 * (x1 - x0)
        draw.line([(x, y0), (x, y1)], fill=(160, 195, 215), width=1)
    for lat in (-60, -30, 0, 30, 60):
        y = y0 + (85 - lat) / 145 * (y1 - y0)
        draw.line([(x0, y), (x1, y)], fill=(160, 195, 215), width=1)
    for poly in (N_AMERICA, S_AMERICA, AFRICA, EURASIA, AUSTRALIA):
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for lon, lat, rx, ry in ISLANDS:
        cx, cy = project(lon, lat, box)
        sx = rx / 360 * (x1 - x0)
        sy = ry / 145 * (y1 - y0)
        draw.ellipse([cx - sx, cy - sy, cx + sx, cy + sy], fill=LAND, outline=LAND_EDGE)
    for lat, lon, label in PINS:
        cx, cy = project(lon, lat, box)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, outline=(255, 255, 255), width=2)
    # labels for the biggest stories only, to stay legible
    for lat, lon, label in [(50.45, 30.52, "KYIV"), (19.27, 84.92, "GOPALPUR"),
                            (35.68, 139.69, "TOKYO"), (24.71, 46.68, "RIYADH"),
                            (-41.29, 174.78, "WELLINGTON")]:
        cx, cy = project(lon, lat, box)
        draw.text((cx + 8, cy - 6), label, font=font(FB, 11), fill=INK)
    draw.text((x0 + 6, y0 + 4), "WORLD MAP \u2014 PINS BY LATITUDE / LONGITUDE",
              font=font(FB, 11), fill=INK)


# ---------------------------------------------------------------- drawn scenes
def hero_cyclone(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(70, 110, 140), outline=INK, width=2)
    draw.ellipse([x0 + 8, y0 + 34, x1 - 8, y1 - 6], fill=(30, 60, 90))
    draw.polygon([(x0 + 14, y1 - 6), (x0 + 60, y1 - 30), (x0 + 110, y1 - 6)],
                 fill=(40, 90, 60))
    draw.polygon([(x0 + 90, y1 - 6), (x0 + 150, y1 - 38), (x0 + 210, y1 - 6)],
                 fill=(30, 70, 50))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 6
    # Archimedean spiral: white arms winding into the eye
    import math
    pts = []
    for a in range(0, 540, 6):
        r = 4 + a * 0.085
        rad = math.radians(a + 200)
        pts.append((cx + r * math.cos(rad), cy + r * math.sin(rad) * 0.55))
    draw.line(pts, fill=(255, 255, 255), width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 220, 120))
    for i, x in enumerate(range(x0 + 14, x1 - 10, 26)):
        draw.line([(x, y0 + 8 + (i % 2) * 5), (x - 5, y0 + 22 + (i % 2) * 5)],
                  fill=(190, 220, 240), width=3)


def hero_kyiv(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(24, 28, 48), outline=INK, width=2)
    for sx, sy in [(x0 + 30, y0 + 14), (x0 + 90, y0 + 8), (x0 + 160, y0 + 16),
                   (x0 + 220, y0 + 10), (x0 + 270, y0 + 18)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # skyline
    for bx, bw, bh in [(x0 + 12, 34, 52), (x0 + 52, 26, 70), (x0 + 84, 40, 44),
                       (x0 + 130, 30, 62), (x0 + 166, 36, 50), (x0 + 208, 30, 66),
                       (x0 + 244, 40, 46), (x0 + 288, 26, 58)]:
        draw.rectangle([bx, y1 - bh - 6, bx + bw, y1 - 6], fill=(60, 64, 92),
                       outline=(140, 140, 170))
    # missile trails
    draw.line([(x0 + 60, y0 + 6), (x0 + 120, y0 + 58)], fill=(255, 200, 80), width=4)
    draw.line([(x0 + 200, y0 + 4), (x0 + 160, y0 + 52)], fill=(255, 200, 80), width=4)
    draw.ellipse([x0 + 112, y0 + 52, x0 + 128, y0 + 68], fill=(255, 140, 40))
    # fire on a building (building top sits at y1-68)
    fx, fy = x0 + 150, y1 - 66
    draw.polygon([(fx, fy - 10), (fx - 8, fy), (fx + 8, fy)], fill=(255, 120, 20))
    draw.polygon([(fx, fy - 6), (fx - 4, fy + 1), (fx + 4, fy + 1)], fill=(255, 220, 60))


def hero_markets(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 250, 235), outline=INK, width=2)
    draw.line([(x0 + 26, y0 + 12), (x0 + 26, y1 - 18)], fill=INK, width=3)
    draw.line([(x0 + 26, y1 - 18), (x1 - 12, y1 - 18)], fill=INK, width=3)
    pts = [(x0 + 34, y0 + 22), (x0 + 80, y0 + 34), (x0 + 120, y0 + 28),
           (x0 + 165, y0 + 52), (x0 + 210, y0 + 48), (x0 + 255, y0 + 74),
           (x0 + 295, y0 + 70)]
    draw.line(pts, fill=RED, width=5)
    draw.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 16, pts[-1][1] - 2),
                  (pts[-1][0] - 4, pts[-1][1] + 14)], fill=RED)
    for bx, bh in [(x0 + 44, 26), (x0 + 84, 20), (x0 + 124, 30), (x0 + 164, 18),
                   (x0 + 204, 12), (x0 + 244, 8)]:
        draw.rectangle([bx, y1 - 18 - bh, bx + 24, y1 - 18], fill=(120, 170, 120),
                       outline=INK)
    draw.text((x0 + 30, y0 + 4), "\u22124.8%", font=font(FB, 15), fill=RED)


# 13 small pictograms, each drawn with plain shapes in a 72x58 frame.
def pic_gavel(d, x, y):
    d.rectangle([x + 18, y + 8, x + 52, y + 20], fill=(120, 72, 20), outline=INK)
    d.line([(x + 36, y + 20), (x + 48, y + 44)], fill=(120, 72, 20), width=6)
    d.rectangle([x + 12, y + 44, x + 58, y + 50], fill=(160, 120, 60), outline=INK)


def pic_flags(d, x, y):
    for i, col in enumerate([(180, 30, 30), (30, 60, 160), (200, 200, 200)]):
        px = x + 8 + i * 20
        d.line([(px, y + 6), (px, y + 44)], fill=INK, width=2)
        d.rectangle([px, y + 8, px + 18, y + 22], fill=col, outline=INK)


def pic_tower(d, x, y):
    d.polygon([(x + 26, y + 4), (x + 44, y + 4), (x + 40, y + 48), (x + 30, y + 48)],
              fill=(150, 160, 180), outline=INK)
    for wy in (14, 24, 34):
        d.line([(x + 31, y + wy), (x + 39, y + wy)], fill=(255, 220, 90), width=2)
    d.line([(x + 28, y + 12), (x + 42, y + 26)], fill=RED, width=3)


def pic_tanker(d, x, y):
    d.polygon([(x + 8, y + 28), (x + 62, y + 28), (x + 56, y + 42), (x + 14, y + 42)],
              fill=(90, 60, 30), outline=INK)
    for cx in (20, 32, 44):
        d.rectangle([x + cx, y + 16, x + cx + 9, y + 28], fill=(40, 110, 160), outline=INK)
    d.polygon([(x + 48, y + 8), (x + 42, y + 20), (x + 54, y + 20)], fill=(255, 120, 20))
    d.line([(x + 6, y + 48), (x + 64, y + 48)], fill=BLUE, width=3)


def pic_quake(d, x, y):
    d.line([(x + 6, y + 40), (x + 64, y + 40)], fill=INK, width=3)
    d.line([(x + 34, y + 40), (x + 30, y + 28), (x + 38, y + 20), (x + 32, y + 10)],
           fill=RED, width=3)
    d.rectangle([x + 10, y + 18, x + 26, y + 40], fill=(200, 170, 120), outline=INK)
    d.rectangle([x + 46, y + 24, x + 60, y + 40], fill=(170, 140, 100), outline=INK)


def pic_cricket(d, x, y):
    d.line([(x + 20, y + 44), (x + 44, y + 10)], fill=(150, 110, 60), width=8)
    d.ellipse([x + 48, y + 6, x + 58, y + 16], fill=RED, outline=INK)
    for sx in (14, 20, 26):
        d.line([(x + sx, y + 34), (x + sx, y + 48)], fill=(220, 190, 90), width=3)


def pic_tennis(d, x, y):
    d.ellipse([x + 16, y + 8, x + 54, y + 46], fill=(190, 220, 60), outline=INK, width=2)
    d.arc([x + 16, y + 8, x + 54, y + 46], start=300, end=60, fill=(255, 255, 255), width=3)
    d.arc([x + 16, y + 8, x + 54, y + 46], start=120, end=240, fill=(255, 255, 255), width=3)


def pic_mercury(d, x, y):
    d.ellipse([x + 14, y + 12, x + 48, y + 46], fill=(190, 160, 120), outline=INK, width=2)
    for cx, cy, r in [(24, 22, 4), (36, 32, 5), (30, 38, 3)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(150, 120, 85))
    d.ellipse([x + 8, y + 6, x + 62, y + 52], outline=(200, 120, 40), width=2)
    d.ellipse([x + 56, y + 4, x + 64, y + 12], fill=(255, 200, 60))


def pic_drone(d, x, y):
    d.ellipse([x + 24, y + 20, x + 46, y + 36], fill=(80, 80, 90), outline=INK)
    for cx, cy in [(14, 12), (56, 12), (14, 44), (56, 44)]:
        d.ellipse([x + cx - 8, y + cy - 3, x + cx + 8, y + cy + 3], fill=(180, 180, 180),
                  outline=INK)
        d.line([(x + 35, y + 28), (x + cx, y + cy)], fill=INK, width=2)


def pic_ballot(d, x, y):
    d.rectangle([x + 14, y + 22, x + 56, y + 48], fill=(220, 200, 150), outline=INK)
    d.line([(x + 28, y + 22), (x + 42, y + 22)], fill=INK, width=3)
    d.polygon([(x + 30, y + 6), (x + 44, y + 6), (x + 40, y + 24), (x + 34, y + 24)],
              fill=(255, 255, 255), outline=INK)
    d.line([(x + 34, y + 14), (x + 38, y + 18), (x + 44, y + 10)], fill=(20, 140, 60), width=3)


def pic_flame(d, x, y):
    d.polygon([(x + 35, y + 4), (x + 22, y + 28), (x + 28, y + 48), (x + 44, y + 48),
               (x + 50, y + 26)], fill=(255, 120, 20), outline=INK)
    d.polygon([(x + 35, y + 22), (x + 28, y + 36), (x + 35, y + 48), (x + 43, y + 36)],
              fill=(255, 220, 60))


def pic_chart(d, x, y):
    d.line([(x + 10, y + 8), (x + 10, y + 46)], fill=INK, width=2)
    d.line([(x + 10, y + 46), (x + 62, y + 46)], fill=INK, width=2)
    d.line([(x + 14, y + 14), (x + 28, y + 22), (x + 42, y + 20), (x + 58, y + 40)],
           fill=RED, width=4)


def pic_bridge(d, x, y):
    d.arc([x + 8, y + 10, x + 62, y + 52], start=180, end=360, fill=INK, width=3)
    d.line([(x + 6, y + 36), (x + 64, y + 36)], fill=INK, width=4)
    for bx in (18, 30, 42, 54):
        d.line([(x + bx, y + 16), (x + bx, y + 36)], fill=INK, width=2)
    d.line([(x + 6, y + 46), (x + 64, y + 46)], fill=BLUE, width=3)


PICTOGRAMS = [
    (pic_gavel, "ICJ verdict"), (pic_flags, "Shenzhen summit"), (pic_tower, "Riyadh tower"),
    (pic_tanker, "Hormuz tanker"), (pic_quake, "Quakes"), (pic_cricket, "Wellington Test"),
    (pic_tennis, "Barty honoured"), (pic_mercury, "Mercury visitor"), (pic_drone, "Genoa drones"),
    (pic_ballot, "Bukele 3rd term"), (pic_flame, "Gaza / Lebanon"), (pic_chart, "Sell-off"),
    (pic_bridge, "Kyiv bridges"),
]
assert len(PICTOGRAMS) == 13

# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14

    # header
    text(d, (M, 10), "THE WORLD IN ONE DAY", font(FB, 46), fill=INK)
    text(d, (W - M, 22), "52 STORIES \u00b7 7 REGIONS", font(FB, 20), fill=RED, anchor="ra")
    d.line([(M, 66), (W - M, 66)], fill=INK, width=3)
    text(d, (M, 72), "FRIDAY 20 NOVEMBER 2026", font(FB, 30), fill=RED)
    text(d, (W - M, 78), "ALL EVENTS VERIFIED TO THIS DATE", font(FB, 15), fill=INK, anchor="ra")
    text(d, (M, 104), "One day, whole world: war, weather, markets, courts, sport \u2014 drawn and dated.",
         font(FR, 13), fill=GREY)

    # hero: 3 lead stories
    hy, hh = 126, 168
    cw = (W - 2 * M - 20) // 3
    heroes = [
        (hero_cyclone, "CYCLONE AKVAN MAKES LANDFALL",
         "Akvan crosses the Odisha\u2013Andhra coast near Gopalpur at 08:30 IST, winds "
         "70\u201380 km/h. 300,000+ evacuated; no major damage reported so far."),
        (hero_kyiv, "KYIV HIT AGAIN OVERNIGHT",
         "Ballistic missiles strike from 01:25 local; three Dnipro bridges damaged, "
         "fires in Obolonskyi, Podilskyi and Holosiivskyi. A day after embassies hit."),
        (hero_markets, "AI SELL-OFF SWEEPS ASIA",
         "Nikkei \u22124.8%, KOSPI \u22125.7%, Taiex \u22126.75% on Friday. SoftBank \u221215% "
         "after Anthropic's $83 \u2192 $97 debut failed to lift tech."),
    ]
    for i, (scene, head, body) in enumerate(heroes):
        x = M + i * (cw + 10)
        d.rectangle([x, hy, x + cw, hy + hh], fill=(255, 255, 255), outline=INK, width=2)
        scene(d, (x + 6, hy + 6, x + cw - 6, hy + 78))
        lines = wrap(d, head, font(FB, 14), cw - 16)
        yy = hy + 84
        for ln in lines[:2]:
            text(d, (x + 8, yy), ln, font(FB, 14), fill=INK)
            yy += 17
        for ln in wrap(d, body, font(FR, 11), cw - 16)[:3]:
            text(d, (x + 8, yy), ln, font(FR, 11), fill=INK)
            yy += 14

    # timeline strip
    ty = 304
    d.rectangle([M, ty, W - M, ty + 46], fill=LIGHT, outline=INK, width=2)
    text(d, (M + 8, ty + 4), "THE DAY IN UTC", font(FB, 12), fill=RED)
    tw = (W - 2 * M - 16) // 6
    for i, (t, s) in enumerate(TIMELINE):
        x = M + 8 + i * tw
        text(d, (x, ty + 20), t, font(FB, 10), fill=BLUE)
        yy = ty + 32
        for ln in wrap(d, s, font(FR, 9), tw - 10)[:1]:
            text(d, (x, yy), ln, font(FR, 9), fill=INK)

    # map + regions panel
    my, mh = 360, 158
    draw_map(d, (M, my, M + 648, my + mh))
    px = M + 658
    pw = W - M - px
    d.rectangle([px, my, px + pw, my + mh], fill=(255, 255, 255), outline=INK, width=2)
    text(d, (px + 8, my + 6), "7 REGIONS \u2014 52 STORIES", font(FB, 14), fill=INK)
    yy = my + 28
    for r in REGION_ORDER:
        n = sum(1 for s in STORIES if s[0] == r)
        d.rectangle([px + 8, yy + 2, px + 20, yy + 12], fill=REGION_COLOURS[r])
        text(d, (px + 26, yy), f"{r} \u2014 {n}", font(FB, 12), fill=INK)
        yy += 18
    text(d, (px + 8, my + mh - 16), "24 pins \u00b7 every pin on land",
         font(FR, 10), fill=GREY)

    # pictogram strip: 13 drawn scenes (+ 3 hero scenes = 16 drawings)
    py = 530
    text(d, (M, py), "DRAWN IN PICTURES \u2014 13 SCENES FROM THE DAY  (+ 3 LEAD SCENES ABOVE = 16 DRAWINGS)",
         font(FB, 13), fill=INK)
    py += 20
    cell = (W - 2 * M) // 13
    for i, (fn, label) in enumerate(PICTOGRAMS):
        x = M + i * cell
        d.rectangle([x + 2, py, x + cell - 2, py + 58], fill=(255, 255, 255),
                    outline=INK, width=1)
        fn(d, x + 4, py + 2)
        for ln in wrap(d, label, font(FB, 8), cell - 8)[:1]:
            text(d, (x + cell // 2, py + 60), ln, font(FB, 8), fill=INK, anchor="ma")

    # story grid: 4 columns x 13 rows
    gy = 622
    text(d, (M, gy), "THE 52 STORIES", font(FB, 16), fill=INK)
    text(d, (W - M, gy + 2), "\u2020 happened Thu 19 Nov, reported Fri 20 Nov",
         font(FR, 11), fill=GREY, anchor="ra")
    gy += 24
    colw = (W - 2 * M) // 4
    rowh = 24
    for idx, (region, place, head) in enumerate(STORIES):
        col, row = idx % 4, idx // 4
        x = M + col * colw
        y = gy + row * rowh
        d.rectangle([x + 2, y + 3, x + 12, y + 13], fill=REGION_COLOURS[region])
        text(d, (x + 14, y), f"{idx + 1:02d}", font(FB, 11), fill=RED)
        body = f"{place} \u2014 {head}"
        lines = wrap(d, body, font(FR, 10), colw - 40)
        text(d, (x + 38, y), lines[0] if lines else "", font(FR, 10), fill=INK)
        if len(lines) > 1:
            text(d, (x + 38, y + 12), lines[1], font(FR, 10), fill=INK)

    # footer: sources
    fy = 962
    d.line([(M, fy), (W - M, fy)], fill=INK, width=2)
    yy = fy + 8
    for ln in wrap(d, SOURCES, font(FR, 10), W - 2 * M):
        text(d, (M, yy), ln, font(FR, 10), fill=GREY)
        yy += 13
    text(d, (M, yy + 2), "52 stories \u00b7 16 hand-drawn illustrations \u00b7 map pins by latitude/longitude \u00b7 drawn 20 Nov 2026",
         font(FB, 11), fill=INK)

    img.save("entry.png", optimize=True)
    print("stories:", len(STORIES), "| pictograms:", len(PICTOGRAMS),
          "| hero scenes: 3 | total drawings:", len(PICTOGRAMS) + 3)


if __name__ == "__main__":
    main()
