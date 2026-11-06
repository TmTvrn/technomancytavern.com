#!/usr/bin/env python3
"""Builds the hand-authored pages of technomancytavern.com (standard library only).

    python3 tools/build.py

Writes: /games/, /devlog/, /devlog/esper-elfy/, the Save Sparky hub, its art-studies index and every post.
Post bodies live in content/posts/<slug>.html; post metadata is POSTS below.
It does NOT touch the generated demo pages (realms/, studies/, art/*.html) or the splash page (index.html).
The output is committed, so deploys need no build step.
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS = "/devlog/esper-elfy/save-sparky/"
GAME = "Esper Elfy: Save Sparky"

POSTS = [
    dict(slug="from-squares-to-elfy", title="From Squares to Elfy",
         sub="One scripted fight, recorded from three different builds of the game.",
         summary="One scripted fight, recorded from three builds: boxes, the same boxes in pixels, then Elfy.",
         thumb="72fd7d7.jpg", tag="Process"),
    dict(slug="boxes-at-work", title="Boxes at Work",
         sub="What a cyan square can do before anyone gives it a face.",
         summary="Squash and stretch, wall slides, spikes and coyote time, and the time a double jump fooled me.",
         thumb="squash.jpg", tag="Game feel"),
    dict(slug="outline-first", title="Outline First, Then Real",
         sub="How to warn someone you are about to hurt them, with a cheerleader made of fire.",
         summary="How the game warns you before it hurts you, with real code and a live cheerleader made of fire.",
         thumb=None, tag="Design"),
]
for i, p in enumerate(POSTS, 1):
    p["n"] = i
    p["url"] = f"{SS}posts/{p['slug']}/"

ART = [  # (group, accent, [(file, title, blurb)])
    ("Same simulation, two drawings", "#3ef2ff", [
        ("blizzard-study", "Blizzard Study", "One snowstorm run by a single simulation and drawn two ways. Same flakes, same gusts, same boss shot; only the drawing changes."),
        ("aero-study", "Aero Study", "The same arena on a bright Frutiger Aero morning, with a live breakdown of how the hybrid builds each frame."),
        ("sparky-resolutions", "Sparky at Four Resolutions", "One simulation drawn four times while corrupted skulls circle Sparky.")]),
    ("Skulls and detail", "#ffd36b", [
        ("laughing-skull", "Laughing Skull", "The 48 px skull bursts out laughing: the jaw drops in whole pixels, the eyes flare."),
        ("skull-ladder", "Skull Detail Ladder", "One skull at eight sprite sizes. Each step up adds features, the way a pixel artist would.")]),
    ("Finding Elfy", "#4dff6a", [
        ("six-styles", "Six Ways to Draw Her", "The same heroine at 48 pixels tall, drawn six ways, with expressions to pick."),
        ("heroic-sizes", "Heroic at Four Sizes", "48, 64, 80 and 96 pixels tall. Each size gives her face more pixels to use."),
        ("heroic-face", "Heroic Face Pass", "A hand-placed face, with a Before toggle to compare against the last version.")]),
    ("The jump and the kick", "#c46bff", [
        ("psychic-jump-v1", "Psychic Triple Jump, first version", "The first triple jump, before the face pass. One rig, five heights."),
        ("psychic-jump", "Psychic Triple Jump, finished", "Jump, two psychic blasts, a flip and a squash landing, live at five sizes."),
        ("kick-victory", "Kick, Spin, Victory", "A side kick with hit-stop and afterimages, then a spin and a V-sign.")]),
]
ART_COUNT = sum(len(g[2]) for g in ART)
e = html.escape


def shell(title, desc, body, path, nav=None, og=False):
    def a(label, href, key):
        cur = ' aria-current="page"' if nav == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#05071a">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://technomancytavern.com/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Chakra+Petch:wght@600;700&family=JetBrains+Mono:wght@500&family=Press+Start+2P&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
  <a class="brand" href="/"><i></i><span>TECHNOMANCY TAVERN</span></a>
  <nav class="nav" aria-label="Main">{a("Games", "/games/", "games")}{a("Devlog", "/devlog/", "devlog")}{a("Art studies", SS + "art/", "art")}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
  <div class="foot-grid">
    <div><h4>Technomancy Tavern</h4><p>An indie game studio where code is the spellbook and AI is the familiar.</p></div>
    <div><h4>Play</h4><ul><li><a href="/games/">Games</a></li><li><a href="{SS}">Save Sparky workbench</a></li></ul></div>
    <div><h4>Read</h4><ul><li><a href="/devlog/">Devlog</a></li><li><a href="{SS}art/">Art studies</a></li><li><a href="{SS}#realms">Realms atlas</a></li></ul></div>
    <div><h4>Find us</h4><ul><li><a href="https://x.com/TmTvrn" rel="noopener">@TmTvrn on X</a></li><li><a href="https://github.com/TmTvrn" rel="noopener">GitHub</a></li><li><a href="mailto:contact@tmtvrn.com">contact@tmtvrn.com</a></li></ul></div>
  </div>
  <p class="fine">&copy; 2026 Technomancy Tavern. Code, drawings and words in the devlog are CC0: copy them, ship them.</p>
</div></footer>
</body>
</html>
"""


