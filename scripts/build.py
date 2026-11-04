"""
High-End Tech & Systems Engineering Profile Generator for Shlok Tiwari (sshloktiwarii)
Featuring:
- Asymmetric Chamfered Cockpit Geometry (45° corner cutouts + technical brackets `[ ]`)
- Systems Deck Information Architecture (Telemetry Ribbon → Command Hero → Split Console)
- Cyber Core & Circuit Bus Hub with animated packet flow lines
- 2x3 Grid Project Showcase with large typography & guaranteed 2-line text wrapping
- 100% Vector outline typography via fontTools Face (Audiowide, BigShouldersDisplay, IBMPlexMono)
"""

import datetime as dt
import html
import json
import math
import os
import re

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
ASSETS = os.path.join(ROOT, "assets")
DATA = os.path.join(ASSETS, "github.json")
USER = "sshloktiwarii"

# Tactical Tech Palette
OLIVE_ACCENT = "#8A9A5B"
OLIVE_GLOW = "#B4C97F"
NAVY_HERO = "#0A1324"
NAVY_DEEP = "#070B14"
W = 1280

THEMES = {
    "dark": dict(
        bg="#070B14",
        cell="#0D1526",
        fg="#E6ECF5",
        dim="#7E8C9F",
        edge="#1E2B40",
        empty="#121A2A",
        hero_bg="#091322",
        accent=OLIVE_ACCENT,
        accent_bright=OLIVE_GLOW,
    ),
    "light": dict(
        bg="#F4F6F9",
        cell="#FFFFFF",
        fg="#0A111E",
        dim="#5A6677",
        edge="#D5DCE6",
        empty="#E9EFF7",
        hero_bg="#E4ECF6",
        accent="#55692A",
        accent_bright="#708736",
    ),
}

LEVELS = ["", "#25331C", "#435928", "#688836", OLIVE_GLOW]
LEVELS_LIGHT = ["", "#D9E8BA", "#B2D17E", "#88AF44", "#5B7C22"]

# 6 Flagship projects with plain English descriptions
PROJECTS = [
    dict(
        slug="semcache",
        name="SemCache",
        repo="SemCache",
        url="https://github.com/sshloktiwarii/SemCache",
        line="Remembers answers from AI so you get instant responses without paying twice.",
        tag="Runtime Cache",
        stack="Python · Vector Cosine · In-Memory Cache",
    ),
    dict(
        slug="agentvault",
        name="AgentVault",
        repo="AgentVault",
        url="https://github.com/sshloktiwarii/AgentVault",
        line="A black-box flight recorder that tracks every move your AI agents make in real time.",
        tag="Security Audit",
        stack="Rust · SQLite WAL · Telemetry",
    ),
    dict(
        slug="sentinel",
        name="Sentinel-AI",
        repo="Sentinel",
        url="https://github.com/sshloktiwarii/Sentinel",
        line="Guards system memory against crashes during heavy local AI model inference.",
        tag="Memory Telemetry",
        stack="C++ · Mach Kernel · Apple Silicon · eBPF",
    ),
    dict(
        slug="aegis",
        name="Aegis Sandbox",
        repo="Aegis",
        url="https://github.com/sshloktiwarii/Aegis",
        line="Stops autonomous AI agents from running destructive terminal commands or leaking keys.",
        tag="Agent Boundary",
        stack="Rust · Landlock · Apple Seatbelt · AST Sanitizer",
    ),
    dict(
        slug="strata",
        name="Strata",
        repo="strata",
        url="https://github.com/sshloktiwarii/strata",
        line="A control center that runs and organizes large fleets of autonomous AI workers.",
        tag="Fleet Control",
        stack="TypeScript · Multi-Agent Runtime · Distributed",
    ),
    dict(
        slug="cortex",
        name="Cortex",
        repo="Cortex",
        url="https://github.com/sshloktiwarii/Cortex",
        line="The central brain that coordinates multiple specialized agents to solve big problems.",
        tag="Cognitive Core",
        stack="Local LLMs · Task Routing · Memory Synthesis",
    ),
]

STACK = ["Rust", "Go", "Python", "TypeScript", "C++", "Linux", "Docker", "SQLite", "Redis", "React"]
INTERESTS = [
    "distributed systems",
    "systems engineering",
    "local-first AI runtimes",
    "eBPF & low latency",
    "database internals",
    "autonomous agent fleets",
    "high-performance compute",
]
STATUS_LINES = [
    "autonomous agent runtimes",
    "low-latency distributed tools",
    "local-first AI infrastructures",
    "bulletproof systems code",
]

