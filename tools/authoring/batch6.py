from helpers import *

# ------------------------------------------------------------------ 10. CHIMBORAZO (globe)
CH = (-1.469, -78.817)
EV = (27.988, 86.925)
save('chimborazo', meta(
    'The Mountain Closest to Space Is NOT Everest 🏔️🚀🤯',
    "Everest 🇳🇵 is the highest mountain above sea level at 8,849 m, but it's not the point closest to space! 🚀 Earth isn't a perfect ball: it's thicker at the equator. Chimborazo in Ecuador 🇪🇨 is only 6,263 m high, but it sits just one degree south of the equator, on top of that bulge. Its summit is 6,384.4 km from Earth's center, about 2.1 km farther out than Everest's 🤯",
    ["The closest point to space is in Ecuador, not Nepal 🤯🇪🇨", "Did you know Earth is fatter at the equator? 👇", "Which record should we explain next? 🗺️"],
    ['chimborazo', 'everest', 'ecuador', 'highest mountain', 'closest to space', 'equatorial bulge', 'earth', 'andes', 'geography', 'maps', 'learn']),
    [
        S("Everest is the highest mountain on Earth. But it's not the point closest to space.", [
            hook('CLOSEST POINT TO *SPACE*?', at=0.05, until='Earth'), ping(*EV, 'Everest', color='#ffd60a'), dot('Everest', *EV, 'Everest', dy=-56), stamp('NOT #1?', 'closest', size=90)],
          cam=at_(25, 80, 1.6), no_claim=True),
        S("That title goes to Chimborazo, a volcano in Ecuador, only 6,263 meters high.", [
            ping(*CH, 'Chimborazo', color='#ff5a5f'), dot('Chimborazo', *CH, 'Chimborazo', dy=-56), hl('ECU', 'flag:ec', 'Ecuador', fillOpacity=0.85), cnt('6,263 m', '6,263', size=170)],
          cam=at_(-1.5, -78.8, 2.2),
          src=[src('Chimborazo is 6,263 m high.', 'Chimborazo', 'With an elevation of 6,263 m (20,548 ft), Chimborazo is the highest mountain in Ecuador')]),
        S("Compared to Everest, it's more than two and a half kilometers lower.", [
            bars([('Everest', 8849, '8,849 m', '#ffd60a', 'np'), ('Chimborazo', 6263, '6,263 m', '#ff5a5f', 'ec')], 'lower', orient='v', shape='mountain', height=380)],
          style='neon',
          src=[src('Chimborazo is 2,585 m lower than Everest above sea level.', 'Chimborazo', 'Despite being 2,585 m (8,481 ft) lower in elevation above sea level, it is 6,384.4 km')]),
        S("So how can it be closer to space? Because Earth is not a perfect ball.", [q(0, -60, 'how')], cam=at_(0, -60, 1.0), style='neon', no_claim=True),
        S("Earth is thicker at the equator than from pole to pole, like it's wearing a belt.", [
            route([(0, -180), (0, -90), (0, 0), (0, 90), (0, 180)], 'equator', rhumb=True, color='#ffd60a', width=10, drawDur=1.4, hold=2), slam('EQUATOR', 6, -40, 'equator', size=70)],
          cam=at_(10, -60, 1.0),
          src=[src('Earth is thicker at the equator than pole to pole.', 'Chimborazo', 'the Earth is thicker at the Equator than it is from pole to pole')]),
        S("And Chimborazo sits just one degree south of the equator, right on top of that bulge.", [
            ping(*CH, 'Chimborazo', color='#ff5a5f'), meas((0, -78.8), CH, '1°', 'degree', countUp=False)],
          cam=at_(-0.5, -78.8, 5),
          src=[src('It lies one degree south of the equator.', 'Chimborazo', 'Chimborazo is one degree south of the Equator')]),
        S("Its summit is 6,384.4 kilometers from the center of the Earth.", [
            cnt('6,384.4 km', '6,384.4', size=150), tilt('summit', deg=36, until=3.5)],
          cam=at_(-1.5, -78.8, 6),
          src=[src('Its summit is 6,384.4 km from Earth\'s center.', 'Chimborazo', 'it is 6,384.4 km (3,967.1 mi) from the Earth\'s center')]),
        S("That's about 2.1 kilometers farther out than the top of Everest.", [
            bars([('Chimborazo', 6384.4, '6,384.4 km', '#ff5a5f', 'ec'), ('Everest', 6382.3, '6,382.3 km', '#ffd60a', 'np')], 'farther', screen=[0.5, 0.3], labelWidth=260),
            stamp('+2.1 KM', '2.1', size=100)],
          cam=at_(0, -78.8, 1.6),
          src=[src('About 2.1 km farther than Everest\'s summit.', 'Chimborazo', 'it is 6,384.4 km (3,967.1 mi) from the Earth\'s center, 2.1 km (1.3 mi) farther than')]),
    ],
    keywords={'chimborazo': '#ff5a5f', 'everest': '#ffd60a', 'equator': '#ffd60a', 'space': '#2de2e6'},
    style='globe', captions={'theme': 'impact'})

