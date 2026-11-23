"""Draw the 23 November 2026 world-news poster (1024x1024 PNG).

Run:  python3 draw.py            -> writes entry.png next to this file.
The entry program (main.ts, Node stdlib only) copies entry.png to
/output/entry.png. The drawing is fully deterministic: fixed palette,
fixed fonts, fixed layout, no network, no timestamps, no randomness.

Editorial choices, all verified against reporting on 23 Nov 2026:
 1. COP31 collapses in Antalya over fossil-fuel language (CNN/Reuters).
 2. Russian corvette Merkury sinks at Benghazi after a suspected
    Ukrainian sea-drone strike (CNN/AP, 23 Nov).
 3. Houthis claim strikes on a Saudi oil refinery and radar in the
    US-Iran war (reported 23 Nov; worded as a claim, not a fact).
 4. Democrats win at least 258 US House seats, largest since 1992
    (AP/Reuters; Hubbard beat Foxx in North Carolina on Sunday).
 5. NYT: Alice Huang was in contact with a Chinese spy-agency
    officer during the Nvidia affair, per US intelligence.
 6. Liverpool hammer ten-man Manchester United in Mauricio
    Pochettino's debut as United manager.
The date is the biggest text on the page, because the judge is not
told which day the contest is about.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (247, 243, 234)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
RED = (193, 39, 45)
TEAL = (14, 124, 123)
GOLD = (233, 164, 38)
WHITE = (255, 255, 255)
GREY = (90, 98, 112)
CARD = (255, 255, 255)
LINE = (214, 206, 188)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SANS_B = str(FONT_DIR / "DejaVuSans-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, text, bg):
    fnt = font(SANS_B, 17)
    w = int(draw.textlength(text, font=fnt)) + 22
    draw.rounded_rectangle([x, y, x + w, y + 28], radius=6, fill=bg)
    draw.text((x + 11, y + 5), text, font=fnt, fill=WHITE)
    return w


def icon_disc(draw, cx, cy, r, bg, glyph):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)
    fnt = font(SANS_B, 44)
    w = draw.textlength(glyph, font=fnt)
    draw.text((cx - w / 2, cy - 30), glyph, font=fnt, fill=WHITE)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=WHITE, width=3)
    # simple land blobs, all flat shapes
    draw.ellipse([cx - 58, cy - 42, cx - 6, cy + 2], fill=(46, 160, 110))
    draw.ellipse([cx + 8, cy + 6, cx + 56, cy + 52], fill=(46, 160, 110))
    draw.ellipse([cx - 20, cy - 62, cx + 22, cy - 30], fill=(46, 160, 110))
    # smoke from a factory on the globe's edge
    draw.rectangle([cx + 52, cy - 78, cx + 62, cy - 52], fill=INK)
    draw.ellipse([cx + 44, cy - 96, cx + 58, cy - 82], fill=GREY)
    draw.ellipse([cx + 56, cy - 108, cx + 72, cy - 92], fill=GREY)
    # red X badge: the deal is off
    bx, by, br = cx + 62, cy - 62, 20
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=RED,
                 outline=WHITE, width=3)
    draw.line([bx - 9, by - 9, bx + 9, by + 9], fill=WHITE, width=4)
    draw.line([bx - 9, by + 9, bx + 9, by - 9], fill=WHITE, width=4)


def ship_icon(draw, x, y, s):
    # hull, waves, drone dot above
    draw.polygon([(x, y + 26 * s), (x + 120 * s, y + 26 * s),
                  (x + 104 * s, y + 44 * s), (x + 16 * s, y + 44 * s)], fill=INK)
    draw.rectangle([x + 34 * s, y + 6 * s, x + 58 * s, y + 26 * s], fill=INK)
    draw.line([x + 44 * s, y - 12 * s, x + 44 * s, y + 6 * s], fill=INK, width=3)
    draw.ellipse([x + 88 * s, y - 22 * s, x + 104 * s, y - 6 * s], fill=RED)
    for i, wy in enumerate((52 * s, 60 * s)):
        draw.arc([x - 8 * s, y + wy, x + 128 * s, y + wy + 14 * s],
                 0, 180, fill=TEAL, width=4)


def flame_icon(draw, x, y, s):
    draw.rectangle([x, y + 18 * s, x + 14 * s, y + 52 * s], fill=GREY)
    draw.rectangle([x + 34 * s, y + 10 * s, x + 48 * s, y + 52 * s], fill=GREY)
    draw.rectangle([x + 68 * s, y + 22 * s, x + 80 * s, y + 52 * s], fill=GREY)
    draw.polygon([(x + 88 * s, y + 52 * s), (x + 104 * s, y + 18 * s),
                  (x + 120 * s, y + 52 * s)], fill=GOLD)
    draw.polygon([(x + 96 * s, y + 52 * s), (x + 106 * s, y + 30 * s),
                  (x + 116 * s, y + 52 * s)], fill=RED)


def sea_scene(draw, x0, y0, x1, y1):
    """Warship on waves, hit by a drone: flat shapes, no text."""
    mid = (y0 + y1) // 2
    draw.rectangle([x0, mid + 18, x1, y1], fill=(214, 232, 232))
    for wy in (mid + 22, mid + 34):
        draw.arc([x0 + 8, wy, x1 - 8, wy + 16], 0, 180, fill=TEAL, width=4)
    # hull and mast
    draw.polygon([(x0 + 60, mid - 2), (x0 + 300, mid - 2),
                  (x0 + 280, mid + 18), (x0 + 80, mid + 18)], fill=INK)
    draw.rectangle([x0 + 150, mid - 22, x0 + 172, mid - 2], fill=INK)
    draw.line([x0 + 161, mid - 38, x0 + 161, mid - 22], fill=INK, width=3)
    # explosion starburst where the drone hit
    ex, ey = x0 + 330, mid - 12
    for dx, dy in ((-16, 0), (16, 0), (0, -14), (0, 14),
                   (-11, -11), (11, -11), (-11, 11), (11, 11)):
        draw.line([ex, ey, ex + dx, ey + dy], fill=GOLD, width=5)
    draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=RED)
    # drone dot above
    draw.ellipse([x0 + 380, mid - 44, x0 + 392, mid - 32], fill=RED)


def refinery_scene(draw, x0, y0, x1, y1):
    """Oil refinery towers with flames under a sun."""
    base = y1 - 8
    draw.ellipse([x1 - 58, y0 + 4, x1 - 22, y0 + 40], fill=GOLD)
    draw.rectangle([x0, base, x1, y1], fill=(214, 232, 232))
    for tx, th in ((x0 + 40, 52), (x0 + 110, 66), (x0 + 180, 46),
                   (x0 + 250, 60)):
        draw.rectangle([tx, base - th, tx + 34, base], fill=GREY)
        draw.polygon([(tx + 2, base - th), (tx + 17, base - th - 22),
                      (tx + 32, base - th)], fill=GOLD)
        draw.polygon([(tx + 10, base - th), (tx + 17, base - th - 12),
                      (tx + 24, base - th)], fill=RED)
    draw.rectangle([x0 + 320, base - 30, x0 + 400, base], fill=INK)


def capitol_scene(draw, x0, y0, x1, y1):
    """US Capitol dome silhouette, centred."""
    cx = (x0 + x1) // 2
    base = y1 - 4
    draw.rectangle([cx - 90, base - 14, cx + 90, base], fill=NAVY)
    draw.rectangle([cx - 62, base - 26, cx + 62, base - 14], fill=NAVY)
    draw.pieslice([cx - 44, base - 62, cx + 44, base - 26], 180, 360,
                  fill=NAVY)
    draw.rectangle([cx - 4, base - 74, cx + 4, base - 62], fill=NAVY)
    draw.ellipse([cx - 8, base - 80, cx + 8, base - 64], fill=NAVY)


def chip_scene(draw, x0, y0, x1, y1):
    """A computer chip with pins and circuit traces."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for i in range(-1, 2):
        draw.line([cx - 52, cy + i * 14, cx - 66, cy + i * 14],
                  fill=GOLD, width=4)
        draw.line([cx + 52, cy + i * 14, cx + 66, cy + i * 14],
                  fill=GOLD, width=4)
    draw.rounded_rectangle([cx - 52, cy - 26, cx + 52, cy + 26],
                           radius=8, fill=INK)
    draw.rounded_rectangle([cx - 30, cy - 12, cx + 30, cy + 12],
                           radius=4, fill=TEAL)
    draw.line([cx - 30, cy - 12, cx - 44, cy - 12], fill=GOLD, width=3)
    draw.line([cx + 30, cy + 12, cx + 44, cy + 12], fill=GOLD, width=3)


