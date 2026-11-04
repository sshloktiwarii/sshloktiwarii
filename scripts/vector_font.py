"""Vector font engine using fontTools.

Converts arbitrary text strings into exact SVG path commands (d="...")
without requiring client-side web fonts. Includes a comprehensive SYMBOLS
dictionary for mathematical, tech, and UI glyphs.
"""

from typing import Dict, Any, Tuple, Optional, Callable, NamedTuple
import math
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen


# ---------------------------------------------------------------------------
# Vector drawing helpers for normalized symbol glyphs (1000 UPM font space)
# Baseline is at y = 0, uppercase top around y = 700.
# ---------------------------------------------------------------------------

def _draw_star_5(pen: Any, cx: float = 350.0, cy: float = 350.0, r_out: float = 320.0, r_in: float = 135.0):
    """Draw a solid 5-pointed star."""
    pts = []
    # 10 alternating points starting at the top apex (angle = pi / 2)
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        angle = math.pi / 2.0 + i * (math.pi / 5.0)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_sparkle_4(pen: Any, cx: float = 350.0, cy: float = 350.0, r_out: float = 330.0, r_in: float = 65.0):
    """Draw a 4-pointed kinetic sparkle / twinkle star."""
    pts = []
    for i in range(8):
        r = r_out if i % 2 == 0 else r_in
        angle = math.pi / 2.0 + i * (math.pi / 4.0)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_arrow_ne(pen: Any):
    """Draw a clean, heavy north-east arrow (↗) at 45 degrees."""
    # Arrow head + shaft polygon in 700x700 box
    # Starts bottom-left, points top-right
    pts = [
        (220.0, 160.0),
        (280.0, 100.0),
        (540.0, 360.0),
        (540.0, 220.0),
        (640.0, 220.0),
        (640.0, 640.0),
        (220.0, 640.0),
        (220.0, 540.0),
        (360.0, 540.0),
        (100.0, 280.0),
        (160.0, 220.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_arrow_right(pen: Any):
    """Draw an arrow pointing right (→)."""
    pts = [
        (100.0, 390.0),
        (460.0, 390.0),
        (360.0, 500.0),
        (470.0, 500.0),
        (640.0, 350.0),
        (470.0, 200.0),
        (360.0, 200.0),
        (460.0, 310.0),
        (100.0, 310.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_arrow_left(pen: Any):
    """Draw an arrow pointing left (←)."""
    pts = [
        (600.0, 390.0),
        (240.0, 390.0),
        (340.0, 500.0),
        (230.0, 500.0),
        (60.0, 350.0),
        (230.0, 200.0),
        (340.0, 200.0),
        (240.0, 310.0),
        (600.0, 310.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_arrow_up(pen: Any):
    """Draw an arrow pointing up (↑)."""
    pts = [
        (310.0, 100.0),
        (390.0, 100.0),
        (390.0, 460.0),
        (500.0, 360.0),
        (500.0, 470.0),
        (350.0, 640.0),
        (200.0, 470.0),
        (200.0, 360.0),
        (310.0, 460.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_arrow_down(pen: Any):
    """Draw an arrow pointing down (↓)."""
    pts = [
        (310.0, 600.0),
        (390.0, 600.0),
        (390.0, 240.0),
        (500.0, 340.0),
        (500.0, 230.0),
        (350.0, 60.0),
        (200.0, 230.0),
        (200.0, 340.0),
        (310.0, 240.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_circle_bezier(pen: Any, cx: float, cy: float, r: float):
    """Draw a smooth circle using 4 cubic Béziers."""
    k = 0.5522847498 * r
    pen.moveTo((cx, cy + r))
    pen.curveTo((cx + k, cy + r), (cx + r, cy + k), (cx + r, cy))
    pen.curveTo((cx + r, cy - k), (cx + k, cy - r), (cx, cy - r))
    pen.curveTo((cx - k, cy - r), (cx - r, cy - k), (cx - r, cy))
    pen.curveTo((cx - r, cy + k), (cx - k, cy + r), (cx, cy + r))
    pen.closePath()


def _draw_bullet(pen: Any):
    """Draw a bullet point (•)."""
    _draw_circle_bezier(pen, cx=250.0, cy=350.0, r=130.0)


def _draw_lightning(pen: Any):
    """Draw high-voltage energy bolt (⚡)."""
    pts = [
        (400.0, 680.0),
        (160.0, 340.0),
        (330.0, 340.0),
        (240.0, 30.0),
        (580.0, 400.0),
        (390.0, 400.0),
        (530.0, 680.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_diamond(pen: Any):
    """Draw a solid diamond (◆)."""
    pts = [
        (350.0, 680.0),
        (660.0, 350.0),
        (350.0, 20.0),
        (40.0, 350.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_triangle_up(pen: Any):
    """Draw equilateral delta triangle up (▲)."""
    pts = [
        (350.0, 670.0),
        (660.0, 60.0),
        (40.0, 60.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_triangle_down(pen: Any):
    """Draw delta triangle down (▼)."""
    pts = [
        (40.0, 640.0),
        (660.0, 640.0),
        (350.0, 30.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_checkmark(pen: Any):
    """Draw a checkmark (✓)."""
    pts = [
        (130.0, 320.0),
        (280.0, 130.0),
        (630.0, 580.0),
        (550.0, 640.0),
        (270.0, 260.0),
        (190.0, 370.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_cross(pen: Any):
    """Draw a multi cross (✕)."""
    pts = [
        (160.0, 630.0),
        (350.0, 440.0),
        (540.0, 630.0),
        (630.0, 540.0),
        (440.0, 350.0),
        (630.0, 160.0),
        (540.0, 70.0),
        (350.0, 260.0),
        (160.0, 70.0),
        (70.0, 160.0),
        (260.0, 350.0),
        (70.0, 540.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_circle_ring(pen: Any):
    """Draw an open ring circle (○)."""
    # Outer clockwise circle
    _draw_circle_bezier(pen, cx=350.0, cy=350.0, r=300.0)
    # Inner hole
    _draw_circle_bezier(pen, cx=350.0, cy=350.0, r=210.0)


def _draw_circle_solid(pen: Any):
    """Draw a solid disk circle (●)."""
    _draw_circle_bezier(pen, cx=350.0, cy=350.0, r=290.0)


def _draw_lambda(pen: Any):
    """Draw Greek lambda (λ)."""
    pts = [
        (120.0, 0.0),
        (200.0, 0.0),
        (380.0, 400.0),
        (230.0, 690.0),
        (330.0, 690.0),
        (450.0, 450.0),
        (580.0, 0.0),
        (670.0, 0.0),
        (500.0, 540.0),
        (430.0, 690.0),
        (200.0, 690.0),
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def _draw_command(pen: Any):
    """Draw the ⌘ command key loop."""
    pts = [
        (220.0, 220.0), (220.0, 480.0), (480.0, 480.0), (480.0, 220.0),
    ]
    # Simple crisp geometric representation
    _draw_circle_bezier(pen, 200.0, 500.0, 120.0)
    _draw_circle_bezier(pen, 500.0, 500.0, 120.0)
    _draw_circle_bezier(pen, 500.0, 200.0, 120.0)
    _draw_circle_bezier(pen, 200.0, 200.0, 120.0)


def _draw_missing_box(pen: Any):
    """Draw a clean hollow rectangle for characters not found in font or symbols."""
    # Outer box
    pen.moveTo((100.0, 0.0))
    pen.lineTo((500.0, 0.0))
    pen.lineTo((500.0, 700.0))
    pen.lineTo((100.0, 700.0))
    pen.closePath()
    # Inner cutout
    pen.moveTo((160.0, 60.0))
    pen.lineTo((160.0, 640.0))
    pen.lineTo((440.0, 640.0))
    pen.lineTo((440.0, 60.0))
    pen.closePath()


# ---------------------------------------------------------------------------
# SYMBOLS catalog
# Maps Unicode symbols to advance width and drawing routine in 1000 UPM space.
# ---------------------------------------------------------------------------

SYMBOLS: Dict[str, Dict[str, Any]] = {
    "★": {"advance": 700, "draw": _draw_star_5},
    "*": {"advance": 700, "draw": _draw_star_5},
    "✦": {"advance": 700, "draw": _draw_sparkle_4},
    "✧": {"advance": 700, "draw": _draw_sparkle_4},
    "↗": {"advance": 700, "draw": _draw_arrow_ne},
    "->": {"advance": 700, "draw": _draw_arrow_right},
    "→": {"advance": 700, "draw": _draw_arrow_right},
    "<-": {"advance": 700, "draw": _draw_arrow_left},
    "←": {"advance": 700, "draw": _draw_arrow_left},
    "↑": {"advance": 700, "draw": _draw_arrow_up},
    "↓": {"advance": 700, "draw": _draw_arrow_down},
    "•": {"advance": 500, "draw": _draw_bullet},
    "·": {"advance": 500, "draw": _draw_bullet},
    "⚡": {"advance": 700, "draw": _draw_lightning},
    "◆": {"advance": 700, "draw": _draw_diamond},
    "◇": {"advance": 700, "draw": _draw_diamond},
    "▲": {"advance": 700, "draw": _draw_triangle_up},
    "▼": {"advance": 700, "draw": _draw_triangle_down},
    "✓": {"advance": 700, "draw": _draw_checkmark},
    "✔": {"advance": 700, "draw": _draw_checkmark},
    "✕": {"advance": 700, "draw": _draw_cross},
    "✖": {"advance": 700, "draw": _draw_cross},
    "λ": {"advance": 700, "draw": _draw_lambda},
    "○": {"advance": 700, "draw": _draw_circle_ring},
    "●": {"advance": 700, "draw": _draw_circle_solid},
    "⌘": {"advance": 700, "draw": _draw_command},
    "missing": {"advance": 600, "draw": _draw_missing_box},
}


class TextMetrics(NamedTuple):
    width: float
    height: float
    ascent: float
    descent: float
    cap_height: float


class Face:
    """Vector typography engine powered by fontTools.

    Converts strings into exact SVG path definitions using font glyph outlines
    and fallback symbols.
    """

    def __init__(self, font_path: str):
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        self.font_path = font_path
        self.font = TTFont(font_path)
        self.glyph_set = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap() or {}
        self.h_metrics = self.font["hmtx"].metrics
        self.units_per_em = float(self.font["head"].unitsPerEm)

        hhea = self.font.get("hhea")
        self.ascent = float(hhea.ascent if hhea else 800)
        self.descent = float(hhea.descent if hhea else -200)

        os2 = self.font.get("OS/2")
        if os2 and hasattr(os2, "sCapHeight") and os2.sCapHeight > 0:
            self.cap_height = float(os2.sCapHeight)
        else:
            self.cap_height = float(self.ascent * 0.72)

        # Determine space advance width
        space_name = self.cmap.get(32) or self.cmap.get(ord(" "))
        if space_name and space_name in self.h_metrics:
            self.space_advance = float(self.h_metrics[space_name][0])
        else:
            self.space_advance = float(self.units_per_em * 0.5)

    def has_char(self, char: str) -> bool:
        """Check if character is supported either by font or by SYMBOLS."""
        return (char in SYMBOLS) or (ord(char) in self.cmap)

    def measure_text(self, text: str, size: float = 16.0, letter_spacing: float = 0.0) -> TextMetrics:
        """Compute bounding metrics for a given text string at specified size."""
        scale = size / self.units_per_em
        total_width = 0.0

        for idx, ch in enumerate(text):
            if ch == " ":
                char_w = self.space_advance * scale
            elif ch in SYMBOLS:
                char_w = SYMBOLS[ch]["advance"] * (size / 1000.0)
            elif ord(ch) in self.cmap:
                g_name = self.cmap[ord(ch)]
                char_w = self.h_metrics[g_name][0] * scale
            else:
                char_w = SYMBOLS["missing"]["advance"] * (size / 1000.0)

            total_width += char_w
            if idx < len(text) - 1:
                total_width += letter_spacing

        return TextMetrics(
            width=round(total_width, 3),
            height=round((self.ascent - self.descent) * scale, 3),
            ascent=round(self.ascent * scale, 3),
            descent=round(self.descent * scale, 3),
            cap_height=round(self.cap_height * scale, 3),
        )

    def text_path(
        self,
        text: str,
        size: float = 16.0,
        x: float = 0.0,
        y: float = 0.0,
        letter_spacing: float = 0.0,
        align: str = "left",
        baseline: str = "alphabetic",
    ) -> str:
        """Convert a text string into an SVG path data string (d="...").

        Args:
            text: Arbitrary string (supports Unicode symbols in SYMBOLS).
            size: Font size in SVG pixels.
            x: Target X position.
            y: Target Y position.
            letter_spacing: Additional spacing between characters in SVG pixels.
            align: 'left', 'center', or 'right'.
            baseline: 'alphabetic' (y = baseline), 'middle'/'central' (y = cap center),
                      'top' (y = top of ascent), 'bottom' (y = descent).

        Returns:
            SVG path data string (e.g. 'M... C... Z').
        """
        if not text:
            return ""

        scale = size / self.units_per_em
        metrics = self.measure_text(text, size=size, letter_spacing=letter_spacing)

        # Horizontal alignment
        if align == "center":
            cur_x = x - (metrics.width / 2.0)
        elif align == "right":
            cur_x = x - metrics.width
        else:
            cur_x = x

        # Vertical baseline adjustment (SVG y goes downward; font y goes upward)
        if baseline in ("middle", "central"):
            base_y = y + (metrics.cap_height / 2.0)
        elif baseline == "top":
            base_y = y + metrics.ascent
        elif baseline == "bottom":
            base_y = y + metrics.descent
        else:  # alphabetic
            base_y = y

        pen = SVGPathPen(self.glyph_set)

        for idx, ch in enumerate(text):
            if ch == " ":
                cur_x += self.space_advance * scale + letter_spacing
                continue

            if ch in SYMBOLS:
                sym = SYMBOLS[ch]
                sym_scale = size / 1000.0
                # Affine transform: scale x, flip y, translate to (cur_x, base_y)
                t_pen = TransformPen(pen, (sym_scale, 0.0, 0.0, -sym_scale, cur_x, base_y))
                sym["draw"](t_pen)
                cur_x += sym["advance"] * sym_scale + letter_spacing
                continue

            code = ord(ch)
            if code in self.cmap:
                glyph_name = self.cmap[code]
                glyph = self.glyph_set[glyph_name]
                t_pen = TransformPen(pen, (scale, 0.0, 0.0, -scale, cur_x, base_y))
                glyph.draw(t_pen)
                cur_x += self.h_metrics[glyph_name][0] * scale + letter_spacing
            else:
                # Missing glyph fallback
                sym = SYMBOLS["missing"]
                sym_scale = size / 1000.0
                t_pen = TransformPen(pen, (sym_scale, 0.0, 0.0, -sym_scale, cur_x, base_y))
                sym["draw"](t_pen)
                cur_x += sym["advance"] * sym_scale + letter_spacing

        return pen.getCommands().strip()

    def svg_path_tag(
        self,
        text: str,
        size: float = 16.0,
        x: float = 0.0,
        y: float = 0.0,
        fill: str = "#EAEFF7",
        letter_spacing: float = 0.0,
        align: str = "left",
        baseline: str = "alphabetic",
        extra_attrs: str = "",
    ) -> str:
        """Convenience method returning a complete SVG <path ... /> element."""
        d = self.text_path(
            text=text,
            size=size,
            x=x,
            y=y,
            letter_spacing=letter_spacing,
            align=align,
            baseline=baseline,
        )
        if not d:
            return ""
        extra = f" {extra_attrs.strip()}" if extra_attrs.strip() else ""
        return f'<path d="{d}" fill="{fill}"{extra} />'
