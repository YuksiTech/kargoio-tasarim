#!/usr/bin/env python3
"""Tasarım taslaklarını statik sayfalara çevirir: python3 build.py"""
import html
import json
import re
from pathlib import Path

KOK = Path(__file__).parent
KAYNAK = KOK / "kaynak"
CIKTI = KOK / "ekranlar"
LOGO_BLOB = re.compile(r"/_blob/[0-9a-f]{32}")

TASLAKLAR = [
    ("G", "Kargoio Premium", "F ve C'nin harmanı: krem zemin, kırmızı başlık blokları ve büyük kutular; ince iri rakamlar, logodaki io işareti, canlı Şimdi kartı, WhatsApp'tan kargo, kart kart onaylanan koyu yönetim.", "Önerilen",
     [("G-Giris", "Giriş"), ("G-Ana", "Ana sayfa"), ("G-Gonder", "Kargo gönder"), ("G-Etiket", "Etiket hazır"), ("G-Takip", "Kargo takip"), ("G-Onay", "Yönetim")]),
    ("H", "Kırmızı Enerji+", "C ağırlıklı: krem zemin, tam kırmızı bloklar, büyük kutular, kutu çizimleri ve kalın yazı; F'den canlı kargo kartı, WhatsApp'tan kargo, io işareti ve etiket hazır anı.", "C ağırlıklı",
     [("H-Giris", "Giriş"), ("H-Ana", "Ana sayfa"), ("H-Gonder", "Kargo gönder"), ("H-Etiket", "Etiket hazır"), ("H-Takip", "Kargo takip"), ("H-Onay", "Yönetim")]),
    ("I", "Kargoio Gece", "F ağırlıklı: koyu giriş, ince iri rakamlar, harita ve koyu yönetim; C'den büyük kırmızı Kargo gönder kutusu, pembe kutular, kalın adım çubukları ve kutu çizimi.", "F ağırlıklı",
     [("I-Giris", "Giriş"), ("I-Ana", "Ana sayfa"), ("I-Gonder", "Kargo gönder"), ("I-Etiket", "Etiket hazır"), ("I-Takip", "Kargo takip"), ("I-Onay", "Yönetim")]),
    ("F", "Kargoio", "Hepsinin harmanı. Logodaki io işareti, canlı Şimdi kartı, WhatsApp'tan kargo, etiket hazır anı ve koyu temalı yönetim.", "İşveren beğendi",
     [("F-Giris", "Giriş"), ("F-Ana", "Ana sayfa"), ("F-Gonder", "Kargo gönder"), ("F-Etiket", "Etiket hazır"), ("F-Takip", "Kargo takip"), ("F-Onay", "Yönetim")]),
    ("C", "Kırmızı Enerji", "Sıcak ve cesur; büyük kutular, tam kırmızı başlıklar.", "İşveren beğendi",
     [("C-Giris", "Giriş"), ("C-Ana", "Ana sayfa"), ("C-Takip", "Kargo takip"), ("C-Onay", "Yönetim")]),
    ("E", "io", "Logonun i / o işaretinden doğan tasarım: nokta başlangıç, eğik çizgi yol, halka varış. Kırmızı-beyaz, sade.", "",
     [("E-Giris", "Giriş"), ("E-Ana", "Ana sayfa"), ("E-Gonder", "Kargo gönder"), ("E-Takip", "Kargo takip"), ("E-Onay", "Yönetim")]),
    ("D", "Kargoio Global", "Logoya yakın geometrik yazı, ince iri rakamlar, firma karşılaştırmalı kargo gönderme.", "",
     [("D-Giris", "Giriş"), ("D-Ana", "Ana sayfa"), ("D-Gonder", "Kargo gönder"), ("D-Takip", "Kargo takip"), ("D-Onay", "Yönetim")]),
    ("A", "Gece Kırmızısı", "Koyu, lüks, sakin. Sistem yazı tipi.", "",
     [("Main", "Giriş"), ("A-Ana", "Ana sayfa"), ("A-Takip", "Kargo takip"), ("A-Onay", "Yönetim")]),
    ("B", "Canlı Durum", "Net ve akıllı; canlı durum kartı ve şehir kodlu rota çizgisi.", "",
     [("B-Giris", "Giriş"), ("B-Ana", "Ana sayfa"), ("B-Takip", "Kargo takip"), ("B-Onay", "Yönetim")]),
]

