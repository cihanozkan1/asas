from helpers import *

# ------------------------------------------------------------------ 1. LONGEST WALK (globe)
WALK = [(-33.92, 18.42), (-24.65, 25.91), (-17.83, 31.05), (-6.8, 39.28), (0.35, 32.58), (4.85, 31.58), (15.5, 32.56),
        (30.04, 31.24), (31.95, 35.93), (33.51, 36.28), (39.93, 32.86), (44.43, 26.1), (53.9, 27.57), (55.75, 37.62),
        (56.01, 92.87), (52.29, 104.3), (62.03, 129.73), (59.57, 150.8)]
BM = 'https://brilliantmaps.com/longest-walk/'
save('walk_world', meta(
    'The Longest Walk on Earth: 22,387 km Without a Plane 🚶‍♂️🌍🤯',
    "What's the longest distance you could walk on Earth without getting on a plane? 🚶‍♂️ A route found on Google Maps runs from Cape Town in South Africa 🇿🇦 all the way to Magadan in the far east of Russia 🇷🇺: about 22,387 km through 16 countries! Google Maps estimates 4,492 hours of walking, that's 187 days non-stop, or 562 days if you walk 8 hours a day 🤯",
    ["22,387 km on foot. Would you try it? 🚶‍♂️🌍", "Which country on the route would you stop in first? 👇", "What should we measure next? 🗺️"],
    ['longest walk', 'cape town', 'magadan', 'walking route', 'google maps', 'africa', 'russia', 'travel', 'geography', 'maps', 'learn', 'fun facts']),
    [
        S("What is the longest walk you could take on Earth, without ever getting on a plane?", [
            hook('THE LONGEST *WALK* ON EARTH', at=0.05, until='plane'), q(0, 20, 'plane')],
          cam=at_(10, 30, 1.0), no_claim=True),
        S("It starts here, at the southern tip of Africa, in Cape Town.", [
            ping(-33.92, 18.42, 'Cape', color='#ffd60a', hold=1), dot('Cape Town', -33.92, 18.42, 'Cape', dy=56), flag('za', -30, 24, 'Africa', size=120)],
          cam=at_(-30, 22, 3.2),
          src=[src('The route starts in Cape Town, South Africa.', BM, 'from Cape Town, South Africa to Magadan, Russia')]),
        S("And it ends on the other side of the world, in Magadan, in the far east of Russia.", [
            ping(59.57, 150.8, 'Magadan', color='#ff5a5f'), dot('Magadan', 59.57, 150.8, 'Magadan', dy=-56), flag('ru', 63, 140, 'Russia', size=120)],
          cam=at_(55, 140, 2.6),
          src=[src('It ends in Magadan, Russia.', BM, 'from Cape Town, South Africa to Magadan, Russia')]),
        S("The whole route is about 22,387 kilometers long, and it crosses 16 countries.", [
            route(WALK, 'route', color='#ffd60a', width=8, drawDur=3.4, mover={'kind': 'icon', 'icon': '🚶', 'size': 110}, id='walk', hold=1),
            cnt('22,387 km', '22,387', size=170), cnt_steps([('16', '16 countries')], size=100, screen=[0.5, 0.3])],
          cam=at_(20, 70, 0.95),
          src=[src('Distance 22,387 km through 16 countries.', BM, 'a distance of 22,387km (13,910 miles)'),
               src('16 countries.', BM, 'You would have to travel through 16 countries')]),
        S("That's more than half of the way around the Earth, which is about 40,000 kilometers at the equator.", [
            bars([('This walk', 22387, '22,387 km', '#ffd60a'), ('Equator', 40075, '40,075 km', '#5ec8ff')], 'half', screen=[0.5, 0.3], labelWidth=240)],
          cam=at_(0, 60, 1.0),
          src=[src("Earth's equatorial circumference is 40,075 km.", 'Earth', '40075.017 km [equatorial]')]),
        S("Through Africa, past Egypt, across Turkey and Russia, and all the way through Siberia.", [
            route(WALK, 'Through', color='#ffd60a', width=7, drawDur=3.0), ping(30.04, 31.24, 'Egypt', color='#5ec8ff'), ping(39.93, 32.86, 'Turkey', color='#5ec8ff'), ping(56.01, 92.87, 'Siberia', color='#5ec8ff'),
            hl('EGY', 'flag:eg', 'Egypt', fillOpacity=0.7), hl('TUR', 'flag:tr', 'Turkey', fillOpacity=0.7), hl('RUS', 'flag:ru', 'Russia', fillOpacity=0.5)],
          cam=at_(30, 50, 1.1),
          src=[src('The route passes through Egypt, Turkey and Russia.', 'https://explorersweb.com/the-longest-walk-in-the-world/', 'Cape Town, South Africa to Magadan, Russia')]),
        S("Google Maps says it would take 4,492 hours of walking.", [
            cnt('4,492 h', '4,492', size=190), char('backpacker', 'walking', name='You', say='My feet!')],
          cam=at_(35, 80, 1.1),
          src=[src('4,492 hours of walking.', BM, 'Google Maps estimates it would take 4,492 hours to walk it')]),
        S("That's 187 days of non-stop walking, day and night.", [
            bars([('Non-stop', 187, '187 days', '#ff5a5f'), ('8 h a day', 562, '562 days', '#ffd60a')], 'non-stop', screen=[0.5, 0.3], labelWidth=240)],
          style='neon',
          src=[src('187 days non-stop.', BM, 'which translates into 187 days of non-stop walking')]),
        S("And if you only walked eight hours a day, it would take you 562 days, more than a year and a half.", [
            bars([('Non-stop', 187, '187 days', '#ff5a5f'), ('8 h a day', 562, '562 days', '#ffd60a')], 0, screen=[0.5, 0.3], labelWidth=240, stagger=0),
            stamp('1.5 YEARS', 'year', size=90)],
          style='neon',
          src=[src('562 days at 8 hours a day.', BM, 'If instead you decided to walk a more sensible 8 hours a day, it would take you 562 days')]),
    ],
    keywords={'cape': '#ffd60a', 'magadan': '#ff5a5f', 'walk': '#ffd60a', 'walking': '#ffd60a'},
    style='globe', captions={'theme': 'impact'})

