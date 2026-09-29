from helpers import *

# ------------------------------------------------------------------ 19. GREENLAND vs ICELAND (globe)
save('greenland_iceland', meta(
    'Why Greenland Is Ice and Iceland Is Green ❄️🌿🤯',
    "Greenland 🇬🇱 is covered by ice, and Iceland 🇮🇸 is surprisingly green. So are the names swapped? 🤔 According to the sagas, Erik the Red named Greenland to attract settlers: 'people would be attracted there if it had a favourable name' 😅 Iceland got its name from Flóki Vilgerðarson, who climbed a mountain after a harsh winter and saw an ice cap. Today about 81% of Greenland is ice sheet, while lakes and glaciers cover only 14.3% of Iceland, which is warmed by the Gulf Stream 🌊",
    ["The world's oldest marketing trick? 😂❄️🌿", "Would you rather visit Greenland or Iceland? 👇", "Which name mix-up next? 🗺️"],
    ['greenland', 'iceland', 'erik the red', 'vikings', 'ice sheet', 'gulf stream', 'denmark', 'arctic', 'geography', 'maps', 'learn']),
    [
        S("Greenland is covered in ice, and Iceland is green. Did someone mix up the names?", [
            hook('GREEN-*ICE*-LAND?', at=0.05, until='names'), hl('GRL', '#38bdf8', 'Greenland', fillOpacity=0.55, neon='#9ee7ff'), hl('ISL', '#16a34a', 'Iceland', fillOpacity=0.9, neon='#4ade80'), lab('GREENLAND', 74, -40, 'Greenland', style='pill', bg='#0369a1', size=50), lab('ICELAND', 66.3, -18, 'Iceland', style='pill', bg='#15803d', size=46),
            q(70, -30, 'mix')],
          cam=at_(70, -30, 2.0), no_claim=True),
        S("Greenland is the largest island in the world, and about 81 percent of it is a giant ice sheet.", [
            hl('GRL', '#38bdf8', 'largest', fillOpacity=0.55, neon='#9ee7ff'), cnt('81%', '81', size=210, color='#9ee7ff'), cnt_steps([('largest', '#1 island')], size=90, screen=[0.5, 0.22])],
          cam=at_(72, -40, 2.2),
          src=[src('Greenland is the world\'s largest island.', 'Greenland', "It is the world's largest island"),
               src('The ice sheet covers 81% of it.', 'Greenland', 'covers 1,755,637 km2 (677,855 sq mi) (81%)')]),
        S("So why call it green? It was a sales trick, by the Viking Erik the Red.", [
            hl('GRL', '#8b5e34', 0.05, fillOpacity=0.5), lab('Greenland', 72, -40, 0.05, style='serif', size=60), char('viking_erik', 'sales', name='Erik the Red', say='Come to Greenland!')],
          cam=at_(64, -45, 3.0), era='history', tr='film',
          src=[src('Erik the Red named it Greenland to attract settlers.', 'Greenland', 'which he called Greenland, as he said people would be attracted there if it had a favourable name')]),
        S("The sagas say he called it Greenland, because people would be attracted there if it had a nice name.", [
            hl('GRL', '#8b5e34', 0.05, fillOpacity=0.5), note('GREAT MARKETING', 75, -42, 'nice', size=58), ship([(64.1, -21.9), (64, -30), (62, -42), (61, -45.5)], 'attracted', 'erik', emblem='#b91c1c', style='longship')],
          cam=at_(64, -35, 2.6), era='history',
          src=[src('Erik: people would be attracted if it had a favourable name.', 'Greenland', 'as he said people would be attracted there if it had a favourable name')]),
        S("And Iceland? Its name comes from Flóki, a Viking who climbed a mountain after a harsh winter, and saw an ice cap.", [
            hl('ISL', '#8b5e34', 'Iceland', fillOpacity=0.6), lab('Iceland', 66.9, -18.5, 'Iceland', style='serif', size=60), icon('🏔️', 65.5, -23, 'mountain', size=120), icon('🧊', 65, -18, 'ice', size=110)],
          cam=at_(64.9, -19, 6), era='history',
          src=[src('Flóki Vilgerðarson named it after seeing an ice cap.', 'Iceland', 'Flóki coined the name after he climbed a mountain, despondent after a harsh winter in present-day Vatnsfjörður, and saw an ice cap.')]),
        S("Today, lakes and glaciers cover only 14.3 percent of Iceland.", [
            lab('ICELAND', 66.3, -18, 0.05, style='pill', bg='#15803d', size=46), bars([('Greenland', 81, '81% ice', '#9ee7ff', 'gl'), ('Iceland', 14.3, '14.3%', '#4ade80', 'is')], 'cover', screen=[0.5, 0.3], labelWidth=280)],
          cam=at_(66, -30, 2.2), tr='flash',
          src=[src('Lakes and glaciers cover 14.3% of Iceland.', 'Iceland', 'Lakes and glaciers cover 14.3% of its surface')]),
        S("Because Iceland is warmed by the Gulf Stream, even though it's just south of the Arctic Circle.", [
            hl('ISL', '#16a34a', 0.05, fillOpacity=0.9, neon='#4ade80'), lab('ICELAND', 66.3, -18, 0.05, style='pill', bg='#15803d', size=46), flow([(40, -60), (50, -40), (58, -28), (64, -20)], 'warmed', color='#ff5a2a', width=14), route([(66.56, -50), (66.56, 0)], 'Arctic', rhumb=True, color='#9ee7ff', width=5, dashed=True, dash=[12, 10])],
          cam=at_(60, -30, 1.8),
          src=[src('Iceland is warmed by the Gulf Stream, just south of the Arctic Circle.', 'Iceland', 'Iceland is warmed by the Gulf Stream and has a temperate climate, despite being at a latitude just south of the Arctic Circle.')]),
    ],
    keywords={'greenland': '#9ee7ff', 'iceland': '#4ade80', 'erik': '#ff5a5f', 'ice': '#9ee7ff'},
    style='globe', captions={'theme': 'pop'})

