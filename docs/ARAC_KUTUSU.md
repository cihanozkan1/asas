# Araç kutusu: mantık hatasız ve kaliteli video için (ücretsiz, telifsiz)

## 1. Rota mantığı (yol denizden, gemi karadan geçmez)
| Araç | Ne yapar |
|---|---|
| `road([(lat,lon), ...], at, ...)` (`helpers.py`) | Natural Earth 10 m yol ağında (kamu malı) en kısa gerçek yol rotası; boşluklar 90 km'ye kadar köprülenir. `tools/roadroute.py` |
| `sea_points(a, b)` / `sea_lane(a, b, at)` / `ship(sea_points(a, b), ...)` | searoute (Apache-2.0) ile karadan geçmeyen deniz yolu |
| `tools/validate_routes.mjs` | gemi suda, araba/tren/yürüyen karada mı denetler (10 m kıyı). `pipeline.mjs` render öncesi otomatik çalıştırır, hata varsa durur (`--skip-route-check` ile atlanır). `medium: 'land'|'water'`, dar kanal/boğaz için `check: false` |
Kural: yol/gemi rotası elle nokta yazarak değil `road()` / `sea_points()` ile kurulur. Yerel kısa rotalar (köy yolu, feribot) elle yazılabilir ama denetimden geçmek zorunda.

## 2. VFX klibi (gerçek patlama, ateş, duman, yanardağ)
Motor `clip` elemanını biliyor: `clip('<ad>', at, lat=, lon=, size=, blend='screen')`. Klipler `assets/vfx/<ad>/` altında WebP kare dizisi (alfa destekli).
- `python3 tools/vfx_ingest.py <dosya> <ad> --key black|alpha|green|none --dur 6 --license "..." --source <url>`: indirilen herhangi bir videoyu içe aktarır. `black` = siyah zeminli ateş/duman/patlama (parlaklık → saydamlık), `alpha` = saydam kanallı (ProRes 4444/WebM), `green` = yeşil perde.
- `python3 tools/commons_search.py "lava fountain"` + `python3 tools/vfx_fetch.py "File:..." <ad>`: Wikimedia Commons'tan yalnız kamu malı/CC0 video bulur, lisansı dosyadan okur, indirir, `docs/LISANSLAR.md`'ye yazar. Dikkat: gerçek görüntülerde kurum logosu / zaman damgası olabilir (ör. PHIVOLCS) → kırp ya da kullanma; logo yasak.
- Ücretsiz profesyonel paketler (hesap açıp elle indirilir, sonra `vfx_ingest.py`): [ActionVFX ücretsiz](https://www.actionvfx.com/blog/450-free-vfx-stock-footage-assets-ready-for-download), [FX Elements ücretsiz](https://www.fxelements.com/free) (hesap + bülten gerekir; patlama, enkaz, toz, namlu alevi, duman), [MyCreativeFX](https://mycreativefx.com/), [PremiumBeat Detonate](https://www.premiumbeat.com/blog/free-explosion-sfx-vfx-elements/). İndirmeden önce lisans metni okunur ve `--license` ile kayda geçirilir.
- Dosya bırakma yeri: `assets/vfx/inbox/` (gitignore dışı kalmaz; ham dosya büyükse git'e girmez, yalnız kareler girer).

## 3. Diğer
- `eruption` (lav, kül, parıltı) ve `wall` + `siege` (top, isabet, yıkılan sur) yerleşik ama gerçek VFX klibi kadar iyi değil: iyi klip varsa `clip` tercih edilir.
- Blender (bpy) bu sunucuda kullanılamıyor (GPU yok).