# ------------------------------------------------------------------ 2. DARIEN GAP
YAV, TUR = (8.18, -77.69), (8.09, -76.73)
DG = 'Darién_Gap'
save('darien_gap', meta(
    'The Darién Gap: The Road That Stops in the Jungle 🌴🇵🇦🇨🇴😱',
    "The Pan-American Highway runs about 30,000 km from Alaska 🇺🇸 to the tip of Argentina 🇦🇷 but it has one gap 🛑 Between Yaviza in Panama 🇵🇦 and Turbo in Colombia 🇨🇴 there's no road for about 106 km: the Darién Gap 🌴 Swamps, mountains and rainforest, deadly wildlife, flash floods and violent crime make it one of the most dangerous places on Earth. Still, in 2023 more than 520,000 people crossed it on foot 😱",
    ["30,000 km of highway… and 106 km of jungle 🌴😱", "Would you ever try to cross the Darién Gap? 👇", "Which dangerous place should we cover next? 🗺️"],
    ['darien gap', 'pan-american highway', 'panama', 'colombia', 'jungle', 'rainforest', 'migration', 'dangerous places', 'geography', 'maps', 'learn']),
    [
        S("This road runs about 30,000 kilometers, from Alaska all the way to the tip of Argentina.", [
            hook('THE ROAD WITH A *GAP*', at=0.05, until='kilometers'),
            route([(70.2, -148.4), (61.2, -149.9), (49.3, -123.1), (34, -118), (19.4, -99.1), (9.9, -84.1), (8.18, -77.69)], 'road', color='#ffd60a', width=8, drawDur=2.2, hold=1),
            route([(8.09, -76.73), (4.6, -74.1), (-0.2, -78.5), (-12, -77), (-33.4, -70.6), (-54.8, -68.3)], 'Argentina', color='#ffd60a', width=8, drawDur=1.6, hold=1),
            cnt('30,000 km', '30,000', size=170)],
          cam=at_(10, -95, 0.8),
          src=[src('The Pan-American Highway is about 30,000 km, from Prudhoe Bay, Alaska, to Ushuaia, Argentina.', 'Pan-American_Highway', 'from Prudhoe Bay, Alaska, United States, in the northernmost part of North America, to Ushuaia, Argentina')]),
        S("It's the Pan-American Highway, and it links 14 countries.", [
            cnt('14', '14', size=200), *[flag(c, la, lo, 'links', size=90) for c, la, lo in [('ca', 52, -108), ('us', 40, -100), ('mx', 23, -102), ('pe', -9, -75), ('cl', -30, -71), ('ar', -38, -65)]]],
          cam=at_(10, -95, 0.8),
          src=[src('The highway links 14 nations.', 'Pan-American_Highway', 'The system links 14 nations')]),
        S("But there is one place where the road simply stops.", [ping(*YAV, 'stops', color='#ff3b3b'), stamp('ROAD ENDS', 'stops', size=90)],
          cam=at_(8.3, -77.4, 9), style='dark', no_claim=True),
        S("It ends in Yaviza, Panama, and only starts again in Turbo, Colombia, about 106 kilometers away.", [
            dot('Yaviza', *YAV, 'Yaviza', dy=-56), dot('Turbo', *TUR, 'Turbo', dy=-56), flag('pa', 8.9, -78.4, 'Panama', size=100), flag('co', 7.4, -76.2, 'Colombia', size=100),
            meas(YAV, TUR, '106 km', 'kilometers')],
          cam=at_(8.2, -77.2, 18, bearing=-3),
          src=[src('The highway breaks at Yaviza, Panama and resumes at Turbo, Colombia, roughly 106 km away.', DG, "The 'Gap' interrupts the Pan-American Highway, which breaks at Yaviza, Panama, and resumes at Turbo, Colombia, roughly 106 km (66 mi) away.")]),
        S("Drivers can't get through. Cars have to be shipped around it by boat.", [
            ship([(8.95, -79.5), (9.6, -78.5), (9.7, -77.2), (8.7, -76.9), (8.09, -76.73)], 'shipped', 'car', emblem='#ffd60a', drawDur=2.0), icon('🚗', 9.1, -79.3, 'Cars', size=100)],
          cam=at_(8.8, -78.2, 8),
          src=[src('Vehicles must be shipped by cargo vessel to get around the gap.', 'Pan-American_Highway', 'vehicles must be shipped by cargo vessel to bridge this section')]),
        S("In between is the Darién Gap: swamps, mountains and thick rainforest.", [
            hl({'admin1s': ['Darién', 'Emberá', 'Kuna Yala'], 'country': 'PAN'}, '#16a34a', 'Darién', fillOpacity=0.5, neon='#4ade80'), hl({'admin1': 'Chocó', 'country': 'COL'}, '#16a34a', 'Darién', fillOpacity=0.5, neon='#4ade80'), slam('DARIÉN GAP', 8.6, -77.3, 'Darién', size=70),
            icon('🌴', 7.7, -77.6, 'rainforest', size=110), icon('⛰️', 8.0, -77.9, 'mountains', size=100), char('jungle_explorer', 'swamps')],
          cam=at_(7.9, -77.3, 14), tr='flash',
          src=[src('Colombian side: Atrato delta marshland; Panamanian side: mountainous rainforest.', DG, "the Colombian side dominated primarily by the river delta of the Atrato River, which creates a flat marshland at least 80 km (50 mi) wide")]),
        S("It's full of venomous wildlife, diseases and flash floods.", [
            tilt('venomous', deg=36, until=4), icon('🐍', 7.6, -77.1, 'venomous', size=110), icon('🦟', 8.1, -77.5, 'diseases', size=100), icon('🌊', 7.8, -77.8, 'floods', size=110)],
          cam=at_(7.9, -77.3, 20),
          src=[src('Dangers include venomous wildlife, diseases and flash floods.', DG, 'venomous and deadly wildlife, tropical insects, parasites and diseases, and frequent heavy rains and flash floods')]),
        S("And there's no police and no hospital, so violent crime is everywhere.", [
            stamp('NO POLICE', 'police', size=86), icon('🚫', 8.0, -77.3, 'hospital', size=110), shake('violent')],
          style='dark',
          src=[src('Law enforcement and medical support are nonexistent; violent crime is rampant.', DG, 'law enforcement and medical support are nonexistent, resulting in rampant violent crime')]),
        S("Still, in 2023, more than 520,000 people crossed it on foot.", [
            cnt('520,000+', '520,000', size=170), scatter({'admin1s': ['Darién', 'Emberá'], 'country': 'PAN'}, '🚶', 'crossed', count=5, size=64, stagger=0.12)],
          cam=at_(7.9, -77.3, 14, bearing=3),
          src=[src('More than 520,000 people crossed in 2023.', DG, 'In 2023, more than 520,000 individuals passed through the gap')]),
        S("That's more than double the year before. The shortest gap on the road, and the most dangerous.", [
            bars([('2022', 240, 'less than half', '#5ec8ff'), ('2023', 520, '520,000+', '#ff5a5f')], 'double', screen=[0.5, 0.3], labelWidth=170)],
          style='dark',
          src=[src('2023 more than doubled the previous year.', DG, "more than doubling the previous year's number of crossings")]),
    ],
    keywords={'darién': '#4ade80', 'gap': '#4ade80', 'panama': '#5ec8ff', 'colombia': '#ffd60a', '520,000': '#ff5a5f'},
    captions={'theme': 'box'})