# ------------------------------------------------------------------ 20. AMAZON BRIDGES
LBV = 'https://www.labrujulaverde.com/en/2026/05/no-bridge-crosses-the-amazon-the-longest-river-in-the-world-how-is-it-possible/'
IFA = 'https://interestingfacts.com/fact/there-are-no-bridges-across-the-amazon-river/'
AMZ = [(-4.4, -73.2), (-3.7, -70.0), (-3.3, -64.7), (-3.1, -60.0), (-2.6, -56.7), (-2.0, -54.0), (-1.5, -52.5), (0.0, -50.0)]
save('amazon_bridges', meta(
    'Why No Bridge Crosses the Amazon River 🌊🌴🤯',
    "The Amazon 🇧🇷 flows for more than 6,400 km, and not a single bridge crosses it 🌉❌ Between December and May the rains swell the river, and in some stretches the water spreads 10, 15 or even 20 km from shore to shore 🌊 Its waters can rise 30 feet, and the soft riverbanks are always eroding. In the 1990s studies found bridge piles would need to go more than 100 m deep! And there are few roads to connect anyway, so ferries and boats do the job ⛴️",
    ["6,400 km of river… zero bridges 🤯🌉", "Would you cross the Amazon by ferry? ⛴️👇", "Which river mystery next? 🗺️"],
    ['amazon river', 'bridges', 'brazil', 'rainforest', 'manaus', 'ferry', 'flooding', 'rivers', 'geography', 'maps', 'learn']),
    [
        S("The Amazon flows for more than 6,400 kilometers. And not a single bridge crosses it.", [
            hook('ZERO *BRIDGES*', at=0.05, until='kilometers'), flow(AMZ, 'flows', color='#5ec8ff', width=12, drawDur=2.4, hold=1), cnt('0', 'single', size=220, color='#ff5a5f')],
          cam=at_(-3, -61, 3.0),
          src=[src('More than 6,400 km and no bridge connects its banks.', LBV, 'along its more than 6,400 kilometers, no bridge connects its banks. Not a single one.')]),
        S("Why? First, the river changes size. From December to May, heavy rains make it swell.", [
            flow(AMZ, 0.05, color='#5ec8ff', width=12, drawDur=0.6), tilt('swell', deg=38, until=4), hl({'admin1': 'Amazonas', 'country': 'BRA'}, '#1d4ed8', 'swell', fillOpacity=0.35)],
          cam=at_(-3.1, -60.5, 7),
          src=[src('Rains swell the basin between December and May.', LBV, 'When torrential rains swell the basin between December and May')]),
        S("Its waters can rise 30 feet, and in some places it spreads 10, 15, even 20 kilometers from shore to shore.", [
            flow(AMZ, 0.05, color='#5ec8ff', width=12, drawDur=0.6), hl({'admin1': 'Amazonas', 'country': 'BRA'}, '#1d4ed8', 0.05, fillOpacity=0.35), meas((-3.35, -60.5), (-2.95, -60.5), '20 km', '20', countUp=False), cnt('+30 ft', '30', size=170, color='#5ec8ff'), cnt_steps([('10', '10 km'), ('15', '15 km'), ('20', '20 km')], size=110, screen=[0.5, 0.23])],
          cam=at_(-3.1, -60.5, 9),
          src=[src('Waters rise 30 feet in the rainy season.', IFA, 'its waters rise 30 feet, causing 3-mile-wide crossings to grow by a factor of 10'),
               src('The water spreads 10, 15 or 20 km between shores.', LBV, 'the water spreads without obstacles to exceed 10, 15, or, in some stretches, 20 kilometers between the extreme shores')]),
        S("The riverbanks are soft mud, always eroding. In the 1990s, studies found a bridge's piles would need to go more than 100 meters deep.", [
            flow(AMZ, 0.05, color='#5ec8ff', width=12, drawDur=0.6), bars([('Piles needed', 100, '100+ m', '#f97316'), ('Statue of Liberty', 93, '93 m', '#4ade80')], 'piles', orient='v', height=360, screen=[0.5, 0.33]), year(1990, '1990s')],
          tr='flash',
          src=[src('The banks are soft, eroding sediment.', IFA, 'The river bank itself is also in a near-constant state of erosion due to how soft the sediment it consists of is'),
               src('Piles would need to go more than 100 m deep.', LBV, 'estimated that to reach competent ground the piles would have to descend more than 100 meters'),
               src('The Statue of Liberty is 93 m tall including its pedestal.', 'Statue_of_Liberty', '93 m')]),
        S("And there are very few roads on either side that would need a bridge anyway.", [
            flow(AMZ, 0.05, color='#5ec8ff', width=12, drawDur=0.6), char('jungle_explorer', 'roads', say='Where is the road?')],
          cam=at_(-3.1, -60.5, 6),
          src=[src('There are few roads on either side that need connecting.', IFA, 'there are few roads on either side of the Amazon that need to be connected')]),
        S("So people cross by boat. A ferry does the job, for a tiny fraction of the cost of a bridge.", [
            ship([(-3.14, -60.1), (-3.2, -59.95)], 'boat', 'ferry', emblem='#ffd60a', drawDur=2.0, style='cargo')],
          cam=at_(-3.15, -60.0, 60, bearing=-3),
          src=[src('Boats and ferries are the preferred way to cross.', IFA, 'boats and ferries are the preferred method of crossing the Amazon'),
               src('A ferry does it at negligible cost compared with a major civil work.', LBV, 'at negligible cost compared to any major civil work')]),
        S("The only big bridge nearby crosses the Rio Negro at Manaus. It opened in 2011, and it's 3,595 meters long.", [
            ping(-3.11, -60.08, 'Manaus', color='#ffd60a'), dot('Rio Negro Bridge', -3.11, -60.08, 'Negro', dy=-56), cnt('3,595 m', '3,595', size=160)],
          cam=at_(-3.1, -60.08, 120),
          src=[src('The bridge over the Negro River opened in 2011 and spans 3,595 m.', LBV, 'to span 3,595 meters')]),
    ],
    keywords={'amazon': '#5ec8ff', 'bridge': '#ffd60a', 'bridges': '#ffd60a', 'ferry': '#ffd60a'},
    captions={'theme': 'classic'})

