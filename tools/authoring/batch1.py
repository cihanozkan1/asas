from helpers import *

# ------------------------------------------------------------------ ALASKA
AK = {'admin1': 'Alaska', 'country': 'USA'}
save('alaska', meta(
    'Why Russia Sold Alaska to the USA 🇷🇺🇺🇸🤯 2 Cents per Acre!',
    "Alaska is by far the biggest US state 🇺🇸 but until 1867 it belonged to Russia 🇷🇺 Then Tsar Alexander II sold all of it for just $7.2 million, about 2 cents per acre 💰 Why? Russia had just lost the Crimean War, money was tight, and the far-away land was hard to defend, especially against Britain next door in Canada 🇬🇧 US Secretary of State William Seward made the deal, and critics mocked it as \"Seward's Folly\" or \"Seward's Icebox\" 🧊 Then in 1896 the Klondike Gold Rush began ⛏️ and the frozen land suddenly looked like a bargain 🤯",
    ["Russia sold Alaska for 2 cents per acre 🤯🇷🇺🇺🇸", "Best deal in history or Russia's biggest mistake? 👇", "Which land deal should we explain next? 🗺️"],
    ['alaska', 'russia', 'usa', 'alaska purchase', 'seward', '1867', 'tsar alexander', 'crimean war', 'klondike', 'gold rush', 'history', 'geography', 'maps', 'learn']),
    [
        S("This is Alaska, by far the biggest state in the USA, and home to about 740,000 people.", [
            hl(AK, 'flag:us', 'Alaska', hold=1), slam('ALASKA', 64, -152, 'Alaska', rotate=-6),
            cnt('#1', 'biggest')],
          cam=fit(AK, pad=0.9, bearing=-4),
          src=[src('Alaska is by far the largest US state; population 740,133 in 2024.', 'Alaska', 'Alaska is by far the largest state in the United States ... a population of 740,133 in 2024')]),
        S("But until 1867, it belonged to Russia.", [
            hl(AK, '#b3202a', 'Russia', fillOpacity=0.85), year(1867, '1867', light=True),
            flag('ru', 62, -150, 'Russia', size=150)],
          src=[src('Alaska was Russian until the 1867 purchase.', 'Alaska_Purchase', 'Signed March 30, 1867')]),
        S("Then, in 1867, Russia sold the whole thing to the United States, for just 7.2 million dollars.", [
            char('tsar', 'Russia', name='Tsar Alexander II'), char('seward', 'States', screen=(0.74, 0.6), name='Seward', flip=True),
            cnt('$7.2M', '7.2', color='#4ade80'), stamp('SOLD!', 'sold', size=110)],
          cam=fit(AK, pad=0.9, zoomMul=0.8),
          src=[src('The price was $7.2 million.', 'Alaska_Purchase', 'Price: $7.2 million')]),
        S("That's about two cents per acre.", [
            cnt('2¢', 'two', color='#4ade80', size=220), pill('per acre', 'acre', bg='#16a34a'), punch('cents')],
          src=[src('About 2 cents per acre.', 'Alaska_Purchase', 'Cost per acre: approximately 2 cents')]),
        S("So why would Russia sell such a huge land?", [
            hl(AK, '#c1121f', 0.05, fillOpacity=0.9), hl('RUS', '#c1121f', 0.05, fillOpacity=0.9), q(63, -150, 'why')],
          cam=at_(63, -175, 0.9), style='dark', no_claim=True),
        S("Russia had just lost the Crimean War against Britain, France and the Ottoman Empire, and money was tight.", [
            year(1856, 'Crimean'), icon('⚔️', 45, 34, 'Crimean', size=140), icon('💸', 55, 45, 'money', size=130),
            hl('RUS', '#8a1c1c', 0.1, fillOpacity=0.85)],
          cam=at_(55, 60, 0.75), era='history', tr='film',
          src=[src('Russia sold after defeat in the Crimean War and under financial pressure.', 'Alaska_Purchase',
                   'After suffering defeat in the Crimean War, Russia recognized that defending this distant territory would be difficult ... Financial pressures from the war also motivated the sale.'),
               src('Crimean War 1853–1856: Russia vs the Ottoman Empire, France, the UK and Sardinia; Russia sued for peace.', 'Crimean_War', 'The conflict lasted from October 1853 to March 1856 ... Russia ultimately sued for peace')]),
        S("And Alaska was far away and hard to defend, especially against Britain, right next door in Canada.", [
            hl(AK, '#8a1c1c', 'Alaska', fillOpacity=0.85), hl('CAN', '#c8102e', 'Britain', fillOpacity=0.55, pattern='hatch'),
            lab('British', 58, -105, 'Britain', style='serif', size=58), arrow((57, -110), (62, -140), 'defend', color='#c8102e')],
          cam=fit(AK, 'CAN', pad=0.9), era='history',
          src=[src('Alaska was hard to defend, particularly against Britain from neighboring Canada.', 'Alaska_Purchase',
                   'defending this distant territory would be difficult, particularly against Britain from neighboring Canada')]),
        S("The deal was negotiated by US Secretary of State William Seward. Critics mocked it as Seward's Folly, or Seward's Icebox, a worthless frozen wasteland.", [
            note("SEWARD'S FOLLY", 66, -160, 'Folly', size=66), note('ICEBOX', 60, -145, 'Icebox', size=70, rotate=6),
            icon('🧊', 63, -138, 'Icebox', size=130), char('seward', 'Seward', name='Seward')],
          cam=fit(AK, pad=0.9), era='history',
          src=[src('Critics dubbed it "Seward\'s Folly" or "Seward\'s Icebox".', 'Alaska_Purchase',
                   'critics dubbed it "Seward\'s Folly" or "Seward\'s Icebox," claiming the U.S. had purchased worthless frozen land'),
               src('William Seward, US Secretary of State, negotiated the purchase.', 'Alaska_Purchase', 'William H. Seward, U.S. Secretary of State, negotiated with Russian diplomat Eduard de Stoeckl')]),
        S("But in 1896, the Klondike Gold Rush began next door, and the frozen land suddenly looked like a bargain.", [
            year(1896, '1896', light=True), ping(64.06, -139.43, 'Klondike', color='#ffd60a'), dot('Klondike', 64.06, -139.43, 'Klondike'),
            scatter(AK, '💰', 'bargain', count=12, size=60), hl(AK, 'flag:us', 'bargain')],
          cam=fit(AK, pad=0.9, bearing=-4), tr='flash',
          src=[src('Alaska stayed sparsely populated until the Klondike Gold Rush began in 1896.', 'Alaska_Purchase',
                   'Alaska remained sparsely populated until the Klondike Gold Rush began in 1896')]),
        S("Today, Alaska is more than twice the size of Texas. All for about two cents an acre.", [
            ghost({'admin1': 'Texas', 'country': 'USA'}, (63.5, -152), 'Texas', fill='#f4a261'),
            lab('Texas', 61, -152, 'Texas', style='pill', bg='#e76f51', size=44), cnt('2¢', 'two', color='#4ade80')],
          cam=fit(AK, pad=0.85),
          src=[src('Alaska is more than twice the size of Texas.', 'Alaska', 'more than twice the size of the second-largest U.S. state (Texas)')]),
    ],
    keywords={'alaska': '#5ec8ff', 'russia': '#ff5a5f', 'seward': '#ffd60a', 'klondike': '#ffd60a', 'texas': '#f4a261'})

