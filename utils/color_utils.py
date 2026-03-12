# color_utils.py (utils 패키지)

import colorsys
from typing import Dict, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """
    Converts a HEX color string to an RGB tuple (values between 0.0 and 1.0).
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def generate_app_neutrals(base_hex: str, num_colors: int = 10) -> Dict[str, str]:
    """
    Generates a scale of neutral colors inheriting the hue from a base color.
    Uses a non-linear saturation curve to enhance depth in darker shades.
    """
    r, g, b = hex_to_rgb(base_hex)
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)

    palette = {}
    for i in range(num_colors):
        t = i / (num_colors - 1)

        v = 0.98 - (t * 0.88)
        s = 0.01 + (0.15 * (t**1.8))

        rgb = colorsys.hsv_to_rgb(h, s, v)
        hex_result = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )

        scale_name = f"Gray_{int(t * 900) if t > 0 else 50}"
        palette[scale_name] = hex_result

    return palette


# ==========================================
# Global Theme Variables
# ==========================================

PRIMARY_COLOR = "#14B4A0"
PRIMARY_HOVER = "#17C8B2"
PRIMARY_ACTIVE = "#109080"

NEUTRALS = generate_app_neutrals(PRIMARY_COLOR)