# ---------------------------------------------------------------- data


def load():
    with open(DATA) as f:
        return json.load(f)


def streaks(days):
    longest = run = 0
    for _, count, _ in days:
        run = run + 1 if count else 0
        longest = max(longest, run)
    current, i = 0, len(days) - 1
    if i >= 0 and days[i][1] == 0:
        i -= 1
    while i >= 0 and days[i][1]:
        current, i = current + 1, i - 1
    return current, longest


# ---------------------------------------------------------------- typography


class Face:
    def __init__(self, file):
        self.font = TTFont(os.path.join(SRC, "fonts", file))
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font["head"].unitsPerEm
        self.hmtx = self.font["hmtx"]

    def path(self, s, size, spacing):
        k = size / self.upm
        pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        x, extra = 0.0, []
        for i, ch in enumerate(s):
            if ch in SYMBOLS:
                pts = " ".join(f"{x + px * size / 1000:.1f},{-py * size / 1000:.1f}" for px, py in SYMBOLS[ch])
                extra.append(f"M{pts}Z")
                advance = 760 * size / 1000
            else:
                name = self.cmap.get(ord(ch)) or self.cmap.get(ord("?"))
                self.glyphs[name].draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))
                advance = self.hmtx[name][0] * k
            x += advance + (spacing if i < len(s) - 1 else 0)
        return pen.getCommands() + "".join(extra), x


def _star():
    pts = []
    for i in range(10):
        r = 360 if i % 2 == 0 else 150
        a = math.pi / 2 + i * math.pi / 5
        pts.append((380 + r * math.cos(a), 300 + r * math.sin(a)))
    return pts


SYMBOLS = {
    "★": _star(),
    "↗": [(130, 60), (480, 410), (480, 230), (570, 230), (570, 570), (230, 570), (230, 480), (410, 480), (60, 130)],
}

FACES = {
    "WM": "Audiowide-Regular.woff2",
    "Disp": "BigShouldersDisplay-Bold.woff2",
    "Mono": "IBMPlexMono-Regular.woff2",
    "MonoB": "IBMPlexMono-Bold.woff2",
}
_loaded = {}
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(h, body, css, w=W, title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
        f"<title>{html.escape(title)}</title><style>{css}{REDUCED}</style>{body}</svg>"
    )


def text(x, y, s, size, family="Mono", fill=None, anchor=None, cls=None, spacing=None):
    face_obj = _loaded.get(family) or _loaded.setdefault(family, Face(FACES[family]))
    gap = float(spacing.rstrip("em")) * size if spacing else 0
    d, width = face_obj.path(str(s), size, gap)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    c = f' class="{cls}"' if cls else ""
    f = f' fill="{fill}"' if fill else ""
    return f'<path transform="translate({x:.1f} {y:.1f})"{c}{f} d="{d}"/>'


# ---------------------------------------------------------------- chamfer cockpit geometry


def chamfer_path(x, y, w, h, c=14):
    """Generates a 45-degree chamfered rectangle path."""
    return (
        f"M {x+c} {y} "
        f"L {x+w-c} {y} L {x+w} {y+c} "
        f"L {x+w} {y+h-c} L {x+w-c} {y+h} "
        f"L {x+c} {y+h} L {x} {y+h-c} "
        f"L {x} {y+c} Z"
    )