# ------------------------------------------------------------------ CHILE
CHL = 'CHL'
save('chile', meta(
    'Why Chile Is So Long & So Thin 🇨🇱🤯 4,300 km Ribbon Country',
    "Chile 🇨🇱 is about 4,300 km long but on average only 177 km wide 📏 Why? To the east, the Andes form a giant wall ⛰️ and to the west there's only the Pacific Ocean 🌊 In the War of the Pacific (1879–1884) Chile defeated Bolivia 🇧🇴 and Peru 🇵🇪 and expanded its territory northward by almost one-third, taking the nitrate-rich Atacama and leaving Bolivia without a coast. That's how Chile became a ribbon squeezed between mountains and ocean 🤯",
    ["A country 4,300 km long but only 177 km wide 🤯🇨🇱", "Chileans: north or south, where's the best part? 👇", "Which weird country shape should we explain next? 🗺️"],
    ['chile', 'andes', 'atacama', 'pacific ocean', 'war of the pacific', 'bolivia', 'peru', 'weird borders', 'country shape', 'geography', 'maps', 'learn']),
    [
        S("Chile is about 4,300 kilometers long, but on average only 177 kilometers wide.", [
            hl(CHL, 'flag:cl', 'Chile', hold=1), meas((-17.5, -69.6), (-55.9, -67.3), '4,300 km', '4,300', labelDy=0, labelDx=0),
            meas((-30, -71.6), (-30, -70), '177 km', '177')],
          cam=fit(CHL, pad=0.95),
          src=[src('Chile is about 4,300 km long with an average width of 177 km.', 'Chile',
                   'approximately 4,300 kilometers north to south with an average width of only 177 kilometers')]),
        S("Put Chile on top of Europe, at its real size, and it would stretch across almost the whole continent.", [
            ghost(CHL, (52, 12), 'Europe', fill='#e63946'), lab('Chile', 50, 20, 'Europe', style='pill', bg='#c1121f', size=44)],
          cam=at_(50, 12, 1.1), no_claim=True),
        S("So why is Chile shaped like this?", [q(-30, -70, 'why'), hl(CHL, '#d62828', 0.05, fillOpacity=0.9)],
          cam=fit(CHL, pad=0.9), style='dark', no_claim=True),
        S("First, look east. The Andes, some of the highest mountains on Earth, form a giant wall along the whole country.", [
            hl(CHL, '#d62828', 0.05, fillOpacity=0.55), route([(-18, -69.2), (-24, -68.2), (-30, -69.8), (-36, -70.4), (-41, -71.8), (-47, -72.9), (-52, -72.9)], 'east', color='#c8a46e', width=16, drawDur=1.4),
            slam('ANDES', -27, -67.5, 'Andes', rotate=-80, size=90), icon('⛰️', -36, -64.5, 'wall', size=130)],
          cam=fit(CHL, pad=0.9),
          src=[src('Chile is a narrow strip between the Andes and the Pacific.', 'Chile', 'a narrow strip of land between the Andes Mountains and the Pacific Ocean')]),
        S("And to the west, there's nothing but the Pacific Ocean. So Chile is trapped in a narrow strip between the two.", [
            hl(CHL, '#d62828', 0.05, fillOpacity=0.55), flow([(-30, -95), (-30, -76)], 'west', color='#5ec8ff', width=14, drawDur=0.8), slam('PACIFIC OCEAN', -32, -84, 'Pacific', rotate=-80, size=80), icon('🌊', -40, -82, 'Ocean', size=120),
            flow([(-30, -60), (-30, -69)], 'trapped', color='#c8a46e', width=14, drawDur=0.6)],
          cam=fit(CHL, pad=0.9),
          src=[src('The Pacific Ocean lies to the west.', 'Chile', 'a narrow strip of land between the Andes Mountains and the Pacific Ocean')]),
        S("But Chile also grew north. From 1879 to 1884, in the War of the Pacific, it fought and defeated Bolivia and Peru.", [
            year(1879, 'War'), hl('BOL', '#f4a261', 'Bolivia'), hl('PER', '#e9c46a', 'Peru'),
            char('soldier_chile', 'Chile', name='Chile'), char('soldier_bolivia', 'Bolivia', screen=(0.74, 0.6), name='Bolivia', flip=True),
            shake('defeated')],
          cam=at_(-20, -68, 3.2), era='history', tr='film',
          src=[src('The War of the Pacific (1879–1884) was fought by Chile against Bolivia and Peru.', 'War_of_the_Pacific', '1 March 1879 – 4 April 1884')]),
        S("Chile took the nitrate-rich north, including the Atacama, the driest non-polar desert in the world. And Bolivia lost its coast.", [
            hl({'admin1': 'Antofagasta', 'country': 'CHL'}, '#c1121f', 'nitrate', reveal={'lat': -23.6, 'lon': -70.4}, fillOpacity=0.85),
            hl({'admin1': 'Tarapacá', 'country': 'CHL'}, '#c1121f', 'north', fillOpacity=0.85),
            lab('Atacama', -23.5, -69.2, 'north', style='serif', size=56), note('NO COAST!', -17, -64, 'coast', size=64)],
          era='history',
          src=[src('Chile acquired Antofagasta and Tarapacá with nitrate deposits; Bolivia lost its access to the Pacific.', 'Chile',
                   'acquiring resource-rich northern territories including the Antofagasta and Tarapacá regions ... eliminating Bolivia\'s access to the Pacific, and acquiring valuable nitrate deposits'),
               src('The Atacama is the driest non-polar desert in the world.', 'Atacama_Desert', 'the driest non-polar desert in the world')]),
        S("Chile expanded its territory north by almost one third.", [
            cnt('+⅓', 'third', size=220), hl(CHL, '#c1121f', 0.1, fillOpacity=0.8)],
          cam=fit(CHL, pad=0.9), era='history',
          src=[src('Chile expanded northward by almost one-third.', 'Chile', 'Chile expanding its territory northward by almost one-third')]),
        S("That's how Chile became a 4,300 kilometer ribbon, squeezed between the mountains and the ocean.", [
            blob(CHL, '#d62828', '#ffb703', 'ribbon', softness=8), cnt('4,300 km', '4,300', size=150)],
          cam=fit(CHL, pad=0.9, bearing=-3), tr='flash',
          src=[src('About 4,300 km long, between the Andes and the Pacific.', 'Chile', 'approximately 4,300 kilometers north to south')]),
    ],
    keywords={'chile': '#ff5a5f', 'andes': '#e9c46a', 'pacific': '#5ec8ff', 'bolivia': '#f4a261', 'peru': '#e9c46a'})

