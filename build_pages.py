#!/usr/bin/env python3
"""Build Platform 3 Furniture site (template v2, t_f9208927, 2026-11-27).
Facts ONLY from card-verified sources:
- county: business.garrettcountymd.gov ribbon-cutting news (owners, siblings, former
  Grand Central Station building, renovation, quotes)
- gazette: wvnews.com/garrettrepublican grand-opening article (address 312 S. Third
  Street, category furniture+mattresses, quotes, new-inventory line)
- geocode: OpenStreetMap Nominatim (Oakland, Garrett County — used only in prose as
  regional naming, not JSON-LD geo since building-level coords are unverified)
Hours/phone/priceRange: NOT published anywhere -> omitted everywhere (rule 3)."""
import json, pathlib, datetime

ORIGIN = "https://platform-3-furniture-demo.up.railway.app"
SITE = "Platform 3 Furniture"
ADDR1, CITYSTATEZIP = "312 S. Third Street", "Oakland, MD 21554"
MAPQ = "312+S.+Third+St,+Oakland,+MD+21554"
FB = "https://www.facebook.com/groups/451442274891155/user/61592030335954/"
TODAY = "2026-11-27"
ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"

def head(title, desc, path):
    canon = ORIGIN + ("" if path == "/" else path)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- BUILT-{TODAY} -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canon}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>"""

MARK = """<svg class="mark" viewBox="0 0 168 52" role="img" aria-label="Platform 3 Furniture emblem: a brass-framed station nameplate reading Platform 3, furniture and mattresses, Oakland Maryland, with a rail line beneath the lettering">
<rect x="1.5" y="1.5" width="165" height="49" rx="7" fill="#142130" stroke="#c9993e" stroke-width="2.6"/>
<circle cx="11" cy="9" r="2.4" fill="#c9993e"/><circle cx="157" cy="9" r="2.4" fill="#c9993e"/>
<circle cx="11" cy="43" r="2.4" fill="#c9993e"/><circle cx="157" cy="43" r="2.4" fill="#c9993e"/>
<text x="84" y="25.5" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-size="16.5" letter-spacing="2.6" fill="#f5efe1">PLATFORM 3</text>
<text x="84" y="36" text-anchor="middle" font-family="'Helvetica Neue',Arial,sans-serif" font-size="6.4" letter-spacing="2.2" fill="#e9c878">FURNITURE &amp; MATTRESSES · OAKLAND MD</text>
<path d="M18 41h132" stroke="#c9993e" stroke-width="1.6"/>
<path d="M30 39.5v3.4M46 39.5v3.4M62 39.5v3.4M78 39.5v3.4M94 39.5v3.4M110 39.5v3.4M126 39.5v3.4M142 39.5v3.4" stroke="#5d6f7f" stroke-width="1.4"/>
</svg>"""

def header(active):
    def li(href, label):
        cls = ' class="on"' if href == active else ""
        return f'<li><a{cls} href="{href}">{label}</a></li>'
    return (f'<header class="top"><div class="wrap"><a class="brand" href="/">{MARK}'
            '<span class="word">Furniture &amp; mattresses<small>in the old Grand Central Station · Oakland, Maryland</small></span></a>'
            '<nav class="main" aria-label="Main"><ul>'
            + li("/showroom", "Showroom") + li("/mattresses-oakland-md", "Mattresses")
            + li("/furniture-garrett-county", "Furniture") + li("/about", "About")
            + '<li><a class="btn ghost" href="/contact">Contact</a></li></ul></nav></div></header>')

STORE_LD = {
    "@context": "https://schema.org", "@type": "FurnitureStore", "@id": ORIGIN + "/#store",
    "name": SITE, "url": ORIGIN,
    "description": "Furniture and mattresses in Oakland&rsquo;s former Grand Central Station building at 312 S. Third Street — opened November 2026.",
    "image": ORIGIN + "/og.png",
    "address": {"@type": "PostalAddress", "streetAddress": "312 S. Third Street",
                "addressLocality": "Oakland", "addressRegion": "MD", "postalCode": "21554",
                "addressCountry": "US"},
    "areaServed": {"@type": "AdministrativeArea", "name": "Garrett County, Maryland"},
    "openingDate": "2026-11",
    "founder": [{"@type": "Person", "name": "Raul Mendoza"}, {"@type": "Person", "name": "Josie Mendoza"}],
    "sameAs": [FB],
}

def ld(*blocks):
    out = ""
    for b in blocks:
        out += '<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False) + '\n</script>\n'
    return out

def crumb(*items):  # (name, path)
    el = [{"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"}]
    for i, (n, p) in enumerate(items, start=2):
        el.append({"@type": "ListItem", "position": i, "name": n, "item": ORIGIN + p})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}

def mapsec(lead="Find the showroom"):
    return f"""<section class="mapsec"><div class="wrap"><div class="mapbox">
