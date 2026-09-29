# probalbose.com

Personal site of Probal Bose: engineering, research, projects and books. Plain static HTML and CSS, hosted on GitHub Pages with the domain registered at Namecheap.

```
_src/pages/*.html           the page contents (edit these)
_src/site.json              LinkedIn and GitHub links, photo path (empty values are left out)
_src/build.py               wraps each page in the shared header and footer
index.html                  home, about me
research/  engineering/  projects/  books/
books/reading-the-greek/    the book page (letter explorer, downloads, where to buy)
reading-the-greek/          short link that redirects to the book page
404.html                    GitHub Pages shows this for missing pages
assets/css/site.css         all styling (book palette, Fira Sans, Libertinus Serif)
assets/js/                  small enhancements and the letter data
assets/img/, downloads/     generated from the book repo
CNAME                       tells GitHub Pages the custom domain
```

## Edit a page

1. Change the text in `_src/pages/`, or the links in `_src/site.json`.
2. Run `python3 _src/build.py` (standard Python 3, nothing to install).
3. Preview, then commit and push.

To add a photo, save it as `assets/img/probal.jpg` (square, about 640 × 640) and set `"photo": "/assets/img/probal.jpg"` in `_src/site.json`.

To add a new book, copy the book block in `_src/pages/40-books.html` and add a detail page like `_src/pages/41-reading-the-greek.html`.

## Preview locally

```bash
python3 -m http.server 8000     # then open http://localhost:8000
```

## Update the book assets

The cheat sheet, the sample chapter, the images and `letters.js` come from the book repo:

```bash
cd ~/projects/books/reading-the-greek
python3 scripts/web_export.py ../probalbose-site      # add --no-build to skip rebuilding the PDFs
```

Then commit and push this repo. GitHub Pages redeploys within a minute or two.

## First deployment

### 1. Put the site on GitHub

1. On github.com/new create a **public** repository in your personal account, for example `probalbose.com`. Don't add a README.
2. In this folder:
   ```bash
   git init -b main
   git add .
   git commit -m "First version of probalbose.com"
   git remote add origin git@github.com:probalbose/probalbose.com.git
   git push -u origin main
   ```

### 2. Verify the domain with GitHub (protects it from takeover)

1. GitHub → your profile picture → **Settings** → **Pages** → **Add a domain** → `probalbose.com`.
2. GitHub shows a TXT record. In Namecheap add it under **Advanced DNS** (Host `_github-pages-challenge-probalbose`, Value as shown), save, wait a few minutes, then click **Verify**.

### 3. Point Namecheap at GitHub Pages

Namecheap → **Domain List** → **Manage** next to probalbose.com → **Advanced DNS**.

1. Delete the default parking records, usually a **CNAME** for `www` pointing at `parkingpage.namecheap.com` and a **URL Redirect** for `@`.
2. Add these host records:

| Type | Host | Value |
|---|---|---|
| A Record | @ | 185.199.108.153 |
| A Record | @ | 185.199.109.153 |
| A Record | @ | 185.199.110.153 |
| A Record | @ | 185.199.111.153 |
| CNAME Record | www | `probalbose.github.io.` |

   Optional for IPv6, 4 AAAA records on `@`: 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153.
3. **Save All Changes**. Never add a wildcard (`*`) record.

### 4. Turn on Pages

Repository → **Settings** → **Pages**:

1. **Source** "Deploy from a branch", branch `main`, folder `/ (root)`, **Save**.
2. **Custom domain** `probalbose.com`, **Save** (the `CNAME` file already says this).
3. Once the DNS check passes, tick **Enforce HTTPS**. The certificate can take up to a day.

Check the DNS from a terminal with `dig probalbose.com +noall +answer` and `dig www.probalbose.com +noall +answer`.

Sources: GitHub Docs, "Managing a custom domain for your GitHub Pages site"; Namecheap, "How do I link my domain to GitHub Pages".