# ------------------------------------------------------------------ 11. MÄRKET (atlas)
MK = (60.3009, 19.1313)
import json as _j, os as _o
_B = _j.load(open(_o.path.join(ROOT, 'videos/market_island/borders.json')))
BNEW, BOLD = [tuple(p) for p in _B['border_new']], [tuple(p) for p in _B['border_old']]
LH = (60.3011, 19.1311)
save('market_island', meta(
    'The Island With the Weirdest Border 🇸🇪🇫🇮🤯 Märket',
    "Märket is a tiny rocky island in the Baltic Sea, split between Sweden 🇸🇪 and Finland (Åland) 🇫🇮 since 1809. In 1885 Finland built a lighthouse on it… on the Swedish side! 😅 In 1985 the two countries redrew the border into a strange zigzag, so the lighthouse ended up in Finland without either country losing any land 🤯 The border is marked by holes drilled in the rock, and it's checked every 25 years.",
    ["They moved a border instead of a lighthouse 🤯🇸🇪🇫🇮", "Would you visit Märket? 👇", "Which border should we explain next? 🗺️"],
    ['market island', 'märket', 'sweden', 'finland', 'aland', 'lighthouse', 'baltic sea', 'weird borders', 'geography', 'maps', 'learn']),
    [
        S("This is one of the strangest borders in the world, on a tiny island in the Baltic Sea.", [
            hook('THE WEIRDEST *BORDER*', at=0.05, until='world'), hl('SWE', 'flag:se', 'Baltic', fillOpacity=0.6), hl('FIN', 'flag:fi', 'Baltic', fillOpacity=0.6), ping(*MK, 'island', color='#ff3b3b')],
          cam=at_(61, 19.5, 5), no_claim=True),
        S("It's called Märket, and since 1809 it has been split between Sweden and Finland.", [
            year(1809, '1809'), vs(('se', 'Sweden'), ('fi', 'Finland'), 'split', screen=[0.5, 0.32])],
          cam=at_(60.3, 19.13, 40),
          src=[src('The island was divided in 1809 by the Treaty of Fredrikshamn.', 'Märket', 'Märket has been divided between the two countries since the Treaty of Fredrikshamn of 1809 defined the border between Sweden and Grand Duchy of Finland as going through the middle of the island.')]),
        S("In 1885, Finland built a lighthouse on its highest point. But that spot was on the Swedish half.", [
            year(1885, '1885'), char('lighthouse_keeper', 'lighthouse', say='Wrong half!', screen=(0.25, 0.62)),
            hl({'geojson': 'sweden_old.geojson'}, 'flag:se', 'Swedish', fillOpacity=0.9), hl({'geojson': 'finland_old.geojson'}, 'flag:fi', 'Finland', fillOpacity=0.9),
            route(BOLD, 'built', rhumb=True, color='#ffffff', width=7, dashed=True, dash=[14, 10], drawDur=0.8), icon('🗼', *LH, 'lighthouse', size=110)],
          cam=at_(60.3009, 19.1318, 14500), era='history', tr='film', style='vintage',
          src=[src('In 1885 the lighthouse was built on the Swedish portion of the island.', 'Märket', 'However, the location selected was within the Swedish portion of the island.')]),
        S("So in 1985, the two countries did something clever. Instead of moving the lighthouse, they moved the border.", [
            year(1985, '1985'), stamp('MOVE THE BORDER', 'moved', size=78), icon('🗼', *LH, 0.05, size=110), hl({'geojson': 'sweden_old.geojson'}, 'flag:se', 0.05, fillOpacity=0.9), hl({'geojson': 'finland_old.geojson'}, 'flag:fi', 0.05, fillOpacity=0.9), route(BOLD, 0.05, rhumb=True, color='#ffffff', width=7, dashed=True, dash=[14, 10], drawDur=0.1)],
          cam=at_(60.3009, 19.1318, 14500), style='atlas', tr='flash',
          src=[src('The border was adjusted in 1985 so the lighthouse is on Finnish territory.', 'Märket', 'As a result, the border was adjusted in 1985 so that the lighthouse is now located on Finnish territory')]),
        S("The new border zigzags around the lighthouse, so it ends up in Finland.", [
            hl({'geojson': 'sweden_new.geojson'}, 'flag:se', 'zigzags', fillOpacity=0.9), hl({'geojson': 'finland_new.geojson'}, 'flag:fi', 'zigzags', fillOpacity=0.9),
            route(BNEW, 'zigzags', rhumb=True, color='#ffd60a', width=9, drawDur=1.6), icon('🗼', *LH, 0.05, size=110), pill('SIMPLIFIED MAP', 0.05, bg='#111827', size=34, screen=(0.5, 0.2))],
          cam=at_(60.3009, 19.1318, 14500, bearing=-3), style='atlas',
          src=[src('The adjusted border takes the form of an inverted S.', 'Märket', "The adjusted border takes the form of an inverted 'S'.")]),
        S("And no country lost any land. Both sides still have exactly the same area.", [
            hl({'geojson': 'sweden_new.geojson'}, 'flag:se', 0.05, fillOpacity=0.9), hl({'geojson': 'finland_new.geojson'}, 'flag:fi', 0.05, fillOpacity=0.9),
            route(BNEW, 0.05, rhumb=True, color='#ffd60a', width=9, drawDur=0.1), vs(('se', 'Sweden'), ('fi', 'Finland'), 'same', screen=[0.5, 0.25]), cnt('=', 'area', size=150, screen=[0.5, 0.38])],
          cam=at_(60.3009, 19.1318, 14500), style='atlas',
          src=[src('No net transfer of territory occurred.', 'Märket', 'The adjustment was carried out such that no net transfer of territory occurred.')]),
        S("Today the border is marked by holes drilled into the rock, and it's inspected every 25 years.", [
            hl({'geojson': 'sweden_new.geojson'}, 'flag:se', 0.05, fillOpacity=0.9), hl({'geojson': 'finland_new.geojson'}, 'flag:fi', 0.05, fillOpacity=0.9),
            route(BNEW, 0.05, rhumb=True, color='#ffd60a', width=9, drawDur=0.1),
            *[icon('🕳️', la, lo, 'holes', size=60) for la, lo in BNEW[1:-1]], cnt('25 years', '25', size=160)],
          cam=at_(60.3009, 19.1318, 13500, bearing=3), style='atlas',
          src=[src('The border is marked by drilled holes.', 'Märket', 'The border is marked by holes drilled into the rock, because the seasonal drift ice would shear off any protruding markers.'),
               src('Resurveyed every 25 years.', 'Märket', 'The border is regularly resurveyed every 25 years by officials representing both countries.')]),
    ],
    keywords={'sweden': '#5ec8ff', 'finland': '#ffd60a', 'märket': '#ff5a5f', 'lighthouse': '#ffd60a'},
    styles={'now': 'atlas', 'history': 'vintage'}, captions={'theme': 'pop'})

