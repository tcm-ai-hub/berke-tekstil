import json, os, shutil
from jinja2 import Environment, DictLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")
C = json.load(open(os.path.join(ROOT, "content.json")))
TR, EN = C["TR"], C["EN"]

# ---------- extra copy: babywear enrichment, product pages, SEO ----------
TR.update({
    "p2d": "Bebek giyim markaları için koleksiyon üretimi: müslin örtülerden zıbın ve tulumlara. Kumaş, aksesuar, nakış ve etiket markanızla birlikte seçilir.",
    "p2c": ["Müslin örtü", "Zıbın & body", "Tulum & pijama", "Aksesuar"],
    "p2l": "Ürün sayfasını inceleyin →",
    "p2img": "Müslin doku · bebek koleksiyonu",
    "menu": "Menü", "skip": "İçeriğe geç", "sent": "Teşekkürler. Talebiniz alındı, en kısa sürede dönüş yapacağız.",
})
EN.update({
    "p2d": "Collection manufacturing for babywear brands, from muslin swaddles to bodysuits and sleepsuits. Fabric, trims, embroidery and labels chosen together with your brand.",
    "p2c": ["Muslin swaddles", "Bodysuits", "Sleepsuits", "Accessories"],
    "p2l": "View product page →",
    "p2img": "Muslin texture · baby collection",
    "menu": "Menu", "skip": "Skip to content", "sent": "Thank you. We have received your request and will get back to you shortly.",
})

