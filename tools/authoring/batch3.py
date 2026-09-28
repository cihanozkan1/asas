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
            slam('EVER GIVEN', 30.12, 32.58, 'Ever', size=70), cnt('400 m', '400', size=180), icon('🌪️', 30.2, 32.7, 'sandstorm', size=110)],
          src=[src('The 400 m ship became wedged across the canal during a sandstorm.', '2021_Suez_Canal_obstruction', 'The 400-meter vessel became wedged across the canal during a sandstorm')]),
        S("About 369 ships got stuck waiting at both ends.", [
            scatter(Q_N, '🚢', 'ships', count=5, size=60, stagger=0.1), scatter(Q_S, '🚢', 'waiting', count=4, size=60, stagger=0.1, seed=3),
            cnt('369', '369', size=190)],
          cam=at_(30.6, 32.45, 14),
          src=[src('Approximately 369 ships queued.', '2021_Suez_Canal_obstruction', 'Approximately 369 ships queued to pass through')]),
        S("Because roughly 12 percent of all world trade passes through this one canal.", [
            cnt('12%', '12', size=210), pill('of world trade', 'trade'), route([(31.26, 32.31), (30.6, 32.33), (29.95, 32.55)], 'canal', color='#5ec8ff', width=9, drawDur=1.0)],
          src=[src('Roughly 12% of worldwide trade.', '2021_Suez_Canal_obstruction', 'representing roughly 12% of worldwide trade')]),
        S("Every day it was blocked, an estimated 9.6 billion dollars of trade was held up.", [
            cnt('$9.6B', '9.6', size=200, color='#4ade80'), pill('per day', 'day', bg='#16a34a'), icon('💸', 30.8, 33.3, 'trade', size=130)],
          src=[src('An estimated $9.6 billion of trade per day.', '2021_Suez_Canal_obstruction', 'The obstruction tied up cargo valued at an estimated $9.6 billion daily')]),
        S("Without the canal, ships between Asia and Europe have to sail all the way around Africa.", [
            ship(AROUND, 'around', 'africa', emblem='#1d4ed8', drawDur=3.2), ship(VIA_SUEZ, 'Asia', 'suez', drawDur=2.2)],
          cam=at_(25, 45, 0.9),
          src=[src('The canal avoids the long route around southern Africa.', 'Suez_Canal', 'vessels avoid the lengthy route around southern Africa')]),
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
save('istanbul', meta(
    'The City on TWO Continents 🇹🇷🤯 Why Istanbul Is in Europe AND Asia',
    "Istanbul 🇹🇷 sits on two continents at once, split by the Bosphorus, a 31 km strait between Europe and Asia 🌊 At its narrowest it's only about 700 meters wide! About two-thirds of its 15+ million people live on the European side. Founded as Byzantium, it became Constantinople in 330 AD, was conquered by the Ottomans in 1453 and officially renamed Istanbul in 1930 🕌 It was the capital of the Roman, Byzantine and Ottoman empires, and today three bridges and a railway tunnel under the strait connect the two continents 🤯",
    ["One city, two continents 🤯🇹🇷", "Do you live on the European or the Asian side? 👇", "Which city should we explain next? 🗺️"],
    ['istanbul', 'turkey', 'bosphorus', 'europe', 'asia', 'constantinople', 'byzantium', 'ottoman empire', 'transcontinental', 'geography', 'history', 'maps', 'learn']),
    [
        S("Istanbul is one of the very few cities in the world that sits on two continents at once.", [
            hl('TUR', 'flag:tr', 'Istanbul', fillOpacity=0.7), ping(*IST, 'cities', color='#ffd60a'), cnt('2', 'two', size=220)],
          cam=at_(39.5, 32, 2.6, bearing=-3),
          src=[src('Istanbul straddles the Bosphorus between Europe and Asia.', 'Istanbul', 'straddles the Bosphorus ... between the Sea of Marmara and the Black Sea')]),
        S("The Bosphorus Strait splits it in two: Europe on one side, and Asia on the other.", [
            route(BOS, 'Bosphorus', color='#5ec8ff', width=10, drawDur=1.4, hold=2), slam('EUROPE', 41.15, 28.8, 'Europe', size=80), slam('ASIA', 41.0, 29.25, 'Asia', size=80)],
          cam=at_(41.08, 29.05, 45, bearing=-6),
          src=[src('The Bosporus forms a continental boundary between Asia and Europe.', 'Bosporus', 'forms one of the continental boundaries between Asia and Europe')]),
        S("It's 31 kilometers long, and at its narrowest point it's only about 700 meters wide.", [
            cnt_steps([('31', '31 km'), ('700', '700 m')], size=180), ping(41.075, 29.057, 'narrowest', color='#ffd60a'), dot('Kandilli', 41.075, 29.06, 'narrowest', dy=48)],
          cam=at_(41.075, 29.05, 120),
          src=[src('31 km long; minimum width 700 m near Kandilli.', 'Bosporus', 'measures "31 km (17 nmi) long" with a minimum width of "700 m (0.38 nmi)" at its narrowest point near Kandilli')]),
        S("More than 15 million people live here, and about two thirds of them are on the European side.", [
            slam('ISTANBUL', 41.2, 28.95, 'More', size=64), cnt('15M+', '15', size=190), pill('⅔ live in Europe', 'thirds', bg='#1d4ed8'),
            scatter({'circle': {'lat': 41.06, 'lon': 28.9, 'km': 12}}, '🏠', 'European', count=4, size=56)],
          cam=at_(41.05, 29.0, 40),
          src=[src('Over 15 million inhabitants; about two-thirds live in Europe.', 'Istanbul', 'Approximately two-thirds of its population resides in Europe ... With over 15 million inhabitants')]),
        S("It was founded by Greek colonists as Byzantium, and in 330 it became Constantinople.", [
            year(330, '330'), lab('Byzantium', 41.1, 28.75, 'Byzantium', style='serif', size=60), lab('Constantinople', 40.95, 29.15, 'Constantinople', style='serif', size=56)],
          cam=at_(41.05, 29.0, 30), era='history', tr='film',
          src=[src('Founded as Byzantium (~660 BC); renamed Constantinople in 330 AD.', 'Istanbul', 'originally called Byzantium when Greek colonists established it around 660 BC. It became Constantinople in 330 AD under Constantine the Great')]),
        S("It was the capital of the Roman, Byzantine and Ottoman empires.", [
            cnt_steps([('Roman', 'ROME'), ('Byzantine', 'BYZANTIUM'), ('Ottoman', 'OTTOMANS')], size=110), icon('👑', 41.0, 28.95, 'capital', size=130)],
          era='history',
          src=[src('Capital of the Roman, Byzantine, Latin and Ottoman empires.', 'Istanbul', 'Istanbul served as capital for four major empires: the Roman Empire (330–395), the Byzantine Empire ... and the Ottoman Empire (1453–1922)')]),
        S("In 1453, the Ottomans conquered it after a 55 day siege. And in 1930, it was officially renamed Istanbul.", [
            year(1453, '1453', until='1930'), year(1930, '1930'), char('sultan', 'Ottomans', name='Mehmed II', until='1930', screen=(0.26, 0.58)), shake('conquered'), lab('Istanbul', 41.03, 29.0, '1930', style='serif', size=68, anim='slam')],
          era='history',
          src=[src('Conquered on 29 May 1453 after a 55-day siege; renamed Istanbul in 1930.', 'Istanbul', 'The Ottomans conquered the city "on 29 May 1453, after a 55-day siege." ... officially renamed Istanbul in 1930')]),
        S("Today, three bridges and a railway tunnel under the strait connect Europe and Asia.", [
            cnt('3 + 1', 'three', size=180), icon('🌉', 41.05, 29.03, 'bridges', size=80), icon('🌉', 41.09, 29.06, 'bridges', size=80), icon('🌉', 41.2, 29.11, 'bridges', size=80),
            icon('🚆', 41.005, 29.0, 'tunnel', size=80)],
          cam=at_(41.1, 29.06, 230, bearing=-6), tr='flash',
          src=[src('Three bridges (1973, 1988, 2016) and the Marmaray rail tunnel (2013).', 'Bosporus', 'three major bridges ... plus the Marmaray railway tunnel that opened in 2013')]),
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
        S("But Liechtenstein wasn't always like this. Before 1918, its neighbor was Austria-Hungary, which had a coast on the Adriatic Sea.", [
            year(1918, '1918'), ping(45.65, 13.78, 'Adriatic', color='#5ec8ff'), dot('Trieste', 45.65, 13.78, 'Adriatic', dy=46),
            hl({'countries': ['AUT', 'HUN', 'CZE', 'SVK', 'SVN', 'HRV', 'BIH']}, '#c9a227', 'Austria-Hungary', fillOpacity=0.6), lab('Austria-Hungary', 47.8, 15.5, 'Austria-Hungary', style='serif', size=58), route([(47.14, 9.52), (46.6, 11.5), (45.65, 13.78)], 'coast', color='#1d4ed8', width=7)],
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
            hl('RUS', 'flag:ru', 'Russia', fillOpacity=0.8), hl('USA', 'flag:us', 'United', fillOpacity=0.8), cnt('3.8 km', '3.8', size=190)],
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