def crumbs(*items):
    out = ['<a href="/">Tavern</a>']
    for label, href in items:
        out.append(f'<a href="{href}">{e(label)}</a>' if href else e(label))
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">' + "<span>/</span>".join(out) + "</nav>"


def head(eyebrow, h1, lede, facts="", actions="", accent=None):
    st = f' style="--accent:{accent}"' if accent else ""
    return f"""<div class="wrap"><header class="page-head"{st}>
<p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{facts}{actions}
</header></div>"""


def post_list(posts):
    rows = "".join(
        f'<li><a href="{p["url"]}"><span class="n">{p["n"]:02d}</span><span><h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p></span><span class="tag">{e(p["tag"])}</span></a></li>'
        for posts_ in [posts] for p in posts_)
    return f'<ol class="posts">{rows}</ol>'


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel)


catalog = json.load(open(os.path.join(ROOT, SS.strip("/"), "catalog.json"), encoding="utf-8"))
realms, studies = catalog["realms"], catalog["studies"]
fights = sum(len(r["fights"]) for r in realms)
latest = POSTS[-1]


def card(href, k, title, text, accent="", more="Open", cls=""):
    st = f' style="--accent:{accent}"' if accent else ""
    tag = "a" if href else "div"
    h = f' href="{href}"' if href else ""
    m = f'<span class="more">{more} &rarr;</span>' if href else ""
    return f'<{tag} class="card {cls}"{h}{st}><span class="k">{e(k)}</span><h3>{e(title)}</h3><p>{text}</p>{m}</{tag}>'


# ------------------------------------------------------------------ /games/
games = head("Games", "What we're making",
             "Small, sharp games drawn almost entirely in code. Everything below is playable or readable in public as it grows.") + f"""
<div class="wrap"><section class="section">
<div class="section-head"><h2>Esper Elfy</h2><p>A psychic fighter, her friend Sparky, a world drawn in code</p></div>
<div class="grid">
<a class="card" href="{SS}" style="--accent:#4dff6a"><span class="status">In development</span><span class="k">Game 1</span><h3>{GAME}</h3>
<p>A strictly-2D precision boss fight in Godot, drawn as pixel art on a 960&times;540 grid. Elfy is a psychic fighter; the boss is a laughing skull that pogos on its own jaw; the arena stands in a blizzard.</p>
<div class="chips"><span class="chip">Godot 4.7</span><span class="chip">Pixel art from code</span><span class="chip">CC0</span></div>
<span class="more">Open the workbench &rarr;</span></a>
<div class="card soon"><span class="status plan">Planned</span><span class="k">Game 2</span><h3>Esper Elfy: BOPIS</h3>
<p>A drive-up toy store, in the spirit of curbside grocery pickup. Its own game with its own art.</p></div>
</div></section>
<section class="section"><div class="section-head"><h2>Where to start</h2></div>
<div class="grid">
{card(latest["url"], "Latest post", latest["title"], e(latest["summary"]), "#ffd36b", "Read")}
{card("/devlog/", "Devlog", "All posts, in order", f"{len(POSTS)} posts so far, each one teaching one thing.", "#3ef2ff", "Browse")}
{card(SS + "art/", "Art studies", "How she got drawn", f"{ART_COUNT} live experiments, from six ways to draw Elfy to her finished triple jump.", "#4dff6a", "Browse")}
</div></section></div>"""
write("games/index.html", shell("Games · Technomancy Tavern", "Games from Technomancy Tavern: Esper Elfy: Save Sparky and what comes next.", games, "games", "games"))

# ------------------------------------------------------------------ /devlog/
l = latest
media = (f'<div class="media"><img src="{SS}posts/{l["slug"]}/{l["thumb"]}" alt="" loading="lazy"></div>' if l["thumb"] else
         '<div class="media" style="display:grid;place-items:center;padding:24px;background:repeating-linear-gradient(45deg,#070a24 0 12px,#0a0f2e 12px 24px)">'
         '<div style="width:140px;height:140px;border:3px dashed #ff5f7a"></div></div>')
