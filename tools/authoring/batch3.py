from helpers import *

# ------------------------------------------------------------------ SUEZ / EVER GIVEN
EG = (30.017, 32.58)
VIA_SUEZ = [(1.2, 103.8), (6, 80), (13, 50), (20, 38.5), (27.5, 33.8), (29.95, 32.55), (31.26, 32.31), (34, 25), (36.5, 12), (36.0, -5.5), (44, -9.5), (49.5, -4), (51.95, 4.1)]
AROUND = [(1.2, 103.8), (6, 80), (-10, 60), (-30, 35), (-35.5, 19), (-25, 8), (-5, 0), (5, -15), (20, -20), (36, -12), (44, -9.5), (49.5, -4), (51.95, 4.1)]
Q_N = {'circle': {'lat': 31.9, 'lon': 32.2, 'km': 45}}
Q_S = {'circle': {'lat': 29.4, 'lon': 32.7, 'km': 35}}
save('suez_ever_given', meta(
    'How ONE Ship Blocked 12% of World Trade 🚢🇪🇬🤯 Ever Given',
    "In March 2021 the 400-meter container ship Ever Given got stuck in the Suez Canal 🇪🇬 and blocked it for six days 🚢 About 369 ships were left waiting, because roughly 12% of world trade passes through this canal, and an estimated $9.6 billion of trade was held up every day 💸 Without Suez, ships between Asia and Europe must sail around Africa; the canal cuts the trip from the Arabian Sea to London by about 8,900 km 🌍 Dredgers and tugboats freed the ship, and Egypt later settled for $540 million 🤯",
    ["One ship. Six days. $9.6 billion of trade a day stuck 🤯🚢", "Remember the Ever Given memes? 😂👇", "Which chokepoint should we explain next? 🗺️"],
    ['suez canal', 'ever given', 'egypt', 'ship stuck', 'container ship', 'world trade', 'shipping', 'supply chain', 'red sea', 'geography', 'maps', 'learn']),
    [
        S("In March 2021, one single ship got stuck right here, and blocked the Suez Canal for six days.", [
            ping(*EG, 'here', color='#ff3b3b', hold=2), icon('🚢', EG[0], EG[1] + 0.05, 'ship', size=120, hold=1), cnt('6 days', 'six', size=180), shake('blocked')],
          cam=at_(30.3, 32.45, 55, bearing=-4),
          src=[src('The Ever Given blocked the canal 23–29 March 2021.', '2021_Suez_Canal_obstruction', 'The Ever Given container ship blocked Egypt\'s crucial waterway from 23–29 March 2021')]),
        S("It was the Ever Given, a container ship 400 meters long, wedged across the canal in a sandstorm.", [
            slam('EVER GIVEN', 30.12, 32.58, 'Ever', size=70), cnt('400 m', '400', size=180), art('dust_storm', 30.2, 32.7, 'sandstorm', size=170)],
          src=[src('The 400 m ship became wedged across the canal during a sandstorm.', '2021_Suez_Canal_obstruction', 'The 400-meter vessel became wedged across the canal during a sandstorm')]),
        S("Strong winds of over 40 knots made the crew lose the ability to steer.", [
            art('wind', 30.2, 32.75, 'winds', size=170), cnt('40 kn', '40', size=170), particles('dust', 'winds', density=0.5), shake('steer')],
          cam=at_(30.1, 32.6, 70, bearing=3),
          src=[src('Winds over 40 knots caused a loss of the ability to steer the ship.', '2021_Suez_Canal_obstruction',
                   "Strong winds exceeding 40 kn (74 km/h; 46 mph) resulted in the 'loss of the ability to steer the ship'")]),
        S("About 369 ships got stuck waiting at both ends.", [
            scatter(Q_N, '🚢', 'ships', count=5, size=60, stagger=0.1), scatter(Q_S, '🚢', 'waiting', count=4, size=60, stagger=0.1, seed=3),
            cnt('369', '369', size=190)],
          cam=at_(30.6, 32.45, 14),
          src=[src('Approximately 369 ships queued.', '2021_Suez_Canal_obstruction', 'Approximately 369 ships queued to pass through')]),
        S("Because roughly 12 percent of all world trade passes through this one canal.", [
            cnt('12%', '12', size=210), pill('of world trade', 'trade'), route([(31.26, 32.31), (30.6, 32.33), (29.95, 32.55)], 'canal', color='#5ec8ff', width=9, drawDur=1.0)],
          src=[src('Roughly 12% of worldwide trade.', '2021_Suez_Canal_obstruction', 'representing roughly 12% of worldwide trade')]),
        S("About fifty ships travel through the canal every day.", [
            ship([(31.26, 32.31), (30.6, 32.33), (29.95, 32.55)], 'fifty', 'st1', drawDur=2.0, style='cargo'), ship([(29.95, 32.56), (30.6, 32.34), (31.26, 32.32)], 'day', 'st2', drawDur=2.0, style='cargo', emblem='#1d4ed8'),
            cnt('~50', 'fifty', size=190), pill('ships per day', 'day')],
          cam=at_(30.6, 32.45, 14),
          src=[src('By 2021 about fifty ships per day travelled through the canal.', '2021_Suez_Canal_obstruction', 'By 2021, about fifty ships per day travelled through the canal, representing about 12 percent of total global trade.')]),
        S("Every day it was blocked, an estimated 9.6 billion dollars of trade was held up.", [
            cnt('$9.6B', '9.6', size=200, color='#4ade80'), pill('per day', 'day', bg='#16a34a'), icon('💸', 30.8, 33.3, 'trade', size=130)],
          src=[src('An estimated $9.6 billion of trade per day.', '2021_Suez_Canal_obstruction', 'The obstruction tied up cargo valued at an estimated $9.6 billion daily')]),
        S("Without the canal, ships between Asia and Europe have to sail all the way around Africa.", [
            ship(AROUND, 'around', 'africa', emblem='#1d4ed8', drawDur=3.2, style='cargo'), ship(VIA_SUEZ, 'Asia', 'suez', drawDur=2.2, style='cargo')],
          cam=at_(25, 45, 0.9),
          src=[src('The canal avoids the long route around southern Africa.', 'Suez_Canal', 'vessels avoid the lengthy route around southern Africa')]),
        S("And that detour can add up to two weeks to the journey.", [
            cnt('+2 weeks', 'two', size=160, color='#ff5a5f'), art('anchor', -34.4, 18.4, 'detour', size=110)],
          cam=at_(-10, 25, 0.85),
          src=[src('Going around Africa can add up to two weeks to the journey.', '2021_Suez_Canal_obstruction', 'a trip which can add up to two weeks to journey time')]),
        S("The canal cuts the trip from the Arabian Sea to London by about 8,900 kilometers.", [
            cnt('8,900 km', '8,900', size=150, color='#4ade80'), pill('shorter', '8,900', bg='#16a34a'), dot('London', 51.5, -0.12, 'London', dy=-46)],
          cam=at_(25, 30, 0.9),
          src=[src('It shortens the Arabian Sea–London journey by about 8,900 km.', 'Suez_Canal', 'The journey "from the Arabian Sea to London" is reduced "by approximately 8,900 km (5,500 mi),"')]),
        S("After six days, dredgers and tugboats finally freed the ship.", [
            icon('🚜', 30.0, 32.5, 'dredgers', size=100), icon('⛴️', 30.05, 32.66, 'tugboats', size=100), ping(*EG, 'freed', color='#4ade80')],
          cam=at_(30.05, 32.58, 60),
          src=[src('Salvage teams freed the ship in six days with dredgers and tugboats.', '2021_Suez_Canal_obstruction', 'salvage teams freed the ship in six days using dredgers, tugboats, and tidal advantages')]),
        S("And Egypt's Suez Canal Authority later settled for 540 million dollars in compensation.", [
            cnt('$540M', '540', size=200, color='#4ade80'), hl('EGY', 'flag:eg', 'Egypt', fillOpacity=0.7)],
          cam=at_(29.5, 31.5, 4, bearing=-3), tr='flash',
          src=[src('The Suez Canal Authority settled for $540 million.', '2021_Suez_Canal_obstruction', 'eventually settling for $540 million in July 2021')]),
    ],
    keywords={'suez': '#5ec8ff', 'canal': '#5ec8ff', 'ship': '#ffd60a', 'africa': '#f4a261', 'egypt': '#ffd60a'},
    imagery=[{'bbox': [32.1, 29.8, 32.8, 31.4], 'width': 1800}])