<iframe src="https://www.google.com/maps?q={MAPQ}&amp;output=embed" loading="eager" referrerpolicy="no-referrer-when-downgrade" title="Map: {SITE}, {ADDR1}, {CITYSTATEZIP}"></iframe>
</div><div class="mapinfo"><p class="k">Address</p><h2>{lead}</h2>
<address>{SITE}<br>{ADDR1}<br>{CITYSTATEZIP}</address>
<p class="heract"><a class="btn big" href="https://maps.google.com/maps?q={MAPQ}" rel="noopener">Get directions</a> <a class="btn ghost" href="/contact">Send a message</a></p></div></div></section>"""

FOOTER = f"""<footer><div class="wrap footgrid">
<div><p class="fbrand">Platform 3 Furniture</p><p class="fsub">Furniture &amp; mattresses in Oakland&rsquo;s former Grand Central Station building — new inventory arriving on an ongoing basis.</p></div>
<div><p class="k">Find us</p><address>{ADDR1}<br>{CITYSTATEZIP}</address><p><a href="https://maps.google.com/maps?q={MAPQ}" rel="noopener">Get directions</a></p></div>
<div><p class="k">Pages</p><p class="flinks"><a href="/showroom">Showroom</a> · <a href="/mattresses-oakland-md">Mattresses</a> · <a href="/furniture-garrett-county">Furniture</a> · <a href="/about">About</a> · <a href="/contact">Contact</a> · <a href="/privacy">Privacy</a></p></div>
</div><div class="wrap footline"><p>© Platform 3 Furniture · Oakland, Maryland</p></div></footer>"""

def page(title, desc, path, active, body, ld_blocks=()):
    html = head(title, desc, path) + header(active) + "\n<main id=\"main\">\n" + body + "\n</main>\n" + FOOTER + "\n" + ld(*ld_blocks) + "</body>\n</html>\n"
    name = "index.html" if path == "/" else path.strip("/") + ".html"
    (PUB / name).write_text(html)

# ---------- art ----------
CLOCK = """<circle cx="210" cy="118" r="64" fill="#142130" stroke="#c9993e" stroke-width="5"/>
<circle cx="210" cy="118" r="52" fill="#f5efe1"/>
<g stroke="#142130" stroke-width="3" stroke-linecap="round"><path d="M210 66v10M210 162v9M158 118h10M252 118h9M173 81l7 7M240 148l7 7M247 81l-7 7M180 148l-7 7"/></g>
<path d="M210 118 210 84" stroke="#142130" stroke-width="6" stroke-linecap="round"/>
<path d="M210 118 238 132" stroke="#7c5230" stroke-width="5" stroke-linecap="round"/>
<circle cx="210" cy="118" r="5.5" fill="#c9993e"/>"""

ARCHES = """<g fill="none" stroke="#223343" stroke-width="5">
<path d="M30 330V150c0-46 34-82 80-82s80 36 80 82v180"/>
<path d="M190 330V150c0-46 34-82 80-82s80 36 80 82v180"/></g>
<g fill="none" stroke="#c9993e" stroke-width="2.4" opacity=".85">
<path d="M46 330V156c0-38 28-68 64-68s64 30 64 68v174"/><path d="M206 330V156c0-38 28-68 64-68s64 30 64 68v174"/></g>"""

CHAIR = """<g><path d="M92 236h96c14 0 24 10 24 24v10H68v-10c0-14 10-24 24-24Z" fill="#7c5230"/>
<path d="M68 248c-12 0-20 8-20 20v26h152v-26c0-12-8-20-20-20Z" fill="#8a5a33"/>
<path d="M60 236c0-34 8-52 28-52h72c20 0 28 18 28 52Z" fill="#a4693a"/>
<path d="M78 196c6-12 14-18 24-18h52c10 0 18 6 24 18" fill="none" stroke="#5d6f7f" stroke-width="4" stroke-linecap="round"/>
<path d="M60 292v28M180 292v28" stroke="#142130" stroke-width="8" stroke-linecap="round"/>
<rect x="204" y="196" width="10" height="96" rx="4" fill="#c9993e"/><path d="M196 196c0-14 6-22 13-22s13 8 13 22Z" fill="#e9c878"/></g>"""

RAILS = """<path d="M0 336h420M0 356h420" stroke="#c9993e" stroke-width="4"/>
<g stroke="#5d6f7f" stroke-width="4"><path d="M28 332v28M76 332v28M124 332v28M172 332v28M220 332v28M268 332v28M316 332v28M364 332v28"/></g>"""

HEROART = f'<svg viewBox="0 0 420 400" aria-hidden="true">{ARCHES}{CLOCK}{CHAIR}<g transform="translate(0 30)">{RAILS}</g></svg>'

FACADE = """<svg viewBox="0 0 420 300" aria-hidden="true">
<rect x="40" y="122" width="340" height="160" fill="#223343"/>
<path d="M40 122h340l-14-26H54Z" fill="#142130"/>
<g fill="#e9c878"><rect x="70" y="152" width="52" height="86" rx="26"/><rect x="146" y="152" width="52" height="86" rx="26"/><rect x="222" y="152" width="52" height="86" rx="26"/><rect x="298" y="152" width="52" height="86" rx="26"/></g>
<g fill="#223343"><rect x="78" y="160" width="36" height="70" rx="18"/><rect x="154" y="160" width="36" height="70" rx="18"/><rect x="230" y="160" width="36" height="70" rx="18"/><rect x="306" y="160" width="36" height="70" rx="18"/></g>
<rect x="188" y="200" width="44" height="82" rx="4" fill="#7c5230"/><path d="M210 200v82" stroke="#142130" stroke-width="3"/>
<circle cx="210" cy="92" r="26" fill="#142130" stroke="#c9993e" stroke-width="3.6"/><circle cx="210" cy="92" r="19" fill="#f5efe1"/>
<path d="M210 92V79M210 92l9 6" stroke="#142130" stroke-width="3" stroke-linecap="round"/>
<rect x="152" y="126" width="116" height="16" rx="3" fill="#c9993e"/><text x="210" y="138" text-anchor="middle" font-family="Georgia,serif" font-size="10" letter-spacing="1.8" fill="#142130">GRAND CENTRAL STATION</text>
<g transform="translate(0 282)"><path d="M0 0h420" stroke="#5d6f7f" stroke-width="5"/><g stroke="#5d6f7f" stroke-width="3.4"><path d="M40 -4v12M100 -4v12M160 -4v12M220 -4v12M280 -4v12M340 -4v12"/></g></g></svg>"""

def faq(items):
    rows = "".join(f"<div class=q><p class=qt>{q}</p><p>{a}</p></div>" for q, a in items)
    return f'<section class="faq"><div class="wrap"><p class="k">Questions shoppers ask</p><h2>Answered</h2>{rows}</div></section>'

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

FAQS = [
    ("Where is Platform 3 Furniture?",
     "312 S. Third Street in Oakland, Maryland — the former Grand Central Station building, in Garrett County."),
    ("What does the store carry?",
     "A growing selection of furniture and mattresses. New inventory continues to arrive as the business grows, so there are always new pieces to look at."),
    ("Who owns Platform 3 Furniture?",
     "Raul and Josie Mendoza — local entrepreneurs who also own and operate Don Patron Mexican Grill, Baja Street Wings and Tacos, and Baja Motel."),
    ("When did the store open?",
     "November 2026, marked with a ribbon-cutting hosted by the Garrett County Department of Business Development."),
    ("How do I ask about hours or a specific piece?",
     "Use the contact form on this page — messages go straight to the shop — or stop by the showroom on Third Street."),
]

# ---------- pages ----------
page("Platform 3 Furniture — Furniture &amp; Mattresses, Oakland MD",
     "Furniture and mattresses in Oakland&rsquo;s former Grand Central Station building at 312 S. Third Street. Owned by Raul and Josie Mendoza. Opened November 2026 — new inventory arriving.",
     "/", None, f"""
