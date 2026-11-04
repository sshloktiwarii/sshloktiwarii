"""Procedural Liquid Chrome Wave & Mesh Generator.

Generates multi-layered undulating sinusoidal ribbons resembling flowing
liquid metal and mercury with specular highlights, multi-angle reflection
gradients, and subtle drift/shimmer animations.
"""

from typing import List, Tuple, Dict, Any, Optional
import math
import random
from palette import PALETTES, get_palette


def _points_to_cubic_bezier(points: List[Tuple[float, float]]) -> str:
    """Convert an ordered list of 2D points into smooth cubic Bézier segments (Catmull-Rom spline)."""
    if len(points) < 2:
        return ""
    segs = []
    n = len(points)
    for i in range(n - 1):
        p0 = points[max(i - 1, 0)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(i + 2, n - 1)]

        # Tension factor 0.5 for fluid curvature
        cp1x = p1[0] + (p2[0] - p0[0]) / 6.0
        cp1y = p1[1] + (p2[1] - p0[1]) / 6.0
        cp2x = p2[0] - (p3[0] - p1[0]) / 6.0
        cp2y = p2[1] - (p3[1] - p1[1]) / 6.0
        segs.append(f"C {cp1x:.2f} {cp1y:.2f}, {cp2x:.2f} {cp2y:.2f}, {p2[0]:.2f} {p2[1]:.2f}")
    return " ".join(segs)


