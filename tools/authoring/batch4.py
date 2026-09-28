from helpers import *

# ------------------------------------------------------------------ INDONESIA CAPITAL
JKT = (-6.2, 106.85)
NUS = (-0.97, 116.7)
save('indonesia_capital', meta(
    'Why Indonesia Is Moving Its Capital 🇮🇩🤯 Jakarta Is Sinking',
    "Indonesia 🇮🇩 is building a brand-new capital city from scratch! Jakarta, on the island of Java, is one of the most crowded urban areas on Earth, with over 40 million people in Greater Jakarta 🏙️ Parts of it lie below sea level, and pumping groundwater makes the land sink, raising the flood risk 🌊 So in August 2019, President Joko Widodo announced a new capital: Nusantara, on the island of Borneo in East Kalimantan 🌴 Construction began in 2022 and the project is estimated at about US$35 billion 💰",
    ["A whole country is moving its capital 🤯🇮🇩", "Would you move to a brand-new city in the jungle? 🌴👇", "Which capital should we explain next? 🗺️"],
    ['indonesia', 'jakarta', 'nusantara', 'new capital', 'sinking city', 'borneo', 'kalimantan', 'java', 'land subsidence', 'geography', 'maps', 'learn']),
    [
        S("Indonesia is building a brand new capital city, from scratch, in the jungle.", [
            hl('IDN', 'flag:id', 'Indonesia', fillOpacity=0.8), ping(*NUS, 'new', color='#4ade80'), icon('🏗️', NUS[0] + 1.2, NUS[1] + 1.4, 'scratch', size=120),
            icon('🌴', NUS[0] - 1.3, NUS[1] - 1.4, 'jungle', size=110)],
          cam=fit('IDN', pad=0.9, bearing=-3),
          src=[src('Indonesia is building Nusantara as its new capital.', 'Nusantara_(city)', 'Construction of the city began in 2022, starting with land clearing and creating access roads.')]),
        S("Its current capital is Jakarta, on the island of Java.", [
            ping(*JKT, 'Jakarta', color='#ff3b3b', hold=2), dot('Jakarta', *JKT, 'Jakarta', dy=-52), slam('JAVA', -7.4, 110.2, 'Java', size=74)],
          cam=at_(-6.8, 108.5, 9, bearing=-3),
          src=[src('Jakarta lies on the northwestern coast of Java.', 'Jakarta', 'It lies on the northwestern coast of Java, borders the provinces of West Java and Banten, and faces the Java Sea to the north.')]),
        S("Greater Jakarta is one of the most crowded urban areas on Earth, with over 40 million people.", [
            cnt('40M+', '40', size=210), hl({'admin1s': ['Jakarta Raya', 'Banten', 'Jawa Barat'], 'country': 'IDN'}, '#ff5a5f', 'crowded', fillOpacity=0.35), pill('Greater Jakarta', 'Greater')],
          cam=at_(-6.3, 106.85, 45),
          src=[src('Greater Jakarta has a population of over 40 million.', 'Jakarta', 'Greater Jakarta is the most populous urban area in the world with a population of over 40 million')]),
        S("So why would anyone leave such a huge city?", [q(-6.2, 106.85, 'why')], style='dark', no_claim=True),
        S("Because Jakarta is sinking. Parts of the city lie below sea level.", [
            hl({'admin1': 'Jakarta Raya', 'country': 'IDN'}, '#1d4ed8', 'sinking', fillOpacity=0.55),
            stamp('SINKING', 'sinking', size=100), icon('🌊', -6.08, 106.8, 'sea', size=120), shake('sinking')],
          cam=at_(-6.15, 106.85, 70),
          src=[src('Parts of Jakarta lie below sea level.', 'Jakarta', 'Much of Jakarta lies on an alluvial plain, with elevations ranging from below sea level to about 50 metres (160 feet).'),
               src('Land subsidence drives flood risk in northern Jakarta.', 'Jakarta', 'Land subsidence is a major driver of coastal-flood risk in northern Jakarta.')]),
        S("Pumping water out of the ground makes the land sink even more, and floods get worse.", [
            icon('🚰', -6.18, 106.8, 'Pumping', size=110), arrow((-6.1, 106.9), (-6.25, 106.9), 'sink', color='#ff5a5f'), icon('🌧️', -6.12, 106.95, 'floods', size=110)],
          src=[src('Groundwater extraction contributes to subsidence and flood risk.', 'Jakarta', 'Land subsidence is a major driver of coastal-flood risk in northern Jakarta.')]),
        S("So in August 2019, President Joko Widodo announced a new capital, on the island of Borneo.", [
            year(2019, '2019', light=True), ship([JKT, (-5.5, 110), (-3.5, 114), (-1.5, 116.9), NUS], 'Borneo', 'move', emblem='#e63946', drawDur=2.2),
            slam('BORNEO', 0.8, 114, 'Borneo', size=74)],
          cam=at_(-3.4, 111.5, 3.2, bearing=-3), tr='flash',
          src=[src('Joko Widodo announced the relocation in August 2019.', 'Nusantara_(city)', 'President Joko Widodo announced the relocation in August 2019'),
               src('Nusantara is in East Kalimantan on Borneo.', 'Nusantara_(city)', 'Nusantara occupies East Kalimantan on Borneo island')]),
        S("The new city sits on the east coast of Borneo, right next to the port city of Balikpapan.", [
            hl({'countries': ['IDN']}, '#16a34a', 'Borneo', fillOpacity=0.35), ping(*NUS, 'new', color='#4ade80'), dot('Balikpapan', -1.24, 116.85, 'Balikpapan', dy=52), dot('Nusantara', *NUS, 'city', dy=-52)],
          cam=at_(-1.1, 116.6, 12, bearing=-3),
          src=[src('Nusantara is adjacent to the port city of Balikpapan.', 'Nusantara_(city)', 'adjacent to the port city of Balikpapan')]),
        S("Its name is Nusantara. Construction began in 2022, and it's estimated to cost about 35 billion dollars.", [
            ping(*NUS, 'Nusantara', color='#4ade80'), slam('NUSANTARA', NUS[0] + 0.25, NUS[1], 'Nusantara', size=62),
            cnt_steps([('2022', '2022'), ('35', '$35B')], size=180), char('jakarta_resident', 'Construction', name='Moving day!')],
          cam=at_(-1.0, 116.6, 18, bearing=3),
          src=[src('Construction began in 2022.', 'Nusantara_(city)', 'Construction of the city began in 2022, starting with land clearing and creating access roads.'),
               src('Estimated at Rp 523 trillion (US$35 billion).', 'Nusantara_(city)', 'estimated to be worth Rp 523 trillion (US$35 billion)')]),
    ],
    keywords={'jakarta': '#ff5a5f', 'sinking': '#ff5a5f', 'nusantara': '#4ade80', 'borneo': '#4ade80', 'indonesia': '#ffd60a'},
    imagery=[{'bbox': [106.55, -6.45, 107.1, -5.95], 'width': 2400}])