PRODUCTS = {
 "home": {
  "tr": {"slug": "ev-tekstili", "n": "01", "name": "Ev Tekstili", "pg": "home",
   "title": "Ev Tekstili Üreticisi · Private Label · Berke Tekstil",
   "desc": "Türkiye'de ev tekstili üreticisi: yatak, banyo, masa ve mutfak, dekoratif ürünlerde markaya özel üretim, nakış, etiket ve ambalaj.",
   "lead": "Yatak, banyo, masa ve mutfak ile dekoratif ürünlerde markanıza özel üretim. Kumaş, nakış, etiket ve ambalaj sizin standardınızda; numuneden sevkiyata tek muhatapla.",
   "img": "towel.jpg", "alt": "Kenarı bej iplikle nakışlı, katlanmış beyaz havlu",
   "tiles": [
     {"t": "Yatak tekstili", "d": "Nevresim, çarşaf ve yastık kılıfı.", "ph": "Yatak tekstili"},
     {"t": "Banyo", "d": "Havlu ve bornoz, nakışlı ya da düz.", "img": "monogram.jpg", "alt": "Waffle bornoza işlenen lacivert monogram"},
     {"t": "Masa ve mutfak", "d": "Masa örtüsü, peçete ve mutfak tekstili.", "ph": "Masa ve mutfak"},
     {"t": "Dekoratif", "d": "Yastık, örtü ve dekoratif tamamlayıcılar.", "ph": "Dekoratif"}],
   "opts": [["Kumaş", "Koleksiyonunuza göre kumaş seçimi; numuneyle onaylanır."], ["İşçilik", "Kendi atölyemizde nakış: logo, monogram ve bordür."], ["Renk ve ölçü", "Koleksiyonunuza göre renk, ölçü ve bitiş."], ["Etiket", "Markanıza özel dokuma ya da baskı etiket."], ["Ambalaj ve sevk", "Perakende ya da e-ticarete uygun paketleme, anlaşmalı kargoyla gönderim."]],
   "care": None},
  "en": {"slug": "home-textiles", "n": "01", "name": "Home Textiles", "pg": "home",
   "title": "Home Textile Manufacturer in Türkiye · Private Label · Berke Tekstil",
   "desc": "Home textile manufacturer in Türkiye: private label bed, bath, table and kitchen, and decorative products with embroidery, labels and packaging.",
   "lead": "Private label manufacturing for bed, bath, table and kitchen, and decorative products. Fabric, embroidery, labels and packaging to your standard, from sample to shipment with one contact.",
   "img": "towel.jpg", "alt": "Folded white towel with a beige embroidered border",
   "tiles": [
     {"t": "Bed linen", "d": "Duvet covers, sheets and pillowcases.", "ph": "Bed linen"},
     {"t": "Bath", "d": "Towels and bathrobes, embroidered or plain.", "img": "monogram.jpg", "alt": "Navy monogram stitched onto a waffle bathrobe"},
     {"t": "Table & kitchen", "d": "Tablecloths, napkins and kitchen textiles.", "ph": "Table & kitchen"},
     {"t": "Decorative", "d": "Cushions, throws and finishing pieces.", "ph": "Decorative"}],
   "opts": [["Fabric", "Chosen for your collection and approved with a sample."], ["Workmanship", "In-house embroidery: logos, monograms and borders."], ["Colour & size", "Colour, size and finish to your collection."], ["Labels", "Woven or printed labels for your brand."], ["Packing & shipping", "Retail or e-commerce ready packing, shipped with partner carriers."]],
   "care": None},
 },
 "baby": {
  "tr": {"slug": "bebek-giyim", "n": "02", "name": "Bebek Giyim", "pg": "baby",
   "title": "Bebek Giyim Üreticisi · Private Label · Berke Tekstil",
   "desc": "Türkiye'de bebek giyim üreticisi: müslin örtü, zıbın, body, tulum ve aksesuarlarda markaya özel üretim, nakış, etiket ve ambalaj.",
   "lead": "Bebek giyim markaları için koleksiyon üretimi. Cilde temas eden ürünlerde kumaş ve aksesuar seçimini sizinle birlikte yapar, temiz dikiş ve markanıza özel etiket ve ambalajla teslim ederiz.",
   "img": "baby-muslin-hero.jpg", "alt": "Bej, adaçayı yeşili ve krem renkte üst üste katlanmış müslin örtüler",
   "tiles": [
     {"t": "Müslin örtü ve battaniye", "d": "Kundak, çok amaçlı örtü ve hafif battaniye.", "img": "baby-muslin-tile.jpg", "alt": "Katlanmış müslin örtüler"},
     {"t": "Zıbın ve body", "d": "Günlük temel parçalar, markanızın kalıbıyla.", "img": "baby-bodysuit.jpg", "alt": "Ahşap zemin üzerinde krem renk uzun kollu bebek body"},
     {"t": "Tulum ve pijama", "d": "Uyku ve ev giyimi koleksiyonları.", "img": "baby-sleepsuit.jpg", "alt": "Ahşap zemin üzerinde katlanmış, ahşap düğmeli örgü bebek tulumu"},
     {"t": "Önlük, şapka, aksesuar", "d": "Setleri tamamlayan küçük parçalar.", "img": "baby-accessories.jpg", "alt": "Müslin önlük ve örgü bere"}],
   "wide_alt": "Krem keten üzerinde müslin önlük, örgü bere, çorap ve ahşap çıngırak", "care": {"h": "Bebek tekstilinde dikkat ettiklerimiz", "items": [
     ["Kumaş", "Cilde temas eden ürünlerde kumaşı markanızla birlikte seçeriz. Pazarınızın istediği test ve belge taleplerini üretim planına baştan dahil ederiz."],
     ["Dikiş", "Yumuşak ve düz dikiş bitişleri. İç etiketin konumu ve malzemesi markanızla belirlenir."],
     ["Aksesuar", "Çıtçıt, düğme ve şerit gibi aksesuarların tedariki ve üretim içi kontrolü."],
     ["Nakış", "Müslin ve pamuk ürünlerde isim, monogram ve küçük motif nakışı, kendi atölyemizde."]]},
   "opts": [["Set ve hediye", "Koleksiyon setleri ve kutulu hediye ambalajı."], ["Etiket", "Markanıza özel dokuma ya da baskı etiket, beden ve bakım etiketleri."], ["Renk ve baskı", "Koleksiyon paletinize göre renk; desen ve baskı seçenekleri."], ["E-ticaret", "Tekli paketleme ve anlaşmalı kargo ile sevke hazırlık."]]},
  "en": {"slug": "babywear", "n": "02", "name": "Babywear", "pg": "baby",
   "title": "Babywear Manufacturer in Türkiye · Private Label · Berke Tekstil",
   "desc": "Babywear manufacturer in Türkiye: private label muslin swaddles, bodysuits, sleepsuits and accessories with embroidery, labels and packaging.",
   "lead": "Collection manufacturing for babywear brands. For products worn next to the skin we choose fabric and trims together with you, and deliver with clean seams and your own labels and packaging.",
   "img": "baby-muslin-hero.jpg", "alt": "Stacked muslin swaddles in sand, sage and cream",
   "tiles": [
     {"t": "Muslin swaddles & blankets", "d": "Swaddles, multi-use cloths and light blankets.", "img": "baby-muslin-tile.jpg", "alt": "Folded muslin swaddles"},
     {"t": "Bodysuits", "d": "Everyday essentials, made to your brand's pattern.", "img": "baby-bodysuit.jpg", "alt": "Cream long-sleeve baby bodysuit on light oak"},
     {"t": "Sleepsuits & pyjamas", "d": "Sleep and loungewear collections.", "img": "baby-sleepsuit.jpg", "alt": "Folded knitted baby sleepsuit with wooden buttons on light oak"},
     {"t": "Bibs, hats, accessories", "d": "Small pieces that complete a set.", "img": "baby-accessories.jpg", "alt": "Muslin bib and knitted beanie"}],
   "wide_alt": "Muslin bib, knitted beanie, socks and a wooden rattle on cream linen", "care": {"h": "What we pay attention to in babywear", "items": [
     ["Fabric", "For products worn next to the skin we choose fabric together with your brand, and build your market's testing and documentation requests into the plan from the start."],
     ["Seams", "Soft, flat seam finishes. Inner label position and material agreed with your brand."],
     ["Trims", "Sourcing and in-line checks of snaps, buttons and tapes."],
     ["Embroidery", "Names, monograms and small motifs on muslin and cotton, in our own atelier."]]},
   "opts": [["Sets & gifting", "Collection sets and boxed gift packaging."], ["Labels", "Woven or printed brand labels, size and care labels."], ["Colour & print", "Colour to your collection palette; pattern and print options."], ["E-commerce", "Single-unit packing and dispatch with partner carriers."]]},
 },
}