# ------------------------------------------------------------------ 21. TORNADO ALLEY (chalk)
TA = 'Tornado_Alley'
save('tornado_alley', meta(
    'Why the USA Has the Most Tornadoes on Earth 🌪️🇺🇸😳',
    "The United States 🇺🇸 gets about 1,200 tornadoes a year, more than any other country. Canada, in second place, averages about 62 🌪️ Why? In Tornado Alley, warm humid air from the Gulf of Mexico meets cold dry air from Canada and the Rocky Mountains 🏔️ North America has no big east-west mountain range to keep these air masses apart, so they collide again and again, creating powerful thunderstorms and supercells ⛈️",
    ["1,200 tornadoes a year 🌪️😳", "Have you ever seen a tornado? 👇", "Which weather mystery next? 🗺️"],
    ['tornado alley', 'tornadoes', 'usa', 'weather', 'supercell', 'gulf of mexico', 'rocky mountains', 'storm', 'geography', 'maps', 'learn']),
    [
        S("The United States gets about 1,200 tornadoes every year. More than any other country on Earth.", [
            hook('TORNADO *ALLEY*', at=0.05, until='States'), hl('USA', '#ff5a5f', 'States', fillOpacity=0.45), cnt('1,200', '1,200', size=200), scatter({'admin1s': ['Texas', 'Oklahoma', 'Kansas', 'Nebraska', 'Iowa', 'Missouri'], 'country': 'USA'}, '🌪️', 'year', count=6, size=64, stagger=0.1)],
          cam=at_(39, -97, 2.2),
          src=[src('The US averages about 1,200 tornadoes a year.', 'Tornado', 'The United States averages about 1,200 tornadoes per year, followed by Canada, averaging 62 reported per year.')]),
        S("Canada comes second, with only about 62.", [
            bars([('USA', 1200, '1,200', '#ff5a5f', 'us'), ('Canada', 62, '62', '#5ec8ff', 'ca')], 'Canada', screen=[0.5, 0.3], labelWidth=220)],
          src=[src('Canada averages 62 per year.', 'Tornado', 'followed by Canada, averaging 62 reported per year')]),
        S("Tornado Alley has no official borders, but it can stretch from central Texas, all the way up to the Canadian Prairies.", [
            hl({'admin1s': ['Texas', 'Oklahoma', 'Kansas', 'Nebraska', 'South Dakota', 'Iowa'], 'country': 'USA'}, '#ff5a5f', 'borders', fillOpacity=0.35), route([(31, -99), (38, -98), (45, -98), (52, -104)], 'stretch', color='#ff5a5f', width=9, drawDur=1.6, arrowHead=True), dot('Central Texas', 31, -99, 'Texas', dy=52), dot('Canadian Prairies', 52, -104, 'Prairies', dy=-52)],
          cam=at_(41, -99, 2.0),
          src=[src('It can reach from central Texas to the Canadian Prairies.', TA, 'Tornado Alley can also be defined as an area reaching from central Texas to the Canadian Prairies and from eastern Colorado to western Ohio')]),
        S("Most of them hit here, in the middle of the country. It's called Tornado Alley.", [
            *[hl({'admin1': st, 'country': 'USA'}, '#ff5a5f', 'middle', fillOpacity=0.55) for st in ['Texas', 'Oklahoma', 'Kansas', 'Nebraska', 'South Dakota', 'Iowa', 'Missouri']],
            slam('TORNADO ALLEY', 38, -98, 'Alley', size=66)],
          cam=at_(38, -97, 3.0),
          src=[src('Tornado Alley covers the central US.', TA, 'The area common to most definitions extends from Arkansas, Illinois, Indiana, Iowa, Kansas, Minnesota, Missouri, Montana, Nebraska, North Dakota, Ohio, Oklahoma, South Dakota, Texas, Wisconsin')]),
        S("Warm, humid air flows up from the Gulf of Mexico.", [
            flow([(24, -92), (29, -95), (34, -97), (38, -97)], 'Warm', color='#ff5a2a', width=18, drawDur=1.6, hold=2), lab('WARM & HUMID', 26, -92, 'humid', style='pill', bg='#ff5a2a', size=44)],
          cam=at_(34, -97, 2.8),
          src=[src('The Gulf of Mexico fuels abundant low-level moisture.', 'Tornado', 'the Gulf of Mexico fuels abundant low-level moisture in the southerly flow to its east')]),
        S("And cold, dry air comes down from Canada and the Rocky Mountains.", [
            flow([(52, -105), (46, -102), (41, -99)], 'cold', color='#5ec8ff', width=18, drawDur=1.6, hold=1), flow([(40, -110), (39, -104), (38.5, -100)], 'Rocky', color='#e5e7eb', width=14, drawDur=1.4, hold=1),
            lab('COLD & DRY', 49, -104, 'dry', style='pill', bg='#1d4ed8', size=44)],
          cam=at_(40, -100, 2.6),
          src=[src('Cold, dry air from Canada and the Rockies meets warm humid air.', TA, 'In Tornado Alley, warm, humid air from the equator meets cool to cold, dry air from Canada and the Rocky Mountains.')]),
        S("When they collide, they create giant thunderstorms, called supercells.", [
            icon('⛈️', 37, -98, 'collide', size=160), shake('collide'), tilt('supercells', deg=40, until=3.5), char('storm_chaser', 'supercells', say='Here it comes!')],
          cam=at_(37, -98, 5), tr='flash',
          src=[src('This creates an ideal environment for tornadoes within supercells.', TA, 'This creates an ideal environment for tornadoes to form within developed thunderstorms and supercells.')]),
        S("And there's no big east-west mountain range to keep these air masses apart. So they meet again and again.", [
            flow([(24, -92), (29, -95), (34, -97), (38, -97)], 'And', color='#ff5a2a', width=16, drawDur=1.0), flow([(52, -105), (46, -102), (41, -99)], 'And', color='#5ec8ff', width=16, drawDur=1.0),
            icon('⛈️', 39, -98, 'again', size=150), stamp('NO BARRIER', 'apart', size=86)],
          cam=at_(38, -97, 2.3),
          src=[src('No major east-west mountain barriers allow frequent collisions of warm and cold air.', 'Tornado', 'This unique topography allows for frequent collisions of warm and cold air, the conditions that breed strong, long-lived storms throughout the year.')]),
    ],
    keywords={'tornado': '#ff5a5f', 'tornadoes': '#ff5a5f', 'warm': '#ff5a2a', 'cold': '#5ec8ff', 'alley': '#ff5a5f'},
    styles={'now': 'chalk', 'history': 'vintage'}, captions={'theme': 'impact'})

