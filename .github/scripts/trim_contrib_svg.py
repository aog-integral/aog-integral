"""Trim a github-profile-3d-contrib SVG down to the calendar and the total.

The action always draws a radar chart, a language pie and star/fork counts.
Those only count public repos, so for work that lives in private repos they
show zeros. The calendar and the total do include private contributions, so
keep those and drop the rest.

Usage: trim_contrib_svg.py FILE [FILE ...]   (files are rewritten in place)
"""

import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def tag(name):
    return f"{{{SVG_NS}}}{name}"


def is_calendar(group):
    return any(e.get("class", "").startswith("cont-") for e in group.iter())


def add_text(root, text, x, y, size, css_class, bold=False):
    style = f"font-size: {size}px" + ("; font-weight: bold" if bold else "")
    element = ET.SubElement(root, tag("text"), {"x": str(x), "y": str(y), "class": css_class, "style": style})
    element.text = text


def trim(path):
    tree = ET.parse(path)
    root = tree.getroot()

    total = next(e.text for e in root.iter(tag("text")) if e.get("class") == "fill-strong")
    # The action writes "12 345" from five digits on.
    total = f"{int(''.join(c for c in total if c.isdigit())):,}"

    for group in root.findall(tag("g")):
        if not is_calendar(group):
            root.remove(group)

    add_text(root, total, 40, 770, 56, "fill-strong", bold=True)
    add_text(root, "contributions in the last year", 42, 808, 22, "fill-weak")

    tree.write(path, encoding="unicode")


if __name__ == "__main__":
    for svg_path in sys.argv[1:]:
        trim(svg_path)