# ------------------------------------------------------------------ 12. GIBRALTAR (satellite)
GIB = 'Strait_of_Gibraltar'
save('gibraltar_bridge', meta(
    "Why There's No Bridge Between Europe and Africa 🌉🇪🇸🇲🇦",
    "At the Strait of Gibraltar, Europe 🇪🇸 and Africa 🇲🇦 are only about 14.2 km apart. So why no bridge? 🌉 The sea there is 300 to 900 m deep, and two strong currents pass through it: lighter Atlantic water flows in on top, while heavy, salty Mediterranean water flows out underneath 🌊 Spain and Morocco have studied an undersea rail tunnel since the 1980s, but after four decades of talks it still hasn't been built 🤯",
    ["Only 14 km between Europe and Africa… and still no bridge 🤯🌉", "Would you rather cross by bridge or tunnel? 👇", "Which strait should we explain next? 🗺️"],
    ['strait of gibraltar', 'europe', 'africa', 'spain', 'morocco', 'bridge', 'tunnel', 'mediterranean', 'geography', 'maps', 'learn']),
    [
        S("Here, Europe and Africa are only about 14 kilometers apart.", [
            hook('WHY NO *BRIDGE*?', at=0.05, until='Africa'), meas((36.02, -5.6), (35.9, -5.52), '14.2 km', 'kilometers'),
            hl('ESP', 'flag:es', 'Europe', fillOpacity=0.7), hl('MAR', 'flag:ma', 'Africa', fillOpacity=0.7)],
          cam=at_(36.0, -5.6, 20, bearing=-3),
          src=[src('The narrowest point is 14.2 km.', GIB, '7.7 nautical miles (14.2 kilometers, 8.9 statute miles)')]),
        S("It's the Strait of Gibraltar, the only door between the Atlantic and the Mediterranean.", [
            slam('GIBRALTAR', 36.2, -5.4, 'Gibraltar', size=70), lab('ATLANTIC', 35.9, -6.3, 'Atlantic', style='map', size=46), lab('MEDITERRANEAN', 36.1, -4.6, 'Mediterranean', style='map', size=42)],
          cam=at_(36.0, -5.5, 12),
          src=[src('The strait connects the Atlantic to the Mediterranean and separates Europe from Africa.', GIB, 'is a narrow strait that connects the Atlantic Ocean to the Mediterranean Sea and separates Europe from Africa')]),
        S("On the north side are Spain and British Gibraltar. On the south side, Morocco and the Spanish city of Ceuta.", [
            dot('Gibraltar 🇬🇧', 36.14, -5.35, 'British', dy=-54, size=40), dot('Ceuta 🇪🇸', 35.89, -5.32, 'Ceuta', dy=54, size=40), ping(36.14, -5.35, 'British', color='#ffd60a'), ping(35.89, -5.32, 'Ceuta', color='#ffd60a')],
          cam=at_(36.0, -5.45, 18),
          src=[src('North: Spain and Gibraltar; South: Morocco and Ceuta.', GIB, 'On the northern side of the Strait are Spain and Gibraltar (a British overseas territory in the Iberian Peninsula). On the southern side are Morocco and Ceuta (a Spanish autonomous city in northern Africa).')]),
        S("So why is there no bridge? First, the water is deep. Between 300 and 900 meters.", [
            tilt('deep', deg=40, until=5), bars([('Strait depth', 900, '900 m', '#1d4ed8'), ('Eiffel Tower', 330, '330 m', '#9ca3af')], 'deep', orient='v', height=380, screen=[0.5, 0.33])],
          cam=at_(35.95, -5.55, 22),
          src=[src('The seabed is 300 to 900 m deep.', GIB, "The Strait's depth ranges between 300 and 900 metres"),
               src('The Eiffel Tower is 330 m tall.', 'Eiffel_Tower', '330 metres')]),
        S("And two currents run through it, one on top of the other.", [
            flow([(35.95, -6.6), (35.97, -5.8), (36.0, -5.0)], 'currents', color='#5ec8ff', width=14), flow([(35.88, -4.9), (35.9, -5.7), (35.92, -6.5)], 'other', color='#1d4ed8', width=14)],
          cam=at_(35.95, -5.7, 14),
          src=[src('Surface water flows east; deeper, saltier water flows west.', GIB, 'A smaller amount of deeper, saltier and therefore denser waters continually flow westwards (the Mediterranean outflow), while a larger amount of surface waters with lower salinity and density continually flow eastwards')]),
        S("Lighter water flows in on the surface, while heavy, salty Mediterranean water flows out underneath.", [
            lab('SURFACE IN ➜', 36.05, -5.9, 'Lighter', style='pill', bg='#0ea5e9', size=42), lab('⬅ DEEP OUT', 35.85, -5.4, 'Mediterranean', style='pill', bg='#1e3a8a', size=42)],
          src=[src('Lighter surface water flows east; denser, saltier water flows west beneath.', GIB, 'A smaller amount of deeper, saltier and therefore denser waters continually flow westwards (the Mediterranean outflow), while a larger amount of surface waters with lower salinity and density continually flow eastwards')]),
        S("Spain and Morocco started talking about a tunnel under the strait in the 1980s.", [
            year(1980, '1980s'), route([(36.03, -5.62), (35.97, -5.65), (35.87, -5.68), (35.78, -5.8)], 'tunnel', color='#ffd60a', width=8, dashed=True, dash=[16, 10], drawDur=1.6),
            vs(('es', 'Spain'), ('ma', 'Morocco'), 'Spain', screen=[0.5, 0.3])],
          cam=at_(35.92, -5.7, 16), tr='flash',
          src=[src('Spain and Morocco began discussing a tunnel in the 1980s.', GIB, 'Discussion between Spain and Morocco of a tunnel under the strait began in the 1980s.')]),
        S("In 2003, both countries agreed to explore an undersea rail tunnel, to connect their train networks.", [
            year(2003, '2003', light=True), icon('🚆', 35.95, -5.65, 'rail', size=120)],
          cam=at_(35.92, -5.7, 16),
          src=[src('In December 2003 both countries agreed to explore an undersea rail tunnel.', GIB, 'In December 2003, both countries agreed to explore the construction of an undersea rail tunnel to connect their rail systems across the Strait.')]),
        S("More than forty years later, it still hasn't been built.", [stamp('STILL WAITING', 'built', size=86), cnt('40+ years', 'forty', size=150)],
          cam=at_(36.0, -5.6, 12, bearing=3),
          src=[src('Talks began in the 1980s; no tunnel exists yet.', GIB, 'Discussion between Spain and Morocco of a tunnel under the strait began in the 1980s.')]),
    ],
    keywords={'europe': '#5ec8ff', 'africa': '#f4a261', 'gibraltar': '#ffd60a', 'tunnel': '#ffd60a'},
    captions={'theme': 'box'})