# ------------------------------------------------------------------ JAPAN ISLANDS
JP4 = [('Hokkaido', 43.4, 142.8), ('Honshu', 37.2, 139.2), ('Shikoku', 33.7, 133.4), ('Kyushu', 32.6, 130.8)]
save('japan_islands', meta(
    'Japan Found 7,000 "New" Islands 🇯🇵🤯',
    "In 2023 Japan recounted its islands and the number jumped from 6,852 to 14,125 🇯🇵🏝️ No new islands appeared: better surveying and digital maps simply found more islands with a coastline of at least 100 meters 🗺️ Only about 260 of them are inhabited, and Honshu alone holds over 80% of the population 🗼 By area, Japan is the fourth-largest island country, after Indonesia, Madagascar and Papua New Guinea 🤯",
    ["Japan 'found' 7,000 islands overnight 🤯🇯🇵🏝️", "Which Japanese island would you visit? 👇", "Which country should we count next? 🗺️"],
    ['japan', 'islands', '14125 islands', 'honshu', 'hokkaido', 'kyushu', 'shikoku', 'island country', 'geography', 'maps', 'learn', 'fun facts']),
    [
        S("For decades, Japan said it had 6,852 islands.", [
            hl('JPN', 'flag:jp', 'Japan', fillOpacity=0.85), cnt('6,852', '6,852', size=200)],
          cam=fit('JPN', pad=0.9, bearing=-4),
          src=[src('A 1987 Japan Coast Guard survey counted 6,852 islands.', 'List_of_islands_of_Japan', 'According to a survey conducted by the Japan Coast Guard in 1987, the number of islands in Japan was 6,852.')]),
        S("But in 2023, they counted again, and the number more than doubled, to 14,125.", [
            year(2023, '2023', light=True), cnt_steps([('counted', '6,852'), ('14,125', '14,125')], size=200),
            punch('doubled')],
          src=[src('Japan is an island country of 14,125 islands.', 'List_of_islands_of_Japan', 'Japan is an island country of 14,125 islands, of which approximately 260 are inhabited.')]),
        S("So where did 7,000 new islands come from?", [q(36, 138, 'where')], style='dark', no_claim=True),
        S("Nothing new appeared. Better surveys and digital maps simply found more islands, with a coastline of at least 100 meters.", [
            char('japanese_surveyor', 'surveys', name='Surveyor'), icon('🛰️', 40, 145, 'digital', size=120), cnt('100 m', '100', size=180),
            ping(34.4, 132.4, 'coastline', color='#ffd60a')],
          cam=at_(34.2, 132.8, 16, bearing=-3), tr='flash',
          src=[src('The increase came from better surveying and digital mapping; the criterion is a coastline of 100 m or more.', 'List_of_islands_of_Japan',
                   'advances in surveying technology and the detailed representation of topographic features through digital mapping ... a coastline of 100 meters or more')]),
        S("And only about 260 of them have people living on them.", [
            cnt('260', '260', size=210), pill('inhabited', 'people', bg='#16a34a'), hl('JPN', '#16a34a', 'people', fillOpacity=0.6)],
          cam=fit('JPN', pad=0.9),
          src=[src('About 260 islands are inhabited.', 'List_of_islands_of_Japan', 'of which approximately 260 are inhabited')]),
        S("Most people live on four main islands: Hokkaido, Honshu, Shikoku and Kyushu.", [
            *[dot(n, la, lo, n, dy=-50, size=46) for n, la, lo in JP4],
            *[ping(la, lo, n, color='#ffd60a') for n, la, lo in JP4]],
          cam=fit('JPN', pad=0.85, bearing=-4),
          src=[src('The four main islands are Hokkaido, Honshu, Kyushu and Shikoku.', 'List_of_islands_of_Japan', 'Honshu – the largest island, with the capital Tokyo and over 80% of the population.')]),
        S("And Honshu alone, home of Tokyo, holds over 80 percent of the population.", [
            cnt('80%+', '80', size=210), slam('HONSHU', 37.8, 139.5, 'Honshu', size=80), ping(35.68, 139.76, 'Tokyo', color='#ff3b3b'), dot('Tokyo', 35.68, 139.76, 'Tokyo', dy=50)],
          src=[src('Honshu has over 80% of the population and the capital Tokyo.', 'List_of_islands_of_Japan', 'Honshu – the largest island, with the capital Tokyo and over 80% of the population.')]),
        S("By area, Japan is the fourth largest island country on Earth, behind Indonesia, Madagascar and Papua New Guinea.", [
            hl('IDN', 'flag:id', 'Indonesia', fillOpacity=0.8), hl('MDG', 'flag:mg', 'Madagascar', fillOpacity=0.8), hl('PNG', 'flag:pg', 'Papua', fillOpacity=0.8), hl('JPN', 'flag:jp', 'Japan', fillOpacity=0.85),
            cnt_steps([('fourth', '#4')], size=200)],
          cam=at_(30, 95, 0.75, bearing=-3),
          src=[src('Island countries by area: Indonesia 1,904,569 km², Madagascar 587,041 km², Papua New Guinea 462,840 km², Japan 377,976 km².', 'List_of_island_countries', 'Madagascar | One main island | 587,041 ... Papua New Guinea | Part of a larger island (New Guinea), and surrounding archipelago | 462,840 ... Japan | Four main islands and thousands of surrounding islands | 377,976')]),
        S("And the second most populous island country, beaten only by Indonesia again.", [
            cnt('#2', 'second', size=210), hl('IDN', 'flag:id', 'Indonesia', fillOpacity=0.85), hl('JPN', 'flag:jp', 'second', fillOpacity=0.85), icon('👥', 36, 139, 'populous', size=120)],
          cam=at_(30, 95, 0.75, bearing=3),
          src=[src('Japan is the second-most-populous island country, behind Indonesia.', 'List_of_islands_of_Japan', 'the second-most-populous island country in the world, behind only Indonesia')]),
    ],
    keywords={'japan': '#ff5a5f', 'islands': '#5ec8ff', 'honshu': '#ffd60a', '14,125': '#4ade80'})