# ------------------------------------------------------------------ 22. RECURSIVE ISLAND
VP = (14.0096, 120.9966)
VPA = 'Vulcan_Point'
save('recursive_island', meta(
    'An Island in a Lake on an Island in a Lake on an Island 🤯🇵🇭',
    "Meet Vulcan Point 🇵🇭 It's an island in Main Crater Lake, which is on Volcano Island, which sits in Taal Lake, which is on the island of Luzon in the Philippines 🤯 It's one of only a few 'islands in a lake on an island in a lake on an island' in the world. When Taal Volcano erupted in January 2020, the crater lake's water disappeared 🌋 Later, typhoon rains refilled it, and the lake and its tiny island came back 🌧️",
    ["Island-ception 🤯🏝️", "Did you know recursive islands exist? 👇", "Which weird island next? 🗺️"],
    ['vulcan point', 'taal volcano', 'taal lake', 'luzon', 'philippines', 'recursive island', 'island in a lake', 'volcano', 'geography', 'maps', 'learn']),
    [
        S("This tiny rock might be the strangest island on Earth.", [hook('ISLAND-*CEPTION*', at=0.05, until='rock'), ping(*VP, 'rock', color='#ffd60a')],
          cam=at_(14.01, 121.0, 1500), no_claim=True),
        S("It's Vulcan Point, an island in a lake.", [slam('VULCAN POINT', 14.012, 120.9966, 'Vulcan', size=58), ping(*VP, 'island', color='#ffd60a')],
          cam=at_(14.01, 121.0, 2200, bearing=-3),
          src=[src('Vulcan Point sits in Main Crater Lake.', VPA, 'one of only a few islands in a lake on an island in a lake on an island in the world')]),
        S("That lake, Main Crater Lake, is on an island too: Volcano Island.", [
            dot('Main Crater Lake', 14.016, 120.998, 'Crater', dy=-50, size=36), dot('Volcano Island', 13.99, 120.99, 'Volcano', dy=56, size=38)],
          cam=at_(14.0, 120.995, 320),
          src=[src('Main Crater Lake sits inside Taal Volcano (Volcano Island).', VPA, 'one of only a few islands in a lake on an island in a lake on an island in the world')]),
        S("Volcano Island sits in another lake: Taal Lake.", [dot('Taal Lake', 13.95, 121.02, 'Taal', dy=-50)],
          cam=at_(13.95, 121.0, 60),
          src=[src('Volcano Island lies in Taal Lake.', VPA, 'one of only a few islands in a lake on an island in a lake on an island in the world')]),
        S("And Taal Lake is on a bigger island: Luzon, in the Philippines.", [hl('PHL', 'flag:ph', 'Luzon', fillOpacity=0.7), dot('Luzon', 15.8, 121, 'Luzon', dy=50)],
          cam=at_(14.5, 121, 6),
          src=[src('Taal Lake is on Luzon.', VPA, 'one of only a few islands in a lake on an island in a lake on an island in the world')]),
        S("An island, in a lake, on an island, in a lake, on an island. One of only a few in the world.", [
            timeline([('An', '1', 'Rock'), ('lake,', '2', 'Crater'), ('on', '3', 'Volcano'), ('in', '4', 'Taal'), ('world', '5', 'Luzon')], screen=(0.5, 0.25), width=940)],
          cam=at_(14.3, 121.0, 12), tr='flash',
          src=[src('One of only a few such recursive islands.', VPA, 'one of only a few islands in a lake on an island in a lake on an island in the world')]),
        S("Then in January 2020, Taal Volcano erupted, and the water of Main Crater Lake disappeared.", [
            year(2020, '2020', light=True), icon('🌋', 14.0, 120.995, 'erupted', size=150), shake('erupted'), stamp('LAKE GONE', 'disappeared', size=86, screen=[0.5, 0.5])],
          cam=at_(14.0, 120.995, 300),
          src=[src('After the January 2020 eruption, the water in Main Crater Lake had disappeared.', VPA, 'the water in Main Crater Lake had disappeared')]),
        S("But typhoon rains later filled it up again, and the little island came back.", [icon('🌧️', 14.02, 121.0, 'rains', size=120), ping(*VP, 'island', color='#4ade80')],
          cam=at_(14.01, 121.0, 1500, bearing=3),
          src=[src('Typhoons let rain re-accumulate and reform Main Crater Lake.', VPA, 'a series of typhoons allowed rain to re-accumulate and reform Main Crater Lake')]),
    ],
    keywords={'island': '#ffd60a', 'lake': '#5ec8ff', 'vulcan': '#ff5a5f', 'taal': '#5ec8ff'},
    captions={'theme': 'box'})

# ------------------------------------------------------------------ 23. UK vs GB vs ENGLAND (atlas)
BT = 'Terminology_of_the_British_Isles'
ENG, SCO, WAL, NIR = [{'geonunit': n, 'country': 'GBR'} for n in ('England', 'Scotland', 'Wales', 'Northern Ireland')]
save('uk_gb_england', meta(
    'UK vs Great Britain vs England: What\'s the Difference? 🇬🇧🏴󠁧󠁢󠁥󠁮󠁧󠁿🤯',
    "England, Great Britain and the United Kingdom are NOT the same thing 🇬🇧 England is one of four countries in the UK, together with Scotland, Wales and Northern Ireland 🏴󠁧󠁢󠁳󠁣󠁴󠁿🏴󠁧󠁢󠁷󠁬󠁳󠁿 Great Britain is the largest island, home to England, Scotland and Wales. The United Kingdom is Great Britain plus Northern Ireland; its full name is 'the United Kingdom of Great Britain and Northern Ireland'. And the British Isles? Great Britain, the island of Ireland and many smaller islands, a term the Irish government rejects 🤯",
    ["England ≠ Great Britain ≠ UK 🤯🇬🇧", "Did you know the difference? 👇", "Which confusing name should we explain next? 🗺️"],
    ['uk', 'united kingdom', 'great britain', 'england', 'scotland', 'wales', 'northern ireland', 'british isles', 'ireland', 'geography', 'maps', 'learn']),
    [
        S("England, Great Britain, the United Kingdom. People mix them up all the time. They're not the same.", [
            hook('UK ≠ GB ≠ *ENGLAND*', at=0.05, until='Kingdom'), q(54, -3, 'same')],
          cam=at_(54.5, -4, 4.2), no_claim=True),
        S("England is one of four countries. The others are Scotland, Wales and Northern Ireland.", [
            hl(ENG, '#e63946', 'England', fillOpacity=0.85), hl(SCO, '#1d4ed8', 'Scotland', fillOpacity=0.85), hl(WAL, '#16a34a', 'Wales', fillOpacity=0.85), hl(NIR, '#f59e0b', 'Northern', fillOpacity=0.85),
            cnt('4', 'four', size=220)],
          cam=at_(54.5, -4, 4.4),
          src=[src('England is one of the four countries of the UK.', BT, 'England, Scotland, Wales and Northern Ireland are the four countries of the United Kingdom')]),
        S("Great Britain is the name of the biggest island. It holds England, Scotland and Wales.", [
            hl(ENG, '#6d28d9', 'Great', fillOpacity=0.75), hl(SCO, '#6d28d9', 'Great', fillOpacity=0.75), hl(WAL, '#6d28d9', 'Great', fillOpacity=0.75),
            slam('GREAT BRITAIN', 55.5, -2.5, 'island', size=60)],
          cam=at_(54.5, -3.5, 4.4), tr='flash',
          src=[src('Great Britain is the largest island of the archipelago.', BT, 'the largest island of the archipelago')]),
        S("Add Northern Ireland, and you get the United Kingdom. Its full name is the United Kingdom of Great Britain and Northern Ireland.", [
            hl('GBR', 'flag:gb', 'United', fillOpacity=0.9, neon='#ffd60a'),
            stamp('UNITED KINGDOM', 'full', size=76)],
          cam=at_(54.5, -4, 4.4),
          src=[src('The UK is Great Britain plus Northern Ireland.', BT, 'Great Britain plus Northern Ireland')]),
        S("And the British Isles? That's Great Britain, the whole island of Ireland, and many smaller islands around them.", [
            hl('IRL', '#16a34a', 'Ireland', fillOpacity=0.7), hl('GBR', '#9ca3af', 'Great', fillOpacity=0.5), lab('+ 6,000 smaller islands', 58.5, -9.5, 'smaller', style='pill', bg='#0f766e', size=38)],
          cam=at_(54.5, -5, 3.6),
          src=[src('British Isles = Great Britain + Ireland + smaller islands.', BT, 'the island of Great Britain plus the island of Ireland and many smaller surrounding islands')]),
        S("But careful. The government of Ireland does not use that term at all.", [hl('IRL', 'flag:ie', 'Ireland', fillOpacity=0.9), stamp('NOT USED', 'term', size=90), shake('term')],
          cam=at_(53.4, -8, 6),
          src=[src('The Irish government\'s policy is not to use the term.', BT, 'The policy of the government of Ireland is that no branch of government should use the term')]),
    ],
    keywords={'england': '#e63946', 'scotland': '#5ec8ff', 'wales': '#4ade80', 'ireland': '#4ade80', 'kingdom': '#ffd60a', 'britain': '#a78bfa'},
    styles={'now': 'atlas', 'history': 'vintage'}, captions={'theme': 'bebas'})