dev = head("Devlog", "How the drinks get made",
           "How Technomancy Tavern builds its games with code, pixels and AI. Written posts with live demos and recorded clips, plus the full workbench behind them.") + f"""
<div class="wrap"><section class="section">
<div class="section-head"><h2>Latest</h2></div>
<a class="feature" href="{l['url']}">{media}
<div class="txt"><span class="k">Post {l['n']:02d} &middot; {e(GAME)}</span><h3>{e(l['title'])}</h3><p>{e(l['summary'])}</p><span class="more" style="font:500 12px var(--mono);color:var(--cyan)">Read the post &rarr;</span></div></a>
</section>
<section class="section"><div class="section-head"><h2>All posts</h2><p>{len(POSTS)} so far &middot; oldest first</p></div>
{post_list(POSTS)}</section>
<section class="section"><div class="section-head"><h2>The workbench</h2><p>Everything the posts are built from</p></div>
<div class="grid">
{card(SS + "#realms", "Atlas", f"{len(realms)} realms, {fights} fights", "Every enemy study, running live in your browser, grouped by realm.", "#ff7a2a", "Open the atlas")}
{card(SS + "art/", "Art studies", f"{ART_COUNT} live experiments", "How Elfy and the skull got drawn, one pixel at a time.", "#4dff6a", "Browse")}
{card(SS + "#studies", "Level studies", f"{len(studies)} isometric experiments", "A diorama, a spire and a chapel, including the one we threw out.", "#78dcc4", "Browse")}
</div></section>
<section class="section"><div class="section-head"><h2>Series</h2></div>
<div class="grid">
{card("/devlog/esper-elfy/", "Franchise", "Esper Elfy", "The character, her games, and where each devlog lives.", "#4dff6a", "Open")}
<div class="card soon"><span class="k">Series soon</span><h3>Mancy</h3><p>How the tavern's technomancer barkeep gets drawn, animated and brought to life.</p></div>
</div></section></div>"""
write("devlog/index.html", shell("Devlog · Technomancy Tavern", "How Technomancy Tavern makes games with code, pixels and AI: posts, live demos and recorded clips.", dev, "devlog", "devlog"))

# ------------------------------------------------------------------ /devlog/esper-elfy/
fr = crumbs(("Devlog", "/devlog/"), ("Esper Elfy", None)) + head(
    "Franchise", "Esper Elfy",
    "Elfy is a psychic fighter. Each game under this name has its own devlog, its own art pipeline and its own jokes. The games share the character, not the code.", accent="#4dff6a") + f"""
<div class="wrap"><section class="section"><div class="section-head"><h2>The games</h2></div>
<div class="grid">
<a class="card" href="{SS}" style="--accent:#4dff6a"><span class="status">In development</span><h3>{GAME}</h3><p>A precision 2D boss fight drawn as pixel art, entirely from code. {len(realms)} realms and {fights} enemy studies to poke at.</p><span class="more">Open the workbench &rarr;</span></a>
<div class="card soon"><span class="status plan">Planned</span><h3>Esper Elfy: BOPIS</h3><p>A drive-up toy store, in the spirit of curbside grocery pickup.</p></div>
</div></section></div>"""
write("devlog/esper-elfy/index.html", shell("Esper Elfy · Technomancy Tavern", "Esper Elfy: a psychic fighter and her friend Sparky. The games and their devlogs.", fr, "elfy", "devlog"))

# ------------------------------------------------------------------ Save Sparky hub
def realm_card(r, kind):
    ember = r["ember"][0] if r.get("ember") else "#3ef2ff"
    n = len(r["fights"])
    k = f"Realm {r['number']} &middot; {n} fights" if kind == "realm" else "Study"
    chips = "".join(f'<a class="chip" href="/devlog/esper-elfy/save-sparky/{r["page"]}#h-{f["key"]}">{e(f["name"])}</a>' for f in r["fights"] if f.get("key"))
    return (f'<article class="card" style="--accent:{ember}"><span class="k">{k}</span>'
            f'<h3><a href="{SS}{r["page"]}" style="color:inherit;text-decoration:none">{e(r["name"])}</a></h3>'
            f'<p>{e(r["tagline"])}</p><div class="chips">{chips}</div></article>')