# ------------------------------------------------------------------ ITALY MICROSTATES
SMR = (43.94, 12.46)
VAT = (41.903, 12.453)
save('italy_microstates', meta(
    'Why Are There 2 Countries Inside Italy? 🇮🇹🇸🇲🇻🇦🤯',
    "There are two whole countries inside Italy 🇮🇹 San Marino 🇸🇲 is only about 61 km² with around 34,000 people, and claims to have been founded in AD 301 🏰 When Italy unified in the 1800s, San Marino had sheltered Giuseppe Garibaldi, and Garibaldi let it stay independent; the two signed a Convention of Friendship in 1862 🤝 Vatican City 🇻🇦 is even smaller: 0.49 km² and about 882 people, the smallest country in the world ⛪ The popes once ruled the Papal States across central Italy, but lost them to the new Kingdom of Italy in 1870. The Lateran Treaty of 1929 created Vatican City 🤯 Together with Lesotho, they're the only countries completely surrounded by one other country 🌍",
    ["Two countries hiding inside Italy 🤯🇸🇲🇻🇦", "Have you visited San Marino or the Vatican? 👇", "Which tiny country should we explain next? 🗺️"],
    ['san marino', 'vatican city', 'italy', 'microstates', 'enclave', 'garibaldi', 'papal states', 'lateran treaty', 'smallest country', 'geography', 'maps', 'learn']),
    [
        S("Italy has not one, but two whole countries inside it.", [
            hl('ITA', 'flag:it', 'Italy', fillOpacity=0.8), ping(*SMR, 'two', color='#ffd60a'), ping(*VAT, 'two', color='#ffd60a'), cnt('2', 'two', size=240)],
          cam=fit('ITA', pad=0.9, bearing=-4),
          src=[src('San Marino and Vatican City are both enclaved by Italy.', 'Enclave_and_exclave', 'Three such sovereign states exist globally: Lesotho (enclaved by South Africa), San Marino, and Vatican City (both enclaved by Italy).')]),
        S("The first is San Marino. Only 61 square kilometers, with about 34,000 people.", [
            ping(*SMR, 'Marino', color='#5ec8ff'), hl('SMR', 'flag:sm', 'Marino', neon='#5ec8ff', hold=1),
            slam('SAN MARINO', SMR[0] + 0.045, SMR[1], 'Marino', size=64), cnt_steps([('61', '61 km²'), ('34,000', '34,000')], size=170)],
          cam=at_(43.94, 12.45, 200, bearing=-3),
          src=[src('San Marino covers just over 61 km².', 'San_Marino', 'with a land area of just over 61 square kilometres (24 sq mi)'),
               src('Population 34,042 (2025).', 'San_Marino', 'a population of 34,042 as of 2025')]),
        S("And it claims to have been founded way back in the year 301.", [
            year(301, '301'), hl('SMR', '#8b5e34', 0.05, fillOpacity=0.6), icon('🏰', SMR[0], SMR[1], 'founded', size=130), lab('San Marino', SMR[0] - 0.035, SMR[1], 0.05, style='serif', size=54)],
          cam=at_(43.94, 12.45, 200),
          era='history', tr='film',
          src=[src('San Marino claims to have been founded in AD 301.', 'San_Marino', 'San Marino claims to have been founded in AD 301')]),
        S("So how did it survive when Italy unified?", [q(43.5, 12.3, 'how')], cam=at_(43, 12.5, 6), style='dark', no_claim=True),
        S("San Marino had sheltered the unification hero Giuseppe Garibaldi. So Garibaldi let it stay independent.", [
            hl('SMR', '#8b5e34', 0.05, fillOpacity=0.6), lab('San Marino', SMR[0] - 0.1, SMR[1], 0.05, style='serif', size=54), char('garibaldi', 'Garibaldi', name='Garibaldi', say='Stay free!'), ping(*SMR, 'independent', color='#5ec8ff'), stamp('INDEPENDENT', 'independent', size=84, screen=[0.5, 0.2])],
          cam=at_(43.93, 12.45, 70), era='history',
          src=[src('San Marino sheltered Garibaldi, who let it remain independent.', 'San_Marino', 'San Marino served as a refuge for many people persecuted because of their support for unification, including Giuseppe Garibaldi and his wife Anita. Garibaldi allowed San Marino to remain independent.')]),
        S("In 1862, the two countries signed a Convention of Friendship.", [
            year(1862, '1862'), hl('SMR', '#8b5e34', 0.05, fillOpacity=0.6), lab('Kingdom of Italy', 43.3, 11.3, 'two', style='serif', size=48), lab('San Marino', 44.05, 12.9, 'two', style='serif', size=48), icon('🤝', 43.7, 12.45, 'Friendship', size=120)],
          era='history',
          src=[src('San Marino and the Kingdom of Italy signed a Convention of Friendship in 1862.', 'San_Marino', 'San Marino and the Kingdom of Italy signed a Convention of Friendship in 1862.')]),
        S("The second country is even smaller. Vatican City, just 0.49 square kilometers, the smallest country in the world.", [
            hl('VAT', '#ffd60a', 'Vatican', neon='#ffd60a', hold=1), dot('Vatican City', *VAT, 'Vatican', dy=-60),
            cnt('0.49 km²', '0.49', size=160), dot('Rome', 41.89, 12.51, 'smallest', dy=52, size=38)],
          cam=at_(41.9, 12.47, 260, bearing=3), tr='flash',
          src=[src('Vatican City is 0.49 km², the smallest country by area and population.', 'Vatican_City', 'the smallest country in the world both by area and by population ... 0.49 km2 (0.19 sq mi)')]),
        S("Only about 882 people live there.", [
            cnt('882', '882', size=210), pill('people', 'people', bg='#b45309')],
          src=[src('Population about 882 (2024).', 'Vatican_City', 'a population of about 882 in 2024')]),
        S("Popes once ruled the Papal States, across central Italy. But in 1870, the new Kingdom of Italy took them.", [
            hl({'admin1s': ['Roma', 'Latina', 'Frosinone', 'Viterbo', 'Rieti', 'Perugia', 'Terni', 'Ancona', 'Macerata', 'Ascoli Piceno', 'Fermo', 'Pesaro e Urbino', 'Bologna', 'Ferrara', 'Ravenna', 'Forlì-Cesena', 'Rimini'], 'country': 'ITA'}, '#d4a017', 'Papal', fillOpacity=0.7),
            lab('Papal States', 43.0, 12.6, 'Papal', style='serif', size=58), year(1870, '1870'), shake('took')],
          cam=at_(42.6, 12.6, 5.5), era='history', tr='film',
          src=[src('The popes ruled the Papal States until the Kingdom of Italy seized them (1870).', 'Vatican_City', 'ruled the Papal States, which covered a large portion of the Italian Peninsula, for more than a thousand years until the mid-19th century, when all the territory belonging to the papacy was seized by the newly created Kingdom of Italy')]),
        S("It wasn't until 1929, with the Lateran Treaty, that Vatican City became its own country.", [
            year(1929, '1929'), stamp('LATERAN TREATY', 'Lateran', size=72), flag('va', 41.95, 12.36, 'country', size=120)],
          cam=at_(41.9, 12.46, 120), era='history',
          src=[src('Vatican City came into existence in 1929 via the Lateran Treaty.', 'Vatican_City', 'The independent state of Vatican City came into existence in 1929 via the Lateran Treaty')]),
        S("Only three countries on Earth are completely surrounded by just one other country. Italy has two of them.", [
            hl('LSO', 'flag:ls', 'three', fillOpacity=0.9), ping(-29.6, 28.2, 'three', color='#ffd60a'), ping(*SMR, 'two', color='#ffd60a'), ping(*VAT, 'two', color='#ffd60a'),
            cnt_steps([('three', '3')], size=220), dot('Lesotho', -29.6, 28.2, 'three', dy=-50)],
          cam=at_(-2, 20, 0.8, bearing=-3),
          src=[src('Lesotho, San Marino and Vatican City are the only three enclaved sovereign states.', 'Enclave_and_exclave', 'Three such sovereign states exist globally: Lesotho (enclaved by South Africa), San Marino, and Vatican City (both enclaved by Italy).')]),
    ],
    keywords={'italy': '#4ade80', 'marino': '#5ec8ff', 'vatican': '#ffd60a', 'garibaldi': '#ff5a5f', 'papal': '#ffd60a'},
    )