# ------------------------------------------------------------------ 24. ANTARCTICA (globe atlas, south-pole view)
TC = 'Territorial_claims_in_Antarctica'
def wedge(w, e):
    return box(w, -90, e, -60)
save('antarctica_claims', meta(
    'Who Owns Antarctica? ❄️🗺️🤯',
    "Antarctica ❄️ is bigger than you think, and seven countries claim a piece of it: Argentina 🇦🇷, Australia 🇦🇺, Chile 🇨🇱, France 🇫🇷, New Zealand 🇳🇿, Norway 🇳🇴 and the United Kingdom 🇬🇧 Australia claims the biggest slice, and three claims even overlap 🤯 But one huge area, Marie Byrd Land, is claimed by nobody: at 1.6 million km² it's the largest unclaimed territory on Earth. Since the Antarctic Treaty of 1959, the continent is set aside for science 🔬",
    ["The biggest no-man's land on Earth is in Antarctica 🤯❄️", "Which country should own it? 👇", "Which map mystery next? 🗺️"],
    ['antarctica', 'territorial claims', 'marie byrd land', 'antarctic treaty', 'south pole', 'australia', 'norway', 'chile', 'argentina', 'geography', 'maps', 'learn']),
    [
        S("Who owns Antarctica? The answer is more complicated than you think.", [hook('WHO OWNS *ANTARCTICA*?', at=0.05, until='Antarctica'), q(-80, 0, 'complicated')],
          cam=at_(-90, 0, 1.4), no_claim=True),
        S("Seven countries claim a piece of it.", [cnt('7', 'Seven', size=220),
            *[flag(c, la, lo, 'claim', size=90) for c, la, lo in [('ar', -70, -50), ('au', -72, 100), ('cl', -72, -80), ('fr', -68, 139), ('nz', -80, -170), ('no', -73, 20), ('gb', -76, -40)]]],
          cam=at_(-90, 0, 1.3),
          src=[src('Seven sovereign states have made claims.', TC, 'Seven sovereign states – Argentina, Australia, Chile, France, New Zealand, Norway, and the United Kingdom – have made eight territorial claims in Antarctica.')]),
        S("Argentina, Australia, Chile, France, New Zealand, Norway, and the United Kingdom.", [
            hl(wedge(-74, -25), '#5ec8ff', 'Argentina', fillOpacity=0.5), hl(wedge(44.6, 136), '#ffd60a', 'Australia', fillOpacity=0.5), hl(wedge(142, 160), '#ffd60a', 'Australia', fillOpacity=0.5),
            hl(wedge(-90, -53), '#ff5a5f', 'Chile', fillOpacity=0.5), hl(wedge(136, 142), '#1d4ed8', 'France', fillOpacity=0.6), hl(wedge(160, 180), '#111827', 'Zealand', fillOpacity=0.5), hl(wedge(-180, -150), '#111827', 'Zealand', fillOpacity=0.5),
            hl(wedge(-20, 44.6), '#b91c1c', 'Norway', fillOpacity=0.45), hl(wedge(-80, -20), '#7c3aed', 'Kingdom', fillOpacity=0.4)],
          cam=at_(-90, 0, 1.3),
          src=[src('Claimants: Argentina, Australia, Chile, France, New Zealand, Norway, UK.', TC, 'Seven sovereign states – Argentina, Australia, Chile, France, New Zealand, Norway, and the United Kingdom – have made eight territorial claims in Antarctica.')]),
        S("Australia claims the biggest slice, almost 5.9 million square kilometers.", [
            hl(wedge(44.6, 136), 'flag:au', 'Australia', fillOpacity=0.8), hl(wedge(142, 160), 'flag:au', 'Australia', fillOpacity=0.8), cnt('5.9M km²', '5.9', size=150)],
          cam=at_(-90, 90, 1.4),
          src=[src('Australia claims 5,896,500 km² (table).', TC, '5,896,500')]),
        S("Norway claims a huge slice called Queen Maud Land, while France has the smallest one.", [
            hl(wedge(-20, 44.6), 'flag:no', 'Norway', fillOpacity=0.8), hl(wedge(136, 142), 'flag:fr', 'France', fillOpacity=0.9),
            bars([('Australia', 5896500, '5.9M km²', '#ffd60a', 'au'), ('Norway', 2700154, '2.7M km²', '#ff5a5f', 'no'), ('France', 351000, '0.35M km²', '#5ec8ff', 'fr')], 'smallest', screen=[0.5, 0.3], labelWidth=240)],
          cam=at_(-90, 60, 1.4),
          src=[src('Norway claims Queen Maud Land (2,700,154 km² incl. Peter I Island); France 351,000 km² (table).', TC, '351,000')]),
        S("And three claims overlap. The UK, Chile and Argentina all want the same land.", [
            hl(wedge(-80, -20), '#7c3aed', 'And', fillOpacity=0.3), hl(wedge(-90, -53), '#ff5a5f', 'And', fillOpacity=0.3), hl(wedge(-74, -25), '#5ec8ff', 'And', fillOpacity=0.3),
            hl(wedge(-74, -53), '#ff0080', 'overlap', fillOpacity=0.7, neon='#ffd60a'), vs(('gb', 'UK'), ('ar', 'Argentina'), 'want', screen=[0.5, 0.3])],
          cam=at_(-90, -60, 1.5), tr='flash',
          src=[src('Argentine, Chilean and British claims overlap.', TC, 'There are overlaps among the territories claimed by Argentina, Chile, and the United Kingdom.')]),
        S("But one huge area is claimed by nobody: Marie Byrd Land. It's the largest unclaimed territory on Earth.", [
            hl(wedge(-150, -90), '#0ea5e9', 'huge', fillOpacity=0.6, neon='#9ee7ff'), lab('MARIE BYRD LAND', -72, -120, 'Marie', style='pill', bg='#0369a1', size=46), cnt('1,610,000 km²', 'largest', size=110)],
          cam=at_(-90, -120, 1.5),
          src=[src('Marie Byrd Land (1,610,000 km²) is the largest unclaimed territory on Earth.', 'Marie_Byrd_Land', 'Marie Byrd Land (MBL) is an unclaimed region of Antarctica. With an area of 1,610,000 km2 (620,000 sq mi), it is the largest unclaimed territory on Earth.')]),
        S("And since the Antarctic Treaty of 1959, the whole continent is set aside for science.", [
            hl({'countries': ['ATA']}, '#9ee7ff', 'Antarctic', fillOpacity=0.35, neon='#9ee7ff'), year(1959, '1959', light=True), char('penguin', 'science', say='Science only!')],
          cam=at_(-90, 0, 1.3, bearing=10),
          src=[src('The 1959 Antarctic Treaty set Antarctica aside as a scientific preserve.', TC, 'set aside Antarctica as a scientific preserve, established freedom of scientific investigation')]),
    ],
    keywords={'antarctica': '#9ee7ff', 'australia': '#ffd60a', 'nobody': '#ffffff', 'marie': '#9ee7ff'},
    style='globe', captions={'theme': 'pop'})