UI = {
 "tr": {"home_url": "/", "ui_crumb_home": "Ana Sayfa", "ui_crumb_pg": "Ürün Grupları", "ui_group": "Ürün grubu", "ui_areas": "Koleksiyon alanları",
        "ui_opts_e": "Kumaş, işçilik ve marka", "ui_opts_h": "Markanıza göre ayarlanan her detay.", "ui_see": "Seçenekleri görün",
        "ui_cap": "Havlu üzerine saten dolgu nakış · atölyemizden", "ui_proc": "Süreç",
        "ui_q_h": "koleksiyonunuzu konuşalım.", "ui_q_p": "Ürün grubu bu sayfaya göre seçili gelir.",
        "proc": ["01 Numune", "02 Kumaş ve aksesuar", "03 Üretim planı", "04 Ara kontrol", "05 Final kontrol", "06 Sevkiyat"],
        "home_title": "Berke Tekstil · Türkiye'de Private Label Tekstil Üretimi",
        "home_desc": "Ev tekstili ve bebek giyim markaları için Türkiye merkezli private label üretim ve tedarik partneri. Numuneden sevkiyata tek muhatap."},
 "en": {"home_url": "/en/", "ui_crumb_home": "Home", "ui_crumb_pg": "Products", "ui_group": "Product group", "ui_areas": "Collection areas",
        "ui_opts_e": "Fabric, workmanship and brand", "ui_opts_h": "Every detail set to your brand.", "ui_see": "See options",
        "ui_cap": "Satin-fill embroidery on terry · from our atelier", "ui_proc": "Process",
        "ui_q_h": "Let's talk about your collection.", "ui_q_p": "The product group is preselected from this page.",
        "proc": ["01 Sample", "02 Fabric & trims", "03 Production plan", "04 In-line check", "05 Final check", "06 Shipment"],
        "home_title": "Berke Tekstil · Private Label Textile Manufacturer in Türkiye",
        "home_desc": "Türkiye-based private label production and supply partner for home textile and babywear brands. From sample to shipment, one contact."},
}