# ------------------------------------------------------------------ HORMUZ
GULF_OUT = [(29.3, 48.5), (27.8, 50.5), (26.6, 53.0), (26.4, 55.2), (26.6, 56.45), (25.6, 57.4), (24.2, 59.0), (22.0, 62.0)]
DEPEND = ['QAT', 'BHR', 'KWT', 'IRQ', 'ARE']
save('hormuz', meta(
    'The 39 km Strait That Controls World Oil 🛢️🌍🤯 Strait of Hormuz',
    "The Strait of Hormuz is only about 39 km wide at its narrowest 🌊 but around 25% of the world's seaborne oil trade and 20% of its liquefied natural gas pass through it 🛢️ It separates Iran 🇮🇷 from Oman's Musandam Peninsula 🇴🇲 and the shipping lanes are just 2 nautical miles wide in each direction 🚢 For countries like Qatar, Bahrain, Kuwait and Iraq it's the only sea route to the open ocean 🤯",
    ["A quarter of the world's seaborne oil squeezes through here 🤯🛢️", "Did you know how narrow Hormuz is? 👇", "Which chokepoint should we explain next? 🗺️"],
    ['strait of hormuz', 'oil', 'persian gulf', 'iran', 'oman', 'musandam', 'uae', 'qatar', 'lng', 'shipping', 'chokepoint', 'geography', 'maps', 'learn']),
    [
        S("A quarter of the world's seaborne oil trade squeezes through this one narrow gap.", [
            ping(26.6, 56.4, 'gap', color='#ff3b3b', hold=2), cnt('25%', 'quarter', size=210), pill('of seaborne oil', 'oil', bg='#111827'),
            icon('🛢️', 27.6, 55.0, 'oil', size=120)],
          cam=at_(26.5, 55.5, 7, bearing=-4),
          src=[src('25% of seaborne oil trade passed through the strait in 2023–2025.', 'Strait_of_Hormuz', 'During 2023–2025, 20% of the world\'s liquefied natural gas and 25% of seaborne oil trade passed through the Strait')]),
        S("This is the Strait of Hormuz. At its narrowest, it's only about 39 kilometers wide.", [
            slam('HORMUZ', 27.5, 57.7, 'Hormuz', size=76), meas((26.52, 56.5), (26.84, 56.36), '39 km', 'narrowest')],
          cam=at_(26.6, 56.4, 22, bearing=-3),
          src=[src('The width varies from about 97 km to 39 km.', 'Strait_of_Hormuz', 'with a width varying from about 60 mi (52 nmi; 97 km) to 24 mi (21 nmi; 39 km)')]),
        S("On one side is Iran. On the other, Oman's Musandam Peninsula.", [
            hl('IRN', 'flag:ir', 'Iran', fillOpacity=0.8), hl('OMN', 'flag:om', 'Oman', fillOpacity=0.8), dot('Musandam', 26.2, 56.25, 'Musandam', dy=56)],
          cam=at_(26.5, 56.4, 12, bearing=-3),
          src=[src('It separates Iran from Oman\'s Musandam Peninsula.', 'Strait_of_Hormuz', 'The waterway separates Iran on the north from Oman\'s Musandam Peninsula on the south')]),
        S("And the shipping lanes are tiny. Just two nautical miles wide, in each direction.", [
            route([(26.35, 56.85), (26.55, 56.55), (26.5, 56.2)], 'lanes', color='#ffd60a', width=7, drawDur=1.0),
            route([(26.45, 56.95), (26.65, 56.6), (26.62, 56.2)], 'direction', color='#5ec8ff', width=7, drawDur=1.0),
            cnt('3.7 km', 'two', size=170), pill('per lane', 'lanes', bg='#1d4ed8')],
          cam=at_(26.55, 56.55, 45, bearing=-6),
          src=[src('Each lane is 2 nautical miles (3.7 km) wide.', 'Strait_of_Hormuz', 'each lane being 2 nautical miles (3.7 km) wide, with the two lanes separated by a similarly wide "median"')]),
        S("And between the two lanes sits a buffer zone, just as wide.", [
            route([(26.45, 56.3), (26.6, 56.55), (26.72, 56.8)], 'buffer', color='#ff5a5f', width=16, drawDur=0.8), note('BUFFER', 26.7, 56.75, 'buffer', size=58)],
          src=[src('The two lanes are separated by a median of similar width.', 'Strait_of_Hormuz', 'with the two lanes separated by a similarly wide "median"')]),
        S("So why does this tiny strait matter so much?", [q(26.6, 56.4, 'why')], style='dark', no_claim=True),
        S("Because for countries like Qatar, Bahrain, Kuwait and Iraq, it's the only sea route to the open ocean.", [
            hl('QAT', 'flag:qa', 'Qatar', fillOpacity=0.85), hl('BHR', 'flag:bh', 'Bahrain', fillOpacity=0.85), hl('KWT', 'flag:kw', 'Kuwait', fillOpacity=0.85), hl('IRQ', 'flag:iq', 'Iraq', fillOpacity=0.85),
            ship(GULF_OUT, 'only', 'tanker', emblem='#111827', drawDur=3.0), stamp('ONLY WAY OUT', 'open', size=80, screen=[0.5, 0.2])],
          cam={'follow': 'tanker', 'zoom': 6, 'zoomTo': 3.2},
          src=[src('It is the only maritime route for the UAE, Qatar, Bahrain, Kuwait and Iraq.', 'Strait_of_Hormuz', 'is also the only maritime route for several Gulf countries including the UAE, Qatar, Bahrain, Kuwait, and Iraq')]),
        S("Tankers also carry about 20 percent of the world's liquefied natural gas through here.", [
            cnt('20%', '20', size=210), pill('of world LNG', 'gas', bg='#0f766e'), char('tanker_captain', 'Tankers', name='Tanker captain'), icon('🔥', 25.3, 57.5, 'gas', size=110)],
          cam=at_(26.3, 56.3, 6),
          src=[src('20% of the world\'s LNG passed through the strait.', 'Strait_of_Hormuz', '20% of the world\'s liquefied natural gas and 25% of seaborne oil trade passed through the Strait')]),
        S("That's why this 39 kilometer gap is one of the most important waterways on Earth.", [
            ping(26.6, 56.4, 'gap', color='#ffd60a'), meas((26.52, 56.5), (26.84, 56.36), '39 km', 'gap'), punch('important')],
          cam=at_(26.6, 56.4, 18, bearing=4), tr='flash',
          src=[src('Width 39 km; carries 25% of seaborne oil.', 'Strait_of_Hormuz', 'with a width varying from about 60 mi (52 nmi; 97 km) to 24 mi (21 nmi; 39 km)')]),
    ],
    keywords={'hormuz': '#ffd60a', 'oil': '#ffd60a', 'iran': '#4ade80', 'oman': '#ff5a5f', 'gas': '#5ec8ff'},
    imagery=[{'bbox': [55.8, 26.0, 57.2, 27.2], 'width': 2600}])