# ------------------------------------------------------------------ 25. NEW YEAR (globe neon)
KIR = (1.87, -157.4)
BAK = (0.19, -176.48)
save('new_year', meta(
    'Who Celebrates New Year First, and Who Is Last? 🎆🌍🕛',
    "The first place on Earth to enter the New Year is Kiribati's Line Islands 🇰🇮, like Kiritimati, in UTC+14, the earliest time zone 🎆 Back in 1994 Kiribati moved its eastern islands across the date line, and in 2000 it was the first country to welcome the new millennium 🥳 The last places are Baker Island and Howland Island 🇺🇸, uninhabited US nature reserves in UTC−12. Between the first and the last New Year there are 26 hours! 🤯",
    ["First and last New Year are only ~2,000 km apart 🤯🎆", "What time do you celebrate New Year? 👇", "Which time mystery next? 🗺️"],
    ['new year', 'time zones', 'kiribati', 'kiritimati', 'baker island', 'howland island', 'international date line', 'utc+14', 'geography', 'maps', 'learn']),
    [
        S("Every New Year, one place on Earth celebrates first. And one place celebrates last.", [hook('FIRST & *LAST* NEW YEAR', at=0.05, until='first'), q(0, -170, 'last')],
          cam=at_(0, -170, 1.0), no_claim=True),
        S("The first is here: Kiribati's Line Islands, like Kiritimati, in the Pacific.", [
            ping(*KIR, 'first', color='#ffd60a'), dot('Kiritimati 🇰🇮', *KIR, 'Kiritimati', dy=-56), clock([('Kiritimati', '23:59'), ('Pacific', '00:00')], screen=(0.5, 0.22), size=180, label='UTC+14'), char('party_kid', 'first')],
          cam=at_(1.87, -157.4, 70),
          src=[src('The Line Islands (Kiritimati) use UTC+14.', 'UTC+14:00', 'the earliest time zone on Earth, meaning that areas in this zone are the first to see a new day, and therefore the first to enter a New Year')]),
        S("They use UTC plus 14, the earliest time zone on the planet.", [cnt('UTC+14', '14', size=170, color='#ffd60a')],
          src=[src('UTC+14 is the earliest time zone.', 'UTC+14:00', 'the earliest time zone on Earth')]),
        S("It wasn't always like that. At the end of 1994, Kiribati moved its eastern islands across the date line.", [
            year(1994, '1994', light=True), route([(20, 180), (-20, 180)], 'line', rhumb=True, color='#9ca3af', width=6, dashed=True, dash=[14, 10]), arrow((1.9, -150), (1.9, 172), 'across', color='#ffd60a'), dot('Kiribati', 1.87, -157.4, 'Kiribati', dy=-56)],
          cam=at_(0, -170, 1.4), tr='film',
          src=[src('Kiribati changed the date for its eastern half on 31 December 1994.', 'UTC+14:00', 'introduced a change of date for its eastern half on 31 December 1994, from time zones UTC−11:00 and UTC−10:00 to UTC+13:00 and UTC+14:00')]),
        S("So in the year 2000, Kiritimati became the first place to start the new millennium.", [year(2000, '2000', light=True), icon('🎆', 3, -157, 'millennium', size=140), stamp('FIRST!', 'first', size=100)],
          cam=at_(1.87, -157.4, 65),
          src=[src('Kiritimati started the year 2000 before any other country.', 'UTC+14:00', 'started the year 2000 on its territory before any other country on Earth')]),
        S("And the last place? Baker Island and Howland Island, in UTC minus 12. Nobody lives there, they're US nature reserves.", [
            ping(*BAK, 'Baker', color='#ff5a5f'), dot('Baker Is.', *BAK, 'Baker', dy=60), ping(0.807, -176.617, 'Howland', color='#ff5a5f'), dot('Howland Is.', 0.807, -176.617, 'Howland', dy=-60), clock([('last', '23:59'), ('nature', '00:00')], screen=(0.5, 0.22), size=180, label='UTC−12', night=True)],
          cam=at_(0.5, -176.55, 30), tr='flash',
          src=[src('Baker and Howland Islands (US nature reserves) use UTC−12, the last to enter the New Year.', 'UTC%E2%88%9212:00', 'comprises the United States Minor Outlying Islands, specifically Baker Island and Howland Island (strict nature reserves belonging to the United States), as standard time')]),
        S("So from the first New Year to the last, the party lasts 26 hours.", [
            bars([('UTC+14', 26, 'first', '#ffd60a'), ('UTC−12', 1, 'last', '#ff5a5f')], 'first', screen=[0.5, 0.3], labelWidth=200), cnt('26 h', '26', size=200)],
          cam=at_(0, -170, 1.0),
          src=[src('UTC−12 is the last to enter a New Year; +14 to −12 is 26 hours.', 'UTC%E2%88%9212:00', 'is the last to enter a New Year')]),
    ],
    keywords={'first': '#ffd60a', 'last': '#ff5a5f', 'kiribati': '#ffd60a', 'baker': '#ff5a5f'},
    style='globe', styles={'now': 'neon', 'history': 'neon'}, captions={'theme': 'impact'})