<section class="hero"><div class="wrap"><div class="herotext">
<p class="kick"><span class="dot" aria-hidden="true"></span>Now open · 312 S. Third Street · Oakland, Maryland</p>
<h1>Furniture &amp; mattresses,<br><em>arriving at Platform 3.</em></h1>
<p class="herosub">Platform 3 Furniture opened this November in Oakland&rsquo;s former Grand Central Station building. Owners Raul and Josie Mendoza bought and renovated the old station to bring Garrett County a new destination for furniture and mattresses — quality pieces to make your house feel like home.</p>
<p class="heract"><a class="btn big" href="/showroom">See the showroom</a> <a class="btn onink" href="https://maps.google.com/maps?q={MAPQ}" rel="noopener">Get directions</a> <a class="btn ghost" href="/contact">Send a message</a></p>
</div><div class="heroart">{HEROART}</div></div></section>

<section class="board"><div class="wrap"><div class="panel">
<p class="k">Departures · where to start</p>
<div class="brow"><a href="/furniture-garrett-county"><span class="bnum">01</span><span class="btxt"><strong>Furniture</strong> — a growing selection under the old station roof<i></i></span><span class="barrow">→</span></a></div>
<div class="brow"><a href="/mattresses-oakland-md"><span class="bnum">02</span><span class="btxt"><strong>Mattresses</strong> — beds for every room, fresh inventory arriving<i></i></span><span class="barrow">→</span></a></div>
<div class="brow"><a href="/about"><span class="bnum">03</span><span class="btxt"><strong>The story</strong> — the Mendoza family and the old Grand Central Station<i></i></span><span class="barrow">→</span></a></div>
<div class="brow"><a href="/contact"><span class="bnum">04</span><span class="btxt"><strong>Visit or ask</strong> — directions, showroom info, quick questions<i></i></span><span class="barrow">→</span></a></div>
</div></div></section>