def chamfer_cell(x, y, w, h, t, fill=None, active=False, c=14, brackets=True):
    """Cockpit module with inner hairline border and corner brackets."""
    stroke = t["accent"] if active else t["edge"]
    inner_stroke = "rgba(255,255,255,0.06)" if t["bg"].startswith("#0") else "#EBF0F7"
    inner_fill = fill or t["cell"]
    path_outer = chamfer_path(x, y, w, h, c=c)
    path_inner = chamfer_path(x + 1, y + 1, w - 2, h - 2, c=max(c - 1, 1))

    res = [
        f'<path d="{path_outer}" fill="{inner_fill}" stroke="{stroke}" stroke-width="1.5"/>',
        f'<path d="{path_inner}" fill="none" stroke="{inner_stroke}" stroke-width="1"/>',
    ]
    if brackets:
        b_len = 8
        b_col = t["accent_bright"] if active else t["accent"]
        res.append(
            f'<path d="M {x-3} {y+b_len} L {x-3} {y-3} L {x+b_len} {y-3}" fill="none" stroke="{b_col}" stroke-width="1.4" opacity="0.6"/>'
        )
        res.append(
            f'<path d="M {x+w+3} {y+b_len} L {x+w+3} {y-3} L {x+w-b_len} {y-3}" fill="none" stroke="{b_col}" stroke-width="1.4" opacity="0.6"/>'
        )
        res.append(
            f'<path d="M {x-3} {y+h-b_len} L {x-3} {y+h+3} L {x+b_len} {y+h+3}" fill="none" stroke="{b_col}" stroke-width="1.4" opacity="0.6"/>'
        )
        res.append(
            f'<path d="M {x+w+3} {y+h-b_len} L {x+w+3} {y+h+3} L {x+w-b_len} {y+h+3}" fill="none" stroke="{b_col}" stroke-width="1.4" opacity="0.6"/>'
        )
    return "".join(res)


def label(x, y, s, t):
    return text(x, y, s.upper(), 13, fill=t["dim"], spacing=".16em")


# ---------------------------------------------------------------- cyber core & bus hub


def cyber_core_hub(cx, cy, color=OLIVE_ACCENT, glow=OLIVE_GLOW, bg=NAVY_DEEP):
    """Central Cyber Core & Bus Hub with animated packet flow."""
    return f"""
    <g class="core_hub" transform="translate({cx}, {cy})">
      <!-- Outgoing Circuit Bus Lines with Flowing Data Packets -->
      <path d="M -220 0 L -80 0 M 80 0 L 220 0" stroke="{color}" stroke-width="1.8" stroke-dasharray="8 8" class="bus_line" opacity="0.7"/>
      <path d="M 0 -110 L 0 -70 M 0 70 L 0 110" stroke="{color}" stroke-width="1.8" stroke-dasharray="8 8" class="bus_line" opacity="0.7"/>
      <path d="M -140 -70 L -60 -30 M 60 30 L 140 70" stroke="{color}" stroke-width="1.4" stroke-dasharray="6 6" class="bus_line" opacity="0.45"/>
      <path d="M 140 -70 L 60 -30 M -60 30 L -140 70" stroke="{color}" stroke-width="1.4" stroke-dasharray="6 6" class="bus_line" opacity="0.45"/>
      
      <!-- Coordinate Crosshairs & Bearing Marks -->
      <line x1="-180" y1="0" x2="180" y2="0" stroke="{color}" stroke-width="0.8" opacity="0.3"/>
      <line x1="0" y1="-100" x2="0" y2="100" stroke="{color}" stroke-width="0.8" opacity="0.3"/>
      <circle cx="0" cy="0" r="130" fill="none" stroke="{color}" stroke-width="0.8" stroke-dasharray="4 8" opacity="0.25"/>
      <circle cx="0" cy="0" r="95" fill="none" stroke="{color}" stroke-width="1.2" stroke-dasharray="16 8" opacity="0.4" class="ring_spin"/>
      
      <!-- Hexagonal Core Chamber -->
      <polygon points="0,-60 52,-30 52,30 0,60 -52,30 -52,-30" fill="{bg}" stroke="{color}" stroke-width="2.2"/>
      <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" fill="none" stroke="{glow}" stroke-width="1" opacity="0.5"/>
      
      <!-- Core Optic Eye & Scanning Iris -->
      <circle cx="0" cy="0" r="26" fill="#03070E" stroke="{color}" stroke-width="2"/>
      <circle cx="0" cy="0" r="14" fill="{glow}" opacity="0.85" class="packet_pulse"/>
      <circle cx="0" cy="0" r="5" fill="#FFFFFF"/>
      
      <!-- Dynamic Data Packet Nodes -->
      <circle cx="-160" cy="0" r="3" fill="{glow}" class="packet_pulse"/>
      <circle cx="160" cy="0" r="3" fill="{glow}" class="packet_pulse"/>
      <circle cx="0" cy="-85" r="3" fill="{glow}" class="packet_pulse"/>
      <circle cx="0" cy="85" r="3" fill="{glow}" class="packet_pulse"/>
    </g>
    """


# ---------------------------------------------------------------- logos


with open(os.path.join(SRC, "icons", "icons.json")) as f:
    LOGOS = json.load(f)


