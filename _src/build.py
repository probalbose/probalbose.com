"""Build probalbose.com from the page fragments in _src/pages/.

Each fragment starts with a JSON header in an HTML comment:

    <!--{"path": "research/", "title": "Research", "description": "...", "nav": "research"}-->

followed by the page's <main> content. This script wraps every fragment in the
shared head, header and footer and writes <path>index.html (or 404.html).
Links in _src/site.json (LinkedIn, GitHub, photo) are filled in everywhere;
empty ones are simply left out.

Usage:  python3 _src/build.py        (run from the site folder or anywhere)
"""
import html
import json
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parents[1]
SRC = SITE / "_src"
CFG = json.loads((SRC / "site.json").read_text(encoding="utf-8"))

NAV = [("research", "/research/", "Research"),
       ("engineering", "/engineering/", "Engineering"),
       ("projects", "/projects/", "Projects"),
       ("books", "/books/", "Books")]

ICON_LINKEDIN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>')
ICON_GITHUB = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .3a12 12 0 0 0-3.8 23.38c.6.12.83-.26.83-.57v-2c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.08-.74.09-.73.09-.73 1.2.09 1.83 1.24 1.83 1.24 1.07 1.83 2.8 1.3 3.49 1 .1-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.14-.3-.54-1.52.1-3.18 0 0 1-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.64 1.66.24 2.88.12 3.18a4.65 4.65 0 0 1 1.23 3.22c0 4.61-2.8 5.63-5.48 5.92.42.36.81 1.1.81 2.22v3.29c0 .32.21.7.82.58A12 12 0 0 0 12 .3"/></svg>')


def social_links(cls="social"):
    out = []
    if CFG.get("linkedin"):
        out.append(f'<a href="{html.escape(CFG["linkedin"])}" rel="me noopener" aria-label="LinkedIn">{ICON_LINKEDIN}<span>LinkedIn</span></a>')
    if CFG.get("github"):
        out.append(f'<a href="{html.escape(CFG["github"])}" rel="me noopener" aria-label="GitHub">{ICON_GITHUB}<span>GitHub</span></a>')
    return f'<span class="{cls}">{"".join(out)}</span>' if out else ""


def portrait():
    if CFG.get("photo"):
        return (f'<img class="portrait photo" src="{html.escape(CFG["photo"])}" width="640" height="640" '
                f'alt="Probal Bose">')
    return '<div class="portrait" role="img" aria-label="Probal Bose"><span>PB</span></div>'


def render(meta, body):
    path = meta["path"]
    url = CFG["url"] + "/" + ("" if path in ("", "404.html") else path)
    title = meta["title"] if meta.get("nav") == "home" else f'{meta["title"]} · {CFG["name"]}'
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{cur if meta.get("nav") == key else ""}>{label}</a>'
        for key, href, label in NAV)
    same_as = [u for u in (CFG.get("linkedin"), CFG.get("github")) if u]
    ld = meta.get("jsonld")
    if meta.get("nav") == "home":
        ld = json.dumps({
            "@context": "https://schema.org", "@type": "Person", "name": CFG["name"], "url": CFG["url"] + "/",
            "jobTitle": "Principal Site Reliability Engineer",
            "affiliation": {"@type": "CollegeOrUniversity", "name": "University College Dublin"},
            "homeLocation": {"@type": "Place", "name": "Dublin, Ireland"},
            "sameAs": same_as + [u for u in [CFG.get("amazon_author")] if u],
        }, ensure_ascii=False, indent=1)
    body = (body.replace("{{portrait}}", portrait())
                .replace("{{social}}", social_links())
                .replace("{{social_btns}}", social_links("social btn-row")))
    robots = '<meta name="robots" content="noindex">\n' if path == "404.html" else ""
    canonical = "" if path == "404.html" else f'<link rel="canonical" href="{url}">\n'
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(meta["description"])}">
{robots}{canonical}<meta property="og:type" content="{meta.get("og_type", "website")}">
<meta property="og:title" content="{html.escape(meta.get("og_title", title))}">
<meta property="og:description" content="{html.escape(meta["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{CFG["url"]}/assets/img/{meta.get("og_image", "social-card-home.png")}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAF9F6">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/FiraSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
{f'<script type="application/ld+json">{ld}</script>' if ld else ""}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Probal Bose, home"><span class="mark" aria-hidden="true">π</span><span class="name">Probal Bose</span></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
  </div>
</header>

<main id="main">
{body.strip()}
</main>

<footer class="site-foot">
  <div class="wrap">
    <span>© 2026 Probal Bose · Dublin, Ireland</span>
    <span class="foot-links"><a href="/research/">Research</a> · <a href="/engineering/">Engineering</a> · <a href="/projects/">Projects</a> · <a href="/books/">Books</a>{social_links("social foot-social")}</span>
  </div>
</footer>

<script src="/assets/js/letters.js"></script>
<script src="/assets/js/main.js"></script>
</body>
</html>
"""


def main():
    pages = []
    for f in sorted((SRC / "pages").glob("*.html")):
        text = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--(\{.*?\})-->\s*", text, re.S)
        meta = json.loads(m.group(1))
        body = text[m.end():]
        out = SITE / (meta["path"] if meta["path"].endswith(".html") else meta["path"] + "index.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(meta, body), encoding="utf-8")
        if meta["path"] != "404.html":
            pages.append(meta["path"])
        print("  wrote", out.relative_to(SITE))

    # short link: /reading-the-greek/ -> /books/reading-the-greek/
    r = SITE / "reading-the-greek" / "index.html"
    r.parent.mkdir(exist_ok=True)
    r.write_text("""<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<title>Reading the Greek</title><link rel="canonical" href="https://probalbose.com/books/reading-the-greek/">
<meta http-equiv="refresh" content="0; url=/books/reading-the-greek/"><meta name="robots" content="noindex"></head>
<body><p><a href="/books/reading-the-greek/">Reading the Greek has moved here.</a></p></body></html>
""", encoding="utf-8")

    urls = "\n".join(f"  <url><loc>{CFG['url']}/{p}</loc></url>" for p in pages)
    (SITE / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")


if __name__ == "__main__":
    main()