<section class="split"><div class="wrap"><div class="grid2">
<article class="card"><h2>Furniture for the whole house</h2><p>The showroom holds a growing selection of furniture — and it keeps growing. &ldquo;Everyone has been so gracious and helpful, and we cannot wait to meet your furniture needs,&rdquo; says co-owner Raul Mendoza.</p><p><a href="/furniture-garrett-county">Browse the furniture →</a></p></article>
<article class="card"><h2>Mattresses, restocked as you shop</h2><p>New inventory continues to arrive, giving shoppers more choices as the business grows. Curious what just landed? Ask the shop.</p><p><a href="/mattresses-oakland-md">Browse the mattresses →</a></p></article>
</div></div></section>

<section class="story"><div class="wrap"><div class="grid2 art2">
<div><p class="k">The building</p><h2>An old station, a new errand</h2>
<p>The store sits in Oakland&rsquo;s former Grand Central Station building. The Mendozas purchased and renovated the property to open Platform 3 Furniture — giving an established commercial building new life and Oakland&rsquo;s downtown another reason to visit.</p>
<p>&ldquo;Purchasing the former Grand Central Station building and giving it a new life has been an exciting opportunity for us,&rdquo; said Josie Mendoza at the store&rsquo;s opening.</p>
<p class="heract"><a class="btn ghost" href="/about">Read the full story</a></p></div>
<div class="art">{FACADE}</div>
</div></div></section>

{mapsec()}