# ------------------------------------------------------------------ 13. UAE (atlas)
AE = 'Emirates_of_the_United_Arab_Emirates'
EM = [('Abu Dhabi', '#ef4444'), ('Dubay', '#f59e0b'), ('Sharjah', '#10b981'), ('Ajman', '#3b82f6'), ('Umm Al Qaywayn', '#8b5cf6'), ('Ras Al Khaymah', '#ec4899'), ('Fujayrah', '#14b8a6')]
save('uae_emirates', meta(
    'Dubai vs Abu Dhabi vs UAE: What\'s the Difference? 🇦🇪🤯',
    "Is Dubai a country? No! 🇦🇪 The United Arab Emirates is a federation of seven emirates: Abu Dhabi, Dubai, Sharjah, Ajman, Umm Al Quwain, Ras Al Khaimah and Fujairah. It was founded on 2 December 1971, and Ras Al Khaimah joined in 1972 🤝 Abu Dhabi is by far the biggest emirate, and its city is the national capital 🏛️ Dubai is both an emirate and a city, and it's the most populous, with about 4.47 million people 🌆",
    ["Dubai is not a country 🤯🇦🇪", "Have you been to Dubai or Abu Dhabi? 👇", "Which country should we explain next? 🗺️"],
    ['uae', 'united arab emirates', 'dubai', 'abu dhabi', 'sharjah', 'emirates', 'federation', 'middle east', 'geography', 'maps', 'learn']),
    [
        S("Dubai, Abu Dhabi, the Emirates. Are they the same thing?", [hook('DUBAI ≠ *COUNTRY*', at=0.05, until='same'), q(24.5, 54.5, 'same')],
          cam=at_(24.3, 54.5, 7), no_claim=True),
        S("The United Arab Emirates is a federation of seven emirates.", [
            *[hl({'admin1': n, 'country': 'ARE'}, c, 'seven', fillOpacity=0.95, stagger=0) for n, c in EM], cnt('7', 'seven', size=220)],
          cam=at_(24.3, 54.5, 7),
          src=[src('The UAE consists of seven emirates.', AE, 'The United Arab Emirates consists of seven emirates')]),
        S("Abu Dhabi, Dubai, Sharjah, Ajman, Umm Al Quwain, Ras Al Khaimah and Fujairah.", [
            *[lab(lbl, la, lo, w, style='pill', bg='#111827', size=54, dy=-70, until=u, fixed=True) for lbl, la, lo, w, u in [('Abu Dhabi', 23.6, 54.3, 'Abu', 'Dubai'), ('Dubai', 25.07, 55.25, 'Dubai', 'Sharjah'), ('Sharjah', 25.3, 55.55, 'Sharjah', 'Ajman'), ('Ajman', 25.4, 55.5, 'Ajman', 'Umm'), ('Umm Al Quwain', 25.52, 55.65, 'Umm', 'Ras'), ('Ras Al Khaimah', 25.75, 56.0, 'Ras', 'Fujairah'), ('Fujairah', 25.25, 56.3, 'Fujairah', None)]],
            *[ping(la, lo, w, color='#ffd60a', until=u) for lbl, la, lo, w, u in [('Abu Dhabi', 23.6, 54.3, 'Abu', 'Dubai'), ('Dubai', 25.07, 55.25, 'Dubai', 'Sharjah'), ('Sharjah', 25.3, 55.55, 'Sharjah', 'Ajman'), ('Ajman', 25.4, 55.5, 'Ajman', 'Umm'), ('Umm Al Quwain', 25.52, 55.65, 'Umm', 'Ras'), ('Ras Al Khaimah', 25.75, 56.0, 'Ras', 'Fujairah'), ('Fujairah', 25.25, 56.3, 'Fujairah', None)]]],
          cam=at_(24.6, 55.0, 22),
          src=[src('The seven emirates.', AE, 'Abu Dhabi, Ajman, Dubai, Fujairah, Ras Al Khaimah, Sharjah, and Umm Al Quwain')]),
        S("They joined together on 2 December 1971. Ras Al Khaimah joined a few months later, in 1972.", [
            cnt_steps([('1971', '1971: 6'), ('1972', '1972: 7')], size=150), flag('ae', 24.2, 54.8, 'joined', size=150)],
          cam=at_(24.3, 54.5, 7), era='history', tr='film',
          src=[src('Six emirates joined on 2 December 1971; Ras Al Khaimah on 10 February 1972 (table).', AE, '2 December 1971')]),
        S("Abu Dhabi is by far the largest emirate, and its city is the capital of the whole country.", [
            hl({'admin1': 'Abu Dhabi', 'country': 'ARE'}, 'flag:ae', 'largest', neon='#ffd60a'), cnt('67,340 km²', 'largest', size=130), ping(24.47, 54.37, 'capital', color='#ffd60a')],
          cam=at_(24.0, 54.2, 8), tr='flash',
          src=[src('Abu Dhabi covers 67,340 km² (table), out of the UAE\'s 83,600 km².', AE, '67,340'),
               src('The UAE covers 83,600 km².', 'United_Arab_Emirates', '83,600 km2')]),
        S("Dubai is both an emirate and a city. The emirate is only about 4,100 square kilometers, but it has the most people: about 4.47 million.", [
            hl({'admin1': 'Dubay', 'country': 'ARE'}, '#ff5a5f', 'Dubai', neon='#ffd60a'), cnt('4.47M', '4.47', size=180), icon('🏙️', 25.2, 55.27, 'city', size=120), tilt('people', deg=36, until=3.5)],
          cam=at_(25.1, 55.3, 30),
          src=[src('Dubai: 4,471,000 people (2024), vs Abu Dhabi 4,135,985 (table).', AE, '4,471,000 (2024)'),
               src('Dubai emirate covers 4,114 km² (table).', AE, '4,114')]),
        S("So Dubai isn't a country. It's one of seven pieces of one.", [
            *[hl({'admin1': n, 'country': 'ARE'}, c, 0.05, fillOpacity=0.95) for n, c in EM], stamp('1 OF 7', 'seven', size=100)],
          cam=at_(24.3, 54.5, 7, bearing=3),
          src=[src('Dubai is one of the seven emirates.', AE, 'The United Arab Emirates consists of seven emirates')]),
    ],
    keywords={'dubai': '#ff5a5f', 'abu': '#ffd60a', 'dhabi': '#ffd60a', 'seven': '#4ade80'},
    styles={'now': 'atlas', 'history': 'vintage'}, captions={'theme': 'bebas'})