# ------------------------------------------------------------------ 3. SPAIN BORDERS (atlas)
LLI = (42.464, 1.975)
PHE = (43.3434, -1.7658)
PEN = (35.1722, -4.3003)
CEU, MEL = (35.89, -5.32), (35.29, -2.94)
save('spain_borders', meta(
    "Spain's Strangest Borders 🇪🇸🤯 An Island That Changes Country Every 6 Months!",
    "Spain 🇪🇸 has some of the strangest borders in the world! Llívia is a Spanish town completely surrounded by France 🇫🇷, thanks to a technicality in the 1659 Treaty of the Pyrenees: it was a 'town', not a 'village' 😅 Pheasant Island belongs to Spain for six months and to France for the other six 🏝️ In Africa, Spain holds Ceuta and Melilla, the EU's only land borders with Africa, and Peñón de Vélez de la Gomera, whose 85 m border with Morocco 🇲🇦 is the world's shortest 🤯",
    ["An island that switches country every 6 months 🤯🇪🇸🇫🇷", "Which one surprised you most? 👇", "Which country's borders should we explain next? 🗺️"],
    ['spain', 'borders', 'llivia', 'pheasant island', 'ceuta', 'melilla', 'penon de velez de la gomera', 'exclave', 'france', 'morocco', 'weird borders', 'geography', 'maps']),
    [
        S("Spain has some of the strangest borders on the planet. Let's look at them.", [
            hook("SPAIN'S *STRANGEST* BORDERS", at=0.05, until='planet'), hl('ESP', 'flag:es', 'Spain', fillOpacity=0.85)],
          cam=fit('ESP', pad=0.85, bearing=-3), no_claim=True),
        S("First, Llívia. A Spanish town completely surrounded by France.", [
            ping(*LLI, 'Llívia', color='#ff3b3b'), flag('es', LLI[0] - 0.014, LLI[1], 'Llívia', size=110),
            hl('FRA', '#9fb8ff', 'France', fillOpacity=0.55), slam('LLÍVIA', 42.482, 1.975, 'Llívia', size=70)],
          cam=at_(42.46, 1.975, 1100),
          src=[src('Llívia is a Spanish exclave surrounded by France.', 'Llívia', 'It is a Spanish exclave surrounded by the French département of Pyrénées-Orientales.')]),
        S("In 1659, Spain gave France the villages of this area. But Llívia was a town, not a village, so it stayed Spanish.", [
            year(1659, '1659'), ping(*LLI, 'Llívia', color='#ffd60a'), lab('Llívia', LLI[0], LLI[1], 'Llívia', style='pill', bg='#c1121f', size=48),
            note('TOWN ≠ VILLAGE', 42.49, 1.975, 'town', size=58), char('spanish_tercio', 'Llívia', say='Still ours!', flip=True, screen=(0.72, 0.6))],
          cam=at_(42.46, 1.975, 1300), era='history', tr='film', style='satellite',
          src=[src('The 1659 Treaty of the Pyrenees transferred only villages; Llívia was a town.', 'Llívia', "Because of a technicality in the Treaty of the Pyrenees, signed in 1659, that transferred only 'villages' in the Pyrenees to France, Llívia, which was a 'town', remains under Spanish control.")]),
        S("Next, Pheasant Island. It's Spanish for six months, and French for the other six.", [
            ping(*PHE, 'Pheasant', color='#ffd60a'), dot('Pheasant Island', *PHE, 'Pheasant', dy=-56),
            vs(('es', 'Feb–Jul'), ('fr', 'Aug–Jan'), 'six', screen=[0.5, 0.26])],
          cam=at_(43.3434, -1.7658, 6000, bearing=-3), tr='flash',
          src=[src('Alternating six-month sovereignty between Spain and France.', 'Pheasant_Island', 'For alternating periods of six months, it is officially under the governance of the naval commander of Hondarribia, Spain (1 February – 31 July) and of a French viceroy (1 August – 31 January).')]),
        S("Then Spain crosses into Africa. Ceuta and Melilla are the EU's only land borders with Africa.", [
            hl('MAR', '#e8b4a0', 'Africa', fillOpacity=0.6), ping(*CEU, 'Ceuta', color='#ffd60a'), ping(*MEL, 'Melilla', color='#ffd60a'),
            dot('Ceuta', *CEU, 'Ceuta', dy=-56), dot('Melilla', *MEL, 'Melilla', dy=-56), flag('eu', 36.9, -3.8, 'EU', size=120)],
          cam=at_(35.8, -4.1, 11),
          src=[src('Ceuta and Melilla are the EU\'s only land borders with Africa.', 'Ceuta', 'an autonomous city of Spain on the North African coast')]),
        S("And the tiny Peñón de Vélez de la Gomera has a border with Morocco only 85 meters long.", [
            ping(*PEN, 'Peñón', color='#ff3b3b'), dot('Peñón de Vélez', *PEN, 'Peñón', dy=-56), cnt('85 m', '85', size=200), char('spanish_soldier', 'Morocco')],
          cam=at_(35.172, -4.3003, 3500),
          src=[src('Its border with Morocco is 85 m long.', 'Peñón_de_Vélez_de_la_Gomera', 'Its border with Morocco is 85 m (279 ft) long.')]),
        S("It became a border by accident: in 1930, a storm washed sand into the channel and joined the island to Africa.", [
            year(1930, '1930'), icon('⛈️', 35.176, -4.296, 'storm', size=120), ping(35.1722, -4.3003, 'island', color='#ffd60a'), shake('storm')],
          cam=at_(35.172, -4.3003, 3500), era='history', tr='film', style='satellite',
          src=[src('In 1930 a storm washed sand into the channel, forming a tombolo.', 'Peñón_de_Vélez_de_la_Gomera', 'In 1930, when a huge thunderstorm washed large quantities of sand into the short channel between the island and the African continent.')]),
        S("It's now the shortest land border in the whole world.", [
            stamp('WORLD RECORD', 'shortest', size=84), cnt('#1', 'shortest', size=180)],
          cam=at_(35.172, -4.3003, 2500, bearing=3),
          src=[src('It is the world\'s shortest single land-border segment.', 'Peñón_de_Vélez_de_la_Gomera', "the world's shortest single land-border segment")]),
    ],
    keywords={'spain': '#ffd60a', 'france': '#5ec8ff', 'africa': '#f4a261', 'llívia': '#ff5a5f', 'morocco': '#4ade80'},
    styles={'now': 'atlas', 'history': 'vintage'}, captions={'theme': 'pop'})