# ------------------------------------------------------------------ 26. NIIHAU
NI = (21.9, -160.15)
NIH = 'Niihau'
save('niihau', meta(
    "Hawaii's Forbidden Island 🚷🏝️ Niʻihau",
    "Niʻihau 🏝️ is a Hawaiian island that almost nobody is allowed to visit. In 1864 Elizabeth Sinclair bought it from King Kamehameha V for US$10,000 in gold 💰 Her descendants, the Robinson family, still own it. Known as 'the Forbidden Isle', it is off-limits to outsiders 🚷 Only 84 people lived there in the 2020 census, and it's the only island where Hawaiian is spoken as the main language. No running water, no power grid: water comes from rain and electricity from solar ☀️",
    ["An island you can't visit in Hawaii 🚷🏝️", "Would you live without running water? 👇", "Which forbidden place next? 🗺️"],
    ['niihau', 'forbidden island', 'hawaii', 'robinson family', 'kamehameha', 'hawaiian language', 'kauai', 'island', 'geography', 'maps', 'learn']),
    [
        S("In Hawaii, there's an island almost nobody is allowed to visit.", [hook('THE *FORBIDDEN* ISLAND', at=0.05, until='Hawaii'), hl({'admin1': 'Hawaii', 'country': 'USA'}, 'flag:us', 'Hawaii', fillOpacity=0.6), ping(*NI, 'island', color='#ff3b3b')],
          cam=at_(21, -158, 10), no_claim=True),
        S("It's Niʻihau, and people call it the Forbidden Isle.", [slam('NIʻIHAU', 22.05, -160.1, 'Niʻihau', size=70), stamp('FORBIDDEN', 'Forbidden', size=90)],
          cam=at_(21.9, -160.15, 300, bearing=-3),
          src=[src('Known as the Forbidden Isle, off-limits to outsiders.', NIH, "Known as 'the Forbidden Isle', it is off-limits to all outsiders except the Robinson family and their relatives")]),
        S("It's the seventh largest island in Hawaii, about 28 kilometers from Kauaʻi.", [
            meas((22.05, -159.75), (21.95, -160.05), '28 km', 'kilometers'), dot('Kauaʻi', 22.05, -159.5, 'Kauaʻi', dy=-52)],
          cam=at_(22.0, -159.8, 22),
          src=[src('Seventh largest island in Hawaii; 17.5 mi (28.2 km) southwest of Kauaʻi.', NIH, 'It is 17.5 miles (28.2 km) southwest of Kauaʻi across the Kaulakahi Channel.')]),
        S("In 1864, Elizabeth Sinclair bought it from King Kamehameha the Fifth, for 10,000 dollars in gold.", [
            year(1864, '1864'), cnt('$10,000', '10,000', size=170, color='#ffd60a'), icon('💰', 21.9, -160.0, 'gold', size=120)],
          cam=at_(21.9, -160.15, 300), era='history', tr='film',
          src=[src('Sinclair bought Niʻihau from Kamehameha V in 1864 for $10,000 in gold.', NIH, 'purchased Niʻihau and parts of Kauaʻi from Kamehameha V in 1864 for US$10,000 in gold')]),
        S("Her family, the Robinsons, still own it today, and outsiders are not allowed in.", [icon('🚷', 21.9, -160.15, 'outsiders', size=170), tilt('outsiders', deg=34, until=3.5)],
          cam=at_(21.9, -160.15, 360),
          src=[src('Off-limits except the Robinson family and relatives.', NIH, "off-limits to all outsiders except the Robinson family and their relatives")]),
        S("In the 2020 census, only 84 people lived there.", [cnt('84', '84', size=220), scatter({'circle': {'lat': 21.9, 'lon': -160.15, 'km': 6}}, '🏠', 'people', count=4, size=64)],
          cam=at_(21.9, -160.15, 360),
          src=[src('Population 84 in 2020.', NIH, 'As of the 2020 census, the population had fallen to 84.')]),
        S("It's the only island where Hawaiian is still spoken as the main language.", [lab('ALOHA!', 21.95, -160.1, 'Hawaiian', style='note', size=70), icon('🗣️', 21.85, -160.2, 'spoken', size=170)],
          cam=at_(21.9, -160.15, 360), tr='flash',
          src=[src('The only island where Hawaiian is the primary language.', NIH, 'Niʻihau is the only island where Hawaiian is spoken as a primary language.')]),
        S("People get around on horses, and alcohol and cigarettes are banned.", [icon('🐎', 21.9, -160.12, 'horses', size=170), icon('🚭', 21.85, -160.2, 'cigarettes', size=170)],
          cam=at_(21.9, -160.15, 360),
          src=[src('Horses are the main transport; alcohol and cigarettes are banned.', NIH, 'Horses are the main form of transportation; bicycles are also used.'),
               src('Ban on alcohol and cigarettes.', NIH, 'The rules include a ban on alcohol and cigarettes.')]),
        S("There's no running water and no power grid. Water comes from the rain, and electricity from the sun.", [
            icon('🌧️', 22.0, -160.1, 'rain', size=170), icon('☀️', 21.8, -160.2, 'sun', size=170), stamp('OFF GRID', 'grid', size=90)],
          cam=at_(21.9, -160.15, 360, bearing=3),
          src=[src('No running water; rainwater catchment; solar power.', NIH, 'Water comes from rainwater catchment')]),
    ],
    keywords={'forbidden': '#ff5a5f', 'niʻihau': '#ffd60a', 'hawaiian': '#4ade80'},
    captions={'theme': 'classic'})