# ------------------------------------------------------------------ KALININGRAD (revamp)
KO = {'admin1': 'Kaliningrad', 'country': 'RUS'}
KGD = (54.71, 20.51)
K = 'Kaliningrad_Oblast'
save('kaliningrad', meta(
    'Why Russia Owns a Piece of the EU 🇷🇺🤯 Kaliningrad Explained 🇪🇺',
    "Russia is the biggest country on Earth 🇷🇺 But one piece of it isn't connected to the rest at all. Kaliningrad sits on the Baltic Sea, squeezed between Poland 🇵🇱 and Lithuania 🇱🇹, surrounded by NATO and the European Union 🇪🇺 For centuries it was Königsberg, founded in 1255 by the Teutonic Knights, and in 1701 the first King in Prussia was crowned there 👑 In April 1945 the Soviet army captured it, the north of East Prussia went to the USSR and the south to Poland. In 1946 the city was renamed Kaliningrad. When Lithuania became independent in 1990 and the Soviet Union dissolved in 1991, Kaliningrad was cut off 🤯 Today about one million people live there, only 65 km of Poland (the Suwałki Gap) separates it from Belarus, and Baltiysk is Russia's only Baltic port that stays ice-free in winter ⚓",
    ["A piece of Russia inside the EU 🇷🇺🇪🇺🤯", "Would you have guessed Kaliningrad used to be German Königsberg? 👑", "Which weird border should we explain next? 👇🗺️"],
    ['kaliningrad', 'russia', 'konigsberg', 'eu', 'nato', 'poland', 'lithuania', 'baltic sea', 'east prussia', 'suwalki gap', 'belarus', 'weird borders', 'exclave', 'history', 'geography', 'maps', 'learn']),
    [
        S("This is Russia, the biggest country on Earth.", [
            hl('RUS', 'flag:ru', 'Russia', hold=1), slam('RUSSIA', 62, 97, 'Russia', size=96), cnt('#1', 'biggest', size=200)],
          cam=fit('RUS', pad=0.95, bearing=-4),
          src=[src('Russia is the largest country in the world by area.', 'Russia', 'It is the largest country in the world by area')]),
        S("But one piece of it is stuck between Poland and Lithuania, not touching the rest of Russia at all.", [
            hl('POL', 'flag:pl', 'Poland', fillOpacity=0.75, hold=1), hl('LTU', 'flag:lt', 'Lithuania', fillOpacity=0.75, hold=1),
            hl(KO, 'flag:ru', 'piece', hold=1, neon='#ff3b3b'), ping(*KGD, 'piece', color='#ff3b3b', hold=1),
            dot('Kaliningrad', *KGD, 'stuck', dy=-54, size=48, hold=1)],
          cam=fit(KO, pad=0.8, zoomMul=0.45, bearing=-3),
          src=[src('Kaliningrad Oblast is a semi-exclave bordered by Poland, Lithuania and the Baltic Sea.', K, 'It is a semi-exclave on the Baltic Sea within the historical Baltic region of Prussia, bordered by Poland to the south, Lithuania to the north and east, and the Baltic Sea to the west.')]),
        S("It's surrounded by NATO and the European Union.", [
            blob({'countries': ['POL', 'LTU', 'LVA', 'EST', 'DEU', 'DNK', 'SWE', 'FIN']}, '#2350b8', '#5ec8ff', 'NATO', fillOpacity=0.7),
            flag('eu', 52.9, 21.2, 'European', size=140), pill('NATO + EU', 'NATO', bg='#1d4ed8')],
          cam=fit(KO, zoomMul=0.3),
          src=[src('Poland joined NATO in 1999.', 'Enlargement_of_NATO', 'Hungary, Poland, and the Czech Republic officially joined NATO in March 1999.'),
               src('Poland and Lithuania joined the EU on 1 May 2004.', '2004_enlargement_of_the_European_Union', 'The largest enlargement of the European Union ... took place on 1 May 2004.')]),
        S("So how did Russia end up with a piece of land in the middle of Europe?", [q(*KGD, 'how')], style='dark', no_claim=True),
        S("In 1255, German crusader knights, the Teutonic Order, built a castle here, and named it Königsberg.", [
            year(1255, '1255'), hl(KO, '#8b5e34', 'German', fillOpacity=0.45), char('teutonic_knight', 'knights', name='Teutonic Knight'), icon('🏰', KGD[0] + 0.1, KGD[1], 'castle', size=130),
            lab('Königsberg', KGD[0] - 0.35, KGD[1], 'Königsberg', style='serif', size=60)],
          cam=at_(54.7, 20.5, 14), era='history', tr='film',
          src=[src('In 1255 the Teutonic Knights built the fortress of Königsberg.', 'Kaliningrad', 'During the conquest of the Sambians by the Teutonic Knights in 1255, Twangste was destroyed and replaced by a fortress named Königsberg')]),
        S("And in 1701, the first King in Prussia was crowned right here.", [
            year(1701, '1701'), char('prussian_king', 'King', name='Frederick I', say='My crown!'), icon('👑', KGD[0] + 0.1, KGD[1], 'crowned', size=120)],
          era='history',
          src=[src('Frederick I was crowned King in Prussia in Königsberg in 1701.', 'Kaliningrad', 'Frederick I of Prussia ... crowned King in Prussia in Königsberg, 1701')]),
        S("Then, in April 1945, the Soviet army captured the city.", [
            year(1945, '1945'), hl({'admin1s': ['Warmian-Masurian'], 'country': 'POL'}, '#8b5e34', 'Then', fillOpacity=0.4), hl(KO, '#8b5e34', 'Then', fillOpacity=0.4), char('soviet_soldier', 'Soviet', name='Red Army'), arrow((54.6, 23.5), (54.72, 20.7), 'captured', color='#c1121f'), shake('captured')],
          cam=at_(54.3, 21.2, 14), era='history',
          src=[src('The Soviet Union captured the city on 9 April 1945.', 'Kaliningrad', 'it was then captured by the Soviet Union on 9 April 1945')]),
        S("After the war, East Prussia was split. The north went to the Soviet Union, the south went to Poland.", [
            hl({'admin1s': ['Warmian-Masurian'], 'country': 'POL'}, '#8b5e34', 'After', fillOpacity=0.4, until='south'), hl(KO, '#8b5e34', 'After', fillOpacity=0.4, until='north'), lab('East Prussia', 54.2, 21.0, 'After', style='serif', size=56, until='north'),
            hl(KO, '#c1121f', 'north', fillOpacity=0.85), lab('USSR', 54.85, 21.2, 'north', style='serif', size=58),
            hl({'admin1s': ['Warmian-Masurian'], 'country': 'POL'}, '#dc143c', 'south', fillOpacity=0.6), lab('Poland', 53.8, 20.9, 'Poland', style='serif', size=58)],
          cam=at_(54.1, 21.0, 13), era='history',
          src=[src('Northern East Prussia went to the USSR; the south came under Polish administration.', 'East_Prussia', 'Northern East Prussia was divided between the Soviet republics of Russia (the Kaliningrad Oblast) and Lithuania ... Southern East Prussia was placed under Polish administration.')]),
        S("In 1946, the city was renamed Kaliningrad, after the Soviet leader Mikhail Kalinin.", [
            year(1946, '1946'), hl(KO, '#c1121f', 'renamed', fillOpacity=0.6), slam('KALININGRAD', KGD[0] + 0.3, KGD[1], 'renamed', size=66)],
          cam=at_(54.7, 20.5, 14), era='history',
          src=[src('Renamed Kaliningrad in July 1946 after Mikhail Kalinin.', 'Kaliningrad', 'Königsberg was renamed Kaliningrad in July 1946 in honour of Mikhail Kalinin')]),
        S("Back then, nobody cared about the border, because Lithuania was Soviet too. But Lithuania became independent in 1990, the Soviet Union dissolved in 1991, and Kaliningrad was suddenly cut off.", [
            hl('LTU', '#c1121f', 'Soviet', fillOpacity=0.7, until='independent'), hl('LTU', 'flag:lt', 'independent', fillOpacity=0.85),
            cnt_steps([('1990', '1990'), ('1991', '1991')], size=180), stamp('CUT OFF', 'cut', size=100), shake('cut')],
          cam=fit(KO, 'LTU', pad=0.7), tr='flash',
          src=[src('Lithuanian independence (1990) and the USSR\'s dissolution (1991) isolated Kaliningrad.', K, 'The independence of Lithuania in 1990 and full dissolution of the Soviet Union in 1991 isolated Kaliningrad from the rest of Russia')]),
        S("Today, about one million people live there. And only 65 kilometers of Poland, the Suwalki Gap, separate it from Russia's ally Belarus.", [
            hl(KO, '#c1121f', 'Today', fillOpacity=0.6, neon='#ff3b3b'), cnt('1M', 'million', size=200), hl('BLR', 'flag:by', 'Belarus', fillOpacity=0.8),
            meas((54.36, 22.79), (53.95, 23.51), '65 km', 'Suwalki')],
          cam=at_(54.3, 22.6, 8.5, bearing=-3),
          src=[src('Population roughly one million (2021 census).', K, 'Kaliningrad Oblast had a population of roughly one million in the 2021 Russian census.'),
               src('Only 65 km of Polish territory separates the two areas.', 'Suwa%C5%82ki_Gap', 'only 65 km (40 mi) of Polish territory separates two areas of the rival Collective Security Treaty Organisation (CSTO) and the Union State')]),
        S("And why does Russia care so much? Its port of Baltiysk is Russia's only Baltic port that stays ice-free in winter.", [
            ping(54.65, 19.9, 'Baltiysk', color='#5ec8ff'), dot('Baltiysk', 54.65, 19.9, 'Baltiysk', dy=-52), icon('⚓', 54.55, 19.6, 'port', size=110),
            icon('🧊', 59.9, 29.5, 'ice', size=110), stamp('ICE-FREE', 'ice', size=90)],
          cam=at_(56.8, 23.5, 3.2, bearing=-3),
          src=[src('Baltiysk is Russia\'s only Baltic Sea port that remains ice-free in winter.', K, 'The port town of Baltiysk is Russia\'s only port on the Baltic Sea that remains ice-free in winter.')]),
    ],
    keywords={'russia': '#ff5a5f', 'kaliningrad': '#ff5a5f', 'poland': '#ffd60a', 'lithuania': '#4ade80', 'nato': '#5ec8ff', 'königsberg': '#ffd60a'},
    imagery=[{'bbox': [17.8, 53.3, 24.6, 56.3], 'width': 4096}])