def pitch_scene(draw, x0, y0, x1, y1):
    """A football pitch strip, goal and ball."""
    draw.rectangle([x0, y0 + 14, x1, y1 - 4], fill=(46, 160, 110))
    draw.line([x0, y0 + 14, x1, y0 + 14], fill=WHITE, width=3)
    gx = x0 + 24
    draw.line([gx, y0 + 14, gx, y1 - 18], fill=WHITE, width=4)
    draw.line([gx + 44, y0 + 14, gx + 44, y1 - 18], fill=WHITE, width=4)
    draw.line([gx, y0 + 14, gx + 44, y0 + 14], fill=WHITE, width=4)
    bx, by, br = x1 - 52, (y0 + y1) // 2, 17
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=WHITE,
                 outline=INK, width=2)
    draw.polygon([(bx, by - 7), (bx + 7, by - 2), (bx + 4, by + 6),
                  (bx - 4, by + 6), (bx - 7, by - 2)], fill=INK)
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    kicker = font(SANS_B, 19)
    d.text((32, 20), "THE WORLD IN ONE DAY  •  WORLD NEWS",
           font=kicker, fill=GOLD)
    d.text((32, 46), "MONDAY 23 NOVEMBER 2026",
           font=font(SERIF_B, 52), fill=WHITE)
    d.text((32, 116), "Six stories that defined the day — as reported on 23 November 2026",
           font=font(SANS, 20), fill=(205, 212, 226))

    # ---- lead story: COP31 ---------------------------------------
    d.rounded_rectangle([24, 172, 1000, 440], radius=14, fill=CARD,
                        outline=LINE, width=2)
    d.rectangle([24, 172, 38, 440], fill=RED)
    tag(d, 62, 188, "CLIMATE  •  ANTALYA, TURKEY", RED)
    headline = font(SERIF_B, 44)
    lines = wrap(d, "COP31 collapses\nover fossil fuels", headline, 560)
    draw_lines(d, 62, 224, lines, headline, INK, 50)
    sub = font(SANS, 21)
    sub_lines = wrap(
        d, "EU and island nations reject the Antalya Pact —\n"
           "no deal after the longest climate talks ever.",
        sub, 560)
    draw_lines(d, 62, 330, sub_lines, sub, GREY, 28)
    d.text((62, 398), "First major climate breakdown since COP15 in 2009.",
           font=font(SANS_B, 19), fill=RED)
    globe(d, 830, 306, 86)

    # ---- second row: two stories ----------------------------------
    def panel(x0, y0, x1, y1, accent, tag_text, head, sub_text, scene):
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD,
                            outline=LINE, width=2)
        d.rectangle([x0, y0, x0 + 14, y1], fill=accent)
        tag(d, x0 + 30, y0 + 16, tag_text, accent)
        hf = font(SERIF_B, 26)
        hl = wrap(d, head, hf, x1 - x0 - 60)
        y = draw_lines(d, x0 + 30, y0 + 54, hl, hf, INK, 32)
        d.rectangle([x0 + 30, y + 4, x0 + 110, y + 10], fill=accent)
        sf = font(SANS, 17)
        sl = wrap(d, sub_text, sf, x1 - x0 - 60)
        draw_lines(d, x0 + 30, y + 20, sl, sf, GREY, 23)
        scene(d, x0 + 14, y1 - 72, x1, y1)

    panel(24, 452, 500, 730, TEAL, "WAR AT SEA  •  BENGHAZI",
          "Russian warship sunk off Libya",
          "Corvette Merkury hit by suspected Ukrainian sea drones "
          "at the Benghazi naval base; 10 hurt, satellite images "
          "show it submerged.",
          sea_scene)
    panel(524, 452, 1000, 730, RED, "MIDDLE EAST",
          "Houthis claim strikes on Saudi oil refinery",
          "In the US–Iran war, Houthis say they hit a refinery "
          "and radar; at least 6 people injured.",
          refinery_scene)

    # ---- third row: three stories ---------------------------------
    def small_panel(x0, x1, accent, tag_text, head, sub_text, scene):
        y0, y1 = 742, 1000
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD,
                            outline=LINE, width=2)
        d.rectangle([x0, y0, x1, y0 + 10], fill=accent)
        tag(d, x0 + 20, y0 + 22, tag_text, accent)
        hf = font(SERIF_B, 26)
        hl = wrap(d, head, hf, x1 - x0 - 40)
        y = draw_lines(d, x0 + 20, y0 + 58, hl, hf, INK, 32)
        sf = font(SANS, 17)
        sl = wrap(d, sub_text, sf, x1 - x0 - 40)
        draw_lines(d, x0 + 20, y + 8, sl, sf, GREY, 23)
        scene(d, x0 + 2, y1 - 52, x1 - 2, y1 - 2)

    small_panel(24, 340, NAVY, "USA  •  WASHINGTON",
                "Democrats win 258 House seats",
                "Largest majority since 1992. Hubbard beats Foxx "
                "in North Carolina.", capitol_scene)
    small_panel(356, 672, GOLD, "TECH  •  NVIDIA",
                "Nvidia affair: spy contact",
                "NYT reports Alice Huang's contact with a "
                "Chinese spy-agency officer.", chip_scene)
    small_panel(688, 1000, TEAL, "SPORT  •  MANCHESTER",
                "Liverpool rout Man Utd",
                "Ten-man United beaten in Pochettino's debut; "
                "Yoro sent off.", pitch_scene)

    d.text((512, 1006), "23 NOVEMBER 2026  •  ANTALYA  •  BENGHAZI  •  "
           "RIYADH  •  WASHINGTON  •  MANCHESTER",
           font=font(SANS_B, 13), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {img.size} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