def url(lang, key=None):
    base = "/" if lang == "tr" else "/en/"
    if key is None: return base
    return base + PRODUCTS[key][lang]["slug"] + "/"

BASE = r"""<!doctype html>
<html lang="{{ lang }}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ desc }}">
<link rel="canonical" href="{{ site }}{{ path }}">
<link rel="alternate" hreflang="tr" href="{{ site }}{{ alt_tr }}">
<link rel="alternate" hreflang="en" href="{{ site }}{{ alt_en }}">
<link rel="alternate" hreflang="x-default" href="{{ site }}{{ alt_en }}">
<meta property="og:title" content="{{ title }}">
<meta property="og:description" content="{{ desc }}">
<meta property="og:image" content="{{ site }}/assets/media/hero-poster.jpg">
<meta name="theme-color" content="#101B30">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..110,300..800&family=Fraunces:opsz,wght@9..144,300..500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Berke Tekstil","url":"{{ site }}","email":"info@berketekstil.com","telephone":"+90 530 540 87 95","address":{"@type":"PostalAddress","streetAddress":"Akçeşme Mah. 2608 Sk. No:5","addressLocality":"Merkezefendi, Denizli","addressCountry":"TR"}}</script>
</head>
<body>
<a class="skip" href="#main">{{ t.skip }}</a>
<header class="site-h">
<div class="wrap" style="position:relative">
<a class="logo" href="{{ home }}"><b>BERKE</b><span class="mono">Tekstil</span></a>
<nav class="nav" id="nav" aria-label="Main">
<a href="{{ home }}#top">{{ t.n1 }}</a>
<a href="{{ home }}#about">{{ t.n2 }}</a>
<a href="{{ home }}#products"{% if page_pg %} aria-current="page"{% endif %}>{{ t.n3 }}</a>
<a href="{{ home }}#services">{{ t.n4 }}</a>
<a href="{{ home }}#quality">{{ t.n5 }}</a>
<a href="{{ home }}#quote">{{ t.n6 }}</a>
</nav>
<div class="h-right">
<div class="langs"><a href="{{ alt_tr }}" hreflang="tr" lang="tr" class="{{ 'on' if lang=='tr' }}">TR</a><a href="{{ alt_en }}" hreflang="en" lang="en" class="{{ 'on' if lang=='en' }}">EN</a><span title="Deutsch — in Vorbereitung" aria-disabled="true">DE</span></div>
<a href="#quote" class="btn btn-red h-cta">{{ t.cta }}</a>
<button type="button" class="menu-btn" aria-expanded="false" aria-controls="nav">{{ t.menu }}</button>
</div>
</div>
</header>
<main id="main">
{% block main %}{% endblock %}
</main>
<footer class="site-f">
<div class="wrap">
<span><b>BERKE</b> Tekstil · © 2026 · Akçeşme Mah. 2608 Sk. No:5, Merkezefendi, Denizli</span>
<span class="mono" style="font-size:11px"><a href="{{ url_home }}">{{ names.home }}</a> · <a href="{{ url_baby }}">{{ names.baby }}</a> · TR · EN · DE ({{ 'hazırlanıyor' if lang=='tr' else 'in preparation' }})</span>
</div>
</footer>
<nav class="mcta" aria-label="Quick contact"><a href="https://wa.me/905419026900">WhatsApp</a><a class="r" href="#quote">{{ t.cta }}</a></nav>
<script src="/assets/site.js" defer></script>
</body>
</html>"""

