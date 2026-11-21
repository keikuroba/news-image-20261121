#!/usr/bin/env python3
"""Render the front page for Saturday 21 November 2026.

Build-time helper only: the submitted program (main.py) ships the PNG
this script produces and never runs this file. Nothing here touches
the clock, the network or any random source, so the picture is the
same every time it is drawn. Pillow is the only dependency.
"""
import math

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
EDGE = 36
TEXT_W = PAGE_W - 2 * EDGE

COLOURS = {
    "paper": (247, 243, 234),
    "ink": (18, 18, 18),
    "grey": (90, 86, 76),
    "red": (178, 34, 34),
    "navy": (16, 32, 64),
    "blue": (28, 68, 128),
    "gold": (176, 128, 28),
    "pale": (150, 144, 128),
    "sky": (214, 228, 240),
    "cream": (226, 220, 205),
    "flame": (232, 120, 40),
}

FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(canvas, text, fnt, width):
    """Split text into lines that fit width."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if canvas.textlength(trial, font=fnt) <= width:
            current = trial
        elif current:
            out.append(current)
            current = word
        else:
            current = word
    if current:
        out.append(current)
    return out


def para(canvas, x, y, text, fnt, width, colour=None, gap=4):
    """Draw wrapped text; return the y below it."""
    colour = colour if colour is not None else COLOURS["ink"]
    for line in wrap_text(canvas, text, fnt, width):
        canvas.text((x, y), line, font=fnt, fill=colour)
        y += fnt.size + gap
    return y


def hrule(canvas, y, weight=2):
    canvas.line([(EDGE, y), (PAGE_W - EDGE, y)],
                fill=COLOURS["ink"], width=weight)


def double_hrule(canvas, y):
    hrule(canvas, y, 3)
    hrule(canvas, y + 6, 1)
    return y + 12


def flame_burst(canvas, cx, cy, r):
    for dx, dy, rr in [(0, 0, r), (-r, r // 2, r // 2),
                       (r // 2, -r // 2, r // 2)]:
        canvas.ellipse([cx + dx - rr, cy + dy - rr,
                        cx + dx + rr, cy + dy + rr],
                       fill=COLOURS["flame"])


def frame(canvas, x, y, w, h, fill):
    canvas.rectangle([x, y, x + w, y + h], fill=fill)
    canvas.rectangle([x, y, x + w, y + h], outline=COLOURS["ink"], width=2)


def pic_poland(canvas, x, y, w, h):
    """Poland with two impact bursts and an incoming arc."""
    frame(canvas, x, y, w, h, COLOURS["sky"])
    canvas.text((x + 10, y + 8), "POLAND",
                font=load_font(FONT_SANS_B, 14), fill=COLOURS["grey"])
    outline = [(x + 34, y + 36), (x + 92, y + 28), (x + 150, y + 32),
               (x + 205, y + 44), (x + 248, y + 38), (x + 270, y + 64),
               (x + 260, y + 96), (x + 238, y + 118), (x + 198, y + 128),
               (x + 148, y + 132), (x + 100, y + 126), (x + 56, y + 112),
               (x + 30, y + 84), (x + 22, y + 58)]
    canvas.polygon(outline, fill=(236, 230, 210), outline=COLOURS["ink"])
    canvas.arc([x + 196, y + 10, x + 292, y + 62], start=195, end=335,
               fill=COLOURS["red"], width=3)
    flame_burst(canvas, x + 238, y + 74, 13)
    flame_burst(canvas, x + 130, y + 92, 10)
    canvas.text((x + 10, y + h - 22), "2 MISSILES + DRONE DOWN",
                font=load_font(FONT_SANS_B, 12), fill=COLOURS["red"])


def pic_chart(canvas, x, y, w, h):
    """A market line falling steeply."""
    frame(canvas, x, y, w, h, (255, 255, 255))
    canvas.text((x + 8, y + 6), "S&P 500  -3.7%",
                font=load_font(FONT_SANS_B, 15), fill=COLOURS["red"])
    pts = [(x + 8 + i * (w - 16) / 6,
            y + 30 + (i * i) * (h - 48) / 36) for i in range(7)]
    canvas.line(pts, fill=COLOURS["red"], width=4, joint="curve")
    canvas.ellipse([pts[-1][0] - 5, pts[-1][1] - 5,
                    pts[-1][0] + 5, pts[-1][1] + 5],
                   fill=COLOURS["red"])


def pic_scales(canvas, x, y, w, h):
    """The scales of justice for the Hague ruling."""
    frame(canvas, x, y, w, h, COLOURS["cream"])
    canvas.text((x + 8, y + 6), "ICJ",
                font=load_font(FONT_SANS_B, 13), fill=COLOURS["grey"])
    cx, cy = x + w // 2, y + 22
    canvas.line([(cx, cy), (cx, y + h - 14)], fill=COLOURS["ink"], width=3)
    canvas.line([(cx - 42, cy + 6), (cx + 42, cy + 6)],
                fill=COLOURS["ink"], width=3)
    for side in (-1, 1):
        px = cx + side * 42
        canvas.line([(px, cy + 6), (px, cy + 30)],
                    fill=COLOURS["ink"], width=2)
        canvas.arc([px - 16, cy + 26, px + 16, cy + 52], start=0, end=180,
                   fill=COLOURS["navy"], width=3)
        canvas.line([(px - 16, cy + 39), (px + 16, cy + 39)],
                    fill=COLOURS["navy"], width=3)
    canvas.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=COLOURS["gold"])


def pic_flags(canvas, x, y, w, h):
    """Union Jack next to the EU ring of stars."""
    frame(canvas, x, y, w, h, (255, 255, 255))
    ux, uy, uw, uh = x + 8, y + 14, 56, 56
    canvas.rectangle([ux, uy, ux + uw, uy + uh], fill=(0, 36, 125))
    for ends in [((ux, uy), (ux + uw, uy + uh)),
                 ((ux + uw, uy), (ux, uy + uh))]:
        canvas.line(ends, fill=(255, 255, 255), width=9)
        canvas.line(ends, fill=(200, 16, 46), width=3)
    canvas.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)],
                fill=(255, 255, 255), width=11)
    canvas.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)],
                fill=(255, 255, 255), width=11)
    canvas.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)],
                fill=(200, 16, 46), width=5)
    canvas.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)],
                fill=(200, 16, 46), width=5)
    ex, ey, ew, eh = x + w - 64, y + 14, 56, 56
    canvas.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    for k in range(12):
        angle = math.pi * 2 * k / 12 - math.pi / 2
        sx = ex + ew // 2 + int(19 * math.cos(angle))
        sy = ey + eh // 2 + int(19 * math.sin(angle))
        canvas.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                       fill=COLOURS["gold"])


def pic_quake(canvas, x, y, w, h):
    """A seismograph trace with one big spike."""
    frame(canvas, x, y, w, h, (255, 255, 255))
    canvas.text((x + 8, y + 6), "M 6.8 · JUNIN",
                font=load_font(FONT_SANS_B, 13), fill=COLOURS["red"])
    mid = y + h // 2 + 6
    spikes = [0, 2, -3, 5, -22, 26, -14, 8, -4, 2, 0]
    pts = [(x + 6 + i * (w - 12) / 11, mid + s)
           for i, s in enumerate(spikes)]
    canvas.line(pts, fill=COLOURS["ink"], width=2, joint="curve")
    canvas.ellipse([pts[5][0] - 4, pts[5][1] - 4,
                    pts[5][0] + 4, pts[5][1] + 4], fill=COLOURS["red"])


def column_story(canvas, x, y, width, kick, head, text, pic):
    """One of the four smaller stories; returns the y below it."""
    kick_f = load_font(FONT_SANS_B, 18)
    canvas.text((x, y), kick, font=kick_f, fill=COLOURS["red"])
    y += 24
    y = para(canvas, x, y, head, load_font(FONT_SERIF, 26), width, gap=2)
    y += 4
    pic_y = y
    body_w = width - 140
    end = para(canvas, x, y, text, load_font(FONT_SANS, 19), body_w, gap=3)
    pic(canvas, x + body_w + 12, pic_y, 128, 84)
    return max(end, pic_y + 84)


def two_column_row(canvas, y, left, right):
    """Draw two column stories side by side; return the y below."""
    col_w = (TEXT_W - 28) // 2
    top = y
    l_end = column_story(canvas, EDGE, y, col_w, *left)
    r_end = column_story(canvas, EDGE + col_w + 28, y, col_w, *right)
    bottom = max(l_end, r_end)
    canvas.line([(EDGE + col_w + 14, top + 4),
                 (EDGE + col_w + 14, bottom)], fill=COLOURS["pale"],
                width=1)
    return bottom


LEAD = {
    "kick": "POLAND  ·  NATO",
    "head": "Russian missiles land in Poland as NATO cries foul",
    "text": ("Two Russian missiles and a suspected drone came down inside "
             "Poland during a massive Russian attack on Ukraine. No "
             "injuries were reported. Prime Minister Donald Tusk called "
             "it an intentional provocation; NATO called it a grave "
             "violation of allied airspace."),
}

ROW_ONE = [
    ("MARKETS  ·  NEW YORK",
     "Wall Street slides into correction as AI shares plunge",
     "US stocks fell about 3.7% on Friday, pushing the S&P 500 and "
     "the Dow into correction territory as chip stocks led the "
     "sell-off. Nvidia's crash deepened the rout.",
     pic_chart),
    ("JUSTICE  ·  THE HAGUE",
     "World Court finds Myanmar committed genocide",
     "The International Court of Justice ruled Myanmar's security "
     "forces committed state-sponsored genocide against the "
     "Rohingya. Myanmar called the ruling unfair.",
     pic_scales),
]

ROW_TWO = [
    ("EUROPE  ·  BRUSSELS",
     "UK and EU strike their biggest post-Brexit deal",
     "The deal scraps food checks, links carbon markets and opens "
     "100,000 youth visas each way for up to three years. Britain "
     "rejoins the Erasmus+ student exchange.",
     pic_flags),
    ("PERU  ·  EARTHQUAKE",
     "Magnitude 6.8 quake shakes central Peru",
     "A strong quake struck the Andean region of Junin, 129 km "
     "deep, and was felt in Lima, where people ran into the "
     "streets. No casualties were reported.",
     pic_quake),
]

TICKER = ("DENMARK FOILS ALLEGED RUSSIAN PLOT, EXPELS ATTACHE  •  "
          "TRUMP THREATENS BAN ON US AI DATA CENTRES ABROAD  •  "
          "MAMDANI: RIKERS TO CLOSE BY 2032  •  KL RAHUL COMPLETES "
          "SENA CENTURIES  •  COP31 IN FINAL STAGE")


def build():
    page = Image.new("RGB", (PAGE_W, PAGE_H), COLOURS["paper"])
    canvas = ImageDraw.Draw(page)

    y = 20
    over = load_font(FONT_SANS_B, 16)
    label = "THE WORLD IN ONE IMAGE"
    canvas.text(((PAGE_W - canvas.textlength(label, font=over)) / 2, y),
                label, font=over, fill=COLOURS["grey"])
    y += 26
    mast = load_font(FONT_SERIF, 76)
    name = "THE DAILY GLOBE"
    canvas.text(((PAGE_W - canvas.textlength(name, font=mast)) / 2, y),
                name, font=mast, fill=COLOURS["ink"])
    y += 88
    date_f = load_font(FONT_SANS_B, 23)
    date = "SATURDAY  21  NOVEMBER  2026"
    canvas.text(((PAGE_W - canvas.textlength(date, font=date_f)) / 2, y),
                date, font=date_f, fill=COLOURS["ink"])
    y += 36
    y = double_hrule(canvas, y)
    y += 6

    # Lead story: Poland, full width with a map on the right.
    kick_f = load_font(FONT_SANS_B, 18)
    canvas.text((EDGE, y), LEAD["kick"], font=kick_f,
                fill=COLOURS["red"])
    y += 24
    y = para(canvas, EDGE, y, LEAD["head"], load_font(FONT_SERIF, 46),
             TEXT_W, gap=2)
    y += 6
    pic_y = y
    end = para(canvas, EDGE, y, LEAD["text"], load_font(FONT_SANS, 21),
               TEXT_W - 320, gap=3)
    pic_poland(canvas, EDGE + TEXT_W - 300, pic_y, 300, 158)
    y = max(end, pic_y + 158) + 8
    y = double_hrule(canvas, y)
    y += 8

    # Two rows of two stories each.
    y = two_column_row(canvas, y, *ROW_ONE)
    y += 8
    hrule(canvas, y, 1)
    y += 10
    y = two_column_row(canvas, y, *ROW_TWO)
    y += 8
    hrule(canvas, y, 1)
    y += 10

    # Ticker band and footer.
    band_h = 58
    canvas.rectangle([EDGE, y, PAGE_W - EDGE, y + band_h],
                     fill=COLOURS["navy"])
    tick_f = load_font(FONT_SANS_B, 16)
    lines = wrap_text(canvas, TICKER, tick_f, TEXT_W - 24)
    ty = y + (band_h - len(lines) * 20) // 2
    for line in lines:
        canvas.text((EDGE + 12, ty), line, font=tick_f,
                    fill=(255, 255, 255))
        ty += 20
    y += band_h
    foot = load_font(FONT_SANS, 15)
    note = "THE DAILY GLOBE  •  SATURDAY 21 NOVEMBER 2026  •  FIVE STORIES, ONE DAY"
    canvas.text(((PAGE_W - canvas.textlength(note, font=foot)) / 2, y + 12),
                note, font=foot, fill=COLOURS["grey"])
    y += 36
    assert y <= PAGE_H - 4, f"layout overflow: y={y}"
    print("layout bottom y =", y)

    page.save("assets/entry.png", format="PNG", optimize=True)
    print("wrote assets/entry.png", page.size)


if __name__ == "__main__":
    build()