hub = crumbs(("Games", "/games/"), (GAME, None)) + head(
    "Workbench", GAME,
    "A strictly-2D precision boss fight drawn as pixel art, entirely from code. This is the workbench: the posts that explain it, the art studies that shaped it, and every enemy we've drawn so far, live in your browser.",
    f'<div class="facts"><span><b>{len(POSTS)}</b> posts</span><span><b>{ART_COUNT}</b> art studies</span><span><b>{len(realms)}</b> realms</span><span><b>{fights}</b> enemy fights</span><span><b>{len(studies)}</b> level studies</span></div>',
    '<div class="actions"><a class="btn primary" href="#posts">Read the posts</a><a class="btn" href="#realms">Explore the atlas</a></div>',
    "#4dff6a") + f"""
<div class="wrap"><nav class="jump" aria-label="On this page"><a href="#posts">Posts</a><a href="#art">Art studies</a><a href="#realms">Realms</a><a href="#studies">Level studies</a></nav>
<section class="section" id="posts" style="--accent:#ffd36b"><div class="section-head"><h2>Posts</h2><a href="/devlog/">All devlog posts &rarr;</a></div>{post_list(POSTS)}</section>
<section class="section" id="art" style="--accent:#4dff6a"><div class="section-head"><h2>Art studies</h2><a href="{SS}art/">All {ART_COUNT} &rarr;</a></div><div class="grid">
{card(SS + "art/psychic-jump.html", "Featured", "Psychic Triple Jump", "The finished jump study: two psychic blasts, a flip and a squash landing, at five sizes.", "#4dff6a", "Open")}
{card(SS + "art/six-styles.html", "Featured", "Six Ways to Draw Her", "The same heroine, six styles, with expressions to pick from.", "#4dff6a", "Open")}
{card(SS + "art/heroic-face.html", "Featured", "Heroic Face Pass", "A hand-placed face, with a Before toggle.", "#4dff6a", "Open")}
</div></section>
<section class="section" id="realms" style="--accent:#ff7a2a"><div class="section-head"><h2>Realms atlas</h2><p>Every enemy, in a loop, politely waiting</p></div>
<div class="grid">{"".join(realm_card(r, "realm") for r in realms)}</div></section>
<section class="section" id="studies" style="--accent:#78dcc4"><div class="section-head"><h2>Level studies</h2><p>The experiments, including the one we threw out</p></div>
<div class="grid">{"".join(realm_card(s, "study") for s in studies)}</div></section></div>"""
write(SS.strip("/") + "/index.html", shell(f"{GAME} · Workbench · Technomancy Tavern", f"{GAME}: posts, art studies and a live atlas of every enemy, all drawn in code.", hub, "hub", "games"))

# ------------------------------------------------------------------ art index
art_sections = ""
for group, acc, items in ART:
    cards = "".join(card(f + ".html", "Study", t, b, acc, "Open") for f, t, b in items)
    art_sections += f'<section class="section"><div class="section-head"><h2 style="--accent:{acc}">{e(group)}</h2></div><div class="grid">{cards}</div></section>'
art = crumbs(("Games", "/games/"), (GAME, SS), ("Art studies", None)) + head(
    "Art studies", "How she got drawn",
    "Live experiments in the order the art grew: one simulation drawn two ways, skulls, six ways to draw Elfy, and the triple jump. Everything is drawn by code in your browser.",
    f'<div class="facts"><span><b>{ART_COUNT}</b> studies</span><span><b>0</b> hand-drawn image files</span></div>', accent="#4dff6a") + f'<div class="wrap">{art_sections}</div>'
write(SS.strip("/") + "/art/index.html", shell(f"Art studies · {GAME} · Technomancy Tavern", f"Live pixel-art experiments from {GAME}, all drawn in code.", art, "art", "art"))

# ------------------------------------------------------------------ posts
for i, p in enumerate(POSTS):
    body_html = open(os.path.join(ROOT, "content/posts", p["slug"] + ".html"), encoding="utf-8").read()
    # drop the post's own leading text-only heading if any; bodies start at the first paragraph
    prev_ = POSTS[i - 1] if i else None
    next_ = POSTS[i + 1] if i + 1 < len(POSTS) else None
    pager = '<nav class="pager" aria-label="More posts">'
    if prev_: pager += f'<a class="prev" href="{prev_["url"]}"><small>&larr; Previous</small><b>{e(prev_["title"])}</b></a>'
    if next_: pager += f'<a class="next" href="{next_["url"]}"><small>Next &rarr;</small><b>{e(next_["title"])}</b></a>'
    pager += "</nav>"
    page = crumbs(("Devlog", "/devlog/"), (GAME, SS), (f"Post {p['n']:02d}", None)) + f"""
<div class="wrap"><header class="post-head" style="--accent:#ffd36b"><p class="eyebrow">{e(GAME)} &middot; Post {p['n']:02d} &middot; {e(p['tag'])}</p>
<h1>{e(p['title'])}</h1><p class="sub">{e(p['sub'])}</p></header>
<article>
{body_html}</article>
{pager}</div>"""
    write(f"devlog/esper-elfy/save-sparky/posts/{p['slug']}/index.html",
          shell(f"{p['title']} · {GAME} devlog", p["summary"], page, "post", "devlog"))