QUOTE = r"""<section id="quote" class="sec dark">
<div class="wrap g2" style="gap:56px">
<div>
<p class="mono eyebrow">{{ t.c_eyebrow }}</p>
<h2 class="h2 serif" style="margin-bottom:22px">{{ q_title or t.c_title }}</h2>
<p class="lead" style="margin-bottom:36px">{{ q_sub or t.c_sub }}</p>
<a href="https://wa.me/905419026900" class="chan"><span class="lbl">WhatsApp</span><span class="v">+90 541 902 69 00</span></a>
<a href="tel:+905305408795" class="chan"><span class="lbl">{{ t.l_phone }}</span><span class="v">+90 530 540 87 95</span></a>
<a href="mailto:info@berketekstil.com" class="chan"><span class="lbl">E-mail</span><span class="v">info@berketekstil.com</span></a>
<div class="chan" style="border-bottom:1px solid rgba(255,255,255,.18)"><span class="lbl">{{ t.l_addr }}</span><span style="font-size:16px;line-height:1.5">Akçeşme Mah. 2608 Sk. No:5, Merkezefendi, Denizli</span></div>
</div>
<form class="form" action="#" method="post">
<div class="serif" style="font-size:30px">{{ t.f_title }}</div>
<div class="row2">
<div class="field"><label for="co" class="lbl">{{ t.f_co }}</label><input id="co" name="company" type="text" autocomplete="organization" required></div>
<div class="field"><label for="em" class="lbl">{{ t.f_em }}</label><input id="em" name="email" type="email" autocomplete="email" required></div>
</div>
<fieldset>
<legend class="lbl" style="margin-bottom:10px">{{ t.f_pg }}</legend>
<div style="display:flex;gap:8px;flex-wrap:wrap">
<label class="radio"><input type="radio" name="product_group" value="home"{% if pg in (None,'home') %} checked{% endif %}>{{ t.p1 }}</label>
<label class="radio"><input type="radio" name="product_group" value="baby"{% if pg=='baby' %} checked{% endif %}>{{ t.p2 }}</label>
<label class="radio"><input type="radio" name="product_group" value="other">{{ t.f_other }}</label>
</div>
</fieldset>
<div class="row2">
<div class="field"><label for="qty" class="lbl">{{ t.f_qty }}</label><input id="qty" name="quantity" type="text" inputmode="numeric"></div>
<div class="field"><label for="dt" class="lbl">{{ t.f_date }}</label><input id="dt" name="target_date" type="date"></div>
</div>
<div class="field"><label for="note" class="lbl">{{ t.f_note }}</label><textarea id="note" name="note" rows="3"></textarea></div>
<button type="submit" class="btn btn-red" style="align-self:flex-start">{{ t.f_send }}</button>
<p class="form-ok" role="status">{{ t.sent }}</p>
</form>
</div>
</section>"""