# ------------------------------------------------------------------ LESOTHO
ZAF, LSO = 'ZAF', 'LSO'
save('lesotho', meta(
    'Why Lesotho Is Trapped Inside South Africa 🇱🇸🇿🇦🤯',
    "Lesotho 🇱🇸 is a whole country completely surrounded by South Africa 🇿🇦 It's one of only three countries on Earth fully inside another (with Vatican City and San Marino) and the only country entirely above 1,000 meters ⛰️ Why isn't it part of South Africa? In the 1800s King Moshoeshoe I united the Basotho in these mountains, and after wars with Boer settlers he asked Britain for protection. Basutoland became a British protectorate in 1868. When South Africa was formed in 1910 it wanted Basutoland too, but Britain refused 🇬🇧 In 1966 it became the independent Kingdom of Lesotho 🤯",
    ["A country completely inside another country 🤯🇱🇸", "Would you visit the 'Kingdom in the Sky'? ⛰️👇", "Which enclave should we explain next? 🗺️"],
    ['lesotho', 'south africa', 'enclave', 'basotho', 'moshoeshoe', 'basutoland', 'africa', 'weird borders', 'mountains', 'geography', 'maps', 'learn']),
    [
        S("This is South Africa. And this is a whole country completely inside it: Lesotho.", [
            hl(ZAF, 'flag:za', 'South', hold=1), hl(LSO, 'flag:ls', 'Lesotho', hold=2),
            slam('LESOTHO', -29.6, 28.3, 'Lesotho', size=80), ping(-29.6, 28.2, 'whole', color='#ffd60a')],
          cam=fit(ZAF, pad=0.9, bearing=-3),
          src=[src('Lesotho is completely surrounded by South Africa.', 'Lesotho', "the largest of the world's three independent states completely surrounded by the territory of another country")]),
        S("It's one of only three countries on Earth completely surrounded by another country. The other two are San Marino and Vatican City, both inside Italy.", [
            cnt('3', 'three', size=220), note('only 3!', -33.5, 27, 'three', size=66), pill('San Marino + Vatican City', 'San', bg='#1d4ed8')],
          src=[src('One of three such states, with Vatican City and San Marino.', 'Lesotho', "the largest of the world's three independent states completely surrounded by the territory of another country")]),
        S("And it's the only country on Earth that lies entirely above 1,000 meters. Even its lowest point is 1,400 meters high.", [
            cnt('1,000 m+', '1,000', size=150), scatter(LSO, '⛰️', 'above', count=8, size=62),
            pill('lowest point: 1,400 m', 'meters', bg='#1d4ed8')],
          cam=fit(LSO, pad=0.85),
          src=[src('The only independent state entirely above 1,000 m; its lowest point is 1,400 m.', 'Lesotho',
                   'the only independent state in the world that lies entirely above 1,000 metres ... its lowest point at 1,400 meters')]),
        S("So why isn't it just part of South Africa?", [
            hl(ZAF, '#e76f51', 0.05, fillOpacity=0.8), hl(LSO, '#2a9d8f', 0.05, fillOpacity=0.95), q(-29.5, 28.3, 'why')],
          cam=fit(ZAF, pad=0.9), style='dark', no_claim=True),
        S("In the early 1800s, King Moshoeshoe the First united the Basotho people here, using the mountains as a natural fortress.", [
            char('moshoeshoe', 'King', name='Moshoeshoe I'), year(1822, 'united'),
            hl(LSO, '#8a5a2b', 'Basotho', fillOpacity=0.85), lab('Basotho', -29.3, 28.3, 'Basotho', style='serif', size=58)],
          cam=fit(LSO, pad=0.8), era='history', tr='film',
          src=[src('King Moshoeshoe I established the Basotho nation; Basutoland emerged under him in 1822.', 'Lesotho',
                   'Basutoland emerged as a single polity under King Moshoeshoe I in 1822')]),
        S("Fighting Boer settlers, he asked Britain for protection, and in 1868 Basutoland became a British protectorate.", [
            hl(LSO, '#8b5e34', 0.05, fillOpacity=0.6), arrow((-28.5, 26.0), (-29.2, 27.6), 'Boer', color='#c1121f'), year(1868, '1868'),
            flag('gb', -29.4, 28.3, 'Britain', pin=True, size=120), lab('Basutoland', -30.2, 28.3, 'Basutoland', style='serif', size=56)],
          era='history',
          src=[src('Moshoeshoe sought British protection; Basutoland became a British protectorate in 1868.', 'Basutoland',
                   'I am giving myself and my country up to Her Majesty\'s Government ... This appeal led to British protection in 1868')]),
        S("In 1910, the new Union of South Africa wanted Basutoland too, but Britain refused.", [
            year(1910, '1910'), hl(LSO, '#8b5e34', 0.05, fillOpacity=0.8), hl(ZAF, '#e76f51', 'Union', fillOpacity=0.7, pattern='hatch'),
            arrow((-27, 26), (-29.2, 27.8), 'wanted', color='#e76f51'), stamp('REFUSED', 'refused', size=96)],
          cam=fit(ZAF, pad=0.9), era='history',
          src=[src('South Africa sought to take over the High Commission Territories incl. Basutoland; Britain refused.', 'Basutoland',
                   'the South African government made numerous overtures to take over the High Commission Territories, which included Basutoland. However these demands were refused by Britain')]),
        S("So in 1966, it became independent as the Kingdom of Lesotho, a country inside a country.", [
            year(1966, '1966', light=True), hl(LSO, 'flag:ls', 'independent', fillOpacity=0.9), hl(ZAF, '#e5e7eb', 'inside', fillOpacity=0.25)],
          cam=fit(LSO, pad=0.75, bearing=-3), tr='flash',
          src=[src('Independence on 4 October 1966 as the Kingdom of Lesotho.', 'Lesotho', 'achieving independence on October 4, 1966')]),
    ],
    keywords={'lesotho': '#5ec8ff', 'south': '#4ade80', 'africa': '#4ade80', 'britain': '#ff5a5f', 'basutoland': '#ffd60a'})