<section class="cta"><div class="wrap"><div>
<h2>Stop by the showroom</h2>
<p>New pieces arrive on an ongoing basis — the best way to see what&rsquo;s here today is to walk in, or send a note and we&rsquo;ll answer.</p>
<p class="heract"><a class="btn big onink" href="/contact">Send a message</a> <a class="btn ghost dark" href="/showroom">Tour the showroom page</a></p>
</div></div></section>
""", (STORE_LD,))

SHOWROOM_FAQS = FAQS[:4] + [
    ("Is there anything to browse right now?",
     "Yes — the store opened with a full selection of furniture and mattresses, and new inventory continues to arrive as the business grows."),
    ("Do you have a website?",
     "This page is the showroom&rsquo;s home on the web: address, directions, what the store carries, and a contact form that reaches the shop."),
]
page("The Showroom — Furniture &amp; Mattresses in Oakland MD — Platform 3 Furniture",
     "Tour Platform 3 Furniture&rsquo;s showroom in Oakland MD: a growing selection of furniture and mattresses in the former Grand Central Station building, 312 S. Third Street.",
     "/showroom", "/showroom", f"""
<section class="pagehead"><div class="wrap"><p class="kick"><span class="dot" aria-hidden="true"></span>Showroom · 312 S. Third Street · Oakland, MD</p>
<h1>The showroom</h1>
<p class="lead">Two aisles tell the whole story: furniture and mattresses. Both keep growing — new inventory continues to arrive, giving shoppers more choices as the business grows.</p></div></section>

<section class="split"><div class="wrap"><div class="grid2">
<article class="card"><h2>A fresh, welcoming place to shop</h2><p>Platform 3 Furniture aims to give customers a fresh, welcoming shopping experience with a variety of furniture and mattress options — in a building locals already know, the former Grand Central Station.</p><p><a href="/furniture-garrett-county">Furniture details →</a></p></article>
<article class="card"><h2>Quality pieces, arriving now</h2><p>The store was built to be a new destination where area residents find quality pieces to make their houses feel like home. Whatever sold last month, there&rsquo;s new stock behind it this month.</p><p><a href="/mattresses-oakland-md">Mattress details →</a></p></article>
</div></div></section>

<section class="story"><div class="wrap"><div class="grid2 art2">
<div><p class="k">How the showroom came to be</p><h2>Two restaurants, a motel — and now a furniture store</h2>
<p>Raul and Josie Mendoza already operate Don Patron Mexican Grill, Baja Street Wings and Tacos, and Baja Motel. In Josie&rsquo;s own words, opening a furniture store &ldquo;wasn&rsquo;t exactly on my bingo card&rdquo; — and it came together through the purchase and renovation of Oakland&rsquo;s Grand Central Station building.</p>
<p>The owners hint the showroom is just the beginning, with additional plans on the horizon.</p></div>
<div class="art">{FACADE}</div>
</div></div></section>

{faq(SHOWROOM_FAQS)}

{mapsec("Come see it in person")}
""", (crumb(("Showroom", "/showroom")), faq_ld(SHOWROOM_FAQS)))

MATT_FAQS = [
    ("Where can I buy a mattress in Oakland?",
     "At Platform 3 Furniture, 312 S. Third Street — the former Grand Central Station building in downtown Oakland, Maryland."),
    ("What mattresses do you have?",
     "The store carries a selection of mattresses alongside its furniture, and new inventory continues to arrive as the business grows. Stop by to compare what&rsquo;s in stock, or ask through the contact form."),
    ("Do you deliver?",
     "Ask at the showroom or through the contact form — the team is glad to talk through what&rsquo;s possible for your pieces."),
    ("Is it open yet?",
     "Yes — the store opened November 2026 and is serving Garrett County shoppers."),
]
page("Mattresses — Platform 3 Furniture, Oakland MD",
     "Mattresses in Oakland MD at 312 S. Third Street. Platform 3 Furniture keeps a growing mattress selection in Garrett County&rsquo;s former Grand Central Station building — new inventory arriving.",
     "/mattresses-oakland-md", "/mattresses-oakland-md", f"""
<section class="pagehead"><div class="wrap"><p class="kick"><span class="dot" aria-hidden="true"></span>Mattresses · Oakland &amp; Garrett County</p>
<h1>Mattresses at Platform 3</h1>
<p class="lead">A new destination for beds in Garrett County — part of the growing furniture and mattress selection in the former Grand Central Station building on Third Street.</p></div></section>