HOME = r"""{% extends "base" %}{% block main %}
<section id="top" class="hero">
<video id="hero-video" class="cover" src="/assets/media/hero.mp4" poster="/assets/media/hero-poster.jpg" muted loop playsinline preload="auto" aria-hidden="true"></video>
<div class="scrim" aria-hidden="true"></div>
<div class="wrap hero-c">
<p class="mono" style="margin:0 0 22px;color:#D7DAE1">{{ t.eyebrow }}</p>
<h1 class="serif">{{ t.heroTitle }}</h1>
<div class="g2" style="align-items:end;gap:40px;margin-top:30px">
<div>
<p class="sub">{{ t.heroSub }}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<a href="#quote" class="btn btn-red">{{ t.cta }}</a>
<a href="#products" class="btn btn-line" style="color:#FFFFFF">{{ t.heroBtn2 }}</a>
</div>
</div>
<div>
<div style="display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:12px">
<span class="mono" style="color:#D7DAE1">{{ t.chapTitle }}</span>
<button type="button" id="hero-toggle" class="chap ctl" data-play="{{ t.play }}" data-pause="{{ t.pause }}">{{ t.pause }}</button>
</div>
<div class="chaps">
{% for c in t.chapters %}<button type="button" class="chap{% if loop.first %} on{% endif %}" data-i="{{ loop.index0 }}"><span class="chap-line"><i></i></span>0{{ loop.index }} · {{ c }}</button>{% endfor %}
</div>
</div>
</div>
</div>
</section>

<section class="strip"><div class="wrap g4">
{% for s in t.strip %}<div><div class="lbl">{{ s.k }}</div><div class="v">{{ s.v }}</div></div>{% endfor %}
</div></section>

<section id="products" class="wrap sec">
<div class="g2" style="align-items:end;margin-bottom:48px">
<div><p class="mono eyebrow">{{ t.p_eyebrow }}</p><h2 class="h2 serif">{{ t.p_title }}</h2></div>
<p class="lead">{{ t.p_sub }}</p>
</div>
<div class="g2" style="gap:24px">
<a href="{{ url_home }}" class="pcard">
<img class="media" src="/assets/media/towel.jpg" alt="{{ t.p1alt }}" loading="lazy">
<div class="body">
<div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="serif">{{ t.p1 }}</h3><span class="mono" style="color:#4A342A">01</span></div>
<p class="lead" style="font-size:16px">{{ t.p1d }}</p>
<div class="chips">{% for c in t.p1c %}<span class="chipx">{{ c }}</span>{% endfor %}</div>
<span class="more">{{ t.p1l }}</span>
</div>
</a>
<a href="{{ url_baby }}" class="pcard">
<img class="media" src="/assets/media/baby-muslin-card.jpg" alt="{{ t.p2img }}" loading="lazy">
<div class="body">
<div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="serif">{{ t.p2 }}</h3><span class="mono" style="color:#4A342A">02</span></div>
<p class="lead" style="font-size:16px">{{ t.p2d }}</p>
<div class="chips">{% for c in t.p2c %}<span class="chipx">{{ c }}</span>{% endfor %}</div>
<span class="more">{{ t.p2l }}</span>
</div>
</a>
</div>
</section>

<section id="services" class="sec cream"><div class="wrap">
<p class="mono eyebrow">{{ t.s_eyebrow }}</p>
<h2 class="h2 serif" style="margin-bottom:56px;max-width:820px">{{ t.s_title }}</h2>
<div class="g4">{% for s in t.services %}<div class="svc"><div class="mono" style="color:#4A342A;margin-bottom:16px">{{ s.n }}</div><h3>{{ s.title }}</h3><p>{{ s.desc }}</p></div>{% endfor %}</div>
</div></section>

<section class="sec dark"><div class="wrap">
<div class="g2" style="align-items:end;margin-bottom:40px">
<div><p class="mono eyebrow">{{ t.i_eyebrow }}</p><h2 class="h2 serif">{{ t.i_title }}</h2></div>
<p class="lead">{{ t.i_sub }}</p>
</div>
<div class="g21">
<div>
<div class="stage">
<video id="stitch-video" class="cover" src="/assets/media/stitch.mp4" poster="/assets/media/stitch-poster.jpg" muted loop playsinline preload="metadata" aria-hidden="true"></video>
{% for s in t.spots %}<button type="button" class="hs{% if loop.first %} on{% endif %}" data-spot="{{ loop.index0 }}" aria-label="{{ s.title }}" style="left:{{ pos[loop.index0][0] }};top:{{ pos[loop.index0][1] }}"><span>0{{ loop.index }}</span></button>{% endfor %}
</div>
<div class="scrubrow">
<button type="button" id="stitch-toggle" class="chap ctl" style="flex:none" data-play="{{ t.play }}" data-pause="{{ t.pause }}">{{ t.pause }}</button>
<label for="scrub" class="lbl" style="color:#AEB5C4;flex:none">{{ t.scrub }}</label>
<input id="scrub" class="range" type="range" min="0" max="100" step="0.1" value="0">
</div>
</div>
<div>
{% for s in t.spots %}<button type="button" class="spot{% if loop.first %} on{% endif %}" data-spot="{{ loop.index0 }}" aria-expanded="{{ 'true' if loop.first else 'false' }}"><span class="mono n">0{{ loop.index }}</span><span class="t">{{ s.title }}</span><span class="d">{{ s.desc }}</span></button>{% endfor %}
<div style="border-top:1px solid rgba(255,255,255,.18);padding-top:20px">
<button type="button" class="ar" disabled>{{ t.ar }}</button>
<p style="margin:10px 0 0;font-size:13px;line-height:1.5;color:#8F97A8">{{ t.arNote }}</p>
</div>
</div>
</div>
</div></section>

<section id="quality" class="wrap sec">
<div class="g2" style="align-items:end;margin-bottom:56px">
<div><p class="mono eyebrow">{{ t.q_eyebrow }}</p><h2 class="h2 serif">{{ t.q_title }}</h2></div>
<p class="lead">{{ t.q_sub }}</p>
</div>
<div class="g6 steps">{% for s in t.steps %}<div class="step"><div class="mono" style="color:#6E263D">{{ s.n }}</div><div class="t">{{ s.title }}</div><div class="lbl" style="margin-top:12px">{{ t.youGet }}</div><p>{{ s['get'] }}</p></div>{% endfor %}</div>
<div class="g2" style="margin-top:56px;gap:40px;align-items:center">
<div class="report">
<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:18px">
<div><div class="lbl">{{ t.r_label }}</div><div style="font-size:20px;font-weight:700;margin-top:4px">{{ t.r_title }}</div></div>
<span class="mono badge">{{ t.r_badge }}</span>
</div>
{% for r in t.report %}<div class="row"><span>{{ r.k }}</span><span class="mono" style="font-size:11px;color:{{ r.c }}">{{ r.v }}</span></div>{% endfor %}
<div class="bar"><i></i></div>
</div>
<div>
<h3 class="serif" style="margin:0 0 14px;font-size:34px;line-height:1.1">{{ t.r_h }}</h3>
<p class="lead" style="font-size:17px;margin-bottom:24px">{{ t.r_p }}</p>
<a href="#quote" class="btn btn-red">{{ t.cta }}</a>
</div>
</div>
</section>

<section id="about" class="sec cream"><div class="wrap g2" style="align-items:center">
<img src="/assets/media/atelier.jpg" alt="{{ t.a_alt }}" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block">
<div>
<p class="mono eyebrow">{{ t.a_eyebrow }}</p>
<h2 class="h2 serif" style="font-size:52px;margin-bottom:24px">{{ t.a_title }}</h2>
<p class="lead" style="font-size:17px;margin-bottom:32px">{{ t.a_body }}</p>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid #CDBFB1">
{% for s in t.stats %}<div style="padding:18px 12px 0 0"><div class="serif" style="font-size:36px">{{ s.big }}</div><div class="lbl" style="margin-top:6px">{{ s.small }}</div></div>{% endfor %}
</div>
</div>
</div></section>
""" + QUOTE + "{% endblock %}"