# ------------------------------------------------------------------ 14. OKLAHOMA PANHANDLE
OKP = {'admin1': 'Oklahoma', 'country': 'USA'}
PH = 'Oklahoma_panhandle'
save('oklahoma_panhandle', meta(
    'Why Oklahoma Has a Panhandle 🇺🇸🤔 No Man\'s Land',
    "Why does Oklahoma 🇺🇸 have that long thin 'handle'? Blame the fight over slavery ⛓️ The Missouri Compromise banned slavery north of 36°30′. When Texas joined the US in 1845 as a slave state, it couldn't keep land north of that line, so in the Compromise of 1850 Texas gave it up 📜 The leftover strip, 166 miles long and 34 miles wide, belonged to no state or territory for 40 years: 'No Man's Land' 🤠 It finally joined Oklahoma Territory in 1890.",
    ["A strip of land that belonged to nobody for 40 years 🤯🤠", "Did you know this about Oklahoma? 👇", "Which weird state border next? 🗺️"],
    ['oklahoma', 'oklahoma panhandle', 'no mans land', 'texas', 'missouri compromise', 'compromise of 1850', 'usa', 'history', 'geography', 'maps', 'learn']),
    [
        S("Why does Oklahoma have this long, thin handle?", [hook('WHY THE *PANHANDLE*?', at=0.05, until='handle'), hl(OKP, '#ef233c', 'Oklahoma', neon='#ffd60a'), q(36.8, -101.5, 'handle')],
          cam=at_(35.5, -98.5, 5), no_claim=True),
        S("It's 166 miles long, and only 34 miles wide.", [
            hl(OKP, '#f97316', 0.05, fillOpacity=0.85, hold=1, neon='#ffd60a'),
            *[hl({'admin1': st, 'country': 'USA'}, c, 0.05, fillOpacity=0.8, hold=1) for st, c in [('Texas', '#f5c6c1'), ('Kansas', '#cfe8b8'), ('Colorado', '#d9d0f0'), ('New Mexico', '#bfe3dc')]],
            *[lab(n, la, lo, 0.05, style='map', size=40, hold=1, color='#334155') for n, la, lo in [('TEXAS', 35.6, -101.8), ('KANSAS', 37.6, -100.3), ('COLORADO', 37.7, -103.3), ('NEW MEXICO', 36.2, -103.6)]],
            meas((36.75, -103.0), (36.75, -100.0), '166 mi', 'long'), meas((36.5, -101.6), (37.0, -101.6), '34 mi', 'wide')],
          cam=at_(36.7, -101.5, 11),
          src=[src('The strip is 166 miles long and 34 miles wide.', PH, '166 miles (267 km) long and 34 miles (55 km) wide')]),
        S("It has three counties, Cimarron, Texas and Beaver, and Oklahoma's highest point, Black Mesa.", [
            *[lab(n + ' County', 36.75, lo, n, style='pill', bg='#111827', size=48, dy=-70, until=u, fixed=True) for n, lo, u in [('Cimarron', -102.5, 'Texas'), ('Texas', -101.5, 'Beaver'), ('Beaver', -100.5, 'Oklahoma')]], *[ping(36.75, lo, n, color='#ffd60a') for n, lo in [('Cimarron', -102.5), ('Texas', -101.5), ('Beaver', -100.5)]], icon('⛰️', 36.93, -102.95, 'Mesa', size=110), lab('Black Mesa', 36.93, -102.95, 'Mesa', style='pill', bg='#7c2d12', size=46, dy=-90, fixed=True)],
          cam=at_(36.7, -101.5, 11),
          src=[src('Its counties are Cimarron, Texas and Beaver.', PH, 'Its constituent counties are, from west to east, Cimarron, Texas and Beaver.'),
               src('Black Mesa, Oklahoma\'s highest point, is in Cimarron County.', PH, 'Black mesa, the highest point in Oklahoma at 4,973 feet (1,516 m), is located in Cimarron County.')]),
        S("The answer is slavery. The Missouri Compromise banned slavery north of a line: 36 degrees 30 minutes.", [
            route([(36.5, -104), (36.5, -89)], 'line', rhumb=True, color='#ffd60a', width=7, dashed=True, dash=[16, 10], drawDur=1.2, hold=2), lab('36°30′', 36.9, -95, 'degrees', style='pill', size=50)],
          cam=at_(35.5, -97, 4.5), era='history', tr='film',
          src=[src('The Missouri Compromise prohibited slavery north of 36°30′.', PH, 'based on the Missouri Compromise, prohibited slavery north of 36°30′ north latitude')]),
        S("When Texas joined the US in 1845, it was a slave state. But it also claimed land north of that line.", [
            year(1845, '1845'), hl({'admin1': 'Texas', 'country': 'USA'}, '#b3202a', 'Texas', fillOpacity=0.75), hl(box(-103, 36.5, -100, 37), '#b3202a', 'north', fillOpacity=0.75)],
          cam=at_(33.5, -99.5, 3.6), era='history',
          src=[src('Texas sought to enter the Union in 1845 as a slave state.', PH, 'When Texas sought to enter the Union in 1845 as a slave state')]),
        S("So in the Compromise of 1850, Texas gave up everything north of 36 degrees 30 minutes.", [
            year(1850, '1850'), hl(box(-103, 36.5, -100, 37), '#f5d76e', 'gave', fillOpacity=0.85), stamp('GIVEN UP', 'gave', size=90)],
          era='history',
          src=[src('Texas surrendered its lands north of 36°30′ under the 1850 Compromise.', PH, 'Texas surrendered its lands north of 36°30′')]),
        S("And that leftover strip belonged to nobody. People called it No Man's Land.", [
            slam("NO MAN'S LAND", 37.1, -101.5, 'Man\'s', size=58), char('cowboy', 'nobody', say='Whose land is this?')],
          cam=at_(36.7, -101.5, 9), era='history',
          src=[src('The strip had no state or territorial ownership and was called No Man\'s Land.', PH, "was left with no state or territorial ownership from 1850 until 1890. It was officially called the 'Public Land Strip' and was commonly referred to as 'No Man's Land.'")]),
        S("It stayed that way for 40 years, until 1890, when it finally became part of Oklahoma Territory.", [
            timeline([('stayed', '1850', 'Given up'), ('1890', '1890', 'Oklahoma')], screen=(0.5, 0.25), width=760), hl(OKP, 'flag:us', 'Oklahoma', fillOpacity=0.8)],
          cam=at_(35.5, -98.5, 5), tr='flash',
          src=[src('The Organic Act of 1890 assigned it to Oklahoma Territory.', PH, 'The passage of the Organic Act in 1890 assigned Public Land Strip to the new Oklahoma Territory')]),
    ],
    keywords={'texas': '#ff5a5f', 'oklahoma': '#ffd60a', 'slavery': '#ff5a5f', 'nobody': '#9ca3af'},
    styles={'now': 'atlas', 'history': 'vintage'}, captions={'theme': 'classic'})

