# Berke Tekstil · web sitesi

Ev tekstili, bebek giyim, hoodie ve sweatshirt, çanta ve kalemlik, otel tekstili üreten Berke Tekstil için iki dilli (TR, EN) statik B2B site.
Tasarım ve geliştirme: TCM Global.

## Metinleri nereden düzenlerim?

GitHub'da dosyayı açıp kalem simgesiyle düzenleyin. `main`'e kaydettiğiniz her değişiklik Vercel'de 1–2 dakikada yayına girer.

| Ne değişecek | Dosya |
|---|---|
| Türkçe metinler | `content/tr.yml` |
| İngilizce metinler | `content/en.yml` |
| Telefon, WhatsApp, e-posta, adres, yıllar | `content/site.yml` → `company` |
| Açılış videosu | `assets/media/fabric.mp4` (aynı adla yeni dosya yükleyin) |
| Ürün gruplarının sırası ve kart görselleri | `content/site.yml` → `products` |
| Teklif formunun gideceği adres | `content/site.yml` → `form_endpoint` |

### Almanca eklemek

`content/en.yml` dosyasını `content/de.yml` olarak kopyalayıp çevirin, `content/site.yml` → `languages` listesine `de` ekleyin.

## Yapı

```
content/          Metinler ve site ayarları
src/templates/    Sayfa şablonları (Jinja2)
assets/           CSS, JS, görsel ve videolar
build.py          content + şablon → _site/ (Vercel bunu otomatik çalıştırır)
```

## Bilgisayarda önizleme

```bash
pip install jinja2 pyyaml
python3 build.py
cd _site && python3 -m http.server 8000
```
