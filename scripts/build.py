"""
High-End Vector SVG Profile Generator for Shlok Tiwari (sshloktiwarii)
Inspired by harsh4k/harsh4k:
- 100% Vector outline typography via fontTools Face (Audiowide, BigShouldersDisplay, IBMPlexMono)
- Live GitHub GraphQL integration (contributions, real languages, stars)
- High-contrast, High-Impact Cyber-Telemetry Bento Grid:
  * Enlarged blocks & typography (bold, crisp, clean, no generic pill borders)
  * Animated bobbing vector mascot + rotating status lines + animated wave mesh
  * Philosophy card with animated gradient sweep
  * Live GitHub telemetry with animated Pop-in counters
  * Language graph with smooth SVG animated grow bars & brand logos
  * Tech stack grid with official SVG brand icons
  * Off the clock marquee animation
  * 6 Animated Flagship Project Cards with unique kinetic SVG icons
"""

import datetime as dt
import html
import json
import math
import os
import re
import urllib.request
import subprocess

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
ASSETS = os.path.join(ROOT, "assets")
DATA = os.path.join(ASSETS, "github.json")
USER = "sshloktiwarii"

# Signature Brand Colors
OLIVE_ACCENT = "#8A9A5B"
OLIVE_GLOW = "#B4C97F"
CHROME_HERO = "#0E1D33"
NAVY_DEEP = "#070B14"
CREAM = "#F0F4FA"
W = 1280

THEMES = {
    "dark": dict(
        bg="#070B14",
        cell="#0D1424",
        fg="#E6ECF5",
        dim="#7E8C9F",
        edge="#1E2A3E",
        empty="#121A2A",
        hero_bg="#0E1E35",
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
        hero_bg="#E2EAF4",
        accent="#55692A",
        accent_bright="#708736",
    ),
}