# ------------------------------------------------------------------ 15. LONGEST SAIL (globe neon)
SMS = 'https://www.smithsonianmag.com/smart-news/longest-straight-line-ocean-journey-earth-180968930/'
SAIL = [(25.3, 66.6), (10, 60), (-12, 43.5), (-35, 30), (-55, -40), (-58, -66), (-45, -110), (-20, -150), (10, -175), (40, 170), (60, 164)]
save('longest_sail', meta(
    'The Longest Straight Line You Can Sail on Earth 🌊⛵🤯',
    "What's the longest straight line you could sail without hitting land? ⛵ Scientists Rohan Chabukswar and Kushal Mukherjee confirmed it in 2018: start on the coast of Pakistan 🇵🇰, slip between Africa and Madagascar, pass between South America and Antarctica, cross the whole Pacific and land in Kamchatka, Russia 🇷🇺 That's about 32,090 km (19,940 miles) in one straight line 🤯",
    ["32,000 km in one straight line without touching land 🌊🤯", "Would you sail it? ⛵👇", "What should we measure next? 🗺️"],
    ['longest straight line', 'sailing', 'ocean', 'pakistan', 'kamchatka', 'russia', 'madagascar', 'antarctica', 'great circle', 'geography', 'maps', 'learn']),
    [
        S("What's the longest straight line you could sail on Earth, without ever touching land?", [
            hook('THE LONGEST *STRAIGHT LINE* AT SEA', at=0.05, until='Earth', size=100), q(-10, 70, 'land')],
          cam=at_(-10, 70, 1.0), no_claim=True),
        S("In 2018, two scientists calculated the answer with a computer.", [
            year(2018, '2018', light=True), icon('💻', -10, 70, 'computer', size=130), char('scientist', 'scientists')],
          cam=at_(-10, 70, 1.0),
          src=[src('Verified by Rohan Chabukswar and Kushal Mukherjee (published 2018).', SMS, 'Rohan Chabukswar, a physicist at United Technologies Research Center Ireland, and Kushal Mukherjee, an engineer at IBM Research India')]),
        S("It was first found by a Reddit user years earlier. The computer confirmed it in just 10 minutes.", [
            clock([('first', '12:00'), ('minutes', '12:10')], screen=(0.5, 0.3), size=200, label='10 min'), icon('💬', -5, 60, 'Reddit', size=110)],
          cam=at_(-10, 70, 1.0),
          src=[src('First mapped by a Reddit user; verified in 10 minutes.', SMS, 'first mapped five years ago by Reddit user Patrick Anderson'),
               src('The computation took 10 minutes.', SMS, 'in just 10 minutes')]),
        S("It starts on the coast of Pakistan, and heads south, straight between Africa and Madagascar.", [
            ping(25.3, 66.6, 'Pakistan', color='#ffd60a'), hl('PAK', 'flag:pk', 'Pakistan', fillOpacity=0.8), hl('MDG', '#ff5a5f', 'Madagascar', fillOpacity=0.7),
            ship(SAIL[:4], 'south', 'sail', emblem='#2de2e6', drawDur=3.0)],
          cam={'follow': 'sail', 'zoom': 1.6, 'zoomTo': 1.2},
          src=[src('It runs from Pakistan through the passage between Madagascar and Africa.', SMS, 'runs from the Pakistan coast through the passage between Madagascar and Africa')]),
        S("Then it slips between South America and Antarctica.", [
            ship(SAIL[3:7], 'slips', 'sail2', emblem='#2de2e6', drawDur=2.6), hl('ARG', '#5ec8ff', 'America', fillOpacity=0.6)],
          cam={'follow': 'sail2', 'zoom': 1.3, 'zoomTo': 1.1},
          src=[src('The route passes between Antarctica and Tierra del Fuego.', SMS, 'around to northeastern Russia')]),
        S("It crosses the whole Pacific Ocean, and finally reaches Kamchatka, in the far east of Russia.", [
            ship(SAIL[6:], 'Pacific', 'sail3', emblem='#2de2e6', drawDur=3.0), ping(60, 164, 'Kamchatka', color='#ff5a5f'), hl('RUS', 'flag:ru', 'Russia', fillOpacity=0.6)],
          cam={'follow': 'sail3', 'zoom': 1.2, 'zoomTo': 1.0},
          src=[src('It ends in northeastern Russia.', SMS, 'around to northeastern Russia')]),
        S("The whole trip is about 32,000 kilometers. One single straight line.", [
            flow(SAIL, 'trip', color='#2de2e6', width=10, drawDur=2.0), cnt('32,090 km', '32,000', size=160)],
          cam=at_(-20, 100, 0.9),
          src=[src('The path is 19,940 miles (about 32,090 km) long.', SMS, 'This 19,940-mile trip runs from the Pakistan coast through the passage between Madagascar and Africa and around to northeastern Russia.')]),
        S("It looks curved on a map, but on a globe, it's perfectly straight.", [stamp('STRAIGHT!', 'straight', size=100)],
          cam=at_(-40, 30, 1.0, bearing=5),
          src=[src('It is the longest straight-line sailable path on Earth.', SMS, 'the longest straight-line sailable path on Earth')]),
    ],
    keywords={'pakistan': '#4ade80', 'russia': '#ff5a5f', 'straight': '#2de2e6', 'madagascar': '#ffd60a'},
    style='globe', styles={'now': 'neon', 'history': 'neon'}, captions={'theme': 'impact'})

# ------------------------------------------------------------------ 16. HOLLAND vs NETHERLANDS (atlas)
HOLL = {'admin1s': ['Noord-Holland', 'Zuid-Holland'], 'country': 'NLD'}
NL = 'Holland'
save('holland_netherlands', meta(
    'Holland vs the Netherlands: What\'s the Difference? 🇳🇱🌷🤯',
    "Holland and the Netherlands are not the same thing! 🇳🇱 The Netherlands has 12 provinces, and 'Holland' is just two of them: North Holland and South Holland 🌷 They cover about 13% of the country but hold around 38% of the people, including Amsterdam, Rotterdam and The Hague 🏙️ Because the name was used for the whole country for so long, in 2019 the Dutch government decided to stop promoting 'Holland' and use 'the Netherlands' instead 🤯",
    ["Holland is only 2 of 12 provinces 🤯🇳🇱", "Did you know the difference? 👇", "Which country name should we explain next? 🗺️"],
    ['holland', 'netherlands', 'dutch', 'amsterdam', 'rotterdam', 'the hague', 'north holland', 'south holland', 'europe', 'geography', 'maps', 'learn']),
    [
        S("Holland and the Netherlands. Most people think they're the same country. They're not.", [
            hook('HOLLAND ≠ *NETHERLANDS*', at=0.05, until='country'), vs(('nl', 'Holland?'), ('nl', 'Netherlands?'), 'same', screen=[0.5, 0.33])],
          cam=at_(52.25, 5.3, 13), no_claim=True),
        S("The Netherlands is the whole country, with 12 provinces.", [
            hl('NLD', 'flag:nl', 'Netherlands', fillOpacity=0.85), cnt('12', '12', size=220)],
          cam=at_(52.25, 5.3, 13),
          src=[src('Holland: two of the country\'s twelve provinces.', NL, 'Holland comprises the provinces of North Holland and South Holland, representing two of the country\'s twelve provinces')]),
        S("Holland is only two of them: North Holland and South Holland.", [
            hl('NLD', '#e5e7eb', 'only', fillOpacity=0.7), hl(HOLL, '#f97316', 'two', neon='#ffd60a'),
            lab('North Holland', 52.6, 4.9, 'North', style='pill', bg='#f97316', size=40), lab('South Holland', 51.95, 4.5, 'South', style='pill', bg='#f97316', size=40)],
          cam=at_(52.25, 5.3, 13), tr='flash',
          src=[src('Holland = North Holland and South Holland.', NL, 'Holland comprises the provinces of North Holland and South Holland')]),
        S("They cover only about 13 percent of the land, but they're home to about 38 percent of the people.", [
            bars([('Land', 13, '13%', '#f97316'), ('People', 38, '38%', '#ffd60a')], 'land', screen=[0.5, 0.3], labelWidth=200), tilt('home', deg=34, until=3.5)],
          cam=at_(52.25, 5.3, 13),
          src=[src('About 13% of the territory and 38% of the population.', NL, 'covering about 13% of its national territory and approximately 38% of the Dutch population')]),
        S("Because that's where the big cities are: Amsterdam, Rotterdam and The Hague.", [
            *[ping(la, lo, w, color='#ffd60a') for la, lo, w in [(52.37, 4.9, 'Amsterdam'), (51.92, 4.48, 'Rotterdam'), (52.08, 4.31, 'Hague')]],
            *[dot(n, la, lo, w, dy=-52, size=40) for n, la, lo, w in [('Amsterdam', 52.37, 4.9, 'Amsterdam'), ('Rotterdam', 51.92, 4.48, 'Rotterdam'), ('The Hague', 52.08, 4.31, 'Hague')]],
            char('dutch_farmer', 'cities')],
          cam=at_(52.2, 4.7, 16),
          src=[src('Holland contains Amsterdam, Rotterdam and The Hague.', NL, 'The main cities in Holland are Amsterdam, Rotterdam and The Hague.')]),
        S("Rotterdam even has Europe's largest port. And with Utrecht, these cities form one giant metro area, the Randstad.", [
            icon('🚢', 51.9, 4.1, 'port', size=110), hl({'admin1': 'Utrecht', 'country': 'NLD'}, '#ffd60a', 'Utrecht', fillOpacity=0.6), slam('RANDSTAD', 52.45, 4.3, 'Randstad', size=62)],
          cam=at_(52.15, 4.75, 13), tr='flash',
          src=[src('The Port of Rotterdam is Europe\'s largest.', NL, "The Port of Rotterdam is Europe's largest and most important harbour and port."),
               src('With Utrecht they form the Randstad conurbation.', NL, 'These cities, combined with Utrecht and other smaller municipalities, effectively form a single metroplex—a conurbation called Randstad.')]),
        S("That's why, for centuries, the name Holland was used for the whole country.", [hl('NLD', '#f97316', 'whole', fillOpacity=0.6), q(52.2, 5.3, 'why')],
          cam=at_(52.25, 5.3, 13),
          src=[src('Holland has frequently been used for the whole Netherlands.', NL, 'The name Holland has frequently been used to refer to the whole of the country of the Netherlands.')]),
        S("So many people called the whole country Holland that in 2019, the government decided to stop using the name.", [
            year(2019, '2019', light=True), stamp('THE NETHERLANDS', 'stop', size=76)],
          cam=at_(52.25, 5.3, 13, bearing=3),
          src=[src('Since 2019 the government officially favours "the Netherlands"; logo changed from Holland to NL.', NL, "In 2019, the Netherlands officially dropped its support of the term Holland for the whole country, which included a logo redesign that changed 'Holland' to 'NL'.")]),
        S("Even the official logo changed, from Holland to just NL.", [
            vs(('nl', 'HOLLAND'), ('nl', 'NL'), 'logo', screen=[0.5, 0.3]), stamp('NL', 'NL', size=110)],
          cam=at_(52.25, 5.3, 13),
          src=[src('The logo changed from Holland to NL.', NL, "which included a logo redesign that changed 'Holland' to 'NL'")]),
    ],
    keywords={'holland': '#f97316', 'netherlands': '#5ec8ff', 'amsterdam': '#ffd60a'},
    styles={'now': 'atlas', 'history': 'vintage'}, captions={'theme': 'pop'})