def _luma(color):
    r, g, b = (int(color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _readable(color, t):
    a, b = sorted((_luma(color), _luma(t["cell"])))
    return color if (b + 0.05) / (a + 0.05) >= 2.2 else t["fg"]


def logo(x, y, size, name, t, fallback=None):
    icon = LOGOS.get(name)
    k = size / 24
    if icon is None:
        return f'<circle cx="{x + size / 2}" cy="{y + size / 2}" r="{size / 3}" fill="{fallback or t["dim"]}"/>'
    if icon.get("kind") == "brand":
        return (
            f'<path transform="translate({x} {y}) scale({k:.3f})" fill="{_readable(icon["hex"], t)}" '
            f'd="{icon["path"]}"/>'
        )
    return (
        f'<g transform="translate({x} {y}) scale({k:.3f})" fill="none" stroke="{t["fg"]}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{icon.get("inner", "")}</g>'
    )


# ---------------------------------------------------------------- systems deck bento


def bento(mode, data):
    t = THEMES[mode]
    current, longest = streaks(data["days"])
    css = (
        ".bus_line{animation:bus_flow 2s linear infinite}"
        "@keyframes bus_flow{to{stroke-dashoffset:-32}}"
        ".packet_pulse{animation:pulse_glow 1.8s ease-in-out infinite alternate}"
        "@keyframes pulse_glow{from{opacity:0.3;transform:scale(0.85)}to{opacity:1;transform:scale(1.15)}}"
        ".beacon_live{animation:beacon 1.2s ease-in-out infinite alternate}"
        "@keyframes beacon{from{opacity:0.35}to{opacity:1}}"
        ".ring_spin{animation:r_spin 30s linear infinite;transform-origin:center}"
        "@keyframes r_spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}"
        ".rot{opacity:0;animation:rot 12s infinite}"
        "@keyframes rot{0%{opacity:0;transform:translateY(12px)}3%,22%{opacity:1;transform:none}25%,100%{opacity:0;transform:translateY(-12px)}}"
        ".grow{animation:grow 1.2s cubic-bezier(.2,.8,.2,1) .3s forwards;transform-box:fill-box;transform-origin:left}"
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".marq{animation:marq 26s linear infinite}@keyframes marq{to{transform:translateX(-50%)}}"
    )
    b = []

    # Section 1: Top Telemetry Ribbon (1280x68)
    b.append(chamfer_cell(0, 0, W, 68, t, c=12, brackets=True))
    b.append(f'<circle cx="28" cy="34" r="4.5" fill="{t["accent_bright"]}" class="beacon_live"/>')
    b.append(text(42, 40, "GITHUB TELEMETRY // SSHLOK TIWARI", 13, "MonoB", t["accent_bright"], spacing=".12em"))
    b.append(text(440, 40, f"CONTRIBUTIONS: {data['total']:,}", 13, "Mono", t["fg"]))
    b.append(text(740, 40, "BUILDING SINCE 2024", 13, "Mono", t["fg"]))
    b.append(text(1040, 40, f"PUBLIC REPOS: {data['repos']}", 13, "Mono", t["fg"]))

    # Section 2: Command Hero Deck (1280x360)
    y = 84
    b.append(chamfer_cell(0, y, W, 360, t, t["hero_bg"], c=16, brackets=True))
    b.append(cyber_core_hub(1020, y + 180, color=t["accent"], glow=t["accent_bright"], bg=t["cell"]))

    b.append(label(46, y + 42, "SOFTWARE ARCHITECTURE // DISTRIBUTED SYSTEMS", t))
    b.append(text(44, y + 140, "HEY, I'M SHLOK", 96, "Disp", t["fg"]))
    b.append(text(46, y + 192, "Systems Architect & Distributed Runtimes Engineer.", 21, "Mono", t["dim"]))
    
    # "I build" + rotating text with generous, fixed gap (zero overlap!)
    b.append(text(46, y + 248, "I build", 22, "MonoB", t["accent_bright"]))
    for i, s in enumerate(STATUS_LINES):
        b.append(f'<g class="rot" style="animation-delay:{i * 3}s">{text(168, y + 248, s, 22, "MonoB", t["fg"])}</g>')
    b.append(text(46, y + 314, "LOCATION: MUMBAI, INDIA · HIGH-PERFORMANCE RUNTIMES & AGENT INFRASTRUCTURE", 13, "Mono", t["dim"]))

    # Section 3: Midsection Deck (1280x320)
    y = 460
    # Left Console: Language Spectrum Matrix (w=626)
    b.append(chamfer_cell(0, y, 626, 320, t, c=14, brackets=True))
    b.append(label(34, y + 40, "REPOSITORY LANGUAGE SPECTRUM", t))
    langs = data["languages"][:6]
    total = sum(x[1] for x in langs) or 1
    bx, bar = 34, ""
    for name, size, color in langs:
        wdt = 558 * size / total
        bar += f'<rect x="{bx:.1f}" y="{y + 64}" width="{max(wdt - 2, 1):.1f}" height="14" rx="2" fill="{color}"/>'
        bx += wdt
    b.append(f'<g class="grow">{bar}</g>')
    for i, (name, size, color) in enumerate(langs):
        lx, ly = 34 + (i % 2) * 280, y + 104 + (i // 2) * 64
        b.append(
            logo(lx + 4, ly + 4, 30, name, t, color)
            + text(lx + 48, ly + 18, name, 17, "Mono", t["fg"])
            + text(lx + 48, ly + 38, f"{100 * size / total:.0f}%  ·  {size // 1024:,} KB", 13, "Mono", t["dim"])
        )

    # Right Console: Core Principles & Tech Stack (w=626)
    b.append(chamfer_cell(654, y, 626, 320, t, c=14, brackets=True))
    b.append(label(688, y + 40, "CORE PRINCIPLES & TECH STACK", t))
    b.append(text(686, y + 84, "SIMPLICITY IS PREREQUISITE FOR RELIABILITY.", 23, "Disp", t["fg"]))
    b.append(text(688, y + 112, "Edsger W. Dijkstra  ·  Core Discipline: LOCAL AI RUNTIMES", 13, "Mono", t["accent_bright"]))

    # Tech Stack Micro-Chips
    b.append(text(688, y + 158, "WHAT I BUILD WITH // CORE TOOLING", 12, "Mono", t["dim"]))
    x, yy = 688, y + 184
    for i, s in enumerate(STACK):
        wdt = 52 + len(s) * 10.5
        if x + wdt > 654 + 626 - 30:
            x, yy = 688, yy + 44
        b.append(
            chamfer_path(x, yy, wdt, 34, c=6)
            and f'<path d="{chamfer_path(x, yy, wdt, 34, c=6)}" fill="none" stroke="{t["edge"]}" stroke-width="1.2"/>'
            + logo(x + 10, yy + 7, 20, s, t)
            + text(x + 36, yy + 22, s, 15, "Mono", t["fg"])
        )
        x += wdt + 10

    # Section 4: Research & Contact Links (1280x92)
    y = 796
    b.append(chamfer_cell(0, y, 840, 92, t, c=12, brackets=True))
    b.append(label(30, y + 32, "RESEARCH & ENGINEERING FOCUS", t))
    b.append(f'<clipPath id="mq"><rect x="2" y="{y + 44}" width="836" height="40"/></clipPath>')
    line = "  ·  ".join(INTERESTS) + "  ·  "
    b.append(f'<g clip-path="url(#mq)"><g class="marq">' + text(30, y + 70, line + line, 20, "Mono", t["fg"]) + "</g></g>")

    b.append(chamfer_cell(860, y, 420, 92, t, c=12, brackets=True))
    b.append(label(884, y + 32, "GITHUB PROFILE // CONNECT", t))
    b.append(text(882, y + 70, "github.com/sshloktiwarii ↗", 23, "WM", t["accent_bright"]))

    return svg(904, "".join(b), css, title="Shlok Tiwari, Systems Architect")


# ---------------------------------------------------------------- activity heatmap


def activity(mode, data):
    t = THEMES[mode]
    levels = LEVELS if mode == "dark" else LEVELS_LIGHT
    days = data["days"][-371:]
    size, gap, x0, y0 = 18, 4, 30, 96
    first = dt.date.fromisoformat(days[0][0])
    offset = (first.weekday() + 1) % 7
    cells = []
    for i, (date, count, level) in enumerate(days):
        k = i + offset
        col, row = divmod(k, 7)
        x, y = x0 + col * (size + gap), y0 + row * (size + gap)
        fill = levels[level] or t["empty"]
        delay = (col + row) * 0.02
        cells.append(
            f'<rect class="d" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="{fill}">'
            f"<title>{count} on {date}</title></rect>"
        )
    css = (
        ".d{animation:in .4s ease-out forwards;transform-box:fill-box;transform-origin:center}"
        "@keyframes in{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:none}}"
        ".beacon_live{animation:beacon 1.2s ease-in-out infinite alternate}@keyframes beacon{from{opacity:0.35}to{opacity:1}}"
    )
    width = x0 * 2 + 53 * (size + gap)
    legend = "".join(
        f'<rect x="{width - 30 - (5 - i) * 24}" y="34" width="18" height="18" rx="3" fill="{levels[i] or t["empty"]}"/>'
        for i in range(5)
    )
    body = (
        chamfer_cell(0, 0, W, 280, t, c=14, brackets=True)
        + f'<circle cx="28" cy="42" r="4.5" fill="{t["accent_bright"]}" class="beacon_live"/>'
        + text(42, 48, f"ACTIVITY MATRIX // {data['total']:,} CONTRIBUTIONS IN THE LAST YEAR", 13, "MonoB", t["accent_bright"], spacing=".12em")
        + text(width - 160, 48, "less", 13, "Mono", t["dim"], "end")
        + legend
        + text(width - 22, 48, "more", 13, "Mono", t["dim"])
        + f'<g transform="translate({(W - width) / 2:.0f} 0)">{"".join(cells)}</g>'
        + text(
            30,
            268,
            "Sample data until the first refresh" if data["updated"] == "sample" else f"STATUS: LIVE TELEMETRY · UPDATED {data['updated']}",
            12,
            "Mono",
            t["dim"],
        )
    )
    return svg(296, body, css, title=f"{data['total']} contributions in the last year")


# ---------------------------------------------------------------- project icons & 2x3 cards

ICONS = {
    "semcache": (
        '<rect x="12" y="14" width="40" height="36" rx="4" stroke-width="2.5"/>'
        '<path d="M20 26h24M20 38h14" stroke-width="2.5"/>'
        '<g class="bolt"><path d="M42 28l-8 10h6l-2 10 10-12h-6z" fill="currentColor"/></g>',
        ".bolt{animation:pulse 1.8s ease-in-out infinite;transform-origin:38px 36px}@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.2)}}",
    ),
    "agentvault": (
        '<rect x="14" y="16" width="36" height="36" rx="4" stroke-width="2.5"/>'
        '<circle cx="32" cy="34" r="8" stroke-width="2.5"/>'
        '<g class="dial"><line x1="32" y1="34" x2="32" y2="28" stroke-width="2.5"/></g>',
        ".dial{animation:spin 4s linear infinite;transform-origin:32px 34px}@keyframes spin{to{transform:rotate(360deg)}}",
    ),
    "sentinel": (
        '<path d="M32 8L14 16v16c0 14 18 24 18 24s18-10 18-24V16L32 8z" stroke-width="2.5"/>'
        '<g class="sweep"><circle cx="32" cy="32" r="10" stroke-width="2"/><line x1="32" y1="32" x2="40" y2="24" stroke-width="2"/></g>',
        ".sweep{animation:spin 2.5s linear infinite;transform-origin:32px 32px}@keyframes spin{to{transform:rotate(360deg)}}",
    ),
    "aegis": (
        '<path d="M14 18h36v28a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4V18z" stroke-width="2.5"/>'
        '<path d="M22 18V12a10 10 0 0 1 20 0v6" stroke-width="2.5"/>'
        '<g class="lock"><circle cx="32" cy="32" r="3.5" fill="currentColor"/><line x1="32" y1="35" x2="32" y2="43" stroke-width="2.5"/></g>',
        ".lock{animation:nod 2s ease-in-out infinite}@keyframes nod{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}",
    ),
    "strata": (
        '<path d="M12 20l20-9 20 9-20 9z" stroke-width="2.5"/>'
        '<path class="l2" d="M12 32l20 9 20-9" stroke-width="2.5"/>'
        '<path class="l3" d="M12 44l20 9 20-9" stroke-width="2.5"/>',
        ".l2{animation:float 2.5s ease-in-out infinite alternate}@keyframes float{to{transform:translateY(-3px)}}"
        ".l3{animation:float 2.5s ease-in-out .5s infinite alternate}",
    ),
    "cortex": (
        '<circle cx="32" cy="32" r="15" stroke-width="2.5"/>'
        '<circle cx="32" cy="32" r="5" fill="currentColor"/>'
        '<g class="orbit"><circle cx="14" cy="32" r="3.5" fill="currentColor"/><circle cx="50" cy="32" r="3.5" fill="currentColor"/></g>',
        ".orbit{animation:orbit 3s ease-in-out infinite alternate;transform-origin:32px 32px}@keyframes orbit{to{transform:rotate(180deg)}}",
    ),
}


def wrap_line(s, limit=46):
    words = s.split()
    lines, cur = [], []
    for w in words:
        if sum(len(x) for x in cur) + len(cur) + len(w) <= limit:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def card(mode, p, data):
    t = THEMES[mode]
    draw, motion = ICONS[p["slug"]]
    stars = data["stars"].get(p["repo"]) if p["repo"] else None
    where = "repo ↗" if p["repo"] else "live ↗"
    meta = f"★ {stars}  ·  {where}" if stars else where
    idx = next((i + 1 for i, item in enumerate(PROJECTS) if item["slug"] == p["slug"]), 1)
    
    # 100% guaranteed 2-line wrapping with large readable typography
    desc_lines = wrap_line(p["line"], limit=46)
    desc_svg = (
        text(28, 156, desc_lines[0], 15.5, "Mono", t["fg"])
        + (text(28, 182, desc_lines[1], 15.5, "Mono", t["fg"]) if len(desc_lines) > 1 else "")
    )

    card_css = (
        motion
        + ".beacon_live{animation:beacon 1.2s ease-in-out infinite alternate}@keyframes beacon{from{opacity:0.35}to{opacity:1}}"
    )

    body = (
        chamfer_cell(0, 0, 620, 240, t, c=14, brackets=True)
        # Header Bar
        + text(28, 40, f"PROJECT 0{idx} // {p['tag'].upper()}", 13, "MonoB", t["accent_bright"], spacing=".12em")
        + f'<circle cx="450" cy="35" r="3.5" fill="{t["accent_bright"]}" class="beacon_live"/>'
        + text(462, 40, "ACTIVE", 12, "MonoB", t["accent_bright"])
        + text(592, 40, meta, 13, "Mono", t["dim"], "end")
        # Embedded Mechanical Icon
        + f'<path d="{chamfer_path(28, 56, 64, 64, c=8)}" fill="{t["accent_bright"]}"/>'
        + f'<g transform="translate(34 62) scale(0.85)" fill="none" stroke="{t["bg"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" color="{t["bg"]}">{draw}</g>'
        # Display Title - Large & Prominent
        + text(108, 112, p["name"].upper(), 52, "Disp", t["fg"])
        # 2-Line Wrapped Description
        + desc_svg
        # Tech Stack Tag
        + text(28, 216, p["stack"], 13.5, "Mono", t["dim"])
    )
    return svg(240, body, card_css, w=620, title=f'{p["name"]}: {p["line"]}')


def footer(mode):
    t = THEMES[mode]
    css = ".beacon_live{animation:beacon 1.2s ease-in-out infinite alternate}@keyframes beacon{from{opacity:0.35}to{opacity:1}}"
    body = (
        chamfer_cell(0, 0, W, 100, t, t["cell"], c=12, brackets=True)
        + f'<circle cx="34" cy="50" r="4.5" fill="{t["accent_bright"]}" class="beacon_live"/>'
        + text(50, 56, "SHLOK TIWARI // MUMBAI, INDIA", 14, "MonoB", t["accent_bright"], spacing=".12em")
        + text(W / 2, 58, "DISTRIBUTED SYSTEMS & LOCAL AI", 22, "Disp", t["fg"], "middle", spacing=".14em")
        + text(W - 40, 56, "Thanks for stopping by ↗", 14, "Mono", t["dim"], "end")
    )
    return svg(100, body, css, title="Shlok Tiwari")


def main():
    data = load()
    os.makedirs(ASSETS, exist_ok=True)
    out = {}
    for mode in THEMES:
        out[f"bento-{mode}.svg"] = bento(mode, data)
        out[f"activity-{mode}.svg"] = activity(mode, data)
        out[f"footer-{mode}.svg"] = footer(mode)
        for p in PROJECTS:
            out[f"project-{p['slug']}-{mode}.svg"] = card(mode, p, data)
    for name, s in out.items():
        with open(os.path.join(ASSETS, name), "w") as f:
            f.write(s)
    print(f"wrote {len(out)} images, data from {data['updated']}")


if __name__ == "__main__":
    main()
