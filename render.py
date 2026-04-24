"""
render.py

Uses Playwright (chromium) to produce:
  1. social.png         — 1080x1080 @2x PNG from social.html
  2. profile.pdf        — A4 multi-page PDF from index.html
  3. preview.png        — 1440x900 PNG of index.html
  4. projects/<n>.pdf   — optional per-project A4 PDF (pass --projects)

Setup (dedicated conda env — recommended):
  conda create -n profile python=3.11 -y
  conda activate profile
  pip install playwright
  python -m playwright install chromium
  python render.py

On this machine (Windows, no `python` on PATH), call the env's
interpreter directly:
  & "C:\\Users\\tiany\\anaconda3\\envs\\profile\\python.exe" render.py

Flags:
  --projects   Also render one PDF per project page into projects/_pdf/
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
INDEX = (HERE / "index.html").as_uri()
SOCIAL = (HERE / "social.html").as_uri()
PROJECTS_DIR = HERE / "projects"
FONT_WAIT_MS = 1400


def _prime_page(page, url: str):
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.fonts && document.fonts.ready")
    page.wait_for_timeout(FONT_WAIT_MS)
    page.evaluate("document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));")
    page.wait_for_timeout(200)


def render_social(browser):
    print("→ social.png (1080x1080 @2x)")
    ctx = browser.new_context(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(SOCIAL, wait_until="networkidle")
    page.evaluate("document.fonts && document.fonts.ready")
    page.wait_for_timeout(FONT_WAIT_MS)
    page.screenshot(
        path=str(HERE / "social.png"),
        clip={"x": 0, "y": 0, "width": 1080, "height": 1080},
    )
    ctx.close()


def render_pdf(browser):
    print("→ profile.pdf (A4)")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    _prime_page(page, INDEX)
    page.emulate_media(media="print")
    page.pdf(
        path=str(HERE / "profile.pdf"),
        format="A4",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        prefer_css_page_size=True,
    )
    ctx.close()


def render_preview(browser):
    print("→ preview.png (1440x900)")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    page = ctx.new_page()
    _prime_page(page, INDEX)
    page.screenshot(
        path=str(HERE / "preview.png"),
        clip={"x": 0, "y": 0, "width": 1440, "height": 900},
    )
    ctx.close()


def render_project_pdfs(browser):
    out_dir = PROJECTS_DIR / "_pdf"
    out_dir.mkdir(exist_ok=True)
    htmls = sorted(PROJECTS_DIR.glob("*.html"))
    for html in htmls:
        print(f"→ projects/_pdf/{html.stem}.pdf")
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = ctx.new_page()
        _prime_page(page, html.as_uri())
        page.emulate_media(media="print")
        page.pdf(
            path=str(out_dir / f"{html.stem}.pdf"),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        ctx.close()


def main():
    do_projects = "--projects" in sys.argv
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            render_social(browser)
            render_pdf(browser)
            render_preview(browser)
            if do_projects:
                render_project_pdfs(browser)
        finally:
            browser.close()
    print("done.")
    for f in ("social.png", "profile.pdf", "preview.png"):
        path = HERE / f
        if path.exists():
            print(f"  {f:<16}  ({path.stat().st_size // 1024} KB)")
        else:
            print(f"  {f:<16}  MISSING")
    if do_projects:
        for p_file in sorted((PROJECTS_DIR / "_pdf").glob("*.pdf")):
            print(f"  projects/_pdf/{p_file.name}  ({p_file.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