# ------------------------------------------------------------------ 17. CENTRALIA
CEN = (40.8043, -76.3408)
CE = 'Centralia,_Pennsylvania'
save('centralia', meta(
    'The Town That Has Been on Fire Since 1962 🔥🇺🇸 Centralia',
    "Under Centralia, Pennsylvania 🇺🇸, a coal mine fire started in 1962, and it's still burning today 🔥 Experts think it could burn for another 250 years. Around 1981 about 1,000 people lived there. In 1992 the state used eminent domain to condemn every building, and by the 2020 census only 5 residents were left 😱 The cracked Route 61 became the famous 'Graffiti Highway' before it was buried under dirt in 2020.",
    ["A fire that has been burning for 60+ years 🔥😱", "Would you visit Centralia? 👇", "Which ghost town should we explain next? 🗺️"],
    ['centralia', 'pennsylvania', 'mine fire', 'ghost town', 'coal', 'graffiti highway', 'usa', 'history', 'geography', 'maps', 'learn']),
    [
        S("There's a town in Pennsylvania where the ground has been on fire since 1962.", [
            hook('A TOWN ON *FIRE*', at=0.05, until='Pennsylvania'), hl({'admin1': 'Pennsylvania', 'country': 'USA'}, 'flag:us', 'Pennsylvania', fillOpacity=0.6), ping(*CEN, 'town', color='#ff5a2a')],
          cam=at_(41, -77.5, 6),
          src=[src('A coal mine fire has burned beneath the borough since 1962.', CE, 'a coal mine fire burning beneath the borough since 1962')]),
        S("This is Centralia. Under it, a coal mine fire started, and it's still burning today.", [
            slam('CENTRALIA', 40.812, -76.341, 'Centralia', size=70), scatter({'circle': {'lat': CEN[0], 'lon': CEN[1], 'km': 1.2}}, '🔥', 'burning', count=10, size=64, stagger=0.08), char('coal_miner', 'coal')],
          cam=at_(40.804, -76.341, 400, bearing=-3),
          src=[src('A coal mine fire has burned beneath the borough since 1962.', CE, 'a coal mine fire burning beneath the borough since 1962')]),
        S("Experts think it could keep burning for another 250 years.", [cnt('250 years', '250', size=180, color='#ff5a2a'), tilt('burning', deg=40, until=3.5)],
          cam=at_(40.804, -76.341, 500),
          src=[src('It could burn for another 250 years.', CE, 'do so for another 250 years')]),
        S("In 1980, about 1,000 people still lived here.", [year(1980, '1980'), cnt('~1,000', '1,000', size=170), scatter({'circle': {'lat': CEN[0], 'lon': CEN[1], 'km': 0.8}}, '🏠', 'lived', count=12, size=54, stagger=0.05)],
          cam=at_(40.804, -76.341, 450), era='history', tr='film',
          src=[src('1,012 residents by 1980.', CE, 'By 1980, it had 1,012 residents.')]),
        S("Then, in 1992, the state condemned every single building in town.", [year(1992, '1992'), stamp('CONDEMNED', 'condemned', size=90), shake('condemned')],
          era='history',
          src=[src('In 1992 the governor invoked eminent domain on all property, condemning all buildings.', CE, 'invoked eminent domain on all property in the borough, condemning all the buildings within')]),
        S("In 2013, the last seven residents were allowed to stay, but only until the end of their lives.", [
            year(2013, '2013', light=True), cnt('7', 'seven', size=200), icon('🏠', 40.804, -76.34, 'residents', size=110)],
          cam=at_(40.804, -76.341, 450),
          src=[src('In 2013 the seven remaining residents were allowed to remain until their deaths.', CE, 'State and local officials reached an agreement with the then seven remaining residents on October 29, 2013, allowing them to remain in Centralia until their deaths')]),
        S("By the 2020 census, only five people were left.", [
            bars([('1980', 1012, '1,012', '#9ca3af'), ('2020', 5, '5', '#ff5a2a')], 'census', screen=[0.5, 0.3], labelWidth=180)],
          cam=at_(40.804, -76.341, 450), style='dark', tr='flash',
          src=[src('Five residents in the 2020 census.', CE, 'As of the census of 2020, there were five people residing in the borough.')]),
        S("The cracked main road became the famous Graffiti Highway, until it was buried under dirt in 2020.", [
            route([(40.797, -76.349), (40.801, -76.345), (40.806, -76.340)], 'road', color='#ff5a2a', width=10, drawDur=1.2), lab('GRAFFITI HIGHWAY', 40.797, -76.349, 'Graffiti', style='note', size=48, dy=-60)],
          cam=at_(40.8, -76.345, 700),
          src=[src('In April 2020 the owners covered the graffiti highway with mounds of dirt.', CE, 'the property\'s current owners made the decision to cover over the graffiti on the highway section of old Route 61. Several hundred mounds of dirt were laid over the area')]),
        S("Today, Centralia is a ghost town, sitting on top of a fire that nobody can put out.", [
            scatter({'circle': {'lat': CEN[0], 'lon': CEN[1], 'km': 1.2}}, '🔥', 'fire', count=12, size=66, stagger=0.06), stamp('GHOST TOWN', 'ghost', size=90)],
          cam=at_(40.804, -76.341, 350, bearing=3), style='dark',
          src=[src('Only five residents remain while the fire still burns.', CE, 'a coal mine fire burning beneath the borough since 1962')]),
    ],
    keywords={'fire': '#ff5a2a', 'burning': '#ff5a2a', 'centralia': '#ffd60a', 'five': '#ff5a2a'},
    captions={'theme': 'box'})