# ------------------------------------------------------------------ 4. USA EAST / WEST (night)
M100 = [(49, -100), (26, -100)]
save('usa_east_west', meta(
    'Why Most Americans Live East of This Line 🇺🇸🌃 The 100th Meridian',
    "Look at the USA at night 🌃 the East glows, the West is mostly dark. The line that splits it is the 100th meridian: John Wesley Powell noticed in the 1870s that rainfall changes dramatically across it 🌧️ East of it the climate is humid, west of it semi-arid, so farming there needs irrigation 🌵 The US center of population is in Missouri, far east of the line, and even after 230 years of moving west it is still there 🤯",
    ["The whole USA is split by one invisible line 🇺🇸🤯", "Do you live east or west of the 100th meridian? 👇", "Which map should we explain next? 🗺️"],
    ['usa', 'population', '100th meridian', 'night lights', 'rainfall', 'great plains', 'john wesley powell', 'center of population', 'missouri', 'geography', 'maps', 'learn']),
    [
        S("This is the United States at night. The East is glowing, the West is almost dark.", [
            hook('WHY THE USA IS *SPLIT*', at=0.05, until='night'), ping(40.7, -74.0, 'glowing', color='#ffd60a'), ping(41.9, -87.6, 'glowing', color='#ffd60a')],
          cam=at_(39, -98, 2.3), no_claim=True),
        S("And the line that splits it is the 100th meridian.", [
            route(M100, 'line', rhumb=True, color='#ffd60a', width=7, dashed=True, dash=[18, 12], drawDur=1.2, hold=5), slam('100°W', 47, -100, '100th', size=74)],
          cam=at_(39, -98, 2.4),
          src=[src('The 100th meridian divides the humid East from the arid West.', '100th_meridian_west', 'As first noted by John Wesley Powell in the 1870s, there is a big difference in rainfall by the different sides of the meridian.')]),
        S("It runs straight down from North Dakota, through Nebraska, Kansas and Oklahoma, all the way to Texas.", [
            *[hl({'admin1': st, 'country': 'USA'}, '#ffd60a', st.split()[0], fillOpacity=0.28) for st in ['North Dakota', 'Nebraska', 'Kansas', 'Oklahoma', 'Texas']]],
          cam=at_(39, -99, 2.6),
          src=[src('The meridian crosses North Dakota, South Dakota, Nebraska, Kansas, Oklahoma and Texas.', '100th_meridian_west', 'North Dakota')]),
        S("In the 1870s, explorer John Wesley Powell noticed that rainfall changes a lot across this line.", [
            year(1870, '1870s'), icon('🌧️', 38, -92, 'rainfall', size=120), icon('☀️', 38, -110, 'rainfall', size=120)],
          era='history', tr='film',
          src=[src('Powell noted the rainfall difference in the 1870s.', '100th_meridian_west', 'As first noted by John Wesley Powell in the 1870s, there is a big difference in rainfall by the different sides of the meridian.')]),
        S("To the east, the climate is humid. To the west, it's semi-arid.", [
            hl({'admin1s': ['Minnesota', 'Iowa', 'Missouri', 'Arkansas', 'Louisiana', 'Wisconsin', 'Illinois', 'Michigan', 'Indiana', 'Ohio', 'Kentucky', 'Tennessee', 'Mississippi', 'Alabama', 'Georgia', 'Florida', 'South Carolina', 'North Carolina', 'Virginia', 'West Virginia', 'Pennsylvania', 'New York', 'Vermont', 'New Hampshire', 'Maine', 'Massachusetts', 'Connecticut', 'Rhode Island', 'New Jersey', 'Delaware', 'Maryland'], 'country': 'USA'}, '#16a34a', 'east', fillOpacity=0.45), hl({'admin1s': ['Washington', 'Oregon', 'California', 'Nevada', 'Idaho', 'Montana', 'Wyoming', 'Utah', 'Arizona', 'New Mexico', 'Colorado'], 'country': 'USA'}, '#d97706', 'west', fillOpacity=0.45),
            lab('HUMID', 38, -88, 'east', style='pill', bg='#16a34a', size=48), lab('SEMI-ARID', 38, -112, 'west', style='pill', bg='#d97706', size=48)],
          cam=at_(38, -98, 2.4),
          src=[src('Semi-arid climate to the west; humid climates to the east.', '100th_meridian_west', 'semi-arid climate to the west')]),
        S("So in the West, raising cattle matters more, and farming needs irrigation.", [
            icon('🐄', 36, -108, 'cattle', size=110), icon('💧', 41, -104, 'irrigation', size=100), tilt('cattle', deg=34, until=3.5)],
          cam=at_(38, -104, 3.2),
          src=[src('West of the meridian livestock is more important and agriculture relies on irrigation.', '100th_meridian_west', 'West of the meridian, raising livestock is much more economically important than east of it, and what agriculture does exist relies heavily on irrigation.')]),
        S("That's why the center of the US population, the average American, is in Missouri. Far east of the line.", [
            ping(37.4, -92.2, 'Missouri', color='#ff3b3b'), dot('Center of population', 37.4, -92.2, 'center', dy=-56), hl({'admin1': 'Missouri', 'country': 'USA'}, '#ff5a5f', 'Missouri', fillOpacity=0.45)],
          cam=at_(38, -96, 3.4), tr='flash',
          src=[src('The 2020 mean center of population is near Hartville, Wright County, Missouri.', 'Mean_center_of_the_United_States_population', '15 miles northeast of Hartville')]),
        S("It has been moving west for 230 years, and it still hasn't even reached Kansas.", [
            route([(39.28, -76.2), (39.0, -80.6), (38.9, -84.5), (39.2, -87.6), (38.6, -90.5), (37.4, -92.2)], 'moving', color='#ff5a5f', width=7, drawDur=2.2, arrowHead=True),
            dot('1790', 39.28, -76.2, 'moving', dy=-50), timeline([('moving', '1790', 'Maryland'), ('Kansas', '2020', 'Missouri')], screen=(0.5, 0.25), width=700)],
          cam=at_(38.5, -86, 3.6),
          src=[src('The center began in Maryland in 1790 and has moved west into Missouri.', 'Mean_center_of_the_United_States_population', 'moving roughly 600 miles (966 km) west by south during the 19th century')]),
    ],
    keywords={'east': '#ffd60a', 'west': '#f4a261', 'humid': '#4ade80', 'missouri': '#ff5a5f', '100th': '#ffd60a'},
    earth='night', captions={'theme': 'bebas'})