# ------------------------------------------------------------------ 27. POINT NEMO (globe)
NEMO = (-48.877, -123.393)
PI = 'Pole_of_inaccessibility'
save('point_nemo', meta(
    'Point Nemo: The Loneliest Place on Earth 🌊🚀😱',
    "Point Nemo 🌊 is the spot in the ocean farthest from any land: about 2,688 km from the nearest islands (Ducie Island, Motu Nui near Easter Island, and Maher Island off Antarctica) 😱 No regular ship or air routes pass within 400 km, so sometimes the closest humans are astronauts on the International Space Station flying overhead 🚀 It's also a 'spacecraft cemetery', where old satellites and space stations are sent to crash safely 🛰️",
    ["The nearest humans are in SPACE 🚀😱", "Would you sail to Point Nemo? 👇", "Which remote place next? 🗺️"],
    ['point nemo', 'pole of inaccessibility', 'pacific ocean', 'space station', 'iss', 'spacecraft cemetery', 'remote places', 'ocean', 'geography', 'maps', 'learn']),
    [
        S("This is the loneliest place on Earth.", [hook('THE *LONELIEST* PLACE', at=0.05, until='Earth'), ping(*NEMO, 'loneliest', color='#ff3b3b', hold=2)],
          cam=at_(-40, -125, 1.2), no_claim=True),
        S("It's called Point Nemo, the spot in the ocean farthest from any land.", [slam('POINT NEMO', -44, -123.4, 'Nemo', size=70)],
          cam=at_(-45, -123, 1.6),
          src=[src('Point Nemo is equidistant from the three closest landmasses.', PI, 'is equidistant along vertices from the three closest landmasses, which are each roughly 2,688 km (1,670 mi) away')]),
        S("Nemo is Latin for nobody, a nod to Captain Nemo from Jules Verne's novel. It was first found in 1992.", [
            year(1992, '1992', light=True), lab('NEMO = NOBODY', -44, -123.4, 'nobody', style='note', size=60)],
          cam=at_(-45, -123, 1.6),
          src=[src('Nemo is Latin for "nobody", a reference to Captain Nemo.', 'Point_Nemo', "Point Nemo, which is Latin for 'nobody' and a reference to Captain Nemo from Jules Verne's 1870 novel"),
               src('First identified by Hrvoje Lukatela in 1992.', 'Point_Nemo', 'Point Nemo was first identified by Croatian survey engineer Hrvoje Lukatela in 1992.')]),
        S("The nearest land is about 2,688 kilometers away, in three directions.", [
            meas(NEMO, (-24.67, -124.78), '2,688 km', 'nearest'), meas(NEMO, (-27.2, -109.45), '2,688 km', 'three', countUp=False), meas(NEMO, (-72.9, -126.3), '2,688 km', 'directions', countUp=False)],
          cam=at_(-48, -122, 1.3),
          src=[src('The nearest land is roughly 2,688 km away.', PI, 'which are each roughly 2,688 km (1,670 mi) away')]),
        S("Ducie Island, Motu Nui near Easter Island, and Maher Island next to Antarctica.", [
            dot('Ducie Island', -24.67, -124.78, 'Ducie', dy=-50, size=38), dot('Motu Nui', -27.2, -109.45, 'Motu', dy=50, size=38), dot('Maher Island', -72.9, -126.3, 'Maher', dy=50, size=38)],
          cam=at_(-48, -120, 1.3),
          src=[src('Nearest: Ducie Island, Motu Nui, Maher Island.', PI, 'They are Pandora Islet of the Ducie Island atoll (an island of the Pitcairn Islands) to the north; Motu Nui (adjacent to Easter Island) to the northeast; and Maher Island')]),
        S("No regular ships or planes pass within 400 kilometers.", [meas(NEMO, (NEMO[0] + 3.6, NEMO[1]), '400 km', 'ships', color='#ff5a5f'), mover_icon([(NEMO[0] + 6.5, NEMO[1] - 14), (NEMO[0] + 6.5, NEMO[1] + 14)], 'planes', '🚢', size=80), cnt('400 km', '400', size=170)],
          cam=at_(-48, -123, 3.0), tr='flash',
          src=[src('No regular marine or air traffic routes within 400 km.', PI, 'since no regular marine or air traffic routes are within 400 kilometres (250 mi)')]),
        S("So sometimes, the closest humans are astronauts on the International Space Station, flying overhead.", [ping(*NEMO, 0.05, color='#ff3b3b'), lab('POINT NEMO', NEMO[0], NEMO[1], 0.05, style='pill', bg='#c1121f', size=46, dy=110), 
            char('astronaut', 'astronauts', say='Hello down there!'), icon('🛰️', -47, -121, 'Station', size=130), tilt('overhead', deg=40, until=3.5)],
          cam=at_(-48.8, -123.4, 3.5),
          src=[src('Sometimes the closest humans are astronauts on the ISS.', PI, 'sometimes the closest human beings are astronauts aboard the International Space Station when it passes overhead')]),
        S("It's also a spacecraft cemetery. Old satellites and space stations are sent to crash here, far from everyone.", [ping(*NEMO, 0.05, color='#ff3b3b'), lab('POINT NEMO', NEMO[0], NEMO[1], 0.05, style='pill', bg='#c1121f', size=46, dy=110), 
            scatter({'circle': {'lat': NEMO[0], 'lon': NEMO[1], 'km': 700}}, '🛰️', 'cemetery', count=5, size=64, stagger=0.12), stamp('SPACECRAFT CEMETERY', 'cemetery', size=70)],
          cam=at_(-48, -123, 2.6, bearing=5),
          src=[src('Spacecraft are made to fall there on re-entry.', PI, "The wider area is also known as a 'spacecraft cemetery', because hundreds of decommissioned satellites, space stations, and other spacecraft have been made to fall there upon re-entering the atmosphere")]),
        S("And one day, the International Space Station itself is planned to end up here, in 2031.", [ping(*NEMO, 0.05, color='#ff3b3b'), lab('POINT NEMO', NEMO[0], NEMO[1], 0.05, style='pill', bg='#c1121f', size=46, dy=110), year(2031, '2031', light=True), icon('🛰️', -48.9, -123.4, 'Station', size=150), shake('end')],
          cam=at_(-48.9, -123.4, 3.0, bearing=-4),
          src=[src('The ISS is planned to crash near Point Nemo in 2031.', 'Point_Nemo', 'The International Space Station (ISS) is planned to crash into the ocean near Point Nemo in 2031.')]),
    ],
    keywords={'nemo': '#5ec8ff', 'space': '#a78bfa', 'astronauts': '#a78bfa', 'land': '#ffd60a'},
    style='globe', captions={'theme': 'box'})