# GitHub's 0-4 activity levels in Olive Green
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
        tag="Performance Engine",
        stack="Python · Vector Cosine · In-Memory Cache",
    ),
    dict(
        slug="agentvault",
        name="AgentVault",
        repo="AgentVault",
        url="https://github.com/sshloktiwarii/AgentVault",
        line="A black-box flight recorder that tracks every move your AI agents make in real time.",
        tag="Security & Audit",
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
        tag="Agent Security",
        stack="Rust · Landlock · Apple Seatbelt · AST Sanitizer",
    ),
    dict(
        slug="strata",
        name="Strata",
        repo="strata",
        url="https://github.com/sshloktiwarii/strata",
        line="A control center that runs and organizes large fleets of autonomous AI workers.",
        tag="Fleet Orchestration",
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

STACK = ["Rust", "Go", "Python", "TypeScript", "C++", "Linux", "Docker", "SQLite", "Redis", "React", "Next.js", "Node.js"]
INTERESTS = [
    "distributed systems",
    "systems engineering",
    "local-first AI",
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


def graphql(query, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": USER},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def refresh(token):
    q = """{ user(login: "%s") {
      contributionsCollection { contributionCalendar { totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } } } }
      repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) { totalCount
        nodes { name stargazerCount
          languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } } } } }""" % USER
    user = graphql(q, token)["user"]
    level = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [
        [d["date"], d["contributionCount"], level[d["contributionLevel"]]]
        for w in cal["weeks"]
        for d in w["contributionDays"]
    ]
    langs, stars = {}, {}
    for r in user["repositories"]["nodes"]:
        stars[r["name"]] = r["stargazerCount"]
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs.setdefault(n, [0, e["node"]["color"] or "#888"])[0] += e["size"]
    data = dict(
        updated=dt.date.today().isoformat(),
        total=cal["totalContributions"],
        days=days,
        repos=user["repositories"]["totalCount"],
        stars=stars,
        languages=sorted(([k, v[0], v[1]] for k, v in langs.items()), key=lambda x: -x[1]),
    )
    with open(DATA, "w") as f:
        json.dump(data, f, indent=1)
    return data


def load():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        try:
            token = subprocess.check_output(["gh", "auth", "token"]).decode().strip()
        except Exception:
            token = None
    if token:
        try:
            return refresh(token)
        except Exception as error:
            if os.environ.get("CI"):
                raise
            print(f"refresh failed, drawing from saved data: {error}")
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


def esc(s):
    return html.escape(str(s))


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


def cell(x, y, w, h, t, fill=None):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill or t["cell"]}" '
        f'stroke="{t["edge"] if not fill else fill}" stroke-width="1.5"/>'
    )


def label(x, y, s, t):
    return text(x, y, s.upper(), 14, fill=t["dim"], spacing=".16em")


# ---------------------------------------------------------------- mascot & terrain


def face(x, y, size):
    """Interactive winking mascot face with idle breathing & wink keyframes."""
    def inner(name, suffix):
        with open(os.path.join(SRC, "faces", name)) as f:
            s = f.read()
        s = re.sub(r"^<svg[^>]*>", "", s).rsplit("</svg>", 1)[0]
        s = re.sub(r"<title>.*?</title>", "", s)
        return s.replace('id="ink"', f'id="ink{suffix}"').replace("url(#ink)", f"url(#ink{suffix})")

    box = f'x="{x}" y="{y}" width="{size}" height="{size}" viewBox="400 330 640 640"'
    return (
        f'<g class="bob"><svg {box} class="open">{inner("face.svg", "a")}</svg>'
        f'<svg {box} class="wink">{inner("face-wink.svg", "b")}</svg></g>'
    )


FACE_CSS = (
    ".wink{opacity:0;animation:wink 5s infinite}.open{animation:open 5s infinite}"
    "@keyframes wink{0%,86%,96%,100%{opacity:0}88%,94%{opacity:1}}"
    "@keyframes open{0%,86%,96%,100%{opacity:1}88%,94%{opacity:0}}"
    ".bob{animation:bob 4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}"
    "@keyframes bob{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-6px) rotate(3deg)}}"
)


def terrain(w, h, y0, rows=14, cols=48, amp=32, color=OLIVE_ACCENT, opacity=0.45):
    """Procedural wireframe terrain contours."""
    out = []
    for r in range(rows):
        z = 1 + r * 0.55
        pts = []
        for c in range(cols + 1):
            u = c / cols * 2 - 1
            x3 = u * 9
            hgt = (
                math.sin(x3 * 0.9 + r * 0.45) * 0.6
                + math.sin(x3 * 0.37 - r * 0.8) * 0.8
                + math.cos(x3 * 1.7 + r * 0.3) * 0.25
            )
            px = w / 2 + (u * w * 1.1) / (z * 0.35 + 0.65)
            py = y0 + (h - y0) * (1 - 1 / z) * 1.25 - hgt * math.exp(-((u * 1.4) ** 2)) * amp / z
            pts.append(f"{px:.1f},{py:.1f}")
        out.append(
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" '
            f'stroke-width="{1.5 / (1 + r * 0.08):.2f}" opacity="{opacity * (1 - r / rows * 0.75):.2f}"/>'
        )
    return f'<g class="drift">{"".join(out)}</g>'


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


# ---------------------------------------------------------------- hero bento


def bento(mode, data):
    t = THEMES[mode]
    current, longest = streaks(data["days"])
    css = (
        FACE_CSS
        + ".drift{animation:drift 9s ease-in-out infinite alternate}"
        "@keyframes drift{from{transform:translateX(-30px)}to{transform:translateX(30px)}}"
        ".rot{opacity:0;animation:rot 12s infinite}"
        "@keyframes rot{0%{opacity:0;transform:translateY(14px)}3%,22%{opacity:1;transform:none}25%,100%{opacity:0;transform:translateY(-14px)}}"
        ".pop{opacity:0;animation:pop .6s ease-out forwards;transform-box:fill-box;transform-origin:left center}"
        "@keyframes pop{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
        ".grow{transform:scaleX(0);transform-box:fill-box;transform-origin:left;animation:grow 1.2s cubic-bezier(.2,.8,.2,1) .3s forwards}"
        "@keyframes grow{to{transform:scaleX(1)}}"
        ".shine{animation:shine 3.5s ease-in-out infinite}"
        "@keyframes shine{0%,60%{transform:translateX(-300px)}100%{transform:translateX(420px)}}"
        ".marq{animation:marq 26s linear infinite}@keyframes marq{to{transform:translateX(-50%)}}"
    )
    b = []

    # Card 1: Hero Identity (Hero card with Mascot + Procedural Terrain + Animated rotating status)
    b.append(cell(0, 0, 820, 400, t, t["hero_bg"]))
    b.append('<clipPath id="hero"><rect width="820" height="400" rx="22"/></clipPath>')
    b.append(f'<g clip-path="url(#hero)">{terrain(820, 400, 220, color=t["accent"])}</g>')
    b.append(face(36, 32, 132))
    b.append(text(40, 248, "HEY, I'M SHLOK", 104, "Disp", t["fg"]))
    b.append(text(42, 298, "Systems Architect & Distributed Runtimes Engineer.", 22, "Mono", t["dim"]))
    b.append(text(42, 352, "I build", 22, "MonoB", t["accent_bright"]))
    for i, s in enumerate(STATUS_LINES):
        b.append(f'<g class="rot" style="animation-delay:{i * 3}s">{text(152, 352, s, 22, "MonoB", t["fg"])}</g>')

    # Card 2: Principles / Philosophy Card
    b.append(cell(840, 0, 440, 190, t))
    b.append(label(870, 42, "WORDS I CODE BY", t))
    b.append(text(868, 96, "SIMPLICITY IS PREREQUISITE", 33, "Disp", t["fg"]))
    b.append(text(868, 138, "FOR RELIABILITY.", 33, "Disp", t["accent_bright"]))
    b.append(text(870, 172, "Edsger W. Dijkstra", 16, "Mono", t["dim"]))

    # Card 3: Special Achievement / Focus Card
    b.append(cell(840, 210, 440, 190, t))
    b.append('<clipPath id="hk"><rect x="840" y="210" width="440" height="190" rx="22"/></clipPath>')
    b.append(
        f'<g clip-path="url(#hk)"><rect class="shine" x="840" y="210" width="100" height="190" fill="{t["accent_bright"]}" opacity=".15" transform="skewX(-20)"/></g>'
    )
    b.append(label(870, 252, "CORE DISCIPLINE", t))
    b.append(text(866, 336, "LOCAL AI", 80, "Disp", t["accent_bright"]))
    b.append(text(1130, 336, "runtimes", 22, "Mono", t["dim"]))

    # Row 2: Live Numbers | Languages in repos | Focus area
    y = 420
    b.append(cell(0, y, 410, 300, t))
    b.append(label(30, y + 42, "On GitHub", t))
    stats = [
        (data["total"], "contributions this year"),
        (current, "day streak now"),
        (longest, "day best streak"),
        (data["repos"], "public repositories"),
    ]
    for i, (n, what) in enumerate(stats):
        yy = y + 100 + i * 56
        b.append(
            f'<g class="pop" style="animation-delay:{.15 * i:.2f}s">'
            + text(30, yy, f"{n:,}", 44, "Disp", t["accent_bright"] if i == 0 else t["fg"])
            + text(150, yy - 6, what, 18, "Mono", t["dim"])
            + "</g>"
        )

    # Real Language Breakdown from user repositories (Animated growing multi-color bar + logos)
    b.append(cell(430, y, 430, 300, t))
    b.append(label(460, y + 42, "Languages in my repos", t))
    langs = data["languages"][:6]
    total = sum(x[1] for x in langs) or 1
    bx, bar = 460, ""
    for name, size, color in langs:
        wdt = 370 * size / total
        bar += f'<rect x="{bx:.1f}" y="{y + 66}" width="{max(wdt - 3, 1):.1f}" height="16" rx="3" fill="{color}"/>'
        bx += wdt
    b.append(f'<g class="grow">{bar}</g>')
    for i, (name, size, color) in enumerate(langs):
        lx, ly = 460 + (i % 2) * 190, y + 106 + (i // 2) * 60
        b.append(
            f'<g class="pop" style="animation-delay:{.6 + .1 * i:.2f}s">'
            + logo(lx + 4, ly + 4, 34, name, t, color)
            + text(lx + 54, ly + 19, name, 18, "Mono", t["fg"])
            + text(lx + 54, ly + 40, f"{100 * size / total:.0f}%", 14, "Mono", t["dim"])
            + "</g>"
        )

    # Architectural Spec Card
    b.append(cell(880, y, 400, 300, t))
    b.append(label(910, y + 42, "SYSTEM ARCHITECTURE", t))
    b.append(text(908, y + 110, "AUTONOMOUS", 48, "Disp", t["fg"]))
    b.append(text(908, y + 154, "AGENT RUNTIMES", 48, "Disp", t["accent_bright"]))
    b.append(text(910, y + 204, "Sub-16ms telemetry, SQLite WAL", 16, "Mono", t["dim"]))
    b.append(text(910, y + 232, "storage & high-resilience kernels", 16, "Mono", t["dim"]))

    # Row 3: Tech Stack Chips (Clean modern chips with official brand SVG icons)
    y = 740
    b.append(cell(0, y, W, 170, t))
    b.append(label(30, y + 42, "What I build with", t))
    x, yy = 30, y + 70
    for i, s in enumerate(STACK):
        wdt = 58 + len(s) * 11.2
        if x + wdt > W - 30:
            x, yy = 30, yy + 52
        b.append(
            f'<g class="pop" style="animation-delay:{.08 * i:.2f}s">'
            f'<rect x="{x}" y="{yy}" width="{wdt}" height="40" rx="12" fill="none" stroke="{t["edge"]}" stroke-width="1.5"/>'
            + logo(x + 14, yy + 10, 20, s, t)
            + text(x + 42, yy + 26, s, 17, "Mono", t["fg"])
            + "</g>"
        )
        x += wdt + 12

    # Row 4: Interests Marquee + Portfolio / Contact Banner
    y = 930
    b.append(cell(0, y, 820, 150, t))
    b.append(label(30, y + 42, "Off the clock & deep research", t))
    b.append(f'<clipPath id="mq"><rect x="1" y="{y + 60}" width="818" height="60"/></clipPath>')
    line = "  ·  ".join(INTERESTS) + "  ·  "
    b.append(f'<g clip-path="url(#mq)"><g class="marq">' + text(30, y + 102, line + line, 24, "Mono", t["fg"]) + "</g></g>")

    b.append(cell(840, y, 440, 150, t))
    b.append(label(870, y + 42, "GitHub Profile", t))
    b.append(text(868, y + 104, "github.com/sshloktiwarii ↗", 26, "WM", t["accent_bright"]))

    return svg(1096, "".join(b), css, title="Shlok Tiwari, Systems Architect")


# ---------------------------------------------------------------- activity heatmap (CLEAN, NO PILLS)


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
            f'<rect class="d" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" width="{size}" height="{size}" rx="4" fill="{fill}">'
            f"<title>{count} on {date}</title></rect>"
        )
    css = (
        ".d{opacity:0;animation:in .4s ease-out forwards;transform-box:fill-box;transform-origin:center}"
        "@keyframes in{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:none}}"
    )
    width = x0 * 2 + 53 * (size + gap)
    legend = "".join(
        f'<rect x="{width - 30 - (5 - i) * 24}" y="34" width="18" height="18" rx="4" fill="{levels[i] or t["empty"]}"/>'
        for i in range(5)
    )
    # Pure clean header with zero pill boxes
    body = (
        cell(0, 0, W, 280, t)
        + label(30, 48, f"{data['total']:,} contributions in the last year", t)
        + text(width - 160, 48, "less", 13, "Mono", t["dim"], "end")
        + legend
        + text(width - 22, 48, "more", 13, "Mono", t["dim"])
        + f'<g transform="translate({(W - width) / 2:.0f} 0)">{"".join(cells)}</g>'
        + text(
            30,
            268,
            "Sample data until the first refresh" if data["updated"] == "sample" else f"Updated {data['updated']}",
            12,
            "Mono",
            t["dim"],
        )
    )
    return svg(296, body, css, title=f"{data['total']} contributions in the last year")


# ---------------------------------------------------------------- project icons & cards (6 BEST PROJECTS)

ICONS = {
    # Custom animated kinetic vector icons tailored for Shlok's systems
    "semcache": (
        '<rect x="12" y="14" width="40" height="36" rx="8" stroke-width="3"/>'
        '<path d="M20 26h24M20 38h14" stroke-width="3"/>'
        '<g class="bolt"><path d="M42 28l-8 10h6l-2 10 10-12h-6z" fill="currentColor"/></g>',
        ".bolt{animation:pulse 1.8s ease-in-out infinite;transform-origin:38px 36px}@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.25)}}",
    ),
    "agentvault": (
        '<rect x="14" y="16" width="36" height="36" rx="6" stroke-width="3"/>'
        '<circle cx="32" cy="34" r="8" stroke-width="3"/>'
        '<g class="dial"><line x1="32" y1="34" x2="32" y2="28" stroke-width="3"/></g>',
        ".dial{animation:spin 4s linear infinite;transform-origin:32px 34px}@keyframes spin{to{transform:rotate(360deg)}}",
    ),
    "sentinel": (
        '<path d="M32 8L14 16v16c0 14 18 24 18 24s18-10 18-24V16L32 8z" stroke-width="3"/>'
        '<g class="sweep"><circle cx="32" cy="32" r="10" stroke-width="2"/><line x1="32" y1="32" x2="40" y2="24" stroke-width="2.5"/></g>',
        ".sweep{animation:spin 2.5s linear infinite;transform-origin:32px 32px}@keyframes spin{to{transform:rotate(360deg)}}",
    ),
    "aegis": (
        '<path d="M12 18h40v30a6 6 0 0 1-6 6H18a6 6 0 0 1-6-6V18z" stroke-width="3"/>'
        '<path d="M22 18V12a10 10 0 0 1 20 0v6" stroke-width="3"/>'
        '<g class="lock"><circle cx="32" cy="32" r="4" fill="currentColor"/><line x1="32" y1="36" x2="32" y2="44" stroke-width="3"/></g>',
        ".lock{animation:nod 2s ease-in-out infinite}@keyframes nod{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}",
    ),
    "strata": (
        '<path d="M10 20l22-10 22 10-22 10z" stroke-width="3"/>'
        '<path class="l2" d="M10 32l22 10 22-10" stroke-width="3"/>'
        '<path class="l3" d="M10 44l22 10 22-10" stroke-width="3"/>',
        ".l2{animation:float 2.5s ease-in-out infinite alternate}@keyframes float{to{transform:translateY(-3px)}}"
        ".l3{animation:float 2.5s ease-in-out .5s infinite alternate}",
    ),
    "cortex": (
        '<circle cx="32" cy="32" r="16" stroke-width="3"/>'
        '<circle cx="32" cy="32" r="6" fill="currentColor"/>'
        '<g class="orbit"><circle cx="12" cy="32" r="4" fill="currentColor"/><circle cx="52" cy="32" r="4" fill="currentColor"/></g>',
        ".orbit{animation:orbit 3s ease-in-out infinite alternate;transform-origin:32px 32px}@keyframes orbit{to{transform:rotate(180deg)}}",
    ),
}


def card(mode, p, data):
    t = THEMES[mode]
    draw, motion = ICONS[p["slug"]]
    stars = data["stars"].get(p["repo"]) if p["repo"] else None
    where = "repo ↗" if p["repo"] else "live ↗"
    meta = f"★ {stars}  ·  {where}" if stars else where
    body = (
        cell(1, 1, 618, 228, t)
        + f'<rect x="28" y="28" width="104" height="104" rx="24" fill="{t["accent_bright"]}"/>'
        + f'<g transform="translate(40 40) scale(1.25)" fill="none" stroke="{t["bg"]}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round" color="{t["bg"]}">{draw}</g>'
        + text(156, 62, p["tag"].upper(), 14, "Mono", t["accent_bright"], spacing=".14em")
        + text(154, 118, p["name"].upper(), 56, "Disp", t["fg"])
        + text(30, 174, p["line"], 17, "Mono", t["fg"])
        + text(30, 206, p["stack"], 14, "Mono", t["dim"])
        + text(590, 206, meta, 14, "Mono", t["dim"], "end")
    )
    return svg(244, body, motion, w=620, title=f'{p["name"]}: {p["line"]}')


def footer(mode):
    t = THEMES[mode]
    body = (
        cell(0, 0, W, 120, t, t["cell"])
        + face(40, 14, 92)
        + text(W / 2, 74, "SHLOK TIWARI", 34, "WM", t["accent_bright"], "middle", spacing=".12em")
        + text(W - 40, 72, "thanks for stopping by", 16, "Mono", t["dim"], "end")
    )
    return svg(120, body, FACE_CSS, title="Shlok Tiwari")


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
