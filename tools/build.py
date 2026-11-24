"""Builds the SVG images for the GitHub profile README.

All text is converted to outlines, so the images look the same on every
device: GitHub shows SVGs through <img>, which cannot load web fonts.

    python3 -m venv .venv && .venv/bin/pip install uharfbuzz
    .venv/bin/python tools/build.py

Fonts (OFL, from github.com/google/fonts) go to tools/fonts/:
    Archivo[wdth,wght].ttf  -> Archivo.ttf
    SplineSansMono[wght].ttf -> SplineSansMono.ttf
"""

from pathlib import Path

import uharfbuzz as hb

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path(__file__).resolve().parent / "fonts"
OUT = ROOT / "assets"

# Colors: the same tokens as the personal site.
THEMES = {
    "light": dict(
        ink="#17221C", muted="#5E6C64", line="#D3DBD1", surface="#FFFFFF",
        tile="#EEF1EC", pass_="#1C7F47", pass_soft="#DDEFE3", select="#BDD6FF",
        panel="#17221C", panel_fg="#E9EFE8", panel_muted="#8A9A90", panel_pass="#6FD39A",
        panel_line="#17221C",
    ),
    "dark": dict(
        ink="#E6ECE6", muted="#93A198", line="#273129", surface="#161D19",
        tile="#121915", pass_="#56C987", pass_soft="#183425", select="#2C4D7F",
        panel="#141B17", panel_fg="#E6ECE6", panel_muted="#7E8C83", panel_pass="#56C987",
        panel_line="#273129",
    ),
}


class Pen:
    """Collects glyph outlines as SVG path data, flipped to SVG coordinates."""

    def __init__(self):
        self.parts = []
        self.dx = self.dy = 0.0
        self.s = 1.0

    def _p(self, pt):
        x, y = pt
        return f"{self.dx + x * self.s:.1f} {self.dy - y * self.s:.1f}"

    def moveTo(self, pt):
        self.parts.append("M" + self._p(pt))

    def lineTo(self, pt):
        self.parts.append("L" + self._p(pt))

    def qCurveTo(self, *pts):
        self.parts.append("Q" + " ".join(self._p(p) for p in pts))

    def curveTo(self, *pts):
        self.parts.append("C" + " ".join(self._p(p) for p in pts))

    def closePath(self):
        self.parts.append("Z")

    def endPath(self):
        pass


class Face:
    def __init__(self, file, **axes):
        blob = hb.Blob.from_file_path(str(FONTS / file))
        face = hb.Face(blob)
        self.upem = face.upem
        self.font = hb.Font(face)
        self.font.set_variations(axes)

    def _shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions

    def width(self, text, size, track=0.0):
        infos, pos = self._shape(text)
        adv = sum(p.x_advance for p in pos) + track * self.upem * len(pos)
        return adv * size / self.upem

    def path(self, text, x, y, size, track=0.0):
        """Returns SVG path data for text with its baseline at (x, y)."""
        infos, pos = self._shape(text)
        pen = Pen()
        s = size / self.upem
        cx = 0.0
        for info, p in zip(infos, pos):
            pen.dx = x + (cx + p.x_offset) * s
            pen.dy = y - p.y_offset * s
            pen.s = s
            self.font.draw_glyph_with_pen(info.codepoint, pen)
            cx += p.x_advance + track * self.upem
        return "".join(pen.parts)


DISPLAY = Face("Archivo.ttf", wdth=116, wght=780)
ROLE = Face("Archivo.ttf", wdth=100, wght=500)
UI = Face("Archivo.ttf", wdth=100, wght=420)
UI_BOLD = Face("Archivo.ttf", wdth=100, wght=560)
MONO = Face("SplineSansMono.ttf", wght=400)
MONO_BOLD = Face("SplineSansMono.ttf", wght=520)


def text(face, s, x, y, size, fill, cls="", track=0.0):
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} fill="{fill}" d="{face.path(s, x, y, size, track)}"/>'