def _generate_ribbon_geometry(
    w: float,
    h: float,
    y_center: float,
    amplitude: float,
    freq: float,
    phase: float,
    thickness: float,
    samples: int = 48,
    rng: Optional[random.Random] = None,
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
    """Generate top and bottom coordinates for a single sinusoidal liquid ribbon."""
    if rng is None:
        rng = random.Random(0)

    p2 = phase * 1.414 + 0.3
    p3 = phase * 0.718 - 0.5
    f2 = freq * 1.95
    f3 = freq * 3.12

    pts_top: List[Tuple[float, float]] = []
    pts_bot: List[Tuple[float, float]] = []

    dx = w / float(samples - 1)
    for i in range(samples):
        x = i * dx
        norm_x = x / w

        # Sum of 3 sinusoidal harmonics for fluid non-repeating viscosity
        h1 = math.sin(norm_x * freq * 2.0 * math.pi + phase)
        h2 = 0.32 * math.cos(norm_x * f2 * 2.0 * math.pi + p2)
        h3 = 0.12 * math.sin(norm_x * f3 * 2.0 * math.pi + p3)
        y_mid = y_center + amplitude * (h1 + h2 + h3)

        # Dynamic thickness modulation (bulges and tapers)
        t_mod = 0.75 + 0.35 * math.sin(norm_x * 3.5 * math.pi + phase)
        t = thickness * t_mod

        # Extend slightly past bounds (-4 to w + 4) for seamless clipping
        pts_top.append((round(x, 2), round(y_mid - t / 2.0, 2)))
        pts_bot.append((round(x, 2), round(y_mid + t / 2.0, 2)))

    return pts_top, pts_bot


def liquid_chrome_mesh(
    w: float = 1200.0,
    h: float = 400.0,
    ribbons: int = 6,
    palette_name: str = "dark",
    mesh_id: str = "liquid_chrome",
    animated: bool = True,
    drift_duration: float = 14.0,
    seed: int = 42,
    samples: int = 50,
    show_grid: bool = False,
    as_svg: bool = False,
    opacity: float = 1.0,
) -> str:
    """Generate layered undulating sinusoidal ribbons resembling liquid chrome.

    Uses specular highlight stops:
        #FFFFFF (specular spike)
        #D2D9E5 (bright silver)
        #8A98A8 (chrome steel)
        #2E3A4B (dark gunmetal reflection)
        #121A29 (deep abyss reflection)
    Accompanied by subtle olive rim-lighting (#B4C97F) and animated drift.

    Args:
        w: Canvas width in pixels.
        h: Canvas height in pixels.
        ribbons: Number of undulating ribbon layers (default 6).
        palette_name: 'dark' or 'light'.
        mesh_id: Prefix for gradient/filter IDs and CSS classes.
        animated: Enable CSS drift keyframes and SVG shimmer animations.
        drift_duration: Cycle time in seconds for the undulating drift.
        seed: Random seed for deterministic procedural generation.
        samples: Number of horizontal spline samples per ribbon.
        show_grid: Include precision milled background grid.
        as_svg: Wrap output in an outer <svg> element.
        opacity: Master group opacity multiplier.

    Returns:
        SVG string (<g> group or <svg> element).
    """
    pal = get_palette(palette_name)
    rng = random.Random(seed)

    defs: List[str] = []
    elements: List[str] = []

    # 1. Background Grid (optional milled silver guide lines)
    if show_grid:
        grid_id = f"{mesh_id}_grid_pat"
        grid_step = 40.0
        defs.append(f"""
    <pattern id="{grid_id}" width="{grid_step}" height="{grid_step}" patternUnits="userSpaceOnUse">
      <path d="M {grid_step} 0 L 0 0 0 {grid_step}" fill="none" stroke="{pal['edge']}" stroke-width="0.5" stroke-opacity="0.25" />
    </pattern>""")
        elements.append(f'<rect width="{w}" height="{h}" fill="url(#{grid_id})" />')

    # 2. Specular Liquid Chrome Linear Gradients
    # Standard stops specified in requirements
    spec_stops = [
        {"offset": "0%",   "color": "#121A29", "opacity": 0.95},
        {"offset": "16%",  "color": "#2E3A4B", "opacity": 0.95},
        {"offset": "38%",  "color": "#8A98A8", "opacity": 1.0},
        {"offset": "56%",  "color": "#D2D9E5", "opacity": 1.0},
        {"offset": "68%",  "color": "#FFFFFF", "opacity": 1.0},  # Liquid specular spike
        {"offset": "78%",  "color": "#D2D9E5", "opacity": 1.0},
        {"offset": "88%",  "color": "#8A98A8", "opacity": 1.0},
        {"offset": "100%", "color": "#121A29", "opacity": 0.95},
    ]

    # For light mode, use inverted metallic contrast stops
    if palette_name == "light":
        spec_stops = [
            {"offset": "0%",   "color": "#9AABB8", "opacity": 0.9},
            {"offset": "20%",  "color": "#BDC8D6", "opacity": 0.95},
            {"offset": "45%",  "color": "#E5EAF2", "opacity": 1.0},
            {"offset": "62%",  "color": "#FFFFFF", "opacity": 1.0},  # Specular spike
            {"offset": "76%",  "color": "#DDE4EE", "opacity": 1.0},
            {"offset": "90%",  "color": "#A6B4C4", "opacity": 0.95},
            {"offset": "100%", "color": "#78899A", "opacity": 0.9},
        ]

    # Generate gradients with varying specular angles for each ribbon
    angles = [35.0, 55.0, 125.0, 70.0, 145.0, 40.0, 85.0, 110.0]

    for i in range(ribbons):
        gid = f"{mesh_id}_grad_{i}"
        ang = angles[i % len(angles)]
        rad = math.radians(ang)
        x1 = round(50 - 50 * math.cos(rad), 2)
        y1 = round(50 - 50 * math.sin(rad), 2)
        x2 = round(50 + 50 * math.cos(rad), 2)
        y2 = round(50 + 50 * math.sin(rad), 2)

        stop_tags = []
        for s in spec_stops:
            stop_tags.append(
                f'      <stop offset="{s["offset"]}" stop-color="{s["color"]}" stop-opacity="{s["opacity"]}" />'
            )

        anim_tag = ""
        if animated:
            # SVG animate fallback for shimmering reflection
            anim_tag = f"""
      <animate attributeName="x1" values="{x1}%;{round(x1 + 12, 1)}%;{x1}%" dur="{drift_duration:.1f}s" repeatCount="indefinite" />
      <animate attributeName="x2" values="{x2}%;{round(x2 + 12, 1)}%;{x2}%" dur="{drift_duration:.1f}s" repeatCount="indefinite" />"""

        defs.append(f"""
    <linearGradient id="{gid}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">{anim_tag}
{chr(10).join(stop_tags)}
    </linearGradient>""")

    # 3. Ambient Radial Specular Glow
    defs.append(f"""
    <radialGradient id="{mesh_id}_glow" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="{pal['olive_glow']}" stop-opacity="0.18" />
      <stop offset="35%" stop-color="{pal['edge']}" stop-opacity="0.08" />
      <stop offset="100%" stop-color="{pal['bg']}" stop-opacity="0.0" />
    </radialGradient>""")

    # Add ambient glow backdrop
    elements.append(f'<rect width="{w}" height="{h}" fill="url(#{mesh_id}_glow)" pointer-events="none" />')

    # 4. Generate Ribbon Geometry
    # Ribbons progress vertically with alternating phases
    y_step = (h * 0.72) / max(ribbons, 1)
    y_start = h * 0.14

    for i in range(ribbons):
        t_norm = i / max(ribbons - 1, 1)  # 0.0 (top/back) to 1.0 (bottom/front)

        # Ribbon wave parameters
        y_center = y_start + (i * y_step) + rng.uniform(-10.0, 10.0)
        amplitude = (h * 0.08) + (h * 0.05) * math.sin(t_norm * math.pi) + rng.uniform(-6.0, 8.0)
        freq = 1.1 + (i * 0.22) + rng.uniform(-0.1, 0.15)
        phase = rng.uniform(0.0, 2.0 * math.pi)
        thickness = (h * 0.11) + (h * 0.09) * (1.0 - 0.4 * t_norm) + rng.uniform(-8.0, 12.0)

        pts_top, pts_bot = _generate_ribbon_geometry(
            w=w,
            h=h,
            y_center=y_center,
            amplitude=amplitude,
            freq=freq,
            phase=phase,
            thickness=thickness,
            samples=samples,
            rng=rng,
        )

        # Forward curve on top, reverse curve on bottom
        top_bezier = _points_to_cubic_bezier(pts_top)
        bot_bezier = _points_to_cubic_bezier(list(reversed(pts_bot)))

        path_d = (
            f"M {pts_top[0][0]:.2f} {pts_top[0][1]:.2f} {top_bezier} "
            f"L {pts_bot[-1][0]:.2f} {pts_bot[-1][1]:.2f} {bot_bezier} Z"
        )

        gid = f"{mesh_id}_grad_{i}"
        ribbon_opacity = round(0.72 + (0.26 * t_norm), 3)

        # Animated drift class / inline style
        anim_style = ""
        if animated:
            delay = round(i * (drift_duration / ribbons * 0.35), 2)
            anim_style = f' style="animation: {mesh_id}_drift_{i % 3} {drift_duration:.1f}s ease-in-out {delay}s infinite alternate;"'

        # Main liquid chrome ribbon body
        elements.append(
            f'    <path class="{mesh_id}_ribbon" d="{path_d}" fill="url(#{gid})" '
            f'fill-opacity="{ribbon_opacity}" stroke="{pal["edge"]}" stroke-width="0.75" '
            f'stroke-opacity="0.4"{anim_style} />'
        )

        # Specular crest hairline highlight (white reflection edge)
        crest_d = f"M {pts_top[0][0]:.2f} {pts_top[0][1]:.2f} {top_bezier}"
        elements.append(
            f'    <path d="{crest_d}" fill="none" stroke="#FFFFFF" stroke-width="1.1" '
            f'stroke-opacity="{round(0.45 + 0.35 * t_norm, 2)}" stroke-linecap="round"{anim_style} />'
        )

        # Subtle olive rim glow on every alternate ribbon
        if i % 2 == 1:
            elements.append(
                f'    <path d="{crest_d}" fill="none" stroke="{pal["olive_glow"]}" stroke-width="1.8" '
                f'stroke-opacity="0.32" stroke-linecap="round" filter="url(#{mesh_id}_blur_subtle)"{anim_style} />'
            )

    # 5. Filter for olive bloom
    defs.append(f"""
    <filter id="{mesh_id}_blur_subtle" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="1.5" />
    </filter>""")

    # 6. CSS Stylesheet for drift and shimmer
    style_block = ""
    if animated:
        style_block = f"""
    <style>
      .{mesh_id}_ribbon {{
        transform-origin: 50% 50%;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      }}
      @keyframes {mesh_id}_drift_0 {{
        0% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-7px) rotate(0.15deg); }}
        100% {{ transform: translateY(0px) rotate(0deg); }}
      }}
      @keyframes {mesh_id}_drift_1 {{
        0% {{ transform: translateY(0px) skewX(0deg); }}
        50% {{ transform: translateY(8px) skewX(-0.25deg); }}
        100% {{ transform: translateY(0px) skewX(0deg); }}
      }}
      @keyframes {mesh_id}_drift_2 {{
        0% {{ transform: translateY(0px) scale(1.0); }}
        50% {{ transform: translateY(-5px) scale(1.008); }}
        100% {{ transform: translateY(0px) scale(1.0); }}
      }}
      @keyframes {mesh_id}_shimmer {{
        0%, 100% {{ filter: drop-shadow(0 0 6px rgba(255, 255, 255, 0.15)); opacity: 0.94; }}
        50% {{ filter: drop-shadow(0 0 16px rgba(180, 201, 127, 0.35)); opacity: 1.0; }}
      }}
      #{mesh_id}_container {{
        animation: {mesh_id}_shimmer {drift_duration * 1.2:.1f}s ease-in-out infinite alternate;
      }}
      @media (prefers-reduced-motion: reduce) {{
        *, #{mesh_id}_container, .{mesh_id}_ribbon {{
          animation: none !important;
          transition: none !important;
        }}
        animate, animateTransform {{
          display: none !important;
        }}
      }}
    </style>"""

    # Assemble defs and body
    defs_markup = f"  <defs>{style_block}\n{''.join(defs)}\n  </defs>"
    elements_markup = "\n".join(elements)

    group_markup = f"""<g id="{mesh_id}_container" opacity="{opacity}">
{defs_markup}
{elements_markup}
</g>"""

    if as_svg:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="{w}" height="{h}" fill="{pal['bg']}" />
{group_markup}
</svg>"""

    return group_markup