HEAD = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{baslik}</title>
{ek}
</head>
"""


def ekrani_cevir(ad: str) -> None:
    kaynak = (KAYNAK / f"{ad}.dc.html").read_text(encoding="utf-8")
    props = re.search(r"data-props='([^']*)'", kaynak)
    vurgu = "#E2001A"
    if props:
        veri = json.loads(html.unescape(props.group(1)))
        vurgu = veri.get("accent", {}).get("default", vurgu)
    helmet = re.search(r"<helmet>(.*?)</helmet>", kaynak, re.S).group(1)
    govde = re.search(r"</helmet>(.*?)</x-dc>", kaynak, re.S).group(1)
    baslik = re.search(r"<title>(.*?)</title>", kaynak).group(1)
    sayfa = HEAD.format(baslik=baslik, ek=helmet.strip()) + "<body>\n" + govde.strip() + "\n</body>\n</html>\n"
    sayfa = sayfa.replace("{{accent}}", vurgu)
    sayfa = LOGO_BLOB.sub("../assets/logo.png", sayfa)
    assert "{{" not in sayfa, ad
    (CIKTI / f"{ad}.html").write_text(sayfa, encoding="utf-8")


def galeri() -> str:
    bolumler = []
    for harf, ad, aciklama, onerilen, ekranlar in TASLAKLAR:
        kartlar = "\n".join(
            f'<figure class="ekran"><div class="cerceve"><iframe src="ekranlar/{dosya}.html" title="{harf} · {etiket}" loading="lazy" scrolling="no"></iframe></div>'
            f'<figcaption>{etiket} <a href="ekranlar/{dosya}.html" target="_blank" rel="noopener">Tam ekran ↗</a></figcaption></figure>'
            for dosya, etiket in ekranlar
        )
        rozet = f'<span class="rozet{" ikincil" if onerilen != "Önerilen" else ""}">{onerilen}</span>' if onerilen else ""
        bolumler.append(
            f'<section id="{harf}"><header class="bolum"><span class="harf">{harf}</span><div><h2>{ad} {rozet}</h2><p>{aciklama}</p></div></header>'
            f'<div class="sira">{kartlar}</div></section>'
        )
    gezinme = " ".join(f'<a href="#{h}">{h} · {a}</a>' for h, a, *_ in TASLAKLAR)
    return HEAD.format(baslik="Kargoio · Uygulama Tasarım Taslakları", ek=STIL) + f"""<body>
<main>
  <header class="ust">
    <img src="assets/logo.png" alt="Kargoio" class="logo">
    <h1>Uygulama tasarım taslakları</h1>
    <p>Kurumsal, bayi ve yönetim tek uygulamada. Ekranlardaki isim, tutar ve fiyatlar örnek veridir.</p>
    <nav>{gezinme}</nav>
  </header>
  {''.join(bolumler)}
  <footer>Kargoio · Ekim 2026</footer>
</main>
</body>
</html>
"""


STIL = """<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{--zemin:#F1F0EC;--metin:#0E0E12;--ikincil:#5E5F66;--kirmizi:#E2001A;--cizgi:#E2E1DC}
*{box-sizing:border-box}
body{margin:0;background:var(--zemin);color:var(--metin);font-family:'Figtree',system-ui,sans-serif}
main{max-width:1500px;margin:0 auto;padding:40px 16px 64px}
.ust{padding:8px 8px 24px}
.logo{height:40px;width:auto;mix-blend-mode:multiply}
h1{font-family:'Outfit',sans-serif;font-weight:300;font-size:clamp(30px,5vw,52px);letter-spacing:-1px;margin:22px 0 8px}
.ust p{color:var(--ikincil);margin:0;font-size:16px}
nav{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
nav a{color:var(--metin);text-decoration:none;font-size:14px;font-weight:500;background:#fff;border:1px solid var(--cizgi);border-radius:999px;padding:8px 14px}
nav a:hover{border-color:var(--metin)}
section{margin-top:40px}
.bolum{display:flex;gap:16px;align-items:flex-start;padding:0 8px}
.harf{flex:0 0 auto;width:48px;height:48px;border-radius:50%;background:var(--metin);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Outfit',sans-serif;font-size:22px}
h2{font-family:'Outfit',sans-serif;font-weight:400;font-size:28px;margin:4px 0 4px;letter-spacing:-.4px}
.bolum p{margin:0;color:var(--ikincil);max-width:760px}
.rozet.ikincil{background:#0E0E12}
.rozet{display:inline-block;vertical-align:middle;font-family:'Figtree',sans-serif;font-size:12px;font-weight:600;color:#fff;background:var(--kirmizi);border-radius:999px;padding:4px 10px;margin-left:6px}
.sira{display:flex;gap:28px;overflow-x:auto;padding:22px 8px 12px;scroll-snap-type:x mandatory}
.ekran{margin:0;flex:0 0 auto;scroll-snap-align:start}
.cerceve{width:312px;height:675px;border-radius:36px;overflow:hidden;background:#fff;box-shadow:0 20px 50px rgba(14,14,18,.14),0 0 0 1px rgba(14,14,18,.06)}
.cerceve iframe{width:390px;height:844px;border:0;transform:scale(.8);transform-origin:0 0}
figcaption{display:flex;justify-content:space-between;margin-top:12px;font-size:14px;font-weight:600;padding:0 6px}
figcaption a{color:var(--ikincil);font-weight:500;text-decoration:none}
figcaption a:hover{color:var(--metin)}
footer{margin-top:56px;color:var(--ikincil);font-size:13px;padding:0 8px}
</style>"""


def main() -> None:
    CIKTI.mkdir(exist_ok=True)
    for _, _, _, _, ekranlar in TASLAKLAR:
        for dosya, _ in ekranlar:
            ekrani_cevir(dosya)
    (KOK / "index.html").write_text(galeri(), encoding="utf-8")
    (KOK / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print("tamam:", sum(len(t[4]) for t in TASLAKLAR), "ekran")


if __name__ == "__main__":
    main()