# ------------------------------------------------------------------ 18. GULF STREAM (neon)
GS = 'Gulf_Stream'
GSP = [(24.5, -81.5), (27, -79.8), (32, -79), (35.3, -75.2), (39, -70), (41.5, -60), (45, -45), (50, -30), (55, -15), (60, -5), (65, 5)]
save('gulf_stream', meta(
    'Why Europe Is Warmer Than Canada at the Same Latitude 🌊🔥❄️',
    "London 🇬🇧 is further north than most of Canada's big cities, so why is it so much milder? 🤔 A big part of the answer is the Gulf Stream 🌊 a warm, fast current that starts in the Gulf of Mexico, runs up the US coast and crosses the Atlantic as the North Atlantic Current. It carries about 30 million cubic metres of water per second through the Florida Straits, more than all the rivers flowing into the Atlantic combined 🤯 That's why Norway's coast can stay ice-free so close to the Arctic.",
    ["A river in the ocean that heats up Europe 🌊🔥", "Did you know this about the Gulf Stream? 👇", "Which ocean secret next? 🗺️"],
    ['gulf stream', 'north atlantic current', 'europe', 'climate', 'ocean currents', 'atlantic', 'norway', 'uk', 'canada', 'geography', 'maps', 'learn']),
    [
        S("London and Calgary are at almost the same latitude. So why are Europe's winters so much milder?", [
            hook('WHY IS EUROPE *WARMER*?', at=0.05, until='latitude'), route([(51.3, -125), (51.3, 20)], 'latitude', rhumb=True, color='#ffd60a', width=5, dashed=True, dash=[14, 10], drawDur=1.4, hold=1),
            dot('London', 51.5, -0.13, 'London', dy=-50), dot('Calgary', 51.05, -114.07, 'Calgary', dy=-50)],
          cam=at_(48, -55, 1.2), no_claim=True),
        S("A big part of the answer is flowing right here: the Gulf Stream.", [
            flow(GSP, 'Gulf', color='#ff5a2a', width=18, drawDur=2.6, flowSpeed=220, hold=3), slam('GULF STREAM', 38, -62, 'Stream', size=66)],
          cam=at_(42, -45, 1.3),
          src=[src('The Gulf Stream is a warm and swift Atlantic current.', GS, 'a warm and swift Atlantic ocean current that originates in the Gulf of Mexico')]),
        S("It's a warm, fast current that starts in the Gulf of Mexico and runs up the coast of the US.", [
            ping(25, -83, 'Gulf', color='#ff5a2a'), lab('WARM', 30, -76, 'warm', style='pill', bg='#ff5a2a', size=46)],
          cam=at_(33, -76, 2.8),
          src=[src('It originates in the Gulf of Mexico and flows along the US East Coast.', GS, 'originates in the Gulf of Mexico')]),
        S("It's about 100 kilometers wide, and up to 1,200 meters deep.", [cnt('100 km', '100', size=160), cnt_steps([('1,200', '1,200 m')], size=110, screen=[0.5, 0.23]), tilt('deep', deg=36, until=3.5)],
          cam=at_(35, -74, 4),
          src=[src('Typically 100 km wide and 800–1,200 m deep.', GS, '100 km (62 mi) wide and 800 to 1,200 m (2,600 to 3,900 ft) deep')]),
        S("Through Florida, it moves 30 million cubic meters of water every second. More than all the rivers flowing into the Atlantic combined.", [
            bars([('Gulf Stream', 30, '30 Sv', '#ff5a2a'), ('All rivers', 0.6, '0.6 Sv', '#5ec8ff')], 'combined', screen=[0.5, 0.3], labelWidth=240)],
          cam=at_(26, -80, 5), tr='flash',
          src=[src('30 million m³/s through the Florida Straits; all Atlantic rivers total 0.6 Sv.', GS, 'transports water at a rate of 30 million cubic metres per second through the Florida Straits')]),
        S("Then it crosses the Atlantic as the North Atlantic Current, and warms the coasts of Northwest Europe.", [
            flow(GSP[5:], 'crosses', color='#ff5a2a', width=18, drawDur=2.0), hl('GBR', '#ff5a2a', 'Europe', fillOpacity=0.35), hl('NOR', '#ff5a2a', 'Europe', fillOpacity=0.35), hl('IRL', '#ff5a2a', 'Europe', fillOpacity=0.35)],
          cam=at_(55, -20, 1.8),
          src=[src('Northwest Europe is warmer than other areas of similar latitude partly because of the North Atlantic Current.', GS, 'the climate of Northwest Europe is warmer than other areas of similar latitude at least partially because of the strong North Atlantic Current')]),
        S("That's why towns on Norway's coast can thrive so close to the Arctic.", [ping(69.65, 18.96, 'Norway', color='#ffd60a'), dot('Tromsø', 69.65, 18.96, 'Norway', dy=-52), icon('🏘️', 67, 14, 'towns', size=110)],
          cam=at_(66, 10, 3.0, bearing=3),
          src=[src('The warming is dramatic along Norway\'s coast.', GS, 'North Atlantic Current')]),
    ],
    keywords={'gulf': '#ff5a2a', 'stream': '#ff5a2a', 'warm': '#ff5a2a', 'europe': '#5ec8ff'},
    styles={'now': 'neon', 'history': 'vintage'}, captions={'theme': 'bebas'})