# ------------------------------------------------------------------ ISTANBUL
IST = (41.03, 29.0)
BOS = [(40.99, 28.99), (41.03, 29.01), (41.07, 29.05), (41.11, 29.06), (41.16, 29.08), (41.2, 29.12), (41.23, 29.14)]
WALLS = [(40.9937, 28.9227), (41.0045, 28.9215), (41.0120, 28.9230), (41.0200, 28.9265), (41.0280, 28.9310), (41.0340, 28.9355), (41.0405, 28.9400), (41.0435, 28.9440)]
FERRY = [(41.014, 28.975), (41.017, 28.99), (41.02, 29.008), (41.023, 29.02)]
save('istanbul', meta(
    'The City on TWO Continents 🇹🇷🤯 Why Istanbul Is in Europe AND Asia',
    "Istanbul 🇹🇷 sits on two continents at once, split by the Bosphorus, a 31 km strait between Europe and Asia 🌊 At its narrowest it's only about 700 meters wide! About two-thirds of its 15+ million people live on the European side. Founded as Byzantium, it became Constantinople in 330 AD, was conquered by the Ottomans in 1453 and officially renamed Istanbul in 1930 🕌 The Bosphorus is the only passage between the Black Sea and the Mediterranean, and today three bridges and a railway tunnel under the strait connect the two continents 🤯",
    ["One city, two continents 🤯🇹🇷", "Do you live on the European or the Asian side? 👇", "Which city should we explain next? 🗺️"],
    ['istanbul', 'turkey', 'bosphorus', 'europe', 'asia', 'constantinople', 'byzantium', 'ottoman empire', 'transcontinental', 'geography', 'history', 'maps', 'learn']),
    [
        S("Istanbul is one of the very few cities in the world that sits on two continents at once.", [
            hl('TUR', 'flag:tr', 0.05, fillOpacity=0.7), ping(*IST, 'Istanbul', color='#ffd60a'), cnt('2', 'two', size=220), react('art:emote_shock', (0.78, 0.3), 'continents', size=170)],
          cam={'lat': 39.5, 'lon': 32, 'zoom': 2.2, 'bearing': -3, 'then': [{'at': 'Istanbul', 'lat': 41.03, 'lon': 29.0, 'zoom': 40, 'duration': 1.4}]},
          src=[src('Istanbul straddles the Bosphorus between Europe and Asia.', 'Istanbul', 'straddles the Bosphorus ... between the Sea of Marmara and the Black Sea')]),
        S("One half is in Europe, the other half is in Asia.", [
            area((40.95, 28.55), (41.35, 28.99), 'Europe', color='#5ec8ff'), giant('EUROPE', 41.14, 28.78, 'Europe', size=80),
            area((40.8, 29.02), (41.25, 29.45), 'Asia', color='#ffd60a'), giant('ASIA', 41.0, 29.24, 'Asia', size=80)],
          cam=at_(41.06, 29.0, 90, bearing=-6), tr='flash',
          src=[src('The Bosporus forms a continental boundary between Asia and Europe.', 'Bosporus', 'forms one of the continental boundaries between Asia and Europe')]),
        S("Between them flows the Bosphorus Strait. Ferries cross it all day long.", [
            route(BOS, 'Bosphorus', color='#5ec8ff', width=10, drawDur=1.6, laser=True, hold=3),
            route(FERRY, 'Ferries', color='#ffffff', width=4, dashed=True, dash=[14, 12], glow=False, id='fer', mover={'kind': 'ship', 'size': 170, 'style': 'ferry'}, drawDur=2.8),
            pathtext('Bosphorus Strait', BOS[1:6], 'Strait', size=44)],
          cam={'follow': 'fer', 'zoom': 200, 'zoomTo': 110, 'duration': 1.0},
          src=[src('The Bosporus forms a continental boundary between Asia and Europe.', 'Bosporus', 'forms one of the continental boundaries between Asia and Europe')]),
        S("It's 31 kilometers long, and at its narrowest point it's only about 700 meters wide.", [
            cnt_steps([('31', '31 km'), ('700', '700 m')], size=180), ping(41.075, 29.057, 'narrowest', color='#ffd60a'), dot('Kandilli', 41.075, 29.06, 'narrowest', dy=48),
            lens('700', screen=(0.5, 0.4), r=300)],
          cam={'lat': 41.12, 'lon': 29.06, 'zoom': 60, 'then': [{'at': 'narrowest', 'lat': 41.075, 'lon': 29.05, 'zoom': 300, 'duration': 1.1}]},
          src=[src('31 km long; minimum width 700 m near Kandilli.', 'Bosporus', 'measures "31 km (17 nmi) long" with a minimum width of "700 m (0.38 nmi)" at its narrowest point near Kandilli')]),
        S("More than 15 million people live here, and about two thirds of them are on the European side.", [
            cnt('15M+', '15', size=190), pill('⅔ live in Europe', 'thirds', bg='#1d4ed8'),
            {'type': 'crowd', 'lat': 41.06, 'lon': 28.86, 'count': 15, 'cols': 5, 'size': 34, 'color': '#5ec8ff', 'red': [{'at': 'European', 'n': 10}], 'redColor': '#ffd60a', 'at': 'million'}],
          cam=at_(41.06, 28.97, 250),
          src=[src('Over 15 million inhabitants; about two-thirds live in Europe.', 'Istanbul', 'Approximately two-thirds of its population resides in Europe ... With over 15 million inhabitants')]),
        S("So why did such a huge city grow right here?", [q(41.03, 29.0, 'why'), react('art:emote_think', (0.28, 0.3), 'why', size=170)],
          cam=at_(41.03, 29.0, 40), style='dark', no_claim=True, tr='flash'),
        S("Because the Bosphorus is the only passage between the Black Sea and the Mediterranean.", [
            route([(43.0, 34.0), (41.6, 29.6), (41.2, 29.1), (41.0, 28.98), (40.6, 27.4), (39.6, 26.2), (37.5, 25.0), (35.5, 20.0)], 'passage', color='#ffd60a', width=8, drawDur=2.6, laser=True, id='pass', mover={'kind': 'ship', 'size': 150, 'style': 'cargo'}),
            lab('BLACK SEA', 43.2, 34.5, 'Black', style='map', size=44), lab('MEDITERRANEAN', 35.5, 22.5, 'Mediterranean', style='map', size=44)],
          cam={'follow': 'pass', 'zoom': 5, 'zoomTo': 3.2, 'duration': 1.0},
          src=[src('The Bosporus is the only passage between the Black Sea and the Mediterranean and has always been of great commercial and military importance.', 'Bosporus', 'As part of the only passage between the Black Sea and the Mediterranean, the Bosporus has always been of great importance from a commercial and military point of view.')]),
        S("It was founded by Greek colonists as Byzantium, and in 330 it became Constantinople.", [
            year(330, '330'), lab('Byzantium', 41.1, 28.75, 'Byzantium', style='serif', size=60), lab('Constantinople', 40.95, 29.15, 'Constantinople', style='serif', size=56),
            timebar(660, 330, 'BC → AD', 'founded')],
          cam=at_(41.05, 29.0, 30), era='history', tr='film',
          src=[src('Founded as Byzantium (~660 BC); renamed Constantinople in 330 AD.', 'Istanbul', 'originally called Byzantium when Greek colonists established it around 660 BC. It became Constantinople in 330 AD under Constantine the Great')]),
        S("It was the capital of the Roman, Byzantine and Ottoman empires.", [
            cnt_steps([('Roman', 'ROME'), ('Byzantine', 'BYZANTIUM'), ('Ottoman', 'OTTOMANS')], size=110), art('hagia_sophia', 41.0086, 28.9802, 'capital', size=190), dot('Hagia Sophia', 41.0086, 28.9802, 'capital', dy=70, size=34),
            art('crown', 41.05, 28.92, 'Byzantine', size=110)],
          era='history', cam=at_(41.01, 28.98, 60),
          src=[src('Capital of the Roman, Byzantine, Latin and Ottoman empires.', 'Istanbul', 'Istanbul served as capital for four major empires: the Roman Empire (330–395), the Byzantine Empire ... and the Ottoman Empire (1453–1922)')]),
        S("In 1453, the Ottomans hit its walls with giant cannons, and after a 55 day siege they conquered it.", [
            year(1453, '1453'), wall(WALLS, 'walls', buildDur=1.6, side=-1, width=16), lab('Theodosian Walls', 41.03, 28.915, 'siege', style='serif', size=40),
            art('cannon', 41.0, 28.87, 'cannons', size=150), shake('cannons'), char('sultan', 'conquered', name='Mehmed II', screen=(0.74, 0.6)), handstamp('CONQUERED', 'conquered', size=84, screen=[0.5, 0.34])],
          cam=at_(41.02, 28.955, 780), era='history',
          src=[src('Conquered on 29 May 1453 after a 55-day siege.', 'Istanbul', 'The Ottomans conquered the city "on 29 May 1453, after a 55-day siege."'),
               src('Mehmed II\'s cannons hurled massive stone balls at the walls.', 'Fall_of_Constantinople', 'His 27-foot-long (8.2 m) cannon was named "Basilica" and was able to hurl a 600-pound (270 kg) stone ball over a mile (1.6 km).'),
               src('The Theodosian land walls run about 5.7 km from the Sea of Marmara to Blachernae.', 'Walls_of_Constantinople', 'the Theodosian walls stretch for about 5.7 km (3.5 mi) from south to north')]),
        S("And in 1930, it was officially renamed Istanbul.", [
            year(1930, '1930'), giant('ISTANBUL', 41.012, 28.968, 'Istanbul', size=90), particles('confetti', 'renamed', density=0.4), flare((0.5, 0.35), 'officially')],
          cam=at_(41.02, 28.97, 90), era='history',
          src=[src('Officially renamed Istanbul in 1930.', 'Istanbul', 'officially renamed Istanbul in 1930')]),
        S("Today, three bridges and a railway tunnel under the strait connect Europe and Asia.", [
            cnt('3 + 1', 'three', size=180, screen=[0.2, 0.1]),
            bridge((41.0479, 29.0262), (41.0426, 29.0424), 'three', buildDur=0.9), dot('15 July Martyrs Bridge · 1973', 41.0452, 29.0343, 'three', dy=-46, size=30),
            bridge((41.0906, 29.0540), (41.0923, 29.0690), 'bridges', buildDur=0.9), dot('Fatih Sultan Mehmet Bridge · 1988', 41.0915, 29.0615, 'bridges', dy=-46, size=30),
            bridge((41.2050, 29.0985), (41.2004, 29.1240), 'railway', buildDur=0.9, towers=(0.3, 0.7)), dot('Yavuz Sultan Selim Bridge · 2016', 41.2027, 29.1112, 'railway', dy=-46, size=30),
            route([(41.0150, 28.9770), (41.0195, 28.9960), (41.0255, 29.0150)], 'tunnel', color='#f97316', width=8, dashed=True, dash=[14, 10], drawDur=1.0), dot('Marmaray tunnel · 2013', 41.0200, 28.9960, 'tunnel', dy=46, size=30)],
          cam=fit({'box': [28.95, 40.995, 29.16, 41.215]}, pad=0.92, bearing=-6), tr='flash',
          src=[src('Bridges: 15 July Martyrs (1973), Fatih Sultan Mehmet (1988), Yavuz Sultan Selim (2016); Marmaray undersea rail tunnel opened 2013.', 'Bosphorus',
                   'the 1,074 m (3,524 ft) long 15th July Martyrs Bridge was completed in 1973 ... Fatih Sultan Mehmet (Bosporus II) Bridge ... was completed in 1988 ... the Yavuz Sultan Selim Bridge ... was completed in 2016 ... The Marmaray project, featuring a 13.7 km (8.5 mi) long undersea railway tunnel, opened on 29 October 2013')]),
        S("That tunnel runs sixty meters below sea level, so a train can cross between continents underwater.", [
            cnt('60 m', 'sixty', size=190, color='#4ade80'), route([(41.0150, 28.9770), (41.0195, 28.9960), (41.0255, 29.0150)], 'train', color='#f97316', width=8, id='tun', mover={'kind': 'icon', 'icon': 'art:train', 'size': 100}, drawDur=2.4),
            react('art:emote_cool', (0.78, 0.3), 'underwater', size=170), grade('cold', 'underwater')],
          cam={'follow': 'tun', 'zoom': 200, 'zoomTo': 140, 'duration': 0.9}, style='dark',
          src=[src('The Marmaray tube was placed 60 metres below sea level.', 'Marmaray', 'The tube was placed 60 metres (197 ft) below sea level, beneath 55 metres (180 ft) of water')]),
    ],
    keywords={'istanbul': '#ff5a5f', 'europe': '#5ec8ff', 'asia': '#ffd60a', 'bosphorus': '#5ec8ff', 'constantinople': '#ffd60a'},
    imagery=[{'bbox': [28.55, 40.8, 29.45, 41.35], 'width': 4096}])