# ------------------------------------------------------------------ 5. TIBET (neon)
TIB = (33.0, 88.0)
MF = 'https://migflug.com/jetflights/why-airliners-dont-fly-over-tibet/'
save('tibet_planes', meta(
    "Why Planes Don't Fly Over Tibet ✈️🏔️😱",
    "Look at a live flight map and you'll see an empty hole over Tibet ✈️ It's not a no-fly zone. The Tibetan Plateau averages about 4,500 m high 🏔️ If a plane loses cabin pressure, the oxygen masks only last about 12 to 22 minutes, and pilots must dive to 10,000 feet (about 3,000 m) where people can breathe. Over Tibet the ground itself is higher than that, airports are rare, and the winds create brutal turbulence 😱",
    ["The 'Roof of the World' has no safe way down ✈️😱", "Would you fly over Tibet? 👇", "Which aviation mystery next? 🗺️"],
    ['tibet', 'tibetan plateau', 'planes', 'aviation', 'no fly zone', 'oxygen masks', 'himalayas', 'roof of the world', 'flights', 'geography', 'maps', 'learn']),
    [
        S("Look at flights over Asia, and you'll notice a giant empty hole right here.", [
            hook("WHY PLANES *AVOID* TIBET", at=0.05, until='Asia'),
            *[plane(p, 'flights', drawDur=2.4) for p in [[(28.6, 77.2), (22.3, 114.2)], [(25.3, 55.4), (39.9, 116.4)], [(41.3, 69.2), (13.7, 100.5)]]],
            hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#ff3b3b', 'hole', fillOpacity=0.25)],
          cam=at_(32, 90, 2.0), no_claim=True),
        S("This is the Tibetan Plateau, the Roof of the World.", [
            slam('TIBET', 33.5, 88, 'Tibetan', size=90), hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#2de2e6', 'Roof', fillOpacity=0.25)],
          cam=at_(32, 88, 2.8),
          src=[src('It is often called the Roof of the World.', 'Tibetan_Plateau', "often referred to as 'the Roof of the World'")]),
        S("It's the largest and highest plateau on Earth, about 2,500 kilometers wide.", [
            hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#2de2e6', 'largest', fillOpacity=0.25),
            stamp('LARGEST & HIGHEST', 'largest', size=78, screen=[0.5, 0.45]), meas((33, 76), (32, 101), '2,500 km', 'wide')],
          cam=at_(32, 88, 2.6),
          src=[src('The world\'s largest and highest plateau; about 2,500 km east to west.', 'Tibetan_Plateau', "It is the world's largest and highest plateau above sea level, with an area of 2,500,000 square kilometres")]),
        S("Its average height is about 4,500 meters.", [
            hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#2de2e6', 0.05, fillOpacity=0.2), bars([('Plateau', 4500, '4,500 m', '#2de2e6'), ('Safe air', 3000, '3,000 m', '#4ade80')], 'height', orient='v', shape='mountain', height=360)],
          src=[src('The plateau averages over 4,500 m.', 'Tibetan_Plateau', 'With an average elevation exceeding 4,500 metres (14,800 ft)')]),
        S("If a plane loses cabin pressure, the oxygen masks last only about 12 to 22 minutes.", [
            hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#2de2e6', 0.05, fillOpacity=0.2), char('pilot', 'plane', say='Masks on!'), clock([('masks', '12:00'), ('minutes', '12:22')], screen=(0.72, 0.33), size=220, label='12–22 min')],
          src=[src('Masks typically last 12 to 22 minutes.', MF, 'typically burn for somewhere between 12 and 22 minutes, depending on the aircraft')]),
        S("So pilots must quickly dive to 10,000 feet, where people can breathe on their own.", [
            hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#2de2e6', 0.05, fillOpacity=0.2), plane([(35, 80), (33, 88), (31, 96)], 'dive', rid='p2'), cnt('10,000 ft', '10,000', size=170), arrow((34, 86), (30, 86), 'dive', color='#ff5a5f')],
          cam=at_(32, 88, 3.0),
          src=[src('Pilots dive to 10,000 feet where humans can breathe unaided.', MF, 'the aircraft dives to 10,000 feet — the altitude where humans can breathe unaided')]),
        S("But over Tibet, the ground itself is higher than that. There's nowhere to go down.", [
            hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#2de2e6', 0.05, fillOpacity=0.2), tilt('ground', deg=40, until=4), stamp('NO WAY DOWN', 'nowhere', size=84), shake('nowhere')],
          cam=at_(31, 86, 4.0),
          src=[src('The plateau floor sits around 14,800 ft, above the 10,000 ft safety level.', MF, "The plateau's valley floors sit at around 14,800 feet")]),
        S("Airports are rare and far apart, and strong winds turn the air into a washing machine.", [
            icon('🛬', 29.3, 90.9, 'Airports', size=150), dot('Lhasa', 29.65, 91.1, 'Airports', dy=-80), icon('🌪️', 34, 84, 'winds', size=170), icon('🌪️', 31.5, 95, 'machine', size=160), shake('machine')],
          cam=at_(32, 89, 4.2),
          src=[src('Airports are rare, far apart and at extreme elevations.', MF, 'Airports are rare, far apart, and themselves perched at extreme elevations.'),
               src('Winds of 100–200 km/h create severe turbulence.', MF, 'the atmosphere downstream turns into a washing machine')]),
        S("So it's not a no-fly zone. It's just a place where an emergency has no safe ending.", [
            hl({'admin1s': ['Xizang', 'Qinghai'], 'country': 'CHN'}, '#ff3b3b', 'emergency', fillOpacity=0.3), stamp('NO SAFE ENDING', 'safe', size=84)],
          cam=at_(32, 90, 2.0),
          src=[src('There is no regulation designating Tibet as a no-fly zone.', MF, "There is no regulation designating Tibet as a no-fly zone.")]),
    ],
    keywords={'tibet': '#2de2e6', 'tibetan': '#2de2e6', 'oxygen': '#ff5a5f', 'pressure': '#ff5a5f'},
    styles={'now': 'neon', 'history': 'vintage'}, captions={'theme': 'impact'})

# ------------------------------------------------------------------ 6. TIME ZONES (globe neon)
save('time_zones', meta(
    'Why Time Zones Look So Strange 🕒🌍🤯',
    "Time zones should be neat 1-hour stripes, but the real map is chaos 🕒 China 🇨🇳 spans five geographical time zones but uses only one, Beijing Time (UTC+8), since 1949, so in far-western Xinjiang shops often open at 10:00 Beijing Time 🌅 Some places are offset by 30 or 45 minutes, like India 🇮🇳 and Nepal 🇳🇵 And the country with the most time zones? France 🇫🇷 with 12, thanks to its overseas territories. Russia and the USA have 11 each 🤯",
    ["France has more time zones than Russia 🤯🇫🇷", "What time is it where you are right now? 👇", "Which map mystery next? 🗺️"],
    ['time zones', 'china', 'beijing time', 'france', 'russia', 'nepal', 'india', 'utc', 'clock', 'geography', 'maps', 'learn']),
    [
        S("In theory, time zones should be neat stripes around the globe, one hour each.", [
            hook('TIME ZONES ARE *CHAOS*', at=0.05, until='globe'),
            *[hl(box(-7.5 + 15 * k, -70, 7.5 + 15 * k, 75), c, 'stripes', fillOpacity=0.35) for k, c in [(-2, '#2de2e6'), (-1, '#ff5a5f'), (0, '#ffd60a'), (1, '#4ade80'), (2, '#a78bfa'), (3, '#2de2e6'), (4, '#ff5a5f')]]],
          cam=at_(25, 20, 1.0), no_claim=True),
        S("But look at China. It's huge, and it uses only one time zone.", [
            hl('CHN', 'flag:cn', 'China', fillOpacity=0.85), clock([('one', '12:00')], screen=(0.5, 0.3), size=200, label='Beijing Time')],
          cam=at_(35, 100, 1.8),
          src=[src('China uses a single time zone, UTC+8.', 'Time_in_China', 'a single standard time offset of UTC+08:00')]),
        S("Since 1949, the whole country follows Beijing Time, even though it spans five geographical time zones.", [
            hl('CHN', 'flag:cn', 'Since', fillOpacity=0.45), year(1949, '1949'), *[hl(box(lo, 18, lo + 15, 54), c, 'five', fillOpacity=0.25) for lo, c in [(72.5, '#ff5a5f'), (87.5, '#ffd60a'), (102.5, '#4ade80'), (117.5, '#2de2e6'), (132.5, '#a78bfa')]],
            cnt('5 → 1', 'five', size=160)],
          cam=at_(35, 100, 1.9),
          src=[src('It spans five geographical time zones; single time since 1949.', 'Time_in_China', 'the country spans five geographical time zones')]),
        S("So in far western Xinjiang, shops often open at ten o'clock, Beijing Time.", [
            hl('CHN', 'flag:cn', 'far', fillOpacity=0.35), ping(43.8, 87.6, 'Xinjiang', color='#ffd60a'), dot('Ürümqi', 43.8, 87.6, 'Xinjiang', dy=-56), clock([('shops', '08:00'), ('ten', '10:00')], screen=(0.5, 0.3), size=200, label='Opening time')],
          cam=at_(47.5, 88, 3.0),
          src=[src('Stores and offices in Xinjiang commonly open 10:00–19:00 Beijing Time.', 'Time_in_China', 'stores and offices in Xinjiang are commonly open from 10:00 to 19:00 Beijing Time')]),
        S("Some countries don't even use whole hours. India and Nepal are offset by an extra 30 or 45 minutes.", [
            clock([('whole', '12:00'), ('hours', '12:30')], screen=(0.5, 0.25), size=200, label='+30 min'), hl('IND', 'flag:in', 'India', fillOpacity=0.8), hl('NPL', 'flag:np', 'Nepal', fillOpacity=0.9), lab('+5:30', 22, 79, 'India', style='pill', size=52), lab('+5:45', 29.8, 84, 'Nepal', style='pill', bg='#1d4ed8', size=52)],
          cam=at_(24, 82, 3.0), tr='flash',
          src=[src('Some zones are offset by an additional 30 or 45 minutes, such as India and Nepal.', 'Time_zone', 'a few zones are offset by an additional 30 or 45 minutes, such as in India and Nepal')]),
        S("So which country has the most time zones? Not Russia, not the USA.", [q(55, 90, 'which'), hl('RUS', '#ff5a5f', 'Russia', fillOpacity=0.5), hl('USA', '#5ec8ff', 'USA', fillOpacity=0.5)],
          cam=at_(50, 20, 0.95), no_claim=True),
        S("It's France. Thanks to its islands all around the world, it has 12. Russia and the USA have 11 each.", [
            hl('FRA', 'flag:fr', 'France', fillOpacity=0.9),
            bars([('France', 12, '12', '#5ec8ff', 'fr'), ('Russia', 11, '11', '#ff5a5f', 'ru'), ('USA', 11, '11', '#ffd60a', 'us')], 'France', screen=[0.5, 0.3], labelWidth=220)],
          cam=at_(20, 0, 0.95),
          src=[src('France has the most time zones, 12 (13 with its Antarctic claim).', 'List_of_time_zones_by_country', 'France, including its overseas territories, has the most time zones with 12 (13 including its claim in Antarctica).'),
               src('Russia has 11 time zones.', 'Time_in_Russia', 'There are 11 time zones in Russia, which currently observe times ranging from UTC+02:00 to UTC+12:00.')]),
        S("Russia alone goes from UTC plus 2 to UTC plus 12. When it's morning in Moscow, it's evening in Kamchatka.", [
            hl('RUS', 'flag:ru', 'Russia', fillOpacity=0.7), clock([('Moscow', '09:00')], screen=(0.28, 0.3), size=180, label='Moscow'), clock([('Kamchatka', '18:00')], screen=(0.72, 0.3), size=180, label='Kamchatka', night=True)],
          cam=at_(60, 100, 1.4),
          src=[src('Russia spans UTC+2 to UTC+12.', 'Time_in_Russia', 'There are 11 time zones in Russia, which currently observe times ranging from UTC+02:00 to UTC+12:00.')]),
    ],
    keywords={'china': '#ff5a5f', 'france': '#5ec8ff', 'beijing': '#ffd60a', 'nepal': '#4ade80', 'india': '#ffd60a'},
    style='globe', styles={'now': 'neon', 'history': 'neon'}, captions={'theme': 'pop'})

# ------------------------------------------------------------------ 7. SHELTERBELT
SB = 'Great_Plains_Shelterbelt'
save('shelterbelt', meta(
    'Why the USA Planted a Wall of Trees From Canada to Texas 🌳🇺🇸😱',
    "In the 1930s the Great Plains 🇺🇸 were hit by the Dust Bowl: giant dust storms blew away farmland 🌪️ So in 1934 President Franklin D. Roosevelt launched the Great Plains Shelterbelt 🌳 By 1942, 220 million trees had been planted in a 100-mile-wide zone from the Canadian border in North Dakota to Texas, forming 30,233 shelterbelts to slow the wind and keep moisture in the soil 💧",
    ["220 million trees to stop the wind 🌳🤯", "Have you ever seen a shelterbelt? 👇", "Which giant project should we explain next? 🗺️"],
    ['great plains shelterbelt', 'dust bowl', 'franklin roosevelt', 'trees', 'usa', 'great plains', 'north dakota', 'texas', 'history', 'geography', 'maps', 'learn']),
    [
        S("In the 1930s, the US built a wall from Canada to Texas. Not of stone, but of trees.", [
            hook('A WALL OF *TREES*', at=0.05, until='Texas'),
            route([(48.9, -100.0), (41.0, -99.8), (33.5, -99.5)], 'wall', color='#16a34a', width=30, drawDur=1.4, glow=True), scatter(box(-101.5, 32, -98.5, 48.5), '🌳', 'Not', count=7, size=58, stagger=0.1, along=[(48.6, -100.0), (41.0, -99.8), (33.8, -99.5)])],
          cam=at_(40, -99, 2.6),
          src=[src('A 100-mile-wide zone from the Canadian border in North Dakota to Texas.', SB, 'a 100-mile (160-kilometre) wide zone from the Canadian border in North Dakota to the Brazos River in Texas')]),
        S("Why? Because of the Dust Bowl, when giant dust storms blew the farmland away.", [
            icon('🌪️', 37, -101, 'dust', size=150), icon('🌪️', 34.5, -99, 'storms', size=120), char('dustbowl_farmer', 'farmland', say='Where did my soil go?'), shake('blew')],
          cam=at_(38, -100, 3.2), era='history', tr='film',
          src=[src('The project was a response to the Dust Bowl dust storms.', SB, 'reduce wind velocity and lessen evaporation of moisture from the soil')]),
        S("So in 1934, President Franklin D. Roosevelt launched the Great Plains Shelterbelt.", [
            hl({'admin1s': ['North Dakota', 'South Dakota', 'Nebraska', 'Kansas', 'Oklahoma'], 'country': 'USA'}, '#b45309', 'Great', fillOpacity=0.4), lab('GREAT PLAINS', 41, -100, 'Great', size=50), year(1934, '1934'), char('fdr', 'Roosevelt', name='F. D. Roosevelt', say='Plant trees!')],
          era='history',
          src=[src('Started in 1934 by President Franklin D. Roosevelt.', SB, '1934')]),
        S("The idea: rows of trees slow down the wind, and keep moisture in the soil.", [
            tilt('rows', deg=40, until=4), scatter(box(-101, 34, -99, 47), '🌳', 'idea', count=5, size=64, stagger=0.12, along=[(41.5, -100.2), (38.5, -100.2)]), flow([(40, -106), (40, -101.8)], 'wind', color='#e5e7eb', width=9)],
          cam=at_(40, -100, 5),
          src=[src('Windbreaks reduce wind velocity and evaporation.', SB, 'reduce wind velocity and lessen evaporation of moisture from the soil')]),
        S("By 1942, they had planted 220 million trees.", [
            route([(48.9, -100.0), (41.0, -99.8), (33.5, -99.5)], 0.05, color='#16a34a', width=30, drawDur=0.4, glow=True), cnt('220,000,000', '220', size=130, color='#4ade80'), timeline([('By', '1934', 'Start'), ('1942', '1942', '220M trees')], screen=(0.5, 0.26), width=700)],
          cam=at_(40, -99, 2.8),
          src=[src('220 million trees by 1942.', SB, '220 million trees had been planted, covering 18,600 square miles')]),
        S("That's 30,233 separate shelterbelts, covering 18,600 square miles.", [
            route([(48.9, -100.0), (41.0, -99.8), (33.5, -99.5)], 0.05, color='#16a34a', width=30, drawDur=0.4, glow=True), cnt_steps([('30,233', '30,233'), ('18,600', '18,600 mi²')], size=150), scatter(box(-101.5, 32, -98.5, 48.5), '🌳', 'shelterbelts', count=7, size=58, stagger=0.1, along=[(48.6, -100.0), (41.0, -99.8), (33.8, -99.5)])],
          src=[src('30,233 shelterbelts were planted.', SB, '30,233 shelterbelts had been planted'),
               src('Covering 18,600 square miles.', SB, 'covering 18,600 square miles (48,000 km2)')]),
        S("It stretched from the Canadian border in North Dakota, all the way to the Brazos River in Texas.", [
            route([(48.9, -100.0), (41.0, -99.8), (33.5, -99.5)], 0.05, color='#16a34a', width=30, drawDur=0.4, glow=True), ping(48.9, -100, 'Canadian', color='#ffd60a'), ping(33.5, -99.5, 'Brazos', color='#ffd60a'), dot('Canada border', 48.9, -100, 'Canadian', dy=-56), dot('Brazos River', 33.5, -99.5, 'Brazos', dy=56),
            route([(48.9, -100), (41, -99.8), (33.5, -99.5)], 'stretched', color='#4ade80', width=8, drawDur=1.4, arrowHead=True)],
          cam=at_(41, -99, 2.5),
          src=[src('From the Canadian border in North Dakota to the Brazos River in Texas.', SB, 'from the Canadian border in North Dakota to the Brazos River in Texas')]),
        S("Experts later called it the largest government effort ever focused on an environmental problem in the US.", [
            route([(48.9, -100.0), (41.0, -99.8), (33.5, -99.5)], 0.05, color='#16a34a', width=30, drawDur=0.4, glow=True), stamp('BIGGEST EVER', 'largest', size=90), scatter(box(-101.5, 32, -98.5, 48.5), '🌳', 'Experts', count=7, size=58, stagger=0.1, along=[(48.6, -100.0), (41.0, -99.8), (33.8, -99.5)])],
          cam=at_(40, -99, 2.6, bearing=3), tr='flash',
          src=[src('Called the largest and most-focused government effort to address an environmental problem (as of 2007).', SB, 'the largest and most-focused effort of the [U.S.] government to address an environmental problem')]),
    ],
    keywords={'trees': '#4ade80', 'dust': '#f4a261', 'roosevelt': '#ffd60a', 'wind': '#5ec8ff'},
    captions={'theme': 'classic'})

# ------------------------------------------------------------------ 8. NORTH ATLANTIC TRACKS (neon)
NAT = 'North_Atlantic_Tracks'
JS = 'Jet_stream'
save('atlantic_tracks', meta(
    'The Invisible Highways Planes Use Over the Atlantic ✈️🌊🤯',
    "Planes crossing the North Atlantic ✈️ don't fly random routes. They follow the North Atlantic Tracks, invisible highways that are re-drawn twice a day to follow the jet stream 🌬️ The jet stream is a river of wind about 30,000 ft up, blowing west to east, sometimes up to 400 km/h! Flights to Europe ride it as a tailwind, flights to America avoid it. About 500,000 flights used the system in 2018 🤯",
    ["The sky has highways that move every day ✈️🤯", "Have you noticed flights to Europe are faster? 👇", "Which aviation secret should we explain next? 🗺️"],
    ['north atlantic tracks', 'jet stream', 'planes', 'aviation', 'transatlantic flights', 'tailwind', 'atlantic ocean', 'geography', 'maps', 'learn']),
    [
        S("Every day, planes cross the Atlantic on invisible highways in the sky.", [
            hook('INVISIBLE *HIGHWAYS* IN THE SKY', at=0.05, until='Atlantic'),
            *[route([(47 + d, -53), (50 + d, -40), (52 + d, -30), (53 + d, -20), (52 + d, -10)], 'highways', color='#2de2e6', width=5, drawDur=1.6, dashed=True, dash=[14, 10], hold=2) for d in (-2, 0, 2, 4)]],
          cam=at_(50, -32, 2.2),
          src=[src('The North Atlantic Tracks are structured transatlantic routes.', NAT, 'A structured set of transatlantic flight routes that stretch from eastern North America to western Europe across the Atlantic Ocean')]),
        S("They're called the North Atlantic Tracks, and they keep planes separated over the ocean, where there's little radar.", [
            *[plane([(47 + d, -53), (50 + d, -40), (52 + d, -30), (53 + d, -20), (52 + d, -10)], 'Tracks', drawDur=3.2) for d in (-2, 2)], icon('📡', 45, -30, 'radar', size=110)],
          src=[src('They separate aircraft over the ocean where there is little radar coverage.', NAT, 'ensure that aircraft are separated over the ocean, where there is little radar coverage')]),
        S("And here's the strange part: they're re-drawn twice every day.", [stamp('NEW ROUTES', 'twice', size=86), clock([('twice', '00:00'), ('day', '12:00')], screen=(0.5, 0.45), size=200)],
          src=[src('The tracks are created twice daily.', NAT, 'created twice daily to take account of the shifting of the winds aloft')]),
        S("Because they follow the jet stream, a river of wind about 30,000 feet up, blowing from west to east.", [
            flow([(40, -75), (45, -55), (50, -35), (52, -15), (50, 0)], 'jet', color='#a78bfa', width=16, drawDur=1.6, flowSpeed=260), slam('JET STREAM', 45, -50, 'jet', size=64)],
          cam=at_(48, -38, 1.9),
          src=[src('Jet streams are westerly winds near the tropopause (~30,000 ft).', JS, 'westerly winds, flowing west to east around the globe')]),
        S("It can reach 400 kilometers per hour.", [flow([(40, -75), (45, -55), (50, -35), (52, -15), (50, 0)], 'It', color='#a78bfa', width=22, drawDur=0.4, flowSpeed=520), cnt('400 km/h', '400', size=180, color='#a78bfa'), tilt('400', deg=34, until=2.5)],
          cam=at_(48, -38, 1.9),
          src=[src('Jet stream winds can reach 400 km/h.', JS, '400 km/h (220 kn; 250 mph)')]),
        S("So flights to Europe ride it as a tailwind, and flights to America try to avoid it.", [
            plane([(42, -72), (47, -50), (51, -30), (52, -10)], 'Europe', rid='east'), plane([(52, -8), (58, -30), (58, -50), (48, -70)], 'America', rid='west'),
            lab('TAILWIND', 45, -45, 'tailwind', style='pill', bg='#16a34a', size=46), lab('HEADWIND', 60, -40, 'avoid', style='pill', size=46)],
          cam=at_(50, -38, 1.9),
          src=[src('Tracks minimize headwinds and maximize tailwinds.', NAT, 'minimize any head winds and maximize tail winds impact on the aircraft')]),
        S("Flying east across North America with the jet stream can save about 30 minutes.", [flow([(38, -122), (41, -105), (42, -90), (41, -74)], 'Flying', color='#a78bfa', width=16, drawDur=1.0, flowSpeed=300), plane([(37.6, -122.4), (41, -100), (40.7, -74)], 'east', rid='us', drawDur=2.6),
            clock([('east', '10:00'), ('minutes', '10:30')], screen=(0.5, 0.26), size=200, label='−30 min')],
          cam=at_(40, -98, 2.4),
          src=[src('Eastbound flights across North America can save about 30 minutes.', JS, 'about 30 minutes')]),
        S("Back in 1952, a Pan Am flight from Tokyo to Honolulu used it to cut the trip from 18 hours to 11 and a half.", [
            year(1952, '1952'), dot('Tokyo', 35.6, 139.8, 'Tokyo', dy=-50), dot('Honolulu', 21.3, -157.9, 'Honolulu', dy=50), plane([(35.6, 139.8), (30, 170), (21.3, -157.9)], 'Tokyo', rid='pa'),
            bars([('Before', 18, '18 h', '#ff5a5f'), ('Jet stream', 11.5, '11.5 h', '#4ade80')], 'cut', screen=[0.5, 0.33], labelWidth=240)],
          cam=at_(42, 170, 1.4), era='history', tr='film',
          src=[src('In 1952 Pan Am cut Tokyo–Honolulu from 18 to 11.5 hours using the jet stream.', JS, 'cut the trip time by over one-third, from 18 to 11.5 hours')]),
        S("In 2018 alone, about 500,000 flights used these moving highways.", [*[route([(47 + d, -53), (50 + d, -40), (52 + d, -30), (53 + d, -20), (52 + d, -10)], 'In', color='#2de2e6', width=5, drawDur=0.8, dashed=True, dash=[14, 10]) for d in (-2, 0, 2, 4)], *[plane([(47 + d, -53), (50 + d, -40), (52 + d, -30), (53 + d, -20), (52 + d, -10)], 'flights', drawDur=3.0) for d in (0, 4)], cnt('500,000', '500,000', size=180)],
          cam=at_(50, -32, 2.2),
          src=[src('500,000 flights went through the system in 2018.', NAT, '500,000 flights went through')]),
    ],
    keywords={'jet': '#a78bfa', 'atlantic': '#2de2e6', 'europe': '#4ade80', 'america': '#ff5a5f'},
    styles={'now': 'neon', 'history': 'vintage'}, captions={'theme': 'box'})

# ------------------------------------------------------------------ 9. WALLACE LINE
WL = 'Wallace_Line'
WLINE = [(12, 121), (4.5, 119.5), (-1.5, 118.3), (-5.5, 117.2), (-8.1, 115.9), (-9.5, 115.8)]
save('wallace_line', meta(
    "Why Animals Don't Cross This Invisible Line 🦘🐒🚧 The Wallace Line",
    "Bali and Lombok 🇮🇩 are only about 35 km apart, but their animals are completely different 🐒🦘 In 1859 naturalist Alfred Russel Wallace noticed an invisible boundary: west of it you find Asian animals like apes, elephants and monkeys, east of it Australasian ones like marsupials 🤯 Why? Deep water. Even when sea levels dropped 120 m in the Ice Age, the islands never connected Asia with Australia 🌊",
    ["35 km of water that animals never crossed 🤯🐒🦘", "Did you know about the Wallace Line? 👇", "Which invisible line should we explain next? 🗺️"],
    ['wallace line', 'bali', 'lombok', 'indonesia', 'alfred russel wallace', 'animals', 'marsupials', 'biogeography', 'geography', 'maps', 'learn']),
    [
        S("There's an invisible line in Indonesia that animals almost never cross.", [
            hook("THE *INVISIBLE* ANIMAL BORDER", at=0.05, until='Indonesia'),
            route(WLINE, 'line', color='#ffd60a', width=7, dashed=True, dash=[18, 12], drawDur=1.6, hold=6)],
          cam=at_(-2, 118, 2.4), no_claim=True),
        S("It runs between Bali and Lombok, two islands only about 35 kilometers apart.", [
            dot('Bali', -8.4, 115.2, 'Bali', dy=-56), dot('Lombok', -8.6, 116.35, 'Lombok', dy=-56), meas((-8.5, 115.6), (-8.5, 116.05), '35 km', 'kilometers')],
          cam=at_(-8.5, 115.8, 16, bearing=-3),
          src=[src('The line runs through the Lombok Strait between Bali and Lombok, about 35 km.', WL, 'through the Lombok Strait between Bali and Lombok, where the distance is strikingly small, only about 35 kilometers (22 mi)')]),
        S("In 1859, naturalist Alfred Russel Wallace noticed something strange.", [year(1859, '1859'), char('alfred_wallace', 'Wallace', say='Hmm, different animals!')],
          cam=at_(-8.5, 115.8, 10), era='history', tr='film',
          src=[src('Alfred Russel Wallace identified the boundary in 1859.', WL, '1859')]),
        S("Travelling through the islands, he saw a clear split in both mammals and birds.", [
            icon('🦜', -6, 110, 'birds', size=110), icon('🐒', -3, 105, 'mammals', size=110), icon('🦘', -6, 125, 'split', size=110)],
          cam=at_(-4, 116, 2.8), era='history',
          src=[src('Wallace noticed the division in land mammals and birds.', WL, 'Wallace noticed this clear division in both land mammals and birds during his travels through the East Indies in the 19th century.')]),
        S("West of the line, you find Asian animals, like apes, elephants and monkeys.", [
            hl({'admin1s': ['Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung', 'Bangka-Belitung', 'Kepulauan Riau', 'Banten', 'Jakarta Raya', 'Jawa Barat', 'Jawa Tengah', 'Yogyakarta', 'Jawa Timur', 'Bali', 'Kalimantan Barat', 'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur'], 'country': 'IDN'}, '#f59e0b', 'West', fillOpacity=0.55), hl({'countries': ['MYS', 'BRN']}, '#f59e0b', 'West', fillOpacity=0.55), icon('🦧', 0.8, 113.8, 'apes', size=96), icon('🐘', -0.3, 101.8, 'elephants', size=96), icon('🐒', -7.4, 110.2, 'monkeys', size=90), lab('ASIA', 5, 106, 'Asian', style='pill', bg='#d97706', size=52)],
          cam=at_(-2, 112, 2.6),
          src=[src('West of the line: Asian fauna such as apes, elephants and monkeys.', WL, 'apes, elephants')]),
        S("East of the line, the animals are Australian, like marsupials.", [
            hl({'admin1s': ['Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Sulawesi Barat', 'Gorontalo', 'Maluku', 'Maluku Utara', 'Papua', 'Papua Barat'], 'country': 'IDN'}, '#16a34a', 'East', fillOpacity=0.55), hl({'countries': ['PNG', 'TLS', 'AUS']}, '#16a34a', 'East', fillOpacity=0.45), icon('🦘', -16.5, 133, 'marsupials', size=96), icon('🐨', -5.5, 142.5, 'marsupials', size=90), lab('AUSTRALIA', -3, 128, 'Australian', style='pill', bg='#16a34a', size=52)],
          cam=at_(-4, 124, 2.6),
          src=[src('East of the line: Australasian species such as marsupials.', WL, 'marsupials')]),
        S("Why? Deep water. Even in the Ice Age, when seas dropped 120 meters, the two sides never joined.", [
            tilt('water', deg=38, until=4.5), cnt('−120 m', '120', size=170, color='#5ec8ff'), route([(-7.2, 115.75), (-8.3, 115.85), (-9.3, 115.8)], 'Deep', color='#5ec8ff', width=14, flow=True, drawDur=0.8), lab('LOMBOK STRAIT', -8.1, 117.2, 'Deep', style='pill', bg='#1d4ed8', size=40)],
          cam=at_(-8.5, 116, 8), tr='flash',
          src=[src('Even when sea level dropped 120 m, the islands never united Asia with Australia.', WL, 'islands became connected, but never uniting Asia with Australia')]),
        S("Bali sits on the Asian shelf, Lombok on the other side. For over 50 million years, deep water kept the two worlds apart.", [
            hl({'admin1s': ['Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung', 'Bangka-Belitung', 'Kepulauan Riau', 'Banten', 'Jakarta Raya', 'Jawa Barat', 'Jawa Tengah', 'Yogyakarta', 'Jawa Timur', 'Bali', 'Kalimantan Barat', 'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur'], 'country': 'IDN'}, '#f59e0b', 'Asian', fillOpacity=0.55), hl({'countries': ['MYS', 'BRN']}, '#f59e0b', 'Asian', fillOpacity=0.55), hl({'admin1s': ['Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Sulawesi Barat', 'Gorontalo', 'Maluku', 'Maluku Utara', 'Papua', 'Papua Barat'], 'country': 'IDN'}, '#16a34a', 'other', fillOpacity=0.55), hl({'countries': ['PNG', 'TLS', 'AUS']}, '#16a34a', 'other', fillOpacity=0.45),
            cnt('50,000,000 years', '50', size=120), lab('ASIAN SIDE', -2, 108, 'Asian', style='pill', bg='#d97706', size=48, fixed=True), lab('AUSTRALIAN SIDE', -6, 128, 'other', style='pill', bg='#16a34a', size=48, fixed=True)],
          cam=at_(-5, 118, 2.3),
          src=[src('Deep water between the Sunda and Sahul shelves separated the fauna for over 50 million years.', WL, 'for over 50 million years, deep water between those two large continental shelf areas created a barrier that kept the flora and fauna of Australia separated from those of Asia.')]),
    ],
    keywords={'wallace': '#ffd60a', 'bali': '#f4a261', 'lombok': '#4ade80', 'asian': '#f4a261', 'australian': '#4ade80'},
    captions={'theme': 'bebas'})