def wrap(face, s, size, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if face.width(trial, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


# ---------------------------------------------------------------- banner

ROWS_WIDE = [
    ("automation", "web, iOS, Android and API suites in four frameworks"),
    ("releases", "Playwright e2e coverage from 0% to 90%, wired into CI"),
    ("people", "led a QA team of five, took interns to full-time hires"),
    ("side work", "13 projects: 9 live, 2 in beta, 2 in progress"),
]
ROWS_NARROW = [
    ("automation", "web, iOS, Android, API"),
    ("releases", "e2e coverage 0% to 90%"),
    ("people", "led a QA team of five"),
    ("side work", "13 projects, 9 live"),
]

# One orchestrated moment: the self-test prints line by line, like a terminal.
ANIM = """
<style>
.o{animation:show 1ms linear both}
.o1{animation-delay:.9s}.o2{animation-delay:1.25s}.o3{animation-delay:1.6s}
.o4{animation-delay:1.95s}.o5{animation-delay:2.45s}
.caret{animation:blink .45s steps(1,end) 0s 5 both,gone 1ms linear 2.25s both}
@keyframes show{from{opacity:0}to{opacity:1}}
@keyframes blink{50%{opacity:0}}
@keyframes gone{to{opacity:0}}
@media (prefers-reduced-motion:reduce){.o{animation:none}.caret{animation:none;opacity:0}}
</style>"""


def banner(theme, narrow):
    t = THEMES[theme]
    W = 720 if narrow else 1280
    out = []

    # Name.
    name_size = 112 if narrow else 104
    track = -0.025
    y = name_size * 0.80
    if narrow:
        for i, word in enumerate(["Artem", "Kupratsevich"]):
            size = name_size
            while DISPLAY.width(word, size, track) > W - 4:
                size -= 1
            out.append(text(DISPLAY, word, 0, y + i * name_size * 0.98, size, t["ink"], track=track))
        y += name_size * 0.98
    else:
        size = name_size
        while DISPLAY.width("Artem Kupratsevich", size, track) > W - 4:
            size -= 1
        out.append(text(DISPLAY, "Artem Kupratsevich", 0, y, size, t["ink"], track=track))

    # Role.
    role = "QA Engineer working remotely from Belgrade, Serbia."
    role_size = 34 if narrow else 30
    y += role_size * 1.9
    for line in wrap(ROLE, role, role_size, W - 4):
        out.append(text(ROLE, line, 0, y, role_size, t["ink"], track=-0.01))
        y += role_size * 1.3
    y += 22 if narrow else 18

    # Self-test panel.
    rows = ROWS_NARROW if narrow else ROWS_WIDE
    ms = 26 if narrow else 22
    pad = 32 if narrow else 36
    lh = ms * 1.7
    ch = MONO.width("0", ms)
    top = y
    rect_at = len(out)
    by = top + pad + ms * 0.8
    out.append(text(MONO, "$ ", pad, by, ms, t["panel_muted"]))
    cmd = "artem --self-test"
    out.append(text(MONO_BOLD, cmd, pad + 2 * ch, by, ms, t["panel_fg"]))
    cx = pad + (2 + len(cmd) + 1) * ch
    out.append(
        f'<rect class="caret" x="{cx:.1f}" y="{by - ms * 0.78:.1f}" width="{ch * 0.9:.1f}" '
        f'height="{ms * 0.98:.1f}" fill="{t["panel_fg"]}"/>'
    )
    by += lh * 0.55
    key_x = pad + 6 * ch
    val_x = key_x + 12 * ch
    for i, (k, v) in enumerate(rows, 1):
        by += lh
        out.append(f'<g class="o o{i}">')
        out.append(text(MONO_BOLD, "pass", pad, by, ms, t["panel_pass"]))
        out.append(text(MONO, k, key_x, by, ms, t["panel_muted"]))
        out.append(text(MONO, v, val_x, by, ms, t["panel_fg"]))
        out.append("</g>")
    by += lh * 1.4
    out.append(f'<g class="o o5">{text(MONO, "4 passed, 0 failed", pad, by, ms, t["panel_pass"])}</g>')
    panel_h = by + ms * 0.25 + pad - top
    out.insert(
        rect_at,
        f'<rect x="0.5" y="{top + 0.5:.1f}" width="{W - 1}" height="{panel_h:.1f}" rx="16" '
        f'fill="{t["panel"]}" stroke="{t["panel_line"]}"/>',
    )
    H = top + panel_h + 2

    rows_text = "; ".join(f"pass {k}: {v}" for k, v in rows)
    title = f"Artem Kupratsevich. {role} Self-test: {rows_text}. 4 passed, 0 failed."
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" '
        f'viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{title}">'
        f"<title>{title}</title>{ANIM}" + "".join(out) + "</svg>"
    )


# ------------------------------------------------- Chrome extension mock

def menu_mock(theme):
    t = THEMES[theme]
    W, H = 1280, 640
    out = [f'<rect width="{W}" height="{H}" rx="20" fill="{t["tile"]}"/>']

    # A classified listing with a selected phrase.
    fs = 34
    x0, y0 = 96, 150
    before, sel, after = "Prodajem ", "Thule 591 nosač za bicikl", ", malo korišćen, Novi Beograd."
    w_before = UI.width(before, fs)
    w_sel = UI.width(sel, fs)
    out.append(
        f'<rect x="{x0 + w_before - 3:.1f}" y="{y0 - fs * 0.86:.1f}" width="{w_sel + 6:.1f}" '
        f'height="{fs * 1.2:.1f}" rx="4" fill="{t["select"]}"/>'
    )
    out.append(text(UI, before, x0, y0, fs, t["muted"]))
    out.append(text(UI, sel, x0 + w_before, y0, fs, t["ink"]))
    out.append(text(UI, after, x0 + w_before + w_sel, y0, fs, t["muted"]))

    # The context menu, opened at the end of the selection.
    items = [
        ("Copy", False),
        ("Search Google for “Thule 591 nosač…”", False),
        ("Search on Kupujemprodajem", True),
        ("Search on Halo Oglasi", False),
        ("Print…", False),
    ]
    ms = 30
    row = 58
    mx, my = x0 + w_before + w_sel * 0.55, y0 + 42
    mw = 640
    mh = row * len(items) + 24
    out.append(
        f'<rect x="{mx + 4:.1f}" y="{my + 10:.1f}" width="{mw}" height="{mh}" rx="14" '
        f'fill="#000" opacity="{0.10 if theme == "light" else 0.35}"/>'
    )
    out.append(
        f'<rect x="{mx:.1f}" y="{my:.1f}" width="{mw}" height="{mh}" rx="14" '
        f'fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2"/>'
    )
    iy = my + 12
    for label, on in items:
        if on:
            out.append(
                f'<rect x="{mx + 8:.1f}" y="{iy:.1f}" width="{mw - 16}" height="{row}" rx="8" '
                f'fill="{t["pass_soft"]}"/>'
            )
        face = UI_BOLD if on else UI
        out.append(text(face, label, mx + 32, iy + row * 0.66, ms, t["pass_"] if on else t["ink"]))
        iy += row

    label = (
        "A browser context menu over a classified listing. The selected words "
        "“Thule 591 nosač za bicikl” can be searched on Kupujemprodajem or Halo Oglasi."
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{label}"><title>{label}</title>' + "".join(out) + "</svg>"
    )


def main():
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"header-{theme}.svg").write_text(banner(theme, narrow=False))
        (OUT / f"header-narrow-{theme}.svg").write_text(banner(theme, narrow=True))
        (OUT / f"kupujemprodajem-{theme}.svg").write_text(menu_mock(theme))
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:32} {f.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
