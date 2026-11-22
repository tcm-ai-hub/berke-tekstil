"""Berke Tekstil · content/*.yml + src/templates → _site/"""
import json, os, shutil
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")
S = yaml.safe_load(open(os.path.join(ROOT, "content", "site.yml"), encoding="utf-8"))
LANGS = {l: yaml.safe_load(open(os.path.join(ROOT, "content", f"{l}.yml"), encoding="utf-8")) for l in S["languages"]}
S["base_url"] = S["base_url"].rstrip("/")


def home_url(lang):
    return "/" if lang == "tr" else f"/{lang}/"


def purl(lang, key):
    return home_url(lang) + LANGS[lang]["products"][key]["slug"] + "/"


env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "src", "templates")), autoescape=select_autoescape(default=True))
def media(name):
    if not name:
        return None
    for ext, kind in (("mp4", "video"), ("jpg", "image")):
        if os.path.exists(os.path.join(ROOT, "assets", "media", f"{name}.{ext}")):
            poster = f"{name}-poster.jpg" if kind == "video" and os.path.exists(os.path.join(ROOT, "assets", "media", f"{name}-poster.jpg")) else None
            return {"kind": kind, "src": f"{name}.{ext}", "poster": poster}
    return None


env.globals.update(S=S, purl=purl, media=media)

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": S["brand"], "url": S["base_url"],
       "email": S["company"]["email"], "telephone": S["company"]["phone"],
       "address": {"@type": "PostalAddress", "streetAddress": S["company"]["address"], "addressCountry": "TR"}}


def write(path, html):
    fp = os.path.join(OUT, path.lstrip("/"), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)


shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
urls = []
for lang, L in LANGS.items():
    common = dict(lang=lang, L=L, home=home_url(lang), org_ld=json.dumps(ORG, ensure_ascii=False))
    needs = json.dumps([h["needs"] for h in L["planner"]["have"]], ensure_ascii=False).replace("'", "&#39;")
    html = env.get_template("home.html").render(**common, title=L["meta"]["home_title"], desc=L["meta"]["home_desc"],
                                                path=home_url(lang), alts={l: home_url(l) for l in LANGS},
                                                is_product=False, needs_json=needs, og_img=None)
    write(home_url(lang), html); urls.append(home_url(lang))
    for i, prod in enumerate(S["products"], 1):
        P = L["products"][prod["key"]]
        html = env.get_template("product.html").render(**common, P=P, prod=prod, idx=i, title=P["title"], desc=P["desc"],
                                                       path=purl(lang, prod["key"]), alts={l: purl(l, prod["key"]) for l in LANGS},
                                                       is_product=True, og_img=P.get("hero_img") or prod.get("img") or None)
        write(purl(lang, prod["key"]), html); urls.append(purl(lang, prod["key"]))

with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    f.write("".join(f"<url><loc>{S['base_url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {S['base_url']}/sitemap.xml\n")
print(f"{len(urls)} sayfa → _site/")
