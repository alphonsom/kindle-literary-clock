#!/usr/bin/env python3
"""Build the web version of the literary clock (for old iPads and other browsers).

Converts the quotes yaml into web/quotes.js and copies the Linux Libertine fonts
next to index.html, so the web folder can be served by any static web server.
"""
import html
import json
import re
import shutil
import sys
from argparse import ArgumentParser
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
REPO_DIR = WEB_DIR.parent
sys.path.insert(0, str(REPO_DIR / 'quote_to_image'))

from common import get_quotes  # noqa: E402

FONT_DIR = REPO_DIR / 'quote_to_image' / 'fonts' / 'LinLibertine'
FONTS = ['LinLibertine_Rah.ttf', 'LinLibertine_RBah.ttf', 'LinLibertine_RIah.ttf']

# placeholders for the only markup used in the yaml (line breaks and small caps)
BR, SC_OPEN, SC_CLOSE = '\x00', '\x01', '\x02'


def get_arguments():
    parser = ArgumentParser(prog='build_web', description=__doc__)
    parser.add_argument('-src', help='source file containing quotes in yaml format', type=Path,
                        default=REPO_DIR / 'quote_to_image' / 'litclock_annotated.yaml')
    parser.add_argument('-dst', help='destination folder', type=Path, default=WEB_DIR)
    return parser.parse_args()


def to_html(text: str):
    """escape text for html, restoring the placeholders as real markup"""
    return (html.escape(text, quote=False)
            .replace(BR, '<br>')
            .replace(SC_OPEN, '<span class="sc">')
            .replace(SC_CLOSE, '</span>'))


def quote_to_html(quote: str, timestring: str):
    quote = re.sub(r'<br\s*/?>', BR, quote)
    quote = re.sub(r'<span variant="smallcaps">', SC_OPEN, quote)
    quote = quote.replace('</span>', SC_CLOSE)
    quote = html.unescape(quote)
    timestring = html.unescape(timestring)

    match = re.search(re.escape(timestring), quote) or re.search(re.escape(timestring), quote, re.IGNORECASE)
    if match is None:
        print(f"warning: timestring '{timestring}' not found in '{quote[:40]}...'")
        return to_html(quote)

    start, end = match.span()
    return f'{to_html(quote[:start])}<b class="time">{to_html(quote[start:end])}</b>{to_html(quote[end:])}'


if __name__ == "__main__":
    args = get_arguments()
    args.dst.mkdir(parents=True, exist_ok=True)

    quotes = {}
    for timestr, datasets in get_quotes(args.src).items():
        quotes[timestr.replace(':', '')] = [
            [quote_to_html(d['quote'], str(d['timestring'])), html.unescape(str(d['title'])),
             html.unescape(str(d['author']))]
            for d in datasets
        ]

    js = 'window.LITCLOCK_QUOTES = ' + json.dumps(quotes, ensure_ascii=False, separators=(',', ':')) + ';\n'
    (args.dst / 'quotes.js').write_text(js, encoding='utf8')
    print(f"wrote {sum(len(v) for v in quotes.values())} quotes for {len(quotes)} minutes "
          f"to {args.dst / 'quotes.js'}")

    font_dst = args.dst / 'fonts'
    font_dst.mkdir(exist_ok=True)
    for font in FONTS:
        shutil.copy(FONT_DIR / font, font_dst / font)
    print(f"copied {len(FONTS)} fonts to {font_dst}")