<section class="split"><div class="wrap"><div class="grid2">
<article class="card"><h2>Fresh stock, on an ongoing basis</h2><p>New inventory continues to arrive, giving shoppers more choices as the business grows. The mattress wall is never standing still — worth a second visit for that reason alone.</p></article>
<article class="card"><h2>One stop for the bedroom</h2><p>Beds and mattresses share the showroom with the furniture selection, so a bedroom can come together in one trip: the bed, the pieces around it, and the questions answered at the counter.</p><p><a href="/furniture-garrett-county">See the furniture side →</a></p></article>
</div></div></section>

{faq(MATT_FAQS)}

{mapsec("Directions to the mattress showroom")}
""", (crumb(("Mattresses", "/mattresses-oakland-md")),
     {"@context": "https://schema.org", "@type": "Service", "serviceType": "Mattress sales",
      "provider": {"@id": ORIGIN + "/#store"}, "areaServed": {"@type": "AdministrativeArea", "name": "Oakland, Garrett County, Maryland"},
      "url": ORIGIN + "/mattresses-oakland-md", "description": "Mattress selection at Platform 3 Furniture, 312 S. Third Street, Oakland, MD 21554. New inventory arriving on an ongoing basis."},
     faq_ld(MATT_FAQS)))

FURN_FAQS = [
    ("Where is the furniture store in Garrett County?",
     "Platform 3 Furniture, 312 S. Third Street, Oakland, MD 21554 — in the former Grand Central Station building."),
    ("What kind of furniture do you carry?",
     "A growing selection of furniture for the house. New inventory continues to arrive, so the floor keeps changing. Ask through the contact form about what&rsquo;s in stock now."),
    ("Who is behind the store?",
     "Raul and Josie Mendoza — the local owners of Don Patron Mexican Grill, Baja Street Wings and Tacos, and Baja Motel — who bought and renovated the Grand Central Station building for this store."),
    ("Does the store serve outside Oakland?",
     "The showroom is in downtown Oakland — county-wide service is exactly why the Garrett County Department of Business Development hosted the opening, and neighbors from the Deep Creek Lake region stop by as well."),
]
page("Furniture — Platform 3 Furniture, Garrett County MD",
     "Furniture in Garrett County MD at 312 S. Third Street, Oakland. Platform 3 Furniture serves Garrett County and the Deep Creek Lake region from the former Grand Central Station building.",
     "/furniture-garrett-county", "/furniture-garrett-county", f"""
<section class="pagehead"><div class="wrap"><p class="kick"><span class="dot" aria-hidden="true"></span>Furniture · Garrett County &amp; the Deep Creek region</p>
<h1>Furniture without the long drive</h1>
<p class="lead">A new destination to find quality pieces to make your house feel like home — right in downtown Oakland, serving shoppers from Garrett County and the Deep Creek Lake region.</p></div></section>

<section class="split"><div class="wrap"><div class="grid2">
<article class="card"><h2>Built to serve the community</h2><p>&ldquo;This business has given us an increased ability to serve this community, and we are thankful for the support,&rdquo; says co-owner Josie Mendoza. The store&rsquo;s growing selection of furniture is the proof of it.</p></article>
<article class="card"><h2>The selection keeps arriving</h2><p>New inventory continues to arrive as the business grows — and the owners say the showroom is just the beginning, with additional plans on the horizon.</p><p><a href="/mattresses-oakland-md">Mattresses in the same showroom →</a></p></article>
</div></div></section>

{faq(FURN_FAQS)}

{mapsec("Find the showroom in Oakland")}
""", (crumb(("Furniture", "/furniture-garrett-county")),
     {"@context": "https://schema.org", "@type": "Service", "serviceType": "Furniture sales",
      "provider": {"@id": ORIGIN + "/#store"}, "areaServed": {"@type": "AdministrativeArea", "name": "Garrett County, Maryland"},
      "url": ORIGIN + "/furniture-garrett-county", "description": "Furniture selection at Platform 3 Furniture, 312 S. Third Street, Oakland, MD 21554 — serving Garrett County and the Deep Creek Lake region."},
     faq_ld(FURN_FAQS)))

page("Our Story — Platform 3 Furniture, Oakland MD",
     "Raul and Josie Mendoza bought and renovated Oakland&rsquo;s former Grand Central Station building to open Platform 3 Furniture in November 2026. The story of the store.",
     "/about", "/about", f"""
