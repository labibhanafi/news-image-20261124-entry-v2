#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE DAILY ORBIT - Tuesday, 24 November 2026 in one image.
make.fun competition: news-image-20261124 (entry v2)

Dense 3-column newspaper front page, 1024x1024 PNG, 47 stories,
8 regions, every event happened or was first reported on
Tuesday 24 November 2026 and verified by live web research at
build time (see SOURCES.md). All facts are hard-coded below:
the program uses NO network at run time.
Deterministic: fixed seeds only, no clocks, no randomness from
the environment - two runs write byte-identical files.
Uses PIL when available; falls back to a stdlib-only renderer.
Output: $MAKEFUN_OUTPUT_DIR/entry.png  (default ./output)
"""
import os

W, H = 1024, 1024

# ---------------------------------------------------------------- data
DATE_LINE = "TUESDAY, 24 NOVEMBER 2026"
PAPER = "THE DAILY ORBIT"
TAGLINE = "All the world's news of one day - Tuesday, 24 November 2026 - on one page"
PRICE_LINE = "Vol. I  -  No. 24  -  47 stories  -  8 regions  -  Free"

LEAD_KICKER = "STRAIT OF HORMUZ  -  IRAN WAR"
LEAD_HEAD = "4TH TANKER HITS MINE IN HORMUZ"
LEAD_SUB = ("Iran's navy and the IRGC say a fourth oil tanker struck a naval mine "
            "and caught fire east of the strait on Tuesday, after two tankers burned "
            "in a restricted zone sailing with ID systems off. Hormuz oil traffic is "
            "reported down 40%, yet Brent held near three-month lows.")
LEAD_FACTS = ["4 tankers ablaze", "traffic -40%", "Brent $87.51", "escort claim disputed"]

CHIPS = [
    ("S&P 500", "7,168", "-0.95%"),
    ("NIKKEI", "58,644", "+3.91%"),
    ("BRENT", "$87.51", "+0.96%"),
    ("NAT GAS", "$3.73", "+5.90%"),
    ("GOLD", "3,629", "-2.28%"),
    ("FTSE 100", "10,467", "-0.13%"),
]
BARS = [("GAS", 5.90), ("NIKKEI", 3.91), ("BRENT", 0.96), ("S&P", -0.95),
        ("STOXX", -1.16), ("GOLD", -2.28), ("COPPER", -5.07)]

# (section, [(headline, one-line detail), ...]) per column; 15/15/16 stories
COLUMN1 = [
    ("MIDDLE EAST", [
        ("HOUTHI STRIKE HITS RIYADH'S TALLEST TOWER", "PIF Tower hit in the KAFD; 11 wounded, 2nd in 5 days."),
        ("ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF", "Naeem Abu Nahel killed in Gaza City; 7 dead Tuesday."),
        ("HOUTHI FIGHTERS NOW 60 KM FROM ADEN", "Advance threatens the government's southern base."),
        ("IRAQ ORDERS TAKEOVER OF KURDISH OILFIELDS", "Ministry fields in 4 provinces put under Baghdad."),
        ("QATAR URGES US AND IRAN TO SHOW RESTRAINT", "Doha keeps contact with both sides, urges dialogue."),
        ("IRAN'S RIAL PLUNGES AFTER US SANCTIONS", "Dollar hit 2.82m rials, up about 5% in one day."),
        ("STRIKES ON YEMEN BUSES KILL ABOUT 25", "Buses and trucks hit in Lahj; both sides blame each."),
    ]),
    ("EUROPE", [
        ("RUSSIA WARNS ESTONIA OF OPEN WAR", "Moscow protests border crossings closing Dec. 1."),
        ("NATO CHIEF VOWS SPACE DEFENCE", "Rutte answers reports of a nuclear-armed satellite."),
        ("GERMANY FIRST TO GET UKRAINE'S DELTA SYSTEM", "Berlin wins access to Kyiv's battlefield software."),
        ("EU PROPOSES 22ND RUSSIA SANCTIONS PACKAGE", "Brussels would bar Russian athletes at EU events."),
        ("COP31 ENDS WITHOUT A DEAL IN ANTALYA", "Longest climate talks fail, 1st time since 2009."),
    ]),
    ("AFRICA", [
        ("SENEGAL RESTORED AS AFRICA CUP CHAMPION", "Top court reverses call giving 2025 title to Morocco."),
        ("FIGHTING TRAPS EBOLA TEAMS IN ITURI", "WHO staff shelter in a hospital in eastern DR Congo."),
        ("DRONE STRIKES HIT UN BUILDING IN KHARTOUM", "UN condemns hits; 19.5m Sudanese face famine risk."),
    ]),
]
COLUMN2 = [
    ("EUROPE (CONT.)", [
        ("UK SANCTIONS 5 MYANMAR GENERALS", "London acts after the ICJ's Rohingya genocide ruling."),
        ("SPAIN'S TOP COURT AMNESTIES PUIGDEMONT", "Cases over Catalonia's 2017 declaration are closed."),
        ("BELGIUM STRIKE HALTS FLIGHTS IN BRUSSELS", "Thousands march against austerity; flights cancelled."),
    ]),
    ("EAST ASIA", [
        ("RUSSIAN JETS ENTER KOREA DEFENCE ZONE", "Seoul scrambled jets; Ulleungdo told to shelter."),
        ("CHINA PROBES POLITBURO MEMBER CHEN JINING", "Shanghai chief is 4th Politburo member probed."),
        ("JAPAN TO PAY ICC IN FULL, A YEAR EARLY", "Tokyo speeds 2027 dues before US sanctions bite."),
        ("SEOUL OFFERS $375,000 FOR AI EXAM CHEATS", "Up to $75,000 per tip guards the entrance test."),
        ("CHINA STARTS 6G PILOTS IN 8 REGIONS", "Next-gen mobile trials launched from Shanghai."),
        ("PAKISTANI ASTRONAUT JOINS SHENZHOU-24", "First foreigner to fly to China's Tiangong station."),
    ]),
    ("SOUTH ASIA & PACIFIC", [
        ("HASINA SAYS SHE RETURNS ON DEC. 16", "Dhaka minister: she will come back in handcuffs."),
        ("NEPAL'S NEW PM MAKES FIRST TRIP TO INDIA", "Shah seeks deeper ties; Delhi pledges 1.4bn euros."),
        ("AUSTRALIA: SUE BIG TECH, FINES TO 5%", "New deal lets people sue platforms over harm."),
    ]),
    ("AFRICA (CONT.)", [
        ("ZAMBIA INDICTS OPPOSITION LEADER", "Main opposition chief, 12 others charged: treason."),
        ("NIGERIA CAMPAIGN TRUCK CRASH KILLS 15", "Zamfara crash hospitalises 25 rally supporters."),
        ("AMNESTY: PROBE TIGRAY SHELLING", "Ethiopian artillery killed dozens in Alamata."),
    ]),
]
COLUMN3 = [
    ("NORTH AMERICA", [
        ("DEMOCRATS WIN HOUSE BY DECADES' MARGIN", "Counting ends: at least 258 House seats won."),
        ("NVIDIA REINSTATES HUANG AS CEO", "Shares +31% Monday; firm value up about $1tn."),
        ("TRUMP ORDERS FASTER DEATH SENTENCES", "DOJ told to expedite federal executions."),
        ("NY FED'S WILLIAMS SIGNALS HIGHER RATES", "S&P 500 fell 0.95% as a Dec. hike is expected."),
        ("ARMY CLEARED TO DETONATE IOWA EXPLOSIVES", "Court rejects a stay; blast set for Wednesday."),
        ("3 HUMAN BIRD FLU CASES IN WASHINGTON", "WHO notified: three cases, including one death."),
        ("FBI PROBES POLICE DATABASE BREACH", "NCIC system holds more than 18m active records."),
        ("HEGSETH'S EX-CHIEF OF STAFF: 'RESIGN'", "Kaspar accuses Pentagon chief of mismanagement."),
    ]),
    ("LATIN AMERICA", [
        ("CAR BOMB INJURES 25 IN COLOMBIA", "Blast at Meta governor's office; ex-FARC blamed."),
        ("BRAZIL CUTS 2027 GROWTH FORECAST", "Growth trimmed to 1.8%; inflation up to 4.5%."),
        ("MEXICO TO TRY 'CHAPO ISIDRO' AT HOME", "Cartel leader tried at home despite US request."),
        ("EL SALVADOR TROOPS PUSH HAITI GANGS", "Force dismantles gang strongholds in Artibonite."),
    ]),
    ("SCIENCE & SPORT", [
        ("BEPICOLOMBO REACHES MERCURY ORBIT", "ESA-JAXA craft arrives after eight-year journey."),
        ("CUBS SIGN SATO IN $120M DEAL", "Six years for Japan's Central League MVP."),
        ("ENGLAND LEVEL T20 SERIES IN AUSTRALIA", "Salt-Donald 150 in 10 overs; win by 8 wickets."),
        ("TEEN SOORYAVANSHI BLASTS 204 OFF 53", "The 15-year-old hits 28 sixes, a senior record."),
    ]),
]
COLUMNS = [COLUMN1, COLUMN2, COLUMN3]

FOOTER = ("Sources: Reuters, AP, BBC, Al Jazeera, UN News, France 24 + 20 more outlets, all reporting "
          "24 Nov 2026 - the full source list is in SOURCES.md in this repository")


# ------------------------------------------------------------------ LCG
class LCG:
    def __init__(self, seed):
        self.s = seed & 0x7FFFFFFF

    def next(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s


# ------------------------------------------------------------------ PIL
def render_pil():
    from PIL import Image, ImageDraw, ImageFont
    import glob

    def find_font(names, size):
        for base in ("/usr/share/fonts", "/usr/local/share/fonts", "/System/Library/Fonts"):
            for n in names:
                hits = sorted(glob.glob(base + "/**/" + n, recursive=True))
                if hits:
                    try:
                        return ImageFont.truetype(hits[0], size)
                    except Exception:
                        pass
        return ImageFont.load_default()

    SERIF_B = lambda s: find_font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"], s)
    SERIF = lambda s: find_font(["DejaVuSerif.ttf", "LiberationSerif.ttf"], s)
    SANS_B = lambda s: find_font(["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"], s)
    SANS = lambda s: find_font(["LiberationSans-Regular.ttf", "DejaVuSans.ttf"], s)

    BG = (246, 241, 228)
    INK = (18, 18, 20)
    ACCENT = (146, 22, 22)
    RULE = (60, 56, 48)
    MUTED = (92, 86, 74)
    BODY = (52, 50, 46)
    CREAM = (255, 250, 238)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    px = img.load()
    # deterministic full-frame paper grain (fixed seed; sets file size)
    rng = LCG(20261124)
    # grain tiles: 4 wide x 2 tall, 9 shades - visible paper feel, bounded size
    for y in range(0, H, 2):
        for x in range(0, W, 4):
            v = rng.next() % 9
            for dy in (0, 1):
                for dx in (0, 1, 2, 3):
                    px[x + dx, y + dy] = (BG[0] - v, BG[1] - v, BG[2] - v)

    M = 26

    def wrap(text, font, maxw):
        words, lines, cur = text.split(), [], ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=font) <= maxw:
                cur = t
            else:
                lines.append(cur)
                cur = w_
        if cur:
            lines.append(cur)
        return lines

    def fit1(text, base, maxw, floor=9):
        fs = base
        while fs > floor and d.textlength(text, font=SANS_B(fs)) > maxw:
            fs -= 1
        return SANS_B(fs)

    # ---- masthead
    d.text((W // 2, 6), DATE_LINE, font=SERIF_B(34), fill=ACCENT, anchor="ma")
    d.line([(M, 46), (W - M, 46)], fill=INK, width=3)
    d.text((W // 2, 52), PAPER, font=SERIF_B(56), fill=INK, anchor="ma")
    d.text((W // 2, 114), TAGLINE, font=SERIF(16), fill=RULE, anchor="ma")
    d.line([(M, 136), (W - M, 136)], fill=INK, width=2)
    d.text((W // 2, 140), PRICE_LINE, font=SANS_B(13), fill=MUTED, anchor="ma")
    d.line([(M, 160), (W - M, 160)], fill=INK, width=3)

    # ---- lead band
    LY = 168
    LB = LY + 158
    d.rectangle([M, LY, W - M, LB], outline=INK, width=2)
    d.rectangle([M, LY, W - M, LY + 24], fill=ACCENT)
    d.text((M + 10, LY + 4), LEAD_KICKER, font=SANS_B(16), fill=CREAM)
    d.text((M + 10, LY + 30), LEAD_HEAD, font=SERIF_B(38), fill=INK)
    # scene panel (right)
    sx0, sy0, sx1, sy1 = W - M - 196, LY + 78, W - M - 10, LY + 148
    d.rectangle([sx0, sy0, sx1, sy1], fill=(38, 62, 86))
    rng2 = LCG(777)
    for _ in range(5200):
        x = sx0 + rng2.next() % (sx1 - sx0)
        y = sy0 + rng2.next() % (sy1 - sy0)
        v = rng2.next() % 44
        px[x, y] = (38 + v, 62 + v, 86 + v)
    d.rectangle([sx0 + 20, sy1 - 26, sx1 - 26, sy1 - 19], fill=(10, 10, 12))
    d.rectangle([sx0 + 36, sy1 - 35, sx0 + 56, sy1 - 26], fill=(10, 10, 12))
    d.rectangle([sx0 + 108, sy1 - 33, sx0 + 122, sy1 - 26], fill=(10, 10, 12))
    for fx in (50, 116):
        d.ellipse([sx0 + fx, sy1 - 50, sx0 + fx + 11, sy1 - 33], fill=(232, 116, 28))
        d.ellipse([sx0 + fx + 3, sy1 - 44, sx0 + fx + 8, sy1 - 35], fill=(250, 196, 60))
    d.text((sx0 + 6, sy0 + 3), "HORMUZ", font=SANS_B(12), fill=(230, 236, 240))
    sub_font = SERIF(15)
    for i, ln in enumerate(wrap(LEAD_SUB, sub_font, 690)):
        d.text((M + 10, LY + 76 + i * 19), ln, font=sub_font, fill=INK)
    fy = LB - 28
    fx = M + 10
    for fact in LEAD_FACTS:
        tw = d.textlength(fact, font=SANS_B(13)) + 16
        d.rectangle([fx, fy, fx + tw, fy + 22], fill=INK)
        d.text((fx + 8, fy + 4), fact, font=SANS_B(13), fill=CREAM)
        fx += tw + 8

    # ---- chips + bars strip
    CY = LB + 8
    d.line([(M, CY), (W - M, CY)], fill=RULE, width=1)
    cx = M
    for label, val, mv in CHIPS:
        col = (22, 110, 40) if mv.startswith("+") else ACCENT
        d.text((cx, CY + 3), label, font=SANS_B(11), fill=MUTED)
        d.text((cx, CY + 17), val, font=SANS_B(14), fill=INK)
        d.text((cx + d.textlength(val, font=SANS_B(14)) + 5, CY + 17), mv, font=SANS_B(14), fill=col)
        cx += 162
    BY = CY + 40
    d.text((M, BY), "DAY MOVES %:", font=SANS_B(11), fill=MUTED)
    bx = M + 92
    for nm, v in BARS:
        col = (22, 110, 40) if v >= 0 else ACCENT
        d.text((bx, BY), nm, font=SANS_B(11), fill=INK)
        nw = d.textlength(nm, font=SANS_B(11))
        ln = int(abs(v) * 5)
        d.rectangle([bx + nw + 4, BY + 2, bx + nw + 4 + ln, BY + 9], fill=col)
        bx += nw + ln + 26
    d.line([(M, BY + 16), (W - M, BY + 16)], fill=RULE, width=1)

    # ---- columns
    TOP = BY + 22
    BOT = H - 30
    colw = (W - 2 * M - 2 * 14) // 3
    body_font = SANS(11)

    def draw_column(x, sections):
        y = TOP
        for sec, stories in sections:
            d.rectangle([x, y, x + colw, y + 19], fill=INK)
            d.text((x + 6, y + 3), sec, font=SANS_B(13), fill=CREAM)
            y += 23
            for head, body in stories:
                d.text((x, y), head, font=fit1(head, 12, colw - 2), fill=INK)
                y += 15
                ln = body
                while ln and d.textlength(ln, font=body_font) > colw - 2:
                    ln = ln[:-1]
                d.text((x, y), ln, font=body_font, fill=BODY)
                y += 14
                d.line([(x, y), (x + colw, y)], fill=(198, 190, 170), width=1)
                y += 4
            y += 3
        return y

    for i, sections in enumerate(COLUMNS):
        x = M + i * (colw + 14)
        if i:
            d.line([(x - 7, TOP), (x - 7, BOT)], fill=RULE, width=1)
        draw_column(x, sections)

    d.line([(M, BOT + 3), (W - M, BOT + 3)], fill=INK, width=2)
    d.text((W // 2, BOT + 7), FOOTER, font=fit1(FOOTER, 10, W - 2 * M, floor=8),
           fill=MUTED, anchor="ma")
    return img


# ------------------------------------------------------- stdlib fallback
FONT57 = {
    "A": (14, 17, 17, 31, 17, 17, 17), "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14), "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31), "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 15), "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14), "J": (7, 2, 2, 2, 2, 18, 12),
    "K": (17, 18, 20, 24, 20, 18, 17), "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17), "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14), "P": (30, 17, 17, 30, 16, 16, 16),
    "Q": (14, 17, 17, 17, 21, 18, 13), "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (15, 16, 16, 14, 1, 1, 30), "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14), "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 27, 17), "X": (17, 10, 4, 4, 4, 10, 17),
    "Y": (17, 10, 4, 4, 4, 4, 4), "Z": (31, 1, 2, 4, 8, 16, 31),
    "0": (14, 17, 19, 21, 25, 17, 14), "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 2, 4, 8, 31), "3": (31, 2, 4, 2, 1, 17, 14),
    "4": (2, 6, 10, 18, 31, 2, 2), "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (6, 8, 16, 30, 17, 17, 14), "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14), "9": (14, 17, 17, 15, 1, 2, 12),
    " ": (0, 0, 0, 0, 0, 0, 0), ".": (0, 0, 0, 0, 0, 12, 12),
    ",": (0, 0, 0, 0, 12, 4, 8), "-": (0, 0, 0, 31, 0, 0, 0),
    "'": (4, 4, 8, 0, 0, 0, 0), ":": (0, 12, 12, 0, 12, 12, 0),
    "%": (24, 25, 2, 4, 8, 19, 3), "$": (4, 15, 20, 14, 5, 30, 4),
    "+": (0, 4, 4, 31, 4, 4, 0), "/": (1, 1, 2, 4, 8, 16, 16),
    "(": (2, 4, 8, 8, 8, 4, 2), ")": (8, 4, 2, 2, 2, 4, 8),
    "&": (12, 18, 20, 8, 21, 18, 13), "?": (14, 17, 1, 2, 4, 0, 4),
    "!": (4, 4, 4, 4, 4, 0, 4),
}


def render_stdlib():
    """Same page, drawn with the standard library alone (bitmap font)."""
    buf = bytearray(bytes((246, 241, 228)) * (W * H))
    rng = LCG(20261124)
    for y in range(0, H, 2):
        for x in range(0, W, 4):
            v = rng.next() % 9
            for dy in (0, 1):
                for dx in (0, 1, 2, 3):
                    i = ((y + dy) * W + (x + dx)) * 3
                    buf[i] = max(0, buf[i] - v)
                    buf[i + 1] = max(0, buf[i + 1] - v)
                    buf[i + 2] = max(0, buf[i + 2] - v)

    def rect(x0, y0, x1, y1, col):
        for yy in range(max(0, y0), min(H, y1)):
            base = yy * W * 3
            for xx in range(max(0, x0), min(W, x1)):
                i = base + xx * 3
                buf[i], buf[i + 1], buf[i + 2] = col

    def text(x, y, s, scale, col):
        cx = x
        for ch in s.upper():
            g = FONT57.get(ch, FONT57[" "])
            for r in range(7):
                bits = g[r]
                for c in range(5):
                    if bits & (16 >> c):
                        rect(cx + c * scale, y + r * scale,
                             cx + c * scale + scale, y + r * scale + scale, col)
            cx += 6 * scale
        return cx

    def text_c(y, s, scale, col):
        text((W - len(s) * 6 * scale) // 2, y, s, scale, col)

    INK = (18, 18, 20)
    ACC = (146, 22, 22)
    text_c(12, DATE_LINE, 4, ACC)
    rect(26, 52, W - 26, 55, INK)
    text_c(60, PAPER, 7, INK)
    text_c(116, "ONE DAY - ONE PAGE - THE WHOLE WORLD", 2, INK)
    rect(26, 140, W - 26, 143, INK)
    rect(26, 152, W - 26, 300, INK)
    rect(28, 154, W - 28, 298, (250, 246, 234))
    text(40, 164, LEAD_KICKER, 2, ACC)
    text(40, 188, "4TH TANKER HITS MINE", 4, INK)
    text(40, 224, "IN HORMUZ", 4, INK)
    text(40, 262, "IRAN SAYS 4 TANKERS ABLAZE - TRAFFIC -40%", 2, INK)
    colw = (W - 52 - 28) // 3
    for ci, sections in enumerate(COLUMNS):
        x = 26 + ci * (colw + 14)
        y = 318
        for sec, stories in sections:
            rect(x, y, x + colw, y + 16, INK)
            text(x + 4, y + 2, sec, 2, (255, 250, 238))
            y += 22
            for head, _body in stories:
                words, lines, cur = head.split(), [], ""
                for w_ in words:
                    t = (cur + " " + w_).strip()
                    if len(t) <= 26:
                        cur = t
                    else:
                        lines.append(cur)
                        cur = w_
                if cur:
                    lines.append(cur)
                for ln in lines[:2]:
                    text(x, y, ln, 2, INK)
                    y += 15
                y += 7
            y += 6
    text_c(H - 26, "THE DAILY ORBIT - TUESDAY, 24 NOVEMBER 2026", 2, INK)
    return buf


def write_png_stdlib(buf, path):
    import zlib
    import struct

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        raw += buf[y * stride:(y + 1) * stride]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    try:
        img = render_pil()
        img.save(path, format="PNG", optimize=True)
    except ImportError:
        write_png_stdlib(render_stdlib(), path)
    print("wrote", path)


if __name__ == "__main__":
    main()
