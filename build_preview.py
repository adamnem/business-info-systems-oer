import re
import markdown as md

SITE_DIR = "/tmp/quarto_site"

md_ext = ["tables", "fenced_code", "sane_lists"]


def render_md(chunk):
    return md.markdown(chunk.strip(), extensions=md_ext)


def qmd_to_html(path):
    with open(path) as f:
        text = f.read()

    # Strip YAML frontmatter, but grab the title first
    title_match = re.search(r'^---\ntitle:\s*"(.*?)"', text, flags=re.S)
    title = title_match.group(1) if title_match else ""
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.S)

    # Split into blocks on the ::: callout fences, preserving order
    pattern = re.compile(
        r'::: \{\.(callout-tip|callout-note)(?:\s+title="([^"]*)")?(?:\s+appearance="[^"]*")?\}\n(.*?)\n:::',
        re.S,
    )

    pieces = []
    last_end = 0
    for m in pattern.finditer(text):
        pieces.append(("md", text[last_end:m.start()]))
        kind, cb_title, body = m.group(1), m.group(2), m.group(3)
        pieces.append(("callout", kind, cb_title, body))
        last_end = m.end()
    pieces.append(("md", text[last_end:]))

    html_parts = []
    for p in pieces:
        if p[0] == "md":
            if p[1].strip():
                html_parts.append(render_md(p[1]))
        else:
            _, kind, cb_title, body = p
            css_class = "callout-tip" if kind == "callout-tip" else "callout-note"
            label = cb_title if cb_title else ("Try It" if kind == "callout-tip" else "Note")
            body_html = render_md(body)
            html_parts.append(
                f'<div class="{css_class}"><div class="callout-title">{label}</div>{body_html}</div>'
            )

    return title, "\n".join(html_parts)


STYLE = """
  :root {
    --navy: #003C6C;
    --gold: #E8B92E;
    --tip-bg: #eaf7f2;
    --tip-border: #2e9e6b;
    --note-bg: #eef2f8;
    --note-border: #6c86ad;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    color: #1a1a1a; background: #fff; display: flex; min-height: 100vh;
  }
  nav.sidebar {
    width: 260px; flex-shrink: 0; background: #f7f7f9; border-right: 1px solid #e3e3e6;
    padding: 24px 18px; position: sticky; top: 0; height: 100vh; overflow-y: auto;
  }
  nav.sidebar h1 { font-size: 15px; color: var(--navy); margin: 0 0 4px; }
  nav.sidebar .subtitle { font-size: 12px; color: #666; margin-bottom: 20px; }
  nav.sidebar .section-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; color: #999; margin: 16px 0 6px; padding: 0 8px; }
  nav.sidebar ul { list-style: none; padding: 0; margin: 0; font-size: 13.5px; }
  nav.sidebar li { margin-bottom: 6px; }
  nav.sidebar a { color: #333; text-decoration: none; display: block; padding: 5px 8px; border-radius: 4px; }
  nav.sidebar a.active { background: var(--navy); color: #fff; }
  nav.sidebar a:hover:not(.active) { background: #eceef1; }
  main { flex: 1; max-width: 820px; margin: 0 auto; padding: 40px 48px 100px; }
  main h1 { color: var(--navy); font-size: 30px; border-bottom: 3px solid var(--gold); padding-bottom: 12px; }
  main h2 { color: var(--navy); font-size: 22px; margin-top: 42px; }
  main h3 { color: #2b537d; font-size: 17px; margin-top: 30px; }
  main p { line-height: 1.65; font-size: 15.5px; }
  main code { background: #f2f2f4; padding: 1px 5px; border-radius: 3px; font-size: 0.9em; }
  main pre { background: #1e1e2e; color: #e8e8e8; padding: 14px 16px; border-radius: 6px; overflow-x: auto; }
  main pre code { background: none; color: inherit; padding: 0; }
  main table { border-collapse: collapse; width: 100%; margin: 18px 0; font-size: 14px; }
  main th, main td { border: 1px solid #dcdde0; padding: 8px 10px; text-align: left; }
  main th { background: var(--navy); color: #fff; }
  main tr:nth-child(even) { background: #f8f9fa; }
  .callout-tip, .callout-note {
    border-left: 4px solid var(--tip-border); background: var(--tip-bg);
    border-radius: 4px; padding: 14px 18px; margin: 20px 0;
  }
  .callout-note { border-left-color: var(--note-border); background: var(--note-bg); }
  .callout-title { font-weight: 700; margin-bottom: 6px; color: var(--tip-border); }
  .callout-note .callout-title { color: var(--note-border); }
  .callout-tip p:last-child, .callout-note p:last-child { margin-bottom: 0; }
  a { color: #1a5fa8; }
  .model-banner {
    background: #fff8e1; border: 1px solid #e8b92e; border-radius: 6px;
    padding: 10px 16px; font-size: 13px; margin-bottom: 28px; color: #6b5100;
  }
"""


def sidebar(active):
    def link(label, href, key):
        cls = "active" if key == active else ""
        return f'<li><a href="{href}" class="{cls}">{label}</a></li>'

    return f"""
<nav class="sidebar">
  <h1>Business Information Systems</h1>
  <div class="subtitle">An Open Textbook</div>
  <ul>
    <li><a href="#">Welcome</a></li>
    {link("Chapter 1: Getting Oriented in Excel", "preview.html", "ch1")}
    <li style="color:#999; padding: 5px 8px;">Chapter 2 (not yet written)</li>
    <li style="color:#999; padding: 5px 8px;">Chapter 3 (not yet written)</li>
  </ul>
  <div class="section-label">Appendices</div>
  <ul>
    {link("Appendix A: Excel Quick Reference", "appendix-preview.html", "appendix-a")}
  </ul>
</nav>
"""


def build_page(qmd_path, out_path, page_title, active_key, banner_extra=""):
    title, body_html = qmd_to_html(qmd_path)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{page_title} — Business Information Systems</title>
<style>{STYLE}</style>
</head>
<body>
{sidebar(active_key)}
<main>
  <div class="model-banner">This is a hand-built static preview standing in for a real Quarto render (Quarto's CLI couldn't be installed in this sandbox — see chat for why). Layout mimics Quarto's default book theme; the actual render will look close to this once built with real Quarto.{banner_extra}</div>
  <h1>{title}</h1>
  {body_html}
</main>
</body>
</html>
"""
    with open(out_path, "w") as f:
        f.write(page)
    print(f"Built {out_path}: {len(page)} bytes")


build_page(
    f"{SITE_DIR}/chapters/chapter-01-excel-intro.qmd",
    f"{SITE_DIR}/preview.html",
    "Chapter 1: Getting Oriented in Excel",
    "ch1",
)

build_page(
    f"{SITE_DIR}/chapters/appendix-a-excel-quick-reference.qmd",
    f"{SITE_DIR}/appendix-preview.html",
    "Appendix A: Excel Quick Reference",
    "appendix-a",
    banner_extra=" In a real Quarto book, this page renders from the same appendices: list in _quarto.yml as any other chapter, just grouped separately in the sidebar.",
)