# ------------------------------------------------------------------ WAKHAN
AFG = 'AFG'
save('wakhan', meta(
    'Why Afghanistan Has a Long Thin Arm 🇦🇫🤯 The Wakhan Corridor',
    "Afghanistan 🇦🇫 has a strange long arm reaching east: the Wakhan Corridor, about 350 km long and in places only 13 km wide 📏 It separates Tajikistan 🇹🇯 from Pakistan 🇵🇰 and touches China 🇨🇳 Why? In the 1800s the Russian Empire and British India were racing for Central Asia in the \"Great Game\" ♟️ Agreements in 1873, 1893 and 1895 left this thin strip to Afghanistan as a buffer, so the two empires would never touch. Today about 18,000 people live there, high in the Pamir mountains 🏔️",
    ["A 13 km wide strip made so two empires would never touch 🤯🇦🇫", "Would you travel to the Wakhan? 🏔️👇", "Which weird country shape next? 🗺️"],
    ['afghanistan', 'wakhan corridor', 'pamir', 'great game', 'russian empire', 'british india', 'tajikistan', 'pakistan', 'china', 'weird borders', 'geography', 'maps', 'learn']),
    [
        S("Look at Afghanistan on a map, and you'll notice a weird, long arm sticking out to the east.", [
            hl(AFG, 'flag:af', 'Afghanistan', hold=1), ping(37.0, 73.5, 'arm', color='#ffd60a'), arrow((34.8, 71.5), (36.8, 73.2), 'arm', color='#ffd60a')],
          cam=fit(AFG, pad=0.9, bearing=-3), no_claim=True),
        S("It's the Wakhan Corridor, about 350 kilometers long, and in places only 13 kilometers wide.", [
            slam('WAKHAN', 37.6, 73.2, 'Wakhan', size=80),
            meas((36.7, 71.6), (37.05, 74.9), '350 km', '350'), cnt('13 km', '13', size=170)],
          cam=at_(37.0, 73.2, 7.5, bearing=-4),
          src=[src('About 350 km long and 13–65 km wide.', 'Wakhan_Corridor', 'approximately 350 km ... varying in width from "13–65 kilometres (8–40 mi)."')]),
        S("It separates Tajikistan from Pakistan, and touches China.", [
            hl('TJK', 'flag:tj', 'Tajikistan', fillOpacity=0.8), hl('PAK', 'flag:pk', 'Pakistan', fillOpacity=0.8), hl('CHN', 'flag:cn', 'China', fillOpacity=0.8)],
          cam=at_(37.0, 73.2, 5.5),
          src=[src('It separates Tajikistan from Pakistan and borders China.', 'Wakhan_Corridor', 'separates "the Badakhshan Mountainous Autonomous Region in Tajikistan from Khyber Pakhtunkhwa in Pakistan" and borders China')]),
        S("So why does it exist?", [q(37.0, 73.2, 'why'), hl(AFG, '#d62828', 0.05, fillOpacity=0.9)], cam=at_(36, 70, 3.5), style='dark', no_claim=True),
        S("In the 1800s, two empires were competing for Central Asia in what's called the Great Game: the Russian Empire in the north, and British India in the south.", [
            year('1800s', '1800s'), lab('CENTRAL ASIA', 41, 66, 'Central', style='serif', size=58), hl(AFG, '#8b5e34', 'Central', fillOpacity=0.45),
            hl({'countries': ['TJK', 'UZB', 'TKM', 'KGZ', 'KAZ']}, '#b3202a', 'Russian', fillOpacity=0.8, hold=2),
            hl({'countries': ['PAK', 'IND']}, '#e9a1a1', 'British', fillOpacity=0.8, hold=2),
            lab('Russian Empire', 42, 66, 'Russian', style='serif', size=56), lab('British India', 27, 72, 'British', style='serif', size=56),
            arrow((44, 68), (38.5, 71), 'north', color='#b3202a'), arrow((27, 73), (34.5, 72), 'south', color='#c95a5a')],
          cam=at_(40, 70, 2.0), era='history', tr='film',
          src=[src('The corridor emerged from Great Game rivalry between the Russian Empire and British India.', 'Wakhan_Corridor', 'The corridor emerged from Great Game rivalry between empires'),
               src('The Great Game was the 19th-century British–Russian rivalry over Central Asia.', 'Great_Game', 'a rivalry between the 19th-century British and Russian empires over influence in Central Asia')]),
        S("Neither side wanted a shared border with the other. So they left this thin strip of mountains to Afghanistan, as a buffer between the two empires.", [
            blob(AFG, '#2a9d8f', '#ffd60a', 'strip', softness=6, hold=1), note('BUFFER', 38.3, 73.5, 'buffer', size=70)],
          cam=at_(36.8, 72.5, 5), era='history',
          src=[src('It was established as a buffer zone between the two empires.', 'Wakhan_Corridor', 'established this territory as "a buffer zone between the two empires."')]),
        S("Agreements in 1873, 1893 and 1895 drew its borders.", [
            cnt_steps([('1873', '1873'), ('1893', '1893'), ('1895', '1895')], size=170), ping(37.0, 73.2, '1873', color='#c1121f'), stamp('BUFFER ZONE', 'borders', size=76)],
          era='history',
          src=[src('1873 agreement (Russia border), 1893 Durand Line (British India), 1895 Pamir Boundary Commission.', 'Wakhan_Corridor',
                   'An 1873 agreement made the Panj and Pamir Rivers the Afghanistan-Russia border, while the "Durand Line Agreement of 1893 ... along with the 1895 Pamir Boundary Commission protocols')]),
        S("The rivalry only ended in 1907, when Britain and Russia signed a convention dividing their influence in Afghanistan, Persia and Tibet.", [
            year(1907, '1907'), hl({'countries': ['AFG', 'IRN']}, '#6b7280', 'convention', fillOpacity=0.6, pattern='hatch'), hl({'admin1': 'Xizang', 'country': 'CHN'}, '#6b7280', 'convention', fillOpacity=0.6, pattern='hatch'),
            lab('Persia', 32.5, 54, 'Persia', style='serif', size=54), lab('Tibet', 31.5, 88, 'Tibet', style='serif', size=54)],
          cam=at_(34, 72, 1.6), era='history',
          src=[src('The Anglo-Russian Convention of 1907 formally delineated control in Afghanistan, Persia and Tibet.', 'Great_Game',
                   'the Anglo-Russian Convention of 1907, which "created an alliance between Britain and Russia, and formally delineated control in Afghanistan, Persia, and Tibet."')]),
        S("Today, about 18,000 people live there, high in the Pamir mountains.", [
            cnt('18,000', '18,000', size=170), pill('people', '18,000'), scatter(AFG, '🏔️', 'Pamir', count=6, size=60, minLat=36.6),
            slam('PAMIR', 37.8, 74.2, 'Pamir', size=76)],
          cam=at_(37.0, 73.2, 6.5, bearing=-4), tr='flash',
          src=[src('About 18,000 residents (2024); the northern section is also called the Pamir.', 'Wakhan_Corridor', 'As of 2024, the district has an estimated population of 18,000 residents')]),
    ],
    keywords={'afghanistan': '#4ade80', 'wakhan': '#ffd60a', 'china': '#ff5a5f', 'russian': '#ff5a5f', 'british': '#f4a261'})