# ------------------------------------------------------------------ DOUBLY LANDLOCKED
UZN = ['KAZ', 'KGZ', 'TJK', 'AFG', 'TKM']
save('doubly_landlocked', meta(
    'The Only 2 Doubly Landlocked Countries 🇺🇿🇱🇮🤯',
    "44 countries in the world have no coast 🌍 but only two are doubly landlocked, meaning you must cross at least two borders to reach the sea 🌊 Uzbekistan 🇺🇿 is surrounded only by landlocked countries, and tiny Liechtenstein 🇱🇮 sits between Switzerland and Austria. Liechtenstein became doubly landlocked in 1918, when Austria-Hungary broke up and Austria lost its Adriatic coast 🤯",
    ["Only 2 countries are 'doubly landlocked' 🤯🇺🇿🇱🇮", "Have you been to Liechtenstein or Uzbekistan? 👇", "Which geography record should we explain next? 🗺️"],
    ['doubly landlocked', 'landlocked', 'uzbekistan', 'liechtenstein', 'switzerland', 'austria', 'austria-hungary', 'central asia', 'geography', 'maps', 'learn', 'weird borders']),
    [
        S("44 countries in the world have no coast at all.", [cnt('44', '44', size=220), pill('landlocked countries', 'coast'), hl({'countries': ['BOL', 'PRY', 'MNG', 'KAZ', 'ETH', 'TCD', 'MLI', 'NER', 'AUT', 'CHE', 'HUN', 'CZE']}, '#e76f51', 'coast', fillOpacity=0.85)],
          cam=at_(20, 20, 0.55), style='dark',
          src=[src('As of 2026 there are 44 landlocked countries.', 'Landlocked_country', 'As of 2026, there are 44 landlocked countries total')]),
        S("The biggest of them is Kazakhstan, and Africa has the most, with 16.", [
            hl('KAZ', 'flag:kz', 'Kazakhstan', fillOpacity=0.85), cnt('16', '16', size=220), pill('landlocked in Africa', 'Africa', bg='#b45309')],
          cam=at_(25, 40, 1.2), style='dark',
          src=[src('Kazakhstan is the largest landlocked country by area.', 'Landlocked_country', "Kazakhstan is the world's largest landlocked country by area."),
               src('Africa has the most landlocked countries, at 16.', 'Landlocked_country', 'Africa has the most landlocked countries, at 16, followed by Europe (14), Asia (12), and South America (2).')]),
        S("But only two are doubly landlocked. To reach the sea, you have to cross at least two borders.", [
            cnt('2', 'two', size=240), note('2 BORDERS!', 30, 50, 'borders', size=66)],
          style='dark',
          src=[src('Doubly landlocked = surrounded only by landlocked countries; only two exist.', 'Landlocked_country', 'A country is "doubly landlocked" when it is surrounded entirely by landlocked countries (i.e. requiring the crossing of at least two national borders to reach a coastline)')]),
        S("So which countries are they?", [q(40, 40, 'which')], style='dark', no_claim=True),
        S("The first is Uzbekistan, in Central Asia. Every single one of its neighbors is landlocked too.", [
            hl('UZB', 'flag:uz', 'Uzbekistan'), hl({'countries': UZN}, '#6b7280', 'neighbors', fillOpacity=0.75, pattern='hatch'),
            slam('UZBEKISTAN', 41.5, 64, 'Uzbekistan', size=70)],
          cam=fit('UZB', pad=0.6),
          src=[src('Uzbekistan is bordered by five landlocked neighbours.', 'Landlocked_country', 'Uzbekistan (Central Asia, bordered by five landlocked neighbors)')]),
        S("Kazakhstan, Kyrgyzstan, Tajikistan, Afghanistan and Turkmenistan. None of them has an ocean coast.", [
            hl('KAZ', 'flag:kz', 'Kazakhstan', fillOpacity=0.8), hl('KGZ', 'flag:kg', 'Kyrgyzstan', fillOpacity=0.8), hl('TJK', 'flag:tj', 'Tajikistan', fillOpacity=0.8),
            hl('AFG', 'flag:af', 'Afghanistan', fillOpacity=0.8), hl('TKM', 'flag:tm', 'Turkmenistan', fillOpacity=0.8), hl('UZB', 'flag:uz', 'Kazakhstan')],
          cam=fit('UZB', 'KAZ', 'AFG', pad=0.85),
          src=[src('Uzbekistan borders Kazakhstan, Kyrgyzstan, Tajikistan, Afghanistan and Turkmenistan.', 'Uzbekistan', 'It is bordered by Kazakhstan to the north, Kyrgyzstan to the northeast, Tajikistan to the southeast, Afghanistan to the south, and Turkmenistan to the south-west.'),
               src('All five are landlocked.', 'Landlocked_country', 'Uzbekistan (Central Asia, bordered by five landlocked neighbors)')]),
        S("The second is tiny Liechtenstein, only 160 square kilometers, squeezed between Switzerland and Austria.", [
            hl('LIE', 'flag:li', 'Liechtenstein'), hl('CHE', 'flag:ch', 'Switzerland', fillOpacity=0.7), hl('AUT', 'flag:at', 'Austria', fillOpacity=0.7),
            ping(47.14, 9.52, 'tiny', color='#ffd60a'), char('swiss_hiker', 'Liechtenstein')],
          cam=at_(47.2, 10.0, 14, bearing=-3),
          src=[src('Liechtenstein is bordered by Austria and Switzerland.', 'Landlocked_country', 'Liechtenstein (Western Europe, bordered by Austria and Switzerland)'),
               src('Area about 160 km².', 'Liechtenstein', '160.50 km2 (61.97 sq mi)')]),
        S("It's the sixth smallest country in the world, and it even uses Swiss money.", [
            cnt('#6', 'sixth', size=200), pill('smallest in the world', 'smallest', bg='#b45309'), art('banknotes', 47.14, 9.52, 'Swiss', size=130), flag('ch', 47.3, 9.1, 'Swiss', size=100, wave=True)],
          cam=at_(47.15, 9.55, 30, bearing=-3),
          src=[src('Liechtenstein is the sixth-smallest sovereign state by area.', 'Liechtenstein', 'Liechtenstein is the sixth-smallest sovereign state in the world by area.'),
               src('It uses the Swiss franc (monetary union with Switzerland).', 'Liechtenstein', 'It has a customs union and a monetary union with Switzerland, with its usage of the Swiss franc.')]),
        S("But Liechtenstein wasn't always like this. Before 1918, its neighbor was Austria-Hungary, which had a coast on the Adriatic Sea.", [
            year(1918, '1918'), ping(45.65, 13.78, 'Adriatic', color='#5ec8ff'), dot('Trieste', 45.65, 13.78, 'Adriatic', dy=46),
            hl({'hist': 1914, 'name': 'Austro-Hungarian Empire'}, '#c9a227', 'Austria-Hungary', fillOpacity=0.6), lab('Austria-Hungary', 47.8, 15.5, 'Austria-Hungary', style='serif', size=58), route([(47.14, 9.52), (46.6, 11.5), (45.65, 13.78)], 'coast', color='#1d4ed8', width=7)],
          cam=at_(46.8, 12.5, 5.5), era='history', tr='film',
          src=[src('Before 1918 it had sea access via Austria-Hungary on the Adriatic.', 'Landlocked_country', 'Before this event, it had access to the Adriatic coastline through the Austro-Hungarian Empire.')]),
        S("When the empire broke up that year, Austria lost its coast, and Liechtenstein became doubly landlocked.", [
            hl('AUT', '#c1121f', 'Austria', fillOpacity=0.8), stamp('NO COAST', 'coast', size=90), shake('broke')],
          era='history',
          src=[src('It became doubly landlocked in 1918 after Austria-Hungary dissolved.', 'Landlocked_country', 'The nation became doubly landlocked specifically in 1918 following Austria-Hungary\'s dissolution, which created an independent but landlocked Austria.')]),
        S("So from Liechtenstein, reaching the sea means crossing at least two countries.", [
            mover_icon([(47.14, 9.52), (46.8, 9.4), (46.2, 9.0), (45.46, 9.19), (44.41, 8.93)], 'reaching', '🚗', size=90, drawDur=2.4),
            cnt_steps([('reaching', '1'), ('two', '2')], size=190), dot('Genoa', 44.41, 8.93, 'sea', dy=50, dx=-90)],
          cam=at_(45.9, 9.3, 7, bearing=-3), tr='flash',
          src=[src('Doubly landlocked means crossing at least two borders to reach a coastline.', 'Landlocked_country', 'requiring the crossing of at least two national borders to reach a coastline')]),
    ],
    keywords={'uzbekistan': '#5ec8ff', 'liechtenstein': '#ff5a5f', 'austria': '#ff5a5f', 'switzerland': '#ff5a5f', 'sea': '#5ec8ff'})