<section class="pagehead"><div class="wrap"><p class="kick"><span class="dot" aria-hidden="true"></span>About · Oakland, Maryland · opened November 2026</p>
<h1>From a station to a showroom</h1>
<p class="lead">Platform 3 Furniture is the newest of several Garrett County businesses owned and operated by Raul and Josie Mendoza — and it lives in one of Oakland&rsquo;s most recognized buildings, the former Grand Central Station.</p></div></section>

<section class="story"><div class="wrap"><div class="grid2 art2">
<div><p class="k">The purchase</p><h2>Giving an old building new life</h2>
<p>The Mendozas — who already operate Don Patron Mexican Grill, Baja Street Wings and Tacos, and Baja Motel — purchased Oakland&rsquo;s former Grand Central Station building and renovated it to house their latest venture, bringing new life to an established commercial building in the heart of downtown Oakland.</p>
<p>The store&rsquo;s ribbon-cutting was hosted by the Garrett County Department of Business Development, with county commissioners, chamber of commerce leaders and local business representatives welcomed in attendance.</p>
<blockquote>&ldquo;With running two restaurants and a hotel, opening a furniture store wasn&rsquo;t exactly on my bingo card. I&rsquo;m so glad it was, though. This business has given us an increased ability to serve this community, and we are thankful for the support.&rdquo;<cite>— Josie Mendoza, co-owner</cite></blockquote>
<blockquote>&ldquo;I want to say thank you to all the community partners who have made this possible. Everyone has been so gracious and helpful, and we cannot wait to meet your furniture needs.&rdquo;<cite>— Raul Mendoza, co-owner</cite></blockquote></div>
<div class="art">{HEROART}</div>
</div></div></section>

<section class="split"><div class="wrap"><div class="grid2">
<article class="card"><h2>What the store is</h2><p>A growing selection of furniture and mattresses, with new inventory arriving on an ongoing basis — a fresh, welcoming shopping experience for area residents.</p><p><a href="/showroom">Tour the showroom →</a></p></article>
<article class="card"><h2>What comes next</h2><p>The owners say the showroom is just the beginning, with additional plans and developments on the horizon for the property and the business.</p><p><a href="/contact">Ask us a question →</a></p></article>
</div></div></section>

{mapsec()}
""", (crumb(("About", "/about")),))

page("Contact — Platform 3 Furniture, Oakland MD",
     "Contact Platform 3 Furniture — 312 S. Third Street, Oakland, MD 21554. Send a note through the form and it goes straight to the shop, or stop by the showroom.",
     "/contact", "/contact", f"""
<section class="pagehead"><div class="wrap"><p class="kick"><span class="dot" aria-hidden="true"></span>Contact · 312 S. Third Street · Oakland, MD</p>
<h1>Send the shop a note</h1>
<p class="lead">Questions about hours, a specific piece, or what just arrived? Fill this out and the message lands at the shop — the team answers between customers.</p></div></section>

