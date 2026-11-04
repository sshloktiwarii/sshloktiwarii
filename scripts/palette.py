"""Color palette definitions for Liquid Chrome Dark and Silver Light themes."""

from typing import Dict, Any

PALETTES: Dict[str, Dict[str, Any]] = {
    "dark": {
        "name": "liquid_chrome_dark",
        "bg": "#080C16",         # Deep Midnight Navy background
        "cell": "#0E1626",       # Grid card / cell background
        "edge": "#2A374A",       # Milled Silver border
        "fg": "#EAEFF7",         # Liquid Chrome Bright text & primary glyphs
        "dim": "#7E8D9F",        # Silver Muted secondary text
        "olive": "#8A9A5B",      # Signature olive green accent
        "olive_glow": "#B4C97F", # Olive specular neon glow
        "chrome_stops": [
            {"offset": "0%",   "color": "#121A29", "opacity": 1.0},
            {"offset": "20%",  "color": "#2E3A4B", "opacity": 1.0},
            {"offset": "42%",  "color": "#8A98A8", "opacity": 1.0},
            {"offset": "60%",  "color": "#D2D9E5", "opacity": 1.0},
            {"offset": "72%",  "color": "#FFFFFF", "opacity": 1.0},  # Liquid chrome specular highlight
            {"offset": "84%",  "color": "#8A98A8", "opacity": 1.0},
            {"offset": "100%", "color": "#121A29", "opacity": 1.0},
        ],
        "specular_stops": [
            "#FFFFFF",
            "#D2D9E5",
            "#8A98A8",
            "#2E3A4B",
            "#121A29",
        ],
        "accent_border": "#374A61",
        "glass_overlay": "rgba(234, 239, 247, 0.03)",
        "badge_bg": "#121D30",
        "badge_fg": "#D2D9E5",
    },
    "light": {
        "name": "silver_milled_light",
        "bg": "#F4F6F9",         # Clean frosty silver off-white
        "cell": "#FFFFFF",       # Pure white cell
        "edge": "#D3D8E2",       # Precision milled silver edge
        "fg": "#0C1322",         # High contrast deep navy/black text
        "dim": "#5C6878",        # Slate silver muted text
        "olive": "#637537",      # Deep olive accent
        "olive_glow": "#8A9A5B", # Olive vibrant highlight
        "chrome_stops": [
            {"offset": "0%",   "color": "#B8C4D4", "opacity": 1.0},
            {"offset": "25%",  "color": "#DDE4EE", "opacity": 1.0},
            {"offset": "50%",  "color": "#FFFFFF", "opacity": 1.0},
            {"offset": "75%",  "color": "#C4CFDE", "opacity": 1.0},
            {"offset": "100%", "color": "#9AABB8", "opacity": 1.0},
        ],
        "specular_stops": [
            "#FFFFFF",
            "#E5EAF2",
            "#A6B4C4",
            "#3C4A5E",
            "#1A2433",
        ],
        "accent_border": "#BDC8D6",
        "glass_overlay": "rgba(12, 19, 34, 0.02)",
        "badge_bg": "#E8ECF2",
        "badge_fg": "#1A263B",
    },
}

def get_palette(name: str = "dark") -> Dict[str, Any]:
    """Retrieve color palette by name ('dark' or 'light')."""
    return PALETTES.get(name.lower(), PALETTES["dark"])