PRODUCT = r"""{% extends "base" %}{% block main %}
<section class="wrap">
<nav class="crumb lbl" aria-label="Breadcrumb"><a href="{{ home }}">{{ u.ui_crumb_home }}</a><span aria-hidden="true">/</span><a href="{{ home }}#products">{{ u.ui_crumb_pg }}</a><span aria-hidden="true">/</span><span style="color:#101B30" aria-current="page">{{ p.name }}</span></nav>
<div class="g2 p-hero">
<div>
<p class="mono eyebrow">{{ u.ui_group }} {{ p.n }}</p>
<h1 class="serif">{{ p.name }}</h1>
<p>{{ p.lead }}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a href="#quote" class="btn btn-red">{{ t.cta }}</a><a href="#options" class="btn btn-line">{{ u.ui_see }}</a></div>
</div>
{% if p.img %}<img class="p-media" src="/assets/media/{{ p.img }}" alt="{{ p.alt }}">{% else %}<div class="muslin p-media"><span class="ph">{{ p.ph }}</span></div>{% endif %}
</div>
</section>

<section class="sec cream" style="padding-top:96px;padding-bottom:96px"><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:24px;flex-wrap:wrap;margin-bottom:36px"><h2 class="serif" style="margin:0;font-size:48px">{{ u.ui_areas }}</h2><span class="lbl">{{ p.tiles|length }}</span></div>
<div class="g4">{% for x in p.tiles %}<div class="tile">{% if x.img %}<img class="img" src="/assets/media/{{ x.img }}" alt="{{ x.alt }}" loading="lazy">{% else %}<div class="muslin img" style="aspect-ratio:4/5"><span class="ph">{{ x.ph }}</span></div>{% endif %}<h3>{{ x.t }}</h3><p>{{ x.d }}</p></div>{% endfor %}</div>
</div></section>

{% if p.care %}<section class="wrap" style="padding-top:96px"><img src="/assets/media/baby-accessories-wide.jpg" alt="{{ p.wide_alt }}" loading="lazy" style="width:100%;aspect-ratio:16/7;object-fit:cover;display:block"></section>
<section class="wrap sec" style="padding-bottom:0">
<h2 class="h2 serif" style="font-size:48px;margin-bottom:40px;max-width:820px">{{ p.care.h }}</h2>
<div class="g4">{% for c in p.care['items'] %}<div class="care"><h3>{{ c[0] }}</h3><p>{{ c[1] }}</p></div>{% endfor %}</div>
</section>{% endif %}

<section id="options" class="wrap sec"><div class="g2" style="align-items:start">
<div>
<p class="mono eyebrow">{{ u.ui_opts_e }}</p>
<h2 class="serif" style="margin:0 0 32px;font-size:52px;line-height:1.05">{{ u.ui_opts_h }}</h2>
{% for o in p.opts %}<div class="opt"><span class="lbl" style="padding-top:3px">{{ o[0] }}</span><span>{{ o[1] }}</span></div>{% endfor %}
</div>
<figure style="margin:0">
<video data-loop src="/assets/media/stitch.mp4" poster="/assets/media/stitch-poster.jpg" muted loop playsinline preload="metadata" aria-hidden="true" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block"></video>
<figcaption class="lbl" style="margin-top:12px">{{ u.ui_cap }}</figcaption>
</figure>
</div></section>

<section class="pstrip"><div class="wrap"><span class="lbl" style="color:#6E263D">{{ u.ui_proc }}</span>{% for s in u.proc %}<span>{{ s }}</span>{% endfor %}</div></section>
""" + QUOTE + "{% endblock %}"

