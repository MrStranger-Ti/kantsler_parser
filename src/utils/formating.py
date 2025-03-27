import html

html_entities = [
    "&amp;",
    "&lt;",
    "&gt;",
    "&quot;",
    "&apos;",
    "&nbsp;",
    "&copy;",
    "&reg;",
    "&trade;",
    "&laquo;",
    "&raquo;",
    "&bull;",
    "&hellip;",
    "&mdash;",
    "&ndash;",
    "&tilde;",
    "&deg;",
    "&times;",
    "&divide;",
]


def _has_html_entity(raw: str) -> bool:
    for entity in html_entities:
        if entity in raw:
            return True

    return False


def clear_html_entity(text: str) -> str:
    while _has_html_entity(text):
        text = html.unescape(text)

    return text
