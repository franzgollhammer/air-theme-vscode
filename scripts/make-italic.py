#!/usr/bin/env python3
"""Generate italic/bold Air variants from the normal VS Code themes."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"

VARIANTS = (
    ("air-dark-color-theme.json", "air-dark-italic-color-theme.json", "Air dark", "Air dark italic"),
    ("air-light-color-theme.json", "air-light-italic-color-theme.json", "Air light", "Air light italic"),
)

SEMANTIC_STYLES = {
    "parameter.declaration": "italic",
    "function": "bold",
    "function.declaration": "bold",
    "method": "bold",
    "method.declaration": "bold",
}

TOKEN_OVERRIDES = """    {
      "name": "Air italic variant: bold functions",
      "scope": [
        "entity.name.function",
        "support.function",
        "variable.function",
        "entity.name.function.decorator",
        "meta.function-call entity.name.function",
        "meta.function-call support.function",
        "meta.function-call variable.function"
      ],
      "settings": {
        "fontStyle": "bold"
      }
    },
    {
      "name": "Air italic variant: italic strings",
      "scope": "string",
      "settings": {
        "fontStyle": "italic"
      }
    },
    {
      "name": "Air italic variant: italic parameters",
      "scope": ["variable.parameter", "function.parameter"],
      "settings": {
        "fontStyle": "italic"
      }
    }"""

SEMANTIC_RE = re.compile(
    r'^    "([^"]+)": "(#[0-9A-Fa-f]{6})"(,?)$',
    re.MULTILINE,
)


def style_semantic_token(match: re.Match) -> str:
    token, color, comma = match.groups()
    style = SEMANTIC_STYLES.get(token)
    if not style:
        return match.group(0)
    return (
        f'    "{token}": {{\n'
        f'      "foreground": "{color}",\n'
        f'      "{style}": true\n'
        f"    }}{comma}"
    )


def generate(src_name: str, dst_name: str, base_name: str, variant_name: str) -> None:
    text = (THEMES / src_name).read_text()
    text = text.replace(f'"name": "{base_name}"', f'"name": "{variant_name}"', 1)
    text = SEMANTIC_RE.sub(style_semantic_token, text)
    text = text.replace(
        '\n  },\n  "tokenColors": [',
        ',\n'
        '    "parameter": {\n'
        '      "italic": true\n'
        '    }\n'
        '  },\n'
        '  "tokenColors": [',
        1,
    )

    token_colors_end = text.rfind("\n  ]\n}")
    if token_colors_end == -1:
        raise ValueError(f"Could not find tokenColors end in {src_name}")

    text = (
        text[:token_colors_end]
        + ",\n"
        + TOKEN_OVERRIDES
        + text[token_colors_end:]
    )

    destination = THEMES / dst_name
    destination.write_text(text)
    print(f"Wrote {destination.relative_to(ROOT)} ({len(text)} bytes)")


def main() -> None:
    for variant in VARIANTS:
        generate(*variant)


if __name__ == "__main__":
    main()