env = Environment(loader=DictLoader({"base": BASE, "home": HOME, "product": PRODUCT}), autoescape=select_autoescape(default=True))
SITE = os.environ.get("SITE_URL", "https://berketekstil.com")
POS = [["54%", "24%"], ["57%", "52%"], ["40%", "60%"], ["8%", "70%"]]

def write(path, html):
    fp = os.path.join(OUT, path.lstrip("/"), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(html)

shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(os.path.join(ROOT, "static"), OUT)
urls = []
for lang, t in (("tr", TR), ("en", EN)):
    u = UI[lang]
    common = dict(lang=lang, t=t, u=u, site=SITE, home=url(lang), url_home=url(lang, "home"), url_baby=url(lang, "baby"),
                  names={"home": PRODUCTS["home"][lang]["name"], "baby": PRODUCTS["baby"][lang]["name"]}, pos=POS)
    html = env.get_template("home").render(**common, title=u["home_title"], desc=u["home_desc"], path=url(lang),
                                           alt_tr=url("tr"), alt_en=url("en"), page_pg=False, pg=None, q_title=None, q_sub=None)
    write(url(lang), html); urls.append(url(lang))
    for key in ("home", "baby"):
        p = PRODUCTS[key][lang]
        html = env.get_template("product").render(**common, p=p, title=p["title"], desc=p["desc"], path=url(lang, key),
                                                  alt_tr=url("tr", key), alt_en=url("en", key), page_pg=True, pg=p["pg"],
                                                  q_title=(p["name"] + " — " + u["ui_q_h"]) if lang == "en" else (p["name"] + " " + u["ui_q_h"]),
                                                  q_sub=u["ui_q_p"])
        write(url(lang, key), html); urls.append(url(lang, key))

open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{p}</loc></url>\n" for p in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
json.dump({"cleanUrls": True, "trailingSlash": True,
           "headers": [{"source": "/assets/media/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}],
           "redirects": [{"source": "/tr", "destination": "/", "permanent": True},
                         {"source": "/tr/hakkimizda", "destination": "/#about", "permanent": True},
                         {"source": "/tr/hizmetlerimiz", "destination": "/#services", "permanent": True},
                         {"source": "/tr/urunler", "destination": "/#products", "permanent": True},
                         {"source": "/tr/iletisim", "destination": "/#quote", "permanent": True}]},
          open(os.path.join(OUT, "vercel.json"), "w"), indent=1)
print("\n".join(urls))