# ------------------------------------------------------------------ DIOMEDE
BIG, LITTLE = (65.78, -169.05), (65.755, -168.93)
save('diomede', meta(
    'Russia and the USA Are Only 3.8 km Apart 🇷🇺🇺🇸🤯 Diomede Islands',
    "Russia 🇷🇺 and the United States 🇺🇸 are only 3.8 km apart! In the Bering Strait, Big Diomede belongs to Russia and Little Diomede to Alaska 🧊 The International Date Line runs between them, so Big Diomede is 21 hours ahead: they're nicknamed \"Tomorrow Island\" and \"Yesterday Island\" ⏰ In winter an ice bridge usually forms between them, but crossing is prohibited. Little Diomede has about 77 residents, while Big Diomede's people were moved to the mainland in 1948 and it has only a military presence 🤯",
    ["You can see tomorrow from yesterday here 🤯⏰🇷🇺🇺🇸", "Would you visit Little Diomede? 🧊👇", "Which border oddity next? 🗺️"],
    ['diomede islands', 'bering strait', 'russia', 'usa', 'alaska', 'international date line', 'tomorrow island', 'yesterday island', 'weird borders', 'geography', 'maps', 'learn']),
    [
        S("Russia and the United States are much closer than you think. In one place, only 3.8 kilometers apart.", [
            hl('RUS', '#d62839', 'Russia', fillOpacity=0.45), flag('ru', 66.2, -174.5, 'Russia', size=90), hl('USA', '#1d4ed8', 'United', fillOpacity=0.45), flag('us', 65.2, -156, 'United', size=90), cnt('3.8 km', '3.8', size=190)],
          cam=at_(65.8, -170, 3.2, bearing=-3),
          src=[src('At their closest points the two islands are about 3.8 km apart.', 'Diomede_Islands', 'At their closest points, the two islands are approximately 2.4 miles (3.8 km) away from each other.')]),
        S("Here in the Bering Strait, Big Diomede belongs to Russia, and Little Diomede belongs to Alaska.", [
            ping(*BIG, 'Big', color='#ff5a5f'), ping(*LITTLE, 'Little', color='#5ec8ff'),
            lab('BIG DIOMEDE', *BIG, 'Big', style='pill', bg='#c1121f', size=46, dy=-150), lab('LITTLE DIOMEDE', *LITTLE, 'Little', style='pill', bg='#1d4ed8', size=46, dy=110),
            flag('ru', BIG[0] + 0.03, BIG[1] - 0.08, 'Russia', size=100), flag('us', LITTLE[0] - 0.02, LITTLE[1] + 0.09, 'Alaska', size=100),
            meas(BIG, LITTLE, '3.8 km', 'Diomede')],
          cam=at_(65.77, -168.99, 300, bearing=-4),
          src=[src('Big Diomede is Russian; Little Diomede is part of Alaska.', 'Diomede_Islands', 'Big Diomede belongs to Russia while Little Diomede is part of Alaska')]),
        S("But these two neighbors don't even live on the same day. How?", [q(65.77, -168.99, 'How')], style='dark', no_claim=True),
        S("And the International Date Line runs right between them. Big Diomede is 21 hours ahead.", [
            route([(65.95, -168.99), (65.6, -168.99)], 'Date', rhumb=True, color='#ffd60a', width=6, dashed=True, dash=[16, 12], drawDur=0.9, hold=1),
            cnt('+21 h', '21', size=200)],
          src=[src('The Date Line runs between them; Big Diomede is 21 hours ahead (20 in summer).', 'Diomede_Islands', 'Big Diomede is 21 hours ahead of Little Diomede (20 in summer).')]),
        S("That's why they're nicknamed Tomorrow Island and Yesterday Island.", [
            note('TOMORROW', 65.83, -169.05, 'Tomorrow', size=62), note('YESTERDAY', 65.71, -168.92, 'Yesterday', size=62, rotate=6)],
          src=[src('They are nicknamed "Tomorrow Island" and "Yesterday Island".', 'Diomede_Islands', 'This quirk earned them the nicknames "Tomorrow Island" and "Yesterday Island."')]),
        S("In winter, an ice bridge usually forms between them. But crossing it is prohibited.", [
            route([(65.78, -169.05), (65.77, -168.93)], 'ice', color='#e0f2fe', width=18, drawDur=0.8),
            icon('🧊', 65.77, -168.99, 'ice', size=110), stamp('PROHIBITED', 'prohibited', size=90, screen=[0.5, 0.22])],
          src=[src('An ice bridge usually forms in winter, but crossing is prohibited.', 'Diomede_Islands', 'An ice bridge usually spans the distance between the two islands in winter, though crossing between them is prohibited')]),
        S("Little Diomede is home to a small Inupiat community of about 77 people.", [
            cnt('77', '77', size=210), char('inuit_kid', 'community'), ping(*LITTLE, 'Little', color='#5ec8ff')],
          src=[src('77 residents as of January 2023.', 'Diomede_Islands', 'Little Diomede supports a small Inupiat community of 77 residents as of January 2023')]),
        S("Supplies come in by helicopter. And in the past, locals even carved a runway into the thick ice, so bush planes could land.", [
            ping(*LITTLE, 'helicopter', color='#5ec8ff'), art('plane_landing', LITTLE[0] + 0.01, LITTLE[1] - 0.035, 'runway', size=150), dot('Heliport', LITTLE[0] - 0.004, LITTLE[1] + 0.004, 'helicopter', dy=56, size=34),
            particles('snow', 'ice', density=0.5)],
          cam=at_(65.76, -168.96, 340, bearing=-3),
          src=[src('Little Diomede has a heliport with regular helicopter flights; locals once carved an ice runway for bush planes.', 'Little_Diomede_Island',
                   'There is a heliport, the Diomede Heliport, with regular helicopter flights. In the past, locals carved a runway into the thick ice sheet so that bush planes could deliver vital products')]),
        S("But Big Diomede has no villagers at all. In 1948, the Soviets moved its people to the mainland, and today only the military is there.", [
            year(1948, '1948'), ping(*BIG, 'military', color='#ff5a5f'), icon('🪖', BIG[0] + 0.02, BIG[1], 'military', size=100)],
          era='history', tr='film',
          src=[src('In 1948 the Soviet government relocated its inhabitants; only military units remain.', 'Diomede_Islands', 'the Soviet government relocated indigenous inhabitants to mainland Russia in 1948 and established a military base there')]),
        S("So from Little Diomede, you can look across the water and see tomorrow.", [
            ping(*LITTLE, 'Little', color='#5ec8ff'), arrow(LITTLE, BIG, 'look', color='#ffd60a'), note('TOMORROW', 65.83, -169.05, 'tomorrow', size=66)],
          cam=at_(65.77, -168.99, 300, bearing=3), tr='flash',
          src=[src('Big Diomede is ahead of Little Diomede across the Date Line, 3.8 km away.', 'Diomede_Islands', 'Big Diomede is 21 hours ahead of Little Diomede (20 in summer).')]),
    ],
    keywords={'russia': '#ff5a5f', 'united': '#5ec8ff', 'alaska': '#5ec8ff', 'tomorrow': '#ffd60a', 'yesterday': '#ffd60a'},
    imagery=[{'bbox': [-169.35, 65.6, -168.65, 65.95], 'width': 3072}])