# ------------------------------------------------------------------ GAMBIA
GMB, SEN = 'GMB', 'SEN'
save('gambia', meta(
    'Why Gambia Is a Snake Inside Senegal 🇬🇲🇸🇳🤯',
    "The Gambia 🇬🇲 is the smallest country on mainland Africa, and apart from its coast it's completely surrounded by Senegal 🇸🇳 It's about 320 km long but only 10–50 km wide, because it follows the Gambia River 🌊 British traders controlled the river, and in 1889 Britain and France agreed a border roughly 16 km north and south of it, drawn with straight lines and arcs 📏 The Gambia became independent in 1965 and even joined Senegal in the Senegambia Confederation from 1982 until 1989 🤯",
    ["A country shaped like a river 🤯🇬🇲", "Gambia & Senegal: should they have stayed united? 👇", "Which weird border should we explain next? 🗺️"],
    ['gambia', 'senegal', 'gambia river', 'africa', 'smallest country', 'colonial borders', 'britain', 'france', 'senegambia', 'weird borders', 'geography', 'maps', 'learn']),
    [
        S("Meet The Gambia, the smallest country on mainland Africa, and one of the strangest shapes on any map.", [
            hl(GMB, '#ef233c', 'Gambia', hold=3, neon='#ffd60a'), slam('THE GAMBIA', 13.9, -15.3, 'Gambia', size=76), cnt('#1', 'smallest', size=170)],
          cam=fit(GMB, pad=0.8, bearing=-3),
          src=[src('The Gambia is the smallest country in continental Africa.', 'The_Gambia', 'the smallest country in continental Africa')]),
        S("And apart from its coast, it's completely surrounded by Senegal.", [
            hl(SEN, 'flag:sn', 'Senegal', fillOpacity=0.85), ping(13.45, -16.58, 'coast', color='#5ec8ff')],
          cam=fit(SEN, pad=0.9),
          src=[src('Senegal surrounds it except for its Atlantic coast.', 'The_Gambia', 'Senegal completely surrounds the country except for "the western part, which is bordered by the Atlantic Ocean."')]),
        S("With just 11,300 square kilometers, it's it's about 320 kilometers long, but only 10 to 50 kilometers wide.", [
            meas((13.3, -16.8), (13.3, -13.8), '320 km', '320'), cnt('10–50 km', 'wide', size=150)],
          cam=fit(GMB, pad=0.8),
          src=[src('Area 11,300 km²; about 320 km long and 10–50 km wide.', 'The_Gambia', 'with an area of 11,300 square kilometers ... approximately 320 km in length but only 10-50 km wide')]),
        S("So why does this country look like a long, thin snake, crawling deep into Senegal?", [q(13.5, -15.2, 'why'), hl(GMB, '#2a9d8f', 0.05, fillOpacity=0.95), hl(SEN, '#3a3b40', 0.05)],
          cam=fit(SEN, pad=0.9), style='dark', no_claim=True),
        S("Because the whole country follows one single river, the Gambia River, all the way from the Atlantic deep into Africa.", [
            route([(13.45, -16.6), (13.4, -16.2), (13.5, -15.6), (13.55, -15.1), (13.45, -14.7), (13.6, -14.2), (13.55, -13.8), (13.4, -13.7)], 'river', color='#5ec8ff', width=10, drawDur=1.8),
            lab('Gambia River', 13.9, -14.8, 'River', style='pill', bg='#1d4ed8', size=44)],
          cam=fit(GMB, pad=0.8),
          src=[src('Its elongated shape follows the Gambia River.', 'The_Gambia', "The nation's distinctive elongated shape follows the Gambia River")]),
        S("In colonial times, British traders controlled the river itself, while France took the land all around it.", [
            flag('gb', 13.5, -15.4, 'British', size=120), flag('fr', 15.0, -14.5, 'France', size=120),
            hl(SEN, '#1d4ed8', 'France', fillOpacity=0.6), hl(GMB, '#c8102e', 'British', fillOpacity=0.8)],
          cam=fit(SEN, pad=0.9), era='history', tr='film',
          src=[src('The British acquired the river trade rights; Britain and France competed for the region.', 'The_Gambia', 'Portuguese merchants received exclusive trade rights along the Gambia River, which the British later acquired')]),
        S("In 1889, they agreed a border about 16 kilometers north and south of the river, using straight lines and arcs.", [
            year(1889, '1889'), hl(GMB, '#c1121f', 0.05, fillOpacity=0.7), meas((13.45, -15.3), (13.6, -15.3), '16 km', 'north', countUp=False)],
          cam=fit(GMB, pad=0.8), era='history',
          src=[src('The 1889 Anglo-French agreement set a border about 16 km north and south of the river with straight lines and arcs.', 'The_Gambia',
                   'The 1889 Anglo-French agreement formally established boundaries, with "straight lines and arcs" giving Britain control of areas roughly 16 kilometers north and south of the river')]),
        S("The Gambia became independent in 1965, and from 1982 to 1989 it even joined Senegal in one confederation.", [
            year(1965, '1965', light=True), hl(GMB, '#ef233c', 0.1, neon='#ffd60a'), hl(SEN, 'flag:sn', '1982', fillOpacity=0.85),
            pill('Senegambia 1982–1989', '1982', bg='#16a34a')],
          cam=fit(SEN, pad=0.9, bearing=-3), tr='flash',
          src=[src('Independence 18 February 1965; Senegambia Confederation 1982–1989.', 'The_Gambia', 'formed the Senegambia Confederation with its neighbor in 1982, but "permanently withdrew from the confederation in 1989."')]),
    ],
    keywords={'gambia': '#ff5a5f', 'senegal': '#4ade80', 'river': '#5ec8ff', 'british': '#ff5a5f', 'france': '#5ec8ff'})