<section class="formsec"><div class="wrap"><form class="cform" method="post" action="/contact">
<div class="frow"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" maxlength="120" required autocomplete="name"></div>
<div class="frow2"><div class="frow"><label for="f-phone">Phone <span>(optional)</span></label><input id="f-phone" name="phone" type="tel" maxlength="60" autocomplete="tel"></div>
<div class="frow"><label for="f-email">Email <span>(optional)</span></label><input id="f-email" name="email" type="email" maxlength="120" autocomplete="email"></div></div>
<div class="frow"><label for="f-msg">What can we help with?</label><textarea id="f-msg" name="message" rows="6" maxlength="4000" required placeholder="e.g. — are you open Saturdays? — do you have a queen mattress in stock?"></textarea></div>
<p class="formnote">We only use this note to answer you. <a href="/privacy">Privacy</a></p>
<p><button class="btn big" type="submit">Send to the shop</button></p>
</form><aside class="visit">
<p class="k">Or stop by</p><address>Platform 3 Furniture<br>312 S. Third Street<br>Oakland, MD 21554</address>
<p><a class="btn ghost" href="https://maps.google.com/maps?q={MAPQ}" rel="noopener">Get directions</a></p>
<p class="fine">Former Grand Central Station building, downtown Oakland.</p>
<div class="mapbox small"><iframe src="https://www.google.com/maps?q={MAPQ}&amp;output=embed" loading="eager" referrerpolicy="no-referrer-when-downgrade" title="Map: {SITE}, {ADDR1}, {CITYSTATEZIP}"></iframe></div>
</aside></div></section>
""", (crumb(("Contact", "/contact")),))

page("Privacy Policy — Platform 3 Furniture",
     "Privacy policy for platform-3-furniture-demo.up.railway.app: what the contact form collects, map-embed cookies, and who reads your message.",
     "/privacy", None, """
<section class="pagehead"><div class="wrap"><p class="k">Privacy</p>
<h1>Privacy policy</h1>
<p class="lead">Short version: this site sets no cookies of its own, loads no advertising, and the only information it collects is what you type into the contact form.</p></div></section>

<section class="prose"><div class="wrap">
<h2>The contact form</h2>
<p>Your name, phone, email and message are sent to Platform 3 Furniture&rsquo;s inbox so the shop can answer your question. They are used for that reply and nothing else — no lists, no marketing mail from this form.</p>
<h2>The map</h2>
<p>The pages that show the embedded map load it from Google Maps. Interacting with the map may set Google cookies under Google&rsquo;s own privacy policy.</p>
<h2>Hosting logs</h2>
<p>The web host keeps standard request logs (page requested, time, browser type). They are used to keep the site running and are not sold or shared.</p>
<h2>Questions</h2>
<p>Ask through the <a href="/contact">contact form</a> and a person will read it.</p>
</div></section>
""", (crumb(("Privacy", "/privacy")),))

page("Message sent — Platform 3 Furniture",
     "Your note reached Platform 3 Furniture. The shop answers between customers — or stop by 312 S. Third Street, Oakland MD.",
     "/thanks", None, """
<section class="pagehead"><div class="wrap"><p class="kick"><span class="dot" aria-hidden="true"></span>Message sent</p>
<h1>Your note reached the shop</h1>
<p class="lead">Thanks for writing — the team reads messages between customers and will get back to you. For anything that can&rsquo;t wait, stop by the showroom at 312 S. Third Street in Oakland.</p>
<p class="heract"><a class="btn big" href="/">Back to the showroom</a> <a class="btn ghost" href="https://maps.google.com/maps?q=312+S.+Third+St,+Oakland,+MD+21554" rel="noopener">Get directions</a></p></div></section>
""",)

(PUB / "404.html").write_text(head("Page not found — Platform 3 Furniture",
     "This page isn&rsquo;t on the board. Head back to the showroom, the furniture or mattress pages, or contact the shop.",
     "/404") + header(None) + """<main id="main"><section class="pagehead"><div class="wrap"><p class="kick"><span class="dot" aria-hidden="true"></span>404 · wrong platform</p>
<h1>This platform doesn&rsquo;t exist</h1>
<p class="lead">The page you were looking for isn&rsquo;t here. Try the showroom, the furniture page, the mattress page — or send the shop a note.</p>
<p class="heract"><a class="btn big" href="/">Back to home</a> <a class="btn ghost" href="/contact">Contact the shop</a></p></div></section></main>""" + FOOTER + "</body>\n</html>\n")

(PUB / "robots.txt").write_text(f"User-agent: *\nDisallow: /thanks\nDisallow: /404\n\nSitemap: {ORIGIN}/sitemap.xml\n")

SITEMAP = ["", "/showroom", "/mattresses-oakland-md", "/furniture-garrett-county", "/about", "/contact", "/privacy"]
(PUB / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"<url><loc>{ORIGIN}{p if p else '/'}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in SITEMAP) + "</urlset>\n")

print("built:", sorted(p.name for p in PUB.glob("*.html")), "+ robots/sitemap")
