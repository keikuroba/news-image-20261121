#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Build-time script only; the entry itself (main.py) just ships the PNG.
Deterministic: no clock, no randomness, no network. Pillow only.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (247, 243, 234)
INK = (18, 18, 18)
GREY = (90, 86, 76)
RED = (178, 34, 34)
NAVY = (16, 32, 64)
BLUE = (28, 68, 128)
GOLD = (176, 128, 28)
LIGHT_LINE = (150, 144, 128)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, spacing=4):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, y, weight=2):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=weight)


def double_rule(draw, y):
    rule(draw, y, 3)
    rule(draw, y + 6, 1)
    return y + 12


def kicker(draw, x, y, text):
    f = font(SANS_B, 18)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 24


def headline(draw, x, y, text, size, width):
    return draw_wrapped(draw, x, y, text, font(SERIF, size), width,
                        fill=INK, spacing=2)


def body(draw, x, y, text, width, size=19):
    return draw_wrapped(draw, x, y, text, font(SANS, size), width,
                        fill=INK, spacing=3)


def burst(draw, cx, cy, r, col=(232, 120, 40)):
    for dx, dy, rr in [(0, 0, r), (-r, r // 2, r // 2),
                       (r // 2, -r // 2, r // 2), (r // 3, r // 2, r // 3)]:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr,
                      cy + dy + rr], fill=col)


def poland_graphic(draw, x, y, w, h):
    """Stylised map of Poland with two missile impacts."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.text((x + 10, y + 8), "POLAND", font=font(SANS_B, 14), fill=GREY)
    # rough Poland outline
    pts = [(x + 30, y + 34), (x + 90, y + 26), (x + 150, y + 30),
           (x + 205, y + 42), (x + 250, y + 36), (x + 272, y + 62),
           (x + 262, y + 96), (x + 240, y + 118), (x + 200, y + 128),
           (x + 150, y + 132), (x + 100, y + 126), (x + 55, y + 112),
           (x + 28, y + 84), (x + 20, y + 58)]
    draw.polygon(pts, fill=(236, 230, 210), outline=INK)
    # missile arc from the east (kept inside the box)
    draw.arc([x + 196, y + 10, x + 292, y + 62], start=195, end=335,
             fill=RED, width=3)
    burst(draw, x + 238, y + 74, 13)
    burst(draw, x + 130, y + 92, 10)
    draw.text((x + 10, y + h - 22), "2 MISSILES + DRONE DOWN",
              font=font(SANS_B, 12), fill=RED)


def chart_graphic(draw, x, y, w, h):
    """Falling market line."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.text((x + 8, y + 6), "S&P 500  -3.7%",
              font=font(SANS_B, 15), fill=RED)
    pts = [(x + 8 + i * (w - 16) / 6,
            y + 30 + (i * i) * (h - 48) / 36) for i in range(7)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.ellipse([pts[-1][0] - 5, pts[-1][1] - 5,
                  pts[-1][0] + 5, pts[-1][1] + 5], fill=RED)


def scales_graphic(draw, x, y, w, h):
    """Scales of justice for the ICJ ruling."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 220, 205))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.text((x + 8, y + 6), "ICJ",
              font=font(SANS_B, 13), fill=GREY)
    cx, cy = x + w // 2, y + 22
    draw.line([(cx, cy), (cx, y + h - 14)], fill=INK, width=3)
    draw.line([(cx - 42, cy + 6), (cx + 42, cy + 6)], fill=INK, width=3)
    for s in (-1, 1):
        px = cx + s * 42
        draw.line([(px, cy + 6), (px, cy + 30)], fill=INK, width=2)
        draw.arc([px - 16, cy + 26, px + 16, cy + 52], start=0, end=180,
                 fill=NAVY, width=3)
        draw.line([(px - 16, cy + 39), (px + 16, cy + 39)], fill=NAVY,
                  width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)


def flags_graphic(draw, x, y, w, h):
    """Union Jack beside the EU ring of stars."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=INK, width=2)
    # Union Jack (simplified)
    ux, uy, uw, uh = x + 8, y + 14, 56, 56
    draw.rectangle([ux, uy, ux + uw, uy + uh], fill=(0, 36, 125))
    draw.line([(ux, uy), (ux + uw, uy + uh)], fill=(255, 255, 255), width=9)
    draw.line([(ux + uw, uy), (ux, uy + uh)], fill=(255, 255, 255), width=9)
    draw.line([(ux, uy), (ux + uw, uy + uh)], fill=(200, 16, 46), width=3)
    draw.line([(ux + uw, uy), (ux, uy + uh)], fill=(200, 16, 46), width=3)
    draw.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)],
              fill=(255, 255, 255), width=11)
    draw.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)],
              fill=(255, 255, 255), width=11)
    draw.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)],
              fill=(200, 16, 46), width=5)
    draw.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)],
              fill=(200, 16, 46), width=5)
    # EU flag (simplified): blue field, ring of gold stars
    ex, ey, ew, eh = x + w - 64, y + 14, 56, 56
    draw.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    import math
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = ex + ew // 2 + int(19 * math.cos(a))
        sy = ey + eh // 2 + int(19 * math.sin(a))
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def quake_graphic(draw, x, y, w, h):
    """Seismograph trace, M6.8."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.text((x + 8, y + 6), "M 6.8 · JUNIN",
              font=font(SANS_B, 13), fill=RED)
    mid = y + h // 2 + 6
    pts = [(x + 6, mid)]
    spikes = [0, 2, -3, 5, -22, 26, -14, 8, -4, 2, 0]
    for i, s in enumerate(spikes):
        pts.append((x + 6 + (i + 1) * (w - 12) / 11, mid + s))
    draw.line(pts, fill=INK, width=2, joint="curve")
    draw.ellipse([pts[5][0] - 4, pts[5][1] - 4,
                  pts[5][0] + 4, pts[5][1] + 4], fill=RED)


def story_block(draw, x, y, width, kick, head, text, graphic):
    """One column story; returns bottom y. Graphic floats right of body."""
    top = y
    y = kicker(draw, x, y, kick)
    y = headline(draw, x, y, head, 26, width)
    y += 4
    gy = y
    text_w = width - 140
    end = body(draw, x, y, text, text_w)
    graphic(draw, x + text_w + 12, gy, 128, 84)
    return max(end, gy + 84), top


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = 20
    top = font(SANS_B, 16)
    label = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(label, font=top)) / 2, y), label,
           font=top, fill=GREY)
    y += 26
    mast = font(SERIF, 76)
    name = "THE DAILY GLOBE"
    d.text(((W - d.textlength(name, font=mast)) / 2, y), name,
           font=mast, fill=INK)
    y += 88
    date_f = font(SANS_B, 23)
    date = "SATURDAY  21  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, y), date,
           font=date_f, fill=INK)
    y += 36
    y = double_rule(d, y)
    y += 6

    # ---- lead story: Poland ----
    y = kicker(d, MARGIN, y, "POLAND  ·  NATO")
    y = headline(d, MARGIN, y,
                 "Russian missiles land in Poland as NATO cries foul",
                 46, CW)
    y += 6
    gy = y
    lead = ("Two Russian missiles and a suspected drone came down inside "
            "Poland during a massive Russian attack on Ukraine. No "
            "injuries were reported. Prime Minister Donald Tusk called "
            "it an intentional provocation; NATO called it a grave "
            "violation of allied airspace.")
    end = body(d, MARGIN, y, lead, CW - 320, size=21)
    poland_graphic(d, MARGIN + CW - 300, gy, 300, 158)
    y = max(end, gy + 158) + 8
    y = double_rule(d, y)
    y += 8

    # ---- row: markets + ICJ ----
    col_w = (CW - 28) // 2
    row_top = y
    left_end, _ = story_block(
        d, MARGIN, y, col_w, "MARKETS  ·  NEW YORK",
        "Wall Street slides into correction as AI shares plunge",
        "US stocks fell about 3.7% on Friday, pushing the S&P 500 and "
        "the Dow into correction territory as chip stocks led the "
        "sell-off. Nvidia's crash deepened the rout.",
        chart_graphic)
    right_end, _ = story_block(
        d, MARGIN + col_w + 28, y, col_w, "JUSTICE  ·  THE HAGUE",
        "World Court finds Myanmar committed genocide",
        "The International Court of Justice ruled Myanmar's security "
        "forces committed state-sponsored genocide against the "
        "Rohingya. Myanmar called the ruling unfair.",
        scales_graphic)
    y = max(left_end, right_end)
    d.line([(MARGIN + col_w + 14, row_top + 4),
            (MARGIN + col_w + 14, y)], fill=LIGHT_LINE, width=1)
    y += 8
    rule(d, y, 1)
    y += 10

    # ---- row: UK-EU + Peru quake ----
    row_top = y
    left_end, _ = story_block(
        d, MARGIN, y, col_w, "EUROPE  ·  BRUSSELS",
        "UK and EU strike their biggest post-Brexit deal",
        "The deal scraps food checks, links carbon markets and opens "
        "100,000 youth visas each way for up to three years. Britain "
        "rejoins the Erasmus+ student exchange.",
        flags_graphic)
    right_end, _ = story_block(
        d, MARGIN + col_w + 28, y, col_w, "PERU  ·  EARTHQUAKE",
        "Magnitude 6.8 quake shakes central Peru",
        "A strong quake struck the Andean region of Junin, 129 km "
        "deep, and was felt in Lima, where people ran into the "
        "streets. No casualties were reported.",
        quake_graphic)
    y = max(left_end, right_end)
    d.line([(MARGIN + col_w + 14, row_top + 4),
            (MARGIN + col_w + 14, y)], fill=LIGHT_LINE, width=1)
    y += 8
    rule(d, y, 1)
    y += 10

    # ---- ticker ----
    ticker = ("DENMARK FOILS ALLEGED RUSSIAN PLOT, EXPELS ATTACHE  •  "
              "TRUMP THREATENS BAN ON US AI DATA CENTRES ABROAD  •  "
              "MAMDANI: RIKERS TO CLOSE BY 2032  •  KL RAHUL COMPLETES "
              "SENA CENTURIES  •  COP31 IN FINAL STAGE")
    band_h = 58
    d.rectangle([MARGIN, y, W - MARGIN, y + band_h], fill=NAVY)
    tf = font(SANS_B, 16)
    lines = wrap(d, ticker, tf, CW - 24)
    ty = y + (band_h - len(lines) * 20) // 2
    for ln in lines:
        d.text((MARGIN + 12, ty), ln, font=tf, fill=(255, 255, 255))
        ty += 20
    y += band_h
    foot = font(SANS, 15)
    note = "THE DAILY GLOBE  •  SATURDAY 21 NOVEMBER 2026  •  FIVE STORIES, ONE DAY"
    d.text(((W - d.textlength(note, font=foot)) / 2, y + 12), note,
           font=foot, fill=GREY)
    y += 36
    assert y <= H - 4, f"layout overflow: y={y}"
    print("layout bottom y =", y)

    img.save("assets/entry.png", format="PNG", optimize=True)
    print("wrote assets/entry.png", img.size)


if __name__ == "__main__":
    main()