# ------------------------------------------------------------------ HAWAII
HI = {'admin1': 'Hawaii', 'country': 'USA'}
HNL = (21.31, -157.86)
save('hawaii', meta(
    'How Hawaii Became Part of the USA 🇺🇸🌺🤯',
    "Hawaii 🌺 is a US state in the middle of the Pacific, but it used to be an independent kingdom 👑 In 1893 a group of mostly American businessmen, backed by US sailors and Marines, overthrew Queen Liliʻuokalani, who surrendered to avoid bloodshed. The United States annexed Hawaii in 1898, it became a territory in 1900 and a state in 1959 🇺🇸 And in 1993, Congress formally apologized for the US role in the overthrow 🤯",
    ["A kingdom that became a US state 🤯🌺", "Did you know the US apologized for this in 1993? 👇", "Which island story should we explain next? 🗺️"],
    ['hawaii', 'usa', 'hawaiian kingdom', 'queen liliuokalani', 'annexation', 'honolulu', 'pacific ocean', 'history', 'geography', 'maps', 'learn']),
    [
        S("Hawaii is part of the United States, even though it sits in the middle of the Pacific Ocean.", [
            hl(HI, 'flag:us', 'Hawaii', hold=1), hl('USA', 'flag:us', 'United', fillOpacity=0.6), slam('HAWAII', 24, -157, 'Hawaii', size=90),
            arrow((33, -120), (23, -152), 'middle', color='#ffd60a')],
          cam=at_(28, -140, 1.2, bearing=-3),
          src=[src('Hawaii became a US state in 1959.', 'Overthrow_of_the_Hawaiian_Kingdom', 'eventually achieved statehood in 1959')]),
        S("It lies about 3,200 kilometers southwest of the US mainland, and it's the only state that is an archipelago.", [
            arrow((34, -120), (22, -156), 'southwest', color='#ffd60a'), cnt('3,200 km', '3,200', size=160), hl(HI, 'flag:us', 'archipelago', fillOpacity=0.85, neon='#ffd60a')],
          cam=at_(27, -138, 1.3, bearing=-3),
          src=[src('About 2,000 miles (3,200 km) southwest of the US mainland.', 'Hawaii', 'in the Pacific Ocean about 2,000 miles (3,200 km) southwest of the U.S. mainland'),
               src('Hawaii is the only state that is an archipelago.', 'Hawaii', 'the only state not on the North American mainland, the only state that is an archipelago, the only state south of the Tropic of Cancer')]),
        S("Its volcano Mauna Kea is even taller than Mount Everest, when you measure from its base on the ocean floor.", [
            art('volcano', 19.82, -155.47, 'Mauna', size=190), cnt('10,200 m', 'taller', size=150), dot('Mauna Kea', 19.82, -155.47, 'Mauna', dy=-70, size=36),
            react('art:emote_shock', (0.79, 0.3), 'taller', size=160)],
          cam=at_(19.8, -155.5, 70, bearing=-3),
          src=[src('Mauna Kea is taller than Everest measured from its base on the Pacific floor (about 10,200 m).', 'Hawaii',
                   'it is taller than Mount Everest when measured from the base of the mountain, which is on the floor of the Pacific Ocean, rising about 33,500 feet (10,200 m)')]),
        S("So how did an island kingdom become an American state?", [q(21, -157, 'how')], cam=at_(20.6, -157.4, 15), style='dark', no_claim=True),
        S("In the 1890s, Hawaii was an independent kingdom, ruled by Queen Liliʻuokalani.", [
            char('queen_liliuokalani', 'Queen', name='Queen Liliʻuokalani'), hl(HI, '#b3202a', 'kingdom', fillOpacity=0.85), icon('👑', 20.3, -156.5, 'kingdom', size=110)],
          cam=at_(20.6, -157.4, 15), era='history', tr='film',
          src=[src('Queen Liliʻuokalani was the monarch deposed in 1893.', 'Overthrow_of_the_Hawaiian_Kingdom', 'Queen Liliʻuokalani was deposed during this coup d\'état against the Hawaiian Kingdom.')]),
        S("The kingdom was founded in 1795 by Kamehameha the First. And in 1843, Britain and France recognized it as an independent state.", [
            year(1795, '1795'), flag('gb', 23.5, -159.5, 'Britain', size=110), flag('fr', 23.5, -155.2, 'France', size=110), stamp('INDEPENDENT', 'independent', size=84)],
          era='history',
          src=[src('Kamehameha I established the Hawaiian Kingdom in 1795.', 'Hawaiian_Kingdom', 'He established the Hawaiian Kingdom in 1795 with the help of western weapons and advisors'),
               src('In 1843 Britain and France jointly declared Hawaii an independent state.', 'Hawaiian_Kingdom', 'Britain and France issued the Anglo-Franco Proclamation, jointly declaring the Hawaiian Islands "an Independent State."')]),
        S("But in 1893, a group of mostly foreign businessmen overthrew her, backed by US sailors and Marines.", [
            year(1893, '1893'), char('businessman', 'businessmen', screen=(0.74, 0.6), name='Committee of Safety', flip=True),
            char('us_marine', 'Marines', screen=(0.5, 0.6)), ping(*HNL, 'overthrew', color='#ff3b3b'), shake('overthrew')],
          cam=at_(21.4, -157.9, 30), era='history',
          src=[src('On 17 January 1893 the Committee of Safety, backed by 162 sailors and Marines from the USS Boston, overthrew the Queen.', 'Overthrow_of_the_Hawaiian_Kingdom',
                   'The "Committee of Safety," composed of foreign-born residents and Hawaiian-born individuals, led the overthrow ... deployed 162 sailors and Marines from the USS Boston')]),
        S("The Queen surrendered, to avoid bloodshed.", [char('queen_liliuokalani', 'Queen', name='Queen Liliʻuokalani'), icon('🕊️', 21.6, -157.5, 'bloodshed', size=110)],
          era='history',
          src=[src('The Queen surrendered to avoid bloodshed.', 'Overthrow_of_the_Hawaiian_Kingdom', 'The Queen surrendered to avoid bloodshed.')]),
        S("In 1898, the United States annexed Hawaii. It became a territory in 1900, and a state in 1959.", [
            cnt_steps([('1898', '1898'), ('1900', '1900'), ('1959', '1959')], size=180), hl(HI, 'flag:us', 'annexed', reveal={'lat': 21.3, 'lon': -157.8})],
          cam=at_(20.6, -157.4, 15), tr='flash',
          src=[src('Annexed via the Newlands Resolution (1898); territory 1900; statehood 1959.', 'Overthrow_of_the_Hawaiian_Kingdom', 'The United States annexed Hawaii through the Newlands Resolution in 1898. Hawaii became a territory in 1900 and eventually achieved statehood in 1959.')]),
        S("And in 1993, the US Congress formally apologized for the overthrow.", [
            year(1993, '1993', light=True), stamp('SORRY', 'apologized', size=110), ping(*HNL, 'overthrow', color='#ffd60a')],
          src=[src('In 1993 Congress passed the Apology Resolution, signed by President Clinton.', 'Overthrow_of_the_Hawaiian_Kingdom', 'In 1993, Congress passed the Apology Resolution, which President Clinton signed, formally apologizing for the U.S. role in the overthrow')]),
    ],
    keywords={'hawaii': '#ff5a5f', 'united': '#5ec8ff', 'queen': '#ffd60a', 'marines': '#5ec8ff'})
