"""Five videos rewritten from scratch with the full toolbox (round 6): istanbul, point_roberts, hawaii, darien_gap, chimborazo.

Facts and quotes are the already verified ones; narration, pacing, visuals and VFX are new:
 - question hook + first-second text hook, loop ending
 - real routes only (road() / sea_points() / road_points()), no hand-typed ship tracks
 - VFX from the clip library (Noto animated emoji, CC BY 4.0): collision, fire, volcano, snake, mosquito, rain, lightning, ...
Run:  python3 tools/authoring/v2_five.py [id ...]
"""
import sys
from helpers import *

WANT = set(sys.argv[1:])


def want(v):
    return not WANT or v in WANT


# =========================================================================================== ISTANBUL
if want('istanbul'):
    IST = (41.03, 29.0)
    BOS = [(40.99, 28.99), (41.03, 29.01), (41.07, 29.05), (41.11, 29.06), (41.16, 29.08), (41.2, 29.12), (41.23, 29.14)]
    WALLS = [(40.9937, 28.9227), (41.0045, 28.9215), (41.0120, 28.9230), (41.0200, 28.9265), (41.0280, 28.9310), (41.0340, 28.9355), (41.0405, 28.9400), (41.0435, 28.9440)]
    IST_PROV = {'admin1': 'Istanbul', 'country': 'TUR'}
    BOS_LINE = [(40.9, 28.97)] + BOS + [(41.4, 29.2)]   # the strait, extended into both seas: the line that splits Istanbul into Europe and Asia
    FERRY = [(41.014, 28.975), (41.017, 28.99), (41.02, 29.008), (41.023, 29.02)]
    TUN = [(41.0150, 28.9770), (41.0195, 28.9960), (41.0255, 29.0150)]
    save('istanbul', meta(
        'The City on TWO Continents 🇹🇷🤯 Why Istanbul Is in Europe AND Asia',
        "Istanbul 🇹🇷 sits on two continents at once, split by the Bosphorus, a 31 km strait between Europe and Asia 🌊 At its narrowest it's only about 700 meters wide! About two-thirds of its 15+ million people live on the European side. Founded as Byzantium, it became Constantinople in 330 AD, was conquered by the Ottomans in 1453 after a 55-day siege 💥 and officially renamed Istanbul in 1930 🕌 The Bosphorus is the only passage between the Black Sea and the Mediterranean, and today three bridges and a railway tunnel under the strait connect the two continents 🤯",
        ["One city, two continents 🤯🇹🇷", "Do you live on the European or the Asian side? 👇", "Which city should we explain next? 🗺️"],
        ['istanbul', 'turkey', 'bosphorus', 'europe', 'asia', 'constantinople', 'byzantium', 'ottoman empire', 'siege of constantinople', 'transcontinental', 'geography', 'history', 'maps', 'learn']),
        [
            S("How can one single city sit on two continents at once?", [
                hook('ONE CITY. *TWO* CONTINENTS?', at=0.05, until='single'),
                hl('TUR', 'flag:tr', 0.05, fillOpacity=0.7), ping(*IST, 'city', color='#ffd60a'), trace(IST_PROV, '#ffd60a', 'city', neon='#ffd60a', fillOpacity=0.2)],
              cam={'lat': 39.5, 'lon': 32, 'zoom': 2.2, 'bearing': -3, 'then': [{'at': 'city', 'lat': 41.1, 'lon': 28.95, 'zoom': 22, 'duration': 1.4}]},
              src=[src('Istanbul straddles the Bosphorus between Europe and Asia.', 'Istanbul', 'straddles the Bosphorus ... between the Sea of Marmara and the Black Sea')]),
            S("Because a narrow strait cuts straight through it: the Bosphorus.", [
                lab('EUROPE', 41.16, 28.72, 'Because', style='map', size=64), lab('ASIA', 40.96, 29.32, 'Because', style='map', size=64),
                route(BOS, 'strait', color='#5ec8ff', width=10, drawDur=1.4, laser=True, hold=2),
                route(BOS[::-1], 'Because', color='#ffffff', width=1, glow=False, id='bs1', mover={'kind': 'ship', 'size': 64, 'style': 'cargo'}, drawDur=2.6, check=False),
                route(BOS, 'narrow', color='#ffffff', width=1, glow=False, id='bs2', mover={'kind': 'ship', 'size': 64, 'style': 'tanker'}, drawDur=2.4, check=False)],
              cam=at_(41.06, 29.0, 90, bearing=-6), tr='flash',
              src=[src('The Bosporus forms a continental boundary between Asia and Europe.', 'Bosporus', 'forms one of the continental boundaries between Asia and Europe')]),
            S("It's 31 kilometers long, and at its narrowest point it's only 700 meters wide.", [
                cnt_steps([('31', '31 km'), ('700', '700 m')], size=180), ping(41.075, 29.057, 'narrowest', color='#ffd60a'), dot('Kandilli', 41.075, 29.06, 'narrowest', dy=104),
                lens('700', screen=(0.5, 0.4), r=300), meas((41.0848, 29.0568), (41.0826, 29.0645), '700 m', '700'),
                route(BOS, '31', color='#ffd60a', width=6, drawDur=1.6)],
              cam={'lat': 41.12, 'lon': 29.06, 'zoom': 60, 'then': [{'at': 'narrowest', 'lat': 41.075, 'lon': 29.05, 'zoom': 300, 'duration': 1.1}]},
              src=[src('31 km long; minimum width 700 m near Kandilli.', 'Bosporus', 'measures "31 km (17 nmi) long" with a minimum width of "700 m (0.38 nmi)" at its narrowest point near Kandilli')]),
            S("More than 15 million people live here, and two thirds of them are on the European side.", [
                cnt('15M+', '15', size=190),
                trace(IST_PROV, '#ffd60a', 0.05, neon='#ffd60a', fillOpacity=0.16),
                scatter(IST_PROV, 'art:person_white', 'million', count=14, size=60, stagger=0.1, sideOf={'line': BOS_LINE, 'keep': -1}),
                scatter(IST_PROV, 'art:person_white', 'thirds', count=28, size=60, stagger=0.07, sideOf={'line': BOS_LINE, 'keep': 1}),
                # the figures stand on the map like 3D pieces: lean the camera back just before they pop up, level it again when the sentence ends
                tilt(0.1, deg=36, until='side')],
              cam=at_(41.2, 28.95, 48, still=True, autoCenter=False),
              src=[src('Over 15 million inhabitants; about two-thirds live in Europe.', 'Istanbul', 'Approximately two-thirds of its population resides in Europe ... With over 15 million inhabitants')]),
            S("So why did such a huge city grow right here?", [q(41.03, 29.0, 'why'), react('art:emote_think', (0.28, 0.3), 'why', size=170)],
              cam=at_(41.03, 29.0, 40), style='dark', no_claim=True, tr='flash'),
            S("Because the Bosphorus is the only passage between the Black Sea and the Mediterranean.", [
                route(sea_points((43.2, 34.0), (35.8, 24.0)), 'passage', color='#ffd60a', width=8, drawDur=2.6, laser=True, id='pass', mover={'kind': 'ship', 'size': 100, 'style': 'cargo'}, check=False),
                lab('BLACK SEA', 42.3, 36.6, 'Black', style='map', size=44), lab('MEDITERRANEAN', 34.0, 27.5, 'Mediterranean', style='map', size=44),
                route(sea_points((35.8, 24.0), (43.2, 34.0)), 'Black', color='#ffffff', width=1, glow=False, id='pass2', mover={'kind': 'ship', 'size': 90, 'style': 'tanker'}, drawDur=3.0, check=False),
                ping(41.1, 29.07, 'Bosphorus', color='#ffd60a'), ping(40.2, 26.4, 'Mediterranean', color='#ffd60a')],
              cam={'follow': 'pass', 'zoom': 3.8, 'zoomTo': 2.8, 'duration': 1.0},
              src=[src('The Bosporus is the only passage between the Black Sea and the Mediterranean and has always been of great commercial and military importance.', 'Bosporus', 'As part of the only passage between the Black Sea and the Mediterranean, the Bosporus has always been of great importance from a commercial and military point of view.')]),
            S("Greek colonists founded Byzantium here, and in the year 330 it became Constantinople.", [
                year(330, '330'), lab('Byzantium', 41.035, 28.925, 'Byzantium', style='serif', size=60), lab('Constantinople', 40.975, 28.99, 'Constantinople', style='serif', size=56)],
              cam=at_(41.03, 28.99, 150), era='history', tr='film',
              src=[src('Founded as Byzantium (~660 BC); renamed Constantinople in 330 AD.', 'Istanbul', 'originally called Byzantium when Greek colonists established it around 660 BC. It became Constantinople in 330 AD under Constantine the Great')]),
            S("It was the capital of the Roman, Byzantine and Ottoman empires.", [
                cnt_steps([('Roman', 'ROME'), ('Byzantine', 'BYZANTIUM'), ('Ottoman', 'OTTOMANS')], size=110), art('hagia_sophia', 41.0086, 28.9802, 'Ottoman', size=190), dot('Hagia Sophia', 41.0086, 28.9802, 'Ottoman', dy=100, size=34), art('crown', 41.0086, 28.9802, 'capital', size=110, dx=-150, dy=-110)],
              era='history', cam=at_(41.03, 28.99, 150),
              src=[src('Capital of the Roman, Byzantine, Latin and Ottoman empires.', 'Istanbul', 'Istanbul served as capital for four major empires: the Roman Empire (330–395), the Byzantine Empire ... and the Ottoman Empire (1453–1922)')]),
            S("In 1453, Ottoman cannons, including a giant one that fired 270 kilogram stone balls, pounded the Theodosian walls for fifty five days, until the city fell.", [
                year(1453, '1453', screen=[0.25, 0.07]), wall(WALLS, 0.2, buildDur=1.2, side=-1, width=22),
                art('cannon', 41.003, 28.889, 'cannons', size=150, pinned=True), art('cannon', 41.018, 28.892, 'cannons', size=150, pinned=True), art('cannon', 41.034, 28.899, 'cannons', size=150, pinned=True),
                cnt_steps([('270', '270 kg'), ('fifty', '55 days')], size=130, screen=[0.5, 0.045]),
                # one volley: the three cannons fire at the same moment, the walls burn until the scene ends
                *[clip('emoji_collision', 'pounded', *w, size=230) for w in (WALLS[1], WALLS[3], WALLS[5])],
                *[clip('emoji_fire', 'pounded', *w, size=130, loop=True, until='fell', dy=-60) for w in (WALLS[1], WALLS[3], WALLS[5])],
                ],
              cam=at_(41.02, 28.93, 900, still=True), era='history',
              src=[src('Conquered on 29 May 1453 after a 55-day siege.', 'Istanbul', 'The Ottomans conquered the city "on 29 May 1453, after a 55-day siege."'),
                   src('The Theodosian land walls run about 5.7 km from the Sea of Marmara to Blachernae.', 'Walls_of_Constantinople', 'the Theodosian walls stretch for about 5.7 km (3.5 mi) from south to north'),
                   src("Mehmed II's cannon Basilica hurled a stone ball weighing 270 kg over 1.6 km.", 'Fall_of_Constantinople', 'His 27-foot-long (8.2 m) cannon was named "Basilica" and was able to hurl a 600-pound (270 kg) stone ball over a mile (1.6 km).')]),
            S("In 1930, it was officially renamed Istanbul.", [
                year(1930, '1930'), giant('ISTANBUL', 41.012, 28.968, 'Istanbul', size=90), flag('tr', 41.012, 28.968, 'renamed', size=110, dy=-210)],
              cam=at_(41.02, 28.97, 90, duration=0.5), era='history',
              src=[src('Officially renamed Istanbul in 1930.', 'Istanbul', 'officially renamed Istanbul in 1930')]),
            S("Today, three bridges and a railway tunnel link the two continents.", [
                cnt('3 + 1', 'three', size=170, screen=[0.33, 0.07]),
                bridge((41.0479, 29.0262), (41.0426, 29.0424), 'three', buildDur=0.9), dot('15 July Martyrs Bridge · 1973', 41.0452, 29.0343, 'three', dy=-46, size=30),
                bridge((41.0906, 29.0540), (41.0923, 29.0690), 'bridges', buildDur=0.9), dot('Fatih Sultan Mehmet Bridge · 1988', 41.0915, 29.0615, 'bridges', dy=-46, size=30),
                bridge((41.2050, 29.0985), (41.2004, 29.1240), 'railway', buildDur=0.9, towers=(0.3, 0.7)), dot('Yavuz Sultan Selim Bridge · 2016', 41.2027, 29.1112, 'railway', dy=-46, size=30),
                route(TUN, 'tunnel', color='#f97316', width=8, dashed=True, dash=[14, 10], drawDur=1.0), dot('Marmaray tunnel · 2013', 41.0200, 28.9960, 'tunnel', dy=46, size=30)],
              cam=fit({'box': [28.95, 40.995, 29.16, 41.215]}, pad=0.92, bearing=-6), tr='flash',
              src=[src('Bridges: 15 July Martyrs (1973), Fatih Sultan Mehmet (1988), Yavuz Sultan Selim (2016); Marmaray undersea rail tunnel opened 2013.', 'Bosphorus',
                       'the 1,074 m (3,524 ft) long 15th July Martyrs Bridge was completed in 1973 ... Fatih Sultan Mehmet (Bosporus II) Bridge ... was completed in 1988 ... the Yavuz Sultan Selim Bridge ... was completed in 2016 ... The Marmaray project, featuring a 13.7 km (8.5 mi) long undersea railway tunnel, opened on 29 October 2013')]),
            S("That tunnel runs sixty meters below sea level, so a train can cross between continents underwater.", [
                # vector cross-section: the strait, the tube under the sea floor, its depth
                section(0.05, structure={'kind': 'tunnel', 'y': 0.77}, coastLabels=['EUROPE', 'ASIA'], waterY=0.4,
                        dims=[{'x': 0.5, 'y0': 0.4, 'y1': 0.77, 'label': '60 m', 'at': 0.9}], floor=[[0, 0.66], [0.3, 0.7], [0.5, 0.78], [0.7, 0.7], [1, 0.66]])],
              cam=at_(41.02, 28.99, 140), no_claim=False,
              src=[src('The Marmaray tube was placed 60 metres below sea level.', 'Marmaray', 'The tube was placed 60 metres (197 ft) below sea level, beneath 55 metres (180 ft) of water')]),
            S("And that is the answer to one simple question:", [hl('TUR', 'flag:tr', 0.05, fillOpacity=0.7)],
              cam={'lat': 39.5, 'lon': 32, 'zoom': 2.2, 'duration': 1.6, 'loopIntro': True}, no_claim=True),
        ],
        keywords={'istanbul': '#ff5a5f', 'europe': '#5ec8ff', 'asia': '#ffd60a', 'bosphorus': '#5ec8ff', 'constantinople': '#ffd60a', 'cannons': '#ff5a5f'},
        imagery=[{'bbox': [28.55, 40.8, 29.45, 41.35], 'width': 4096, 'mask': False}, {'bbox': [28.885, 40.985, 28.975, 41.06], 'width': 2048, 'mask': False}], v2=True)

# =========================================================================================== POINT ROBERTS
if want('point_roberts'):
    PR = (48.985, -123.055)
    BLAINE = (48.993, -122.75)
    PRW = 'Point_Roberts,_Washington'
    # Point Roberts' real outline, traced on the Sentinel-2 mosaic (north edge = the 49th parallel)
    PRB = {'poly': [[49.0, -123.0907], [48.9908, -123.0889], [48.9822, -123.0867], [48.9752, -123.0849], [48.9719, -123.0843], [48.9734, -123.0788], [48.9745, -123.0724], [48.9749, -123.0669], [48.9749, -123.0596], [48.9745, -123.0486], [48.9749, -123.0376], [48.9752, -123.0285], [48.9774, -123.0215], [48.9835, -123.0233], [48.989, -123.0263], [48.9945, -123.0296], [49.0, -123.0336]]}
    # real road geometry (Natural Earth) from Tsawwassen around Boundary Bay to the Blaine crossing; the first hop is the 3 km to the border
    PR_ROAD = [(48.9765, -123.0585), (49.001, -123.075)] + [tuple(p) for p in road_points((49.0299, -123.0954), (48.993, -122.757), max_pts=40)][0:]
    FERRY = [(48.968, -123.045), (48.955, -123.0), (48.945, -122.92), (48.96, -122.84), (48.975, -122.805)]
    BORDER = (49.0, -123.062)
    save('point_roberts', meta(
        "The US Town You Can Only Drive to Through Canada 🇺🇸🇨🇦🤯 Point Roberts",
        "Point Roberts 🇺🇸 is a piece of Washington State on the tip of a Canadian peninsula south of Vancouver 🇨🇦 To reach the rest of the USA by land you have to drive about 40 km through Canada 🚗 Why? The 1846 Oregon Treaty set the US–Canada border at the 49th parallel, and the line cut straight across the tip of the Tsawwassen peninsula 📏 About 1,191 people live there, older kids cross the border four times on every school trip, and when the border closed in 2020 the town lost about 80% of its business 🚨🤯",
        ["Kids here cross an international border 4 times to go to school 🤯🚌", "Would you live in Point Roberts? 👇", "Which weird border should we explain next? 🗺️"],
        ['point roberts', 'washington', 'canada', 'usa', 'border', '49th parallel', 'oregon treaty', 'vancouver', 'exclave', 'weird borders', 'geography', 'maps', 'learn']),
        [
            S("Why can you only drive to this American town by going through Canada?", [
                hook('AMERICA, *STUCK* INSIDE CANADA?', at=0.05, until='only'),
                hl('CAN', 'flag:ca', 0.05, fillOpacity=0.5), hl(PRB, 'flag:us', 'town', fillOpacity=0.95), ping(*PR, 'town', color='#ffd60a')],
              cam={'lat': 49.0, 'lon': -123.0, 'zoom': 120, 'bearing': -3, 'then': [{'at': 'town', 'lat': 48.99, 'lon': -123.055, 'zoom': 700, 'duration': 1.4}]},
              src=[src('Point Roberts is a US pene-exclave reachable by land only through Canada (or by boat/plane).', PRW, 'a pene-exclave of the US state of Washington ... "25 mi (40 km) through Canada, or without passing through Canada by boat or private airplane."')]),
            S("It's Point Roberts, on the tip of a Canadian peninsula just south of Vancouver.", [
                giant('POINT ROBERTS', 48.76, -123.25, 'Point', size=70), ping(*PR, 'Point', color='#ffd60a'), dot('Vancouver', 49.25, -123.1, 'Vancouver', dy=-46),
                trace({'admin1': 'Washington', 'country': 'USA'}, '#ffd60a', 'Point', neon='#ffd60a', fillOpacity=0.12),
                arrow((49.22, -123.1), (49.04, -123.07), 'south', color='#ffd60a', width=10)],
              cam=at_(49.08, -123.05, 60, autoCenter=False),
              src=[src('On the southern tip of the Tsawwassen peninsula, south of Vancouver.', PRW, 'on the southernmost tip of the Tsawwassen peninsula, south of Vancouver, British Columbia, Canada')]),
            S("George Vancouver named it in 1792, after his friend Henry Roberts.", [
                year(1792, '1792', light=True), ping(*PR, 'named', color='#ffd60a'), lab('Henry Roberts', 48.8, -123.45, 'Henry', style='serif', size=44),
                ship(sea_points((49.2, -123.7), (48.96, -123.12)), 'Vancouver', 'hms', style='caravel', drawDur=2.6, size=120, check=False)],
              era='history', tr='film', cam=at_(49.06, -123.3, 26),
              src=[src('Point Roberts was named by George Vancouver after his friend Henry Roberts (1792 expedition).', PRW, 'Point Roberts acquired its present name from George Vancouver, who named it after his friend Henry Roberts')]),
            S("So why is it American?", [q(PR[0], PR[1], 'why'), react('art:emote_think', (0.3, 0.32), 'why', size=170)], cam=at_(49.0, -123.0, 90), style='dark', no_claim=True, tr='flash'),
            S("In 1846, the Oregon Treaty set the border between the US and British Canada along the 49th parallel.", [
                year(1846, '1846'), route([(49, -125), (49, -120)], '49th', rhumb=True, color='#ffd60a', width=7, drawDur=1.3, laser=True),
                lab('BRITISH CANADA', 49.5, -122.0, 'British', style='serif', size=50), lab('UNITED STATES', 48.5, -122.0, 'US', style='serif', size=52),
                flag('gb', 49.78, -122.0, 'British', size=100), flag('us', 48.25, -122.0, 'US', size=100), art('handshake', 49.0, -123.2, 'treaty', size=120)],
              cam=at_(49.0, -122.5, 12), era='history', tr='film',
              src=[src('The 1846 Oregon Treaty fixed the boundary at the 49th parallel.', PRW, 'the 1846 Oregon Treaty, which established "the 49th parallel would define the boundary between their respective territories"')]),
            S("But this perfectly straight line cut right across the peninsula, leaving its tip on the American side.", [
                route([(49.0, -123.3), (49.0, -122.8)], 'line', rhumb=True, color='#ffd60a', width=7, drawDur=0.8, laser=True),
                lab('CANADA', 49.045, -123.07, 'perfectly', style='map', size=46), lab('USA', 48.945, -123.06, 'tip', style='map', size=46),
                hl(PRB, 'flag:us', 'tip', fillOpacity=0.95)],
              cam=at_(48.995, -123.055, 450), tr='flash',
              src=[src('The 49th parallel left the southern peninsula tip on the US side.', PRW, 'leaving this southern peninsula on the American side')]),
            S("So to reach the rest of the USA by land, you drive about 40 kilometers through Canada.", [
                route(PR_ROAD, 'drive', color='#ffffff', width=5, dashed=True, dash=[14, 12], glow=False, id='road', mover={'kind': 'icon', 'icon': 'art:car', 'size': 90}, drawDur=3.6, medium='land', smooth=False),
                dot('Blaine, USA', *BLAINE, 'Canada', dy=90, dx=0), cnt('40 km', '40', size=160), ping(49.0, -123.066, 'Canada', color='#ff3b3b')],
              cam={'follow': 'road', 'zoom': 130, 'zoomTo': 100, 'duration': 1.0},
              src=[src('Residents travel about 25 mi (40 km) through Canada.', PRW, 'traveling "25 mi (40 km) through Canada, or without passing through Canada by boat or private airplane."')]),
            S("Older kids go to school in Blaine, so they cross the border four times on every round trip.", [
                route(PR_ROAD, 'school', color='#ffffff', width=5, dashed=True, dash=[14, 12], glow=False, id='bus', mover={'kind': 'icon', 'icon': 'art:bus', 'size': 72}, drawDur=4.0, medium='land', smooth=False), dot('Blaine, USA', *BLAINE, 'cross', dy=90, dx=0), ping(49.0, -123.066, 'cross', color='#ff3b3b'),
                cnt_steps([('school', '1'), ('cross', '2'), ('four', '4')], size=200)],
              cam={'follow': 'bus', 'zoom': 130, 'zoomTo': 100, 'duration': 0.9},
              src=[src('Students in grade 4 and above commute to Blaine, crossing the border four times.', PRW,
                       'Students attending grades 4 and above must commute to Blaine, Washington. This journey requires them to "cross the US–Canada border four times, two on the trip to Blaine and two on the trip back."')]),
            S("In March 2020, the border closed, and the town lost about eighty percent of its business.", [
                year('2020', 'March', light=True), handstamp('BORDER CLOSED', 'closed', size=92, screen=[0.5, 0.2]),
                clip('emoji_police-car-light', 'closed', 49.014, -123.035, size=170, loop=True, until='lost'), ban('art:car', 'closed', lat=49.014, lon=-123.095, size=130), grade('cold', 'March', until=5.5),
                cnt('-80%', 'eighty', size=200, color='#ff5a5f', screen=[0.5, 0.31])],
              cam=at_(48.99, -123.05, 100, bearing=3), tr='flash',
              src=[src('The border closed to non-essential travel in March 2020; Point Roberts lost 80 percent of its business.', PRW,
                       'In 2020, a study found that Point Roberts had lost 80 percent of its business and hundreds of seasonal residents as a result of the pandemic and border shutdown.')]),
            S("So a temporary passenger ferry carried people to Blaine, over the water.", [
                route(FERRY, 'ferry', color='#ffffff', width=5, dashed=True, dash=[14, 12], glow=False, id='ferry', mover={'kind': 'ship', 'size': 170, 'style': 'ferry'}, drawDur=3.0),
                dot('Blaine', 48.99, -122.77, 'Blaine', dy=90, dx=-20), ping(*FERRY[0], 'ferry', color='#ffd60a')],
              cam={'follow': 'ferry', 'zoom': 130, 'zoomTo': 100, 'duration': 1.0},
              src=[src('A temporary passenger ferry ran from Point Roberts to Blaine.', PRW, 'A temporary passenger ferry service from Point Roberts to Blaine operated by the Port of Bellingham')]),
            S("Today, Canadians drive in for cheaper American gas, alcohol and food.", [
                scatter(PRB, 'art:beer_glass', 'alcohol', count=3, size=80, stagger=0.25), scatter(PRB, 'art:oil_barrel', 'gas', count=3, size=100, stagger=0.25, until='alcohol'),
                scatter(PRB, 'art:wheat', 'food', count=3, size=90, stagger=0.25), art('money_bag', 49.012, -123.02, 'cheaper', size=110)],
              cam=at_(48.985, -123.055, 600),
              src=[src('Canadians visit Point Roberts for cheaper American gasoline, alcohol and food.', PRW, 'Canadians visit for cheaper American gasoline, alcohol, and food when the Canadian dollar is strong')]),
            S("Forty times more Canadians have mailboxes here than there are residents.", [
                lab('MAILBOXES', at='mailboxes', screen=[0.5, 0.29], style='map', size=54), cnt('40x', 'Forty', size=140, color='#ff5a5f', screen=[0.5, 0.18]),
                scatter(PRB, 'art:mailbox', 'mailboxes', count=6, size=70, stagger=0.1), hl(PRB, 'flag:us', 'mailboxes', fillOpacity=0.5)],
              cam=at_(48.985, -123.055, 600),
              src=[src('Forty times more Canadians have mailboxes in Point Roberts than there are residents.', PRW, 'Forty times more Canadians have mailboxes in Point Roberts than the number of residents')]),
            S("Only 1,191 people live in this American town, cut off by Canada.", [
                hl(PRB, 'flag:us', 0.05, fillOpacity=0.95), lab('POINT ROBERTS', 48.972, -123.055, 0.05, style='map', size=54),
                cnt('1,191', '1,191', size=180), scatter(PRB, 'art:person_white', 'people', count=8, size=44, stagger=0.15)],
              cam=at_(48.985, -123.055, 1000, bearing=-4, autoCenter=False), tr='flash',
              src=[src('Population 1,191 (2020 census).', PRW, 'The 2020 census recorded 1,191 residents across 4.884 square miles of territory.')]),
            S("Which brings us back to the very first question:", [],
              cam=at_(49.0, -123.0, 120, duration=1.6, loopIntro=True), no_claim=True),
        ],
        keywords={'canada': '#ff5a5f', 'usa': '#5ec8ff', 'american': '#5ec8ff', 'blaine': '#ffd60a', 'vancouver': '#ffd60a'},
        imagery=[{'bbox': [-124.3, 48.5, -122.1, 49.6], 'width': 4096}, {'bbox': [-123.35, 48.85, -122.6, 49.35], 'width': 4096, 'landExtra': [[[49.0042, -123.0948], [48.9919, -123.0928], [48.9823, -123.0903], [48.9744, -123.0883], [48.9707, -123.0876], [48.9724, -123.0815], [48.9737, -123.0743], [48.9741, -123.0681], [48.9741, -123.06], [48.9737, -123.0476], [48.9741, -123.0353], [48.9744, -123.0251], [48.9769, -123.0173], [48.9837, -123.0193], [48.9899, -123.0227], [48.9961, -123.0264], [49.0042, -123.0308]]]}], v2=True)

# =========================================================================================== HAWAII
if want('hawaii'):
    HI = {'admin1': 'Hawaii', 'country': 'USA'}
    HNL = (21.31, -157.86)
    MK = (19.82, -155.47)
    save('hawaii', meta(
        'How Hawaii Became Part of the USA 🇺🇸🌺🤯',
        "Hawaii 🌺 is a US state in the middle of the Pacific, but it used to be an independent kingdom 👑 In 1893 a group of mostly American businessmen, backed by US sailors and Marines, overthrew Queen Liliʻuokalani, who surrendered to avoid bloodshed 🏳️ The United States annexed Hawaii in 1898, it became a territory in 1900 and a state in 1959 🇺🇸 And in 1993, Congress formally apologized for the US role in the overthrow 🤯",
        ["A kingdom that became a US state 🤯🌺", "Did you know the US apologized for this in 1993? 👇", "Which island story should we explain next? 🗺️"],
        ['hawaii', 'usa', 'hawaiian kingdom', 'queen liliuokalani', 'annexation', 'honolulu', 'pacific ocean', 'history', 'geography', 'maps', 'learn']),
        [
            S("Why is Hawaii a US state, when it sits all alone in the middle of the Pacific Ocean?", [
                hook('WHY IS *HAWAII* AMERICAN?', at=0.05, until='state'),
                hl(HI, 'flag:us', 'Hawaii', hold=1, neon='#ffd60a'), ping(21.0, -157.0, 'Pacific', color='#ffd60a'),
                plane([(33.94, -118.4), (23.2, -156.4)], 'sits', 'jet', drawDur=3.0, medium='air', check=False)],
              cam=at_(23, -150, 1.3, bearing=-3),
              src=[src('Hawaii became a US state in 1959.', 'Overthrow_of_the_Hawaiian_Kingdom', 'eventually achieved statehood in 1959')]),
            S("It lies 3,200 kilometers from the US mainland, and it's the only state that is an archipelago.", [
                arrow((34, -122), (22.5, -153), 'lies', color='#ffd60a'),
                cnt('3,200 km', '3,200', size=160), hl(HI, 'flag:us', 'archipelago', fillOpacity=0.85, neon='#ffd60a')],
              cam=at_(23, -148, 1.4, bearing=-3),
              src=[src('About 2,000 miles (3,200 km) southwest of the US mainland.', 'Hawaii', 'in the Pacific Ocean about 2,000 miles (3,200 km) southwest of the U.S. mainland'),
                   src('Hawaii is the only state that is an archipelago.', 'Hawaii', 'the only state not on the North American mainland, the only state that is an archipelago, the only state south of the Tropic of Cancer')]),
            S("Its volcano Mauna Kea is taller than Mount Everest, when you measure it from the ocean floor.", [
                ping(*MK, 'Mauna', color='#ff5a5f'), dot('Mauna Kea', *MK, 'Mauna', dy=-90, size=40), cnt('10,200 m', 'taller', size=150),
                ellipse(19.6, -155.5, 'Everest', rx=300, ry=330)],
              cam=at_(19.8, -155.5, 70, bearing=-3),
              src=[src('Mauna Kea is taller than Everest measured from its base on the Pacific floor (about 10,200 m).', 'Hawaii',
                       'it is taller than Mount Everest when measured from the base of the mountain, which is on the floor of the Pacific Ocean, rising about 33,500 feet (10,200 m)')]),
            S("So how did an island kingdom become an American state?", [q(21, -157, 'how')], cam=at_(20.6, -157.4, 15), style='dark', no_claim=True),
            S("In the 1890s, Hawaii was an independent kingdom, ruled by Queen Liliʻuokalani.", [
                char('queen_liliuokalani', 'Queen', name='Queen Liliʻuokalani'), hl(HI, '#b3202a', 'kingdom', fillOpacity=0.85),
                art('crown', 21.35, -157.9, 'ruled', size=110, dy=-120)],
              cam=at_(20.6, -157.4, 15), era='history', tr='film',
              src=[src('Queen Liliʻuokalani was the monarch deposed in 1893.', 'Overthrow_of_the_Hawaiian_Kingdom', "Queen Liliʻuokalani was deposed during this coup d'état against the Hawaiian Kingdom.")]),
            S("It was founded in 1795 by Kamehameha the First, and in 1843 Britain and France recognized it as an independent state.", [
                year(1795, '1795'), year(1843, '1843'), ping(19.6, -155.5, 'Kamehameha', color='#ffd60a'), dot('Kamehameha I', 19.6, -155.5, 'Kamehameha', dy=-150, size=40, until='1843'), flag('gb', 23.5, -159.5, 'Britain', size=110), flag('fr', 23.5, -155.2, 'France', size=110), lab('Independent state', 18.6, -157.4, 'independent', style='serif', size=48)],
              era='history',
              src=[src('Kamehameha I established the Hawaiian Kingdom in 1795.', 'Hawaiian_Kingdom', 'He established the Hawaiian Kingdom in 1795 with the help of western weapons and advisors'),
                   src('In 1843 Britain and France jointly declared Hawaii an independent state.', 'Hawaiian_Kingdom', 'Britain and France issued the Anglo-Franco Proclamation, jointly declaring the Hawaiian Islands "an Independent State."')]),
            S("But in 1893, mostly foreign businessmen overthrew the Queen, backed by US sailors and Marines.", [
                year(1893, '1893'), char('businessman', 'businessmen', screen=(0.52, 0.625), size=290, name='Committee of Safety', flip=True),
                char('us_marine', 'Marines', screen=(0.22, 0.625), size=290), ping(*HNL, 'overthrew', color='#ff3b3b'), shake('overthrew')],
              cam=at_(21.4, -157.9, 30), era='history',
              src=[src('On 17 January 1893 the Committee of Safety, backed by 162 sailors and Marines from the USS Boston, overthrew the Queen.', 'Overthrow_of_the_Hawaiian_Kingdom',
                       'The "Committee of Safety," composed of foreign-born residents and Hawaiian-born individuals, led the overthrow ... deployed 162 sailors and Marines from the USS Boston')]),
            S("She surrendered, to avoid bloodshed.", [char('queen_liliuokalani', 'surrendered', name='Queen Liliʻuokalani'), icon('art:dove', 22.45, -158.15, 'bloodshed', size=130)],
              era='history', cam=at_(21.4, -157.9, 25),
              src=[src('The Queen surrendered to avoid bloodshed.', 'Overthrow_of_the_Hawaiian_Kingdom', 'The Queen surrendered to avoid bloodshed.')]),
            S("In 1898, the United States annexed Hawaii. In 1900 it became a territory, and in 1959, it finally became a state.", [
                cnt_steps([('1898', '1898'), ('1900', '1900'), ('1959', '1959')], size=180), hl(HI, 'flag:us', 'annexed', reveal={'lat': 21.3, 'lon': -157.8}),
                flag('us', 22.6, -157.4, 'annexed', size=120), stamp('STATE', 'finally', size=90, screen=[0.5, 0.24])],
              cam=at_(20.6, -157.4, 15), tr='flash',
              src=[src('Annexed via the Newlands Resolution (1898); territory 1900; statehood 1959.', 'Overthrow_of_the_Hawaiian_Kingdom', 'The United States annexed Hawaii through the Newlands Resolution in 1898. Hawaii became a territory in 1900 and eventually achieved statehood in 1959.')]),
            S("And in 1993, the US Congress formally apologized for the overthrow.", [
                year(1993, '1993', light=True), stamp('SORRY', 'apologized', size=100, screen=[0.5, 0.57]),
                art('gavel', 21.7, -159.2, 'Congress', size=120), ring(*HNL, 'overthrow', r=70)],
              cam=at_(19.2, -157.0, 15, autoCenter=False),
              src=[src('In 1993 Congress passed the Apology Resolution, signed by President Clinton.', 'Overthrow_of_the_Hawaiian_Kingdom', 'In 1993, Congress passed the Apology Resolution, which President Clinton signed, formally apologizing for the U.S. role in the overthrow')]),
            S("And that is the real story behind one simple question:", [],
              cam=at_(23, -150, 1.3, duration=1.6, loopIntro=True), no_claim=True),
        ],
        keywords={'hawaii': '#ff5a5f', 'united': '#5ec8ff', 'queen': '#ffd60a', 'marines': '#5ec8ff'}, v2=True)

# =========================================================================================== DARIEN GAP
if want('darien_gap'):
    YAV, TUR = (8.18, -77.69), (8.09, -76.73)
    DG = 'Darién_Gap'
    PAH = 'Pan-American_Highway'
    GAP_PAN = {'admin1s': ['Darién', 'Emberá', 'Kuna Yala'], 'country': 'PAN'}
    GAP_COL = {'admin1': 'Chocó', 'country': 'COL'}
    HW_N = road_points((70.3, -148.7), (64.84, -147.72), (60.72, -135.05), (55.76, -120.24), (49.28, -123.12), (34.05, -118.24), (32.5, -117.0), (19.43, -99.13), (14.63, -90.51), (9.93, -84.08), (8.98, -79.52), (8.15, -77.69), max_pts=110)
    HW_S = road_points((8.1, -76.73), (6.25, -75.57), (4.71, -74.07), (-0.18, -78.47), (-12.05, -77.04), (-33.45, -70.67), (-34.6, -58.38), (-54.8, -68.3), max_pts=90)
    SHIP = sea_points((10.6, -80.0), (10.3, -76.2))
    COUNTRIES = [('CAN', 'ca', 'Canada,'), ('USA', 'us', 'United'), ('MEX', 'mx', 'Mexico,'), ('GTM', 'gt', 'Guatemala,'), ('SLV', 'sv', 'Salvador,'), ('HND', 'hn', 'Honduras,'),
                 ('NIC', 'ni', 'Nicaragua,'), ('CRI', 'cr', 'Costa'), ('PAN', 'pa', 'Panama,'), ('COL', 'co', 'Colombia,'), ('ECU', 'ec', 'Ecuador,'), ('PER', 'pe', 'Peru,'),
                 ('CHL', 'cl', 'Chile'), ('ARG', 'ar', 'Argentina.')]
    DUR_N, DUR_S = 5.6, 2.6
    save('darien_gap', meta(
        'The Darién Gap: The Road That Stops in the Jungle 🌴🇵🇦🇨🇴😱',
        "The Pan-American Highway runs about 30,000 km from Alaska 🇺🇸 to the tip of Argentina 🇦🇷 but it has one gap 🛑 Between Yaviza in Panama 🇵🇦 and Turbo in Colombia 🇨🇴 there's no road for about 106 km: the Darién Gap 🌴 A road was planned in 1971 and halted in 1974, and swamps, mountains, rainforest, deadly wildlife 🐍 and violent crime make it one of the most dangerous places on Earth. Still, in 2023 more than 520,000 people crossed it on foot 😱",
        ["30,000 km of highway… and 106 km of jungle 🌴😱", "Would you ever try to cross the Darién Gap? 👇", "Which dangerous place should we cover next? 🗺️"],
        ['darien gap', 'pan-american highway', 'panama', 'colombia', 'jungle', 'rainforest', 'migration', 'dangerous places', 'geography', 'maps', 'learn']),
        [
            S("Why does a highway that runs from Alaska all the way to Argentina suddenly stop?", [
                hook('THE ROAD THAT *STOPS*', at=0.05, until='Argentina'),
                route(HW_N, 0.05, id='hw1', color='#ffd60a', width=9, drawDur=3.3, hold=1, medium='land', smooth=False),
                route(HW_S, 'Argentina', color='#ffd60a', width=9, drawDur=1.5, hold=1, medium='land', smooth=False),
                cnt('30,000 km', 'suddenly', size=170), ping(70.3, -148.7, 'Alaska', color='#ffd60a'), ping(-54.8, -68.3, 'Argentina', color='#ffd60a')],
              cam={'follow': 'hw1', 'zoom': 3.4, 'zoomTo': 1.0, 'duration': 0.8, 'then': [{'at': 'Argentina', 'lat': -22, 'lon': -68, 'zoom': 1.15, 'duration': 1.3}]},
              src=[src('The Pan-American Highway is about 30,000 km, from Prudhoe Bay, Alaska, to Ushuaia, Argentina.', PAH, 'from Prudhoe Bay, Alaska, United States, in the northernmost part of North America, to Ushuaia, Argentina')]),
            S("It's the Pan-American Highway, and it crosses 14 countries, one border after another, from the top of Alaska all the way down to the tip of Argentina.", [
                cnt('14', '14', size=170, screen=[0.5, 0.2]),
                # slow, steady drawing; each country's flag fills its shape the moment the road head crosses its border (no names needed)
                route(HW_N, 0.3, id='hw2', color='#ffd60a', width=8, drawDur=DUR_N, medium='land', smooth=False, ease='linear'),
                route(HW_S, DUR_N + 0.45, id='hw3', color='#ffd60a', width=8, drawDur=DUR_S, medium='land', smooth=False, ease='linear'),
                *[hl(iso, 'flag:' + fl, 0.3, fillOpacity=0.8, flagKeep=True, onRoute=('hw3' if iso in ('COL', 'ECU', 'PER', 'CHL', 'ARG') else 'hw2')) for iso, fl, word in COUNTRIES]],
              cam={'follow': ['hw2', 'hw3'], 'zoom': 3.0, 'zoomAlong': [[[0, 3.0], [0.45, 3.2], [0.7, 4.4], [0.8, 7.0], [1, 9.0]], [[0, 7.0], [0.2, 4.6], [0.6, 3.4], [1, 3.0]]], 'duration': 0.9},
              src=[src('The highway links 14 countries.', PAH, 'The highway connects 14 countries: Canada, the United States, Mexico, Guatemala, El Salvador, Honduras, Nicaragua, Costa Rica, Panama, Colombia, Ecuador, Peru, Chile, and Argentina.')]),
            S("But in Panama, the road simply ends, in the town of Yaviza.", [
                {'type': 'dim', 'except': ['PAN', 'COL'], 'amount': 0.5, 'color': '#05070c', 'at': 0.1},
                ping(*YAV, 'ends', color='#ff3b3b'), dot('Yaviza', *YAV, 'Yaviza', dy=-90), handstamp('ROAD ENDS', 'ends', size=88, screen=[0.5, 0.2]), shake('ends'),
                hl('PAN', 'flag:pa', 'Panama', fillOpacity=0.4)],
              cam=at_(8.3, -77.4, 6, duration=1.0, autoCenter=False), tr='zoom',
              src=[src('The highway breaks at Yaviza, Panama and resumes at Turbo, Colombia, roughly 106 km away.', DG, "The 'Gap' interrupts the Pan-American Highway, which breaks at Yaviza, Panama, and resumes at Turbo, Colombia, roughly 106 km (66 mi) away.")]),
            S("It only starts again in Turbo, Colombia, 106 kilometers away.", [
                dot('Turbo', *TUR, 'Turbo', dy=86), dot('Yaviza', *YAV, 'again', dy=-90),
                meas(YAV, TUR, '106 km', 'kilometers'), ],
              cam=at_(8.2, -77.2, 18, bearing=-3, duration=1.5, autoCenter=False),
              src=[src('The highway breaks at Yaviza, Panama and resumes at Turbo, Colombia, roughly 106 km away.', DG, "The 'Gap' interrupts the Pan-American Highway, which breaks at Yaviza, Panama, and resumes at Turbo, Colombia, roughly 106 km (66 mi) away.")]),
            S("Between them lies the Darién Gap: swamps, mountains and thick rainforest.", [
                trace(GAP_PAN, '#16a34a', 'Darién', neon='#4ade80', fillOpacity=0.5), trace(GAP_COL, '#16a34a', 'Darién', neon='#4ade80', fillOpacity=0.5),
                giant('DARIÉN GAP', 9.9, -77.3, 'Darién', size=84),
                scatter(GAP_COL, 'art:water_drop', 'swamps', count=5, size=70, stagger=0.15), scatter(GAP_PAN, 'art:mountain', 'mountains', count=4, size=90, stagger=0.15), scatter(GAP_PAN, 'art:tree', 'rainforest', count=7, size=80, stagger=0.1)],
              cam=at_(7.9, -77.3, 14, duration=1.2), tr='flash',
              src=[src('Colombian side: Atrato delta marshland; Panamanian side: mountainous rainforest.', DG, "the Colombian side dominated primarily by the river delta of the Atrato River, which creates a flat marshland at least 80 km (50 mi) wide")]),
            S("Cars have to be shipped around it, by boat.", [
                ban('art:car', 'Cars', lat=8.0, lon=-77.55, size=150),
                ship(SHIP, 'shipped', 'car', style='cargo', emblem='#ffd60a', drawDur=1.5, size=110)],
              cam=at_(9.2, -78.0, 8, duration=0.5),
              src=[src('Vehicles must be shipped by cargo vessel to get around the gap.', PAH, 'vehicles must be shipped by cargo vessel to bridge this section')]),
            S("Heavy rain sends flash floods roaring through the jungle.", [
                clip('emoji_rain-cloud', 'rain', 8.1, -77.7, size=260, loop=True), particles('rain', 0.3, density=0.7),
                scatter(GAP_PAN, 'art:water_drop', 'floods', count=7, size=70, stagger=0.12)],
              cam=at_(7.9, -77.3, 20, duration=1.2),
              src=[src('Rain in the Darién Gap produces flash floods.', DG, 'Rainfall in the Darién Gap produces flash floods that can carry sleepers to their deaths.')]),
            S("A road was planned there in 1971, but halted in 1974, after environmentalists raised serious concerns.", [
                year(1971, '1971', light=True), year(1974, '1974', light=True), stamp('HALTED', 'halted', size=100, screen=[0.5, 0.52]),
                art('excavator', 8.95, -77.95, 'planned', size=130), art('tree', 7.6, -76.9, 'environmentalists', size=100), art('people', 7.7, -77.3, 'environmentalists', size=100)],
              style='pastel', tr='film', cam=at_(8.3, -77.4, 6, autoCenter=False),
              src=[src('Road planning began in 1971 with US funding and was halted in 1974 after environmentalists raised concerns.', DG, 'Planning began in 1971 with the help of US funding, but was halted in 1974 after multiple environmentalists expressed serious concerns.')]),
            S("Then in 1978, the United States blocked its support, to stop foot-and-mouth disease from spreading north.", [
                year(1978, '1978', light=True), art('cow', 7.1, -75.95, 'foot-and-mouth', size=90), art('cow', 8.0, -75.9, 'disease', size=90),
                arrow((6.5, -76.6), (9.2, -77.9), 'spreading', color='#e11d2e', width=14)],
              style='pastel', cam=at_(7.9, -77.3, 8),
              src=[src('In 1978 the US Department of Agriculture blocked US support to prevent the spread of foot-and-mouth disease.', DG, 'US support was further blocked by the US Department of Agriculture in 1978, with the intention of preventing the spread of foot-and-mouth disease.')]),
            S("Today the jungle is full of venomous wildlife and tropical diseases.", [
                clip('emoji_snake', 'venomous', screen=[0.66, 0.5], size=240, loop=True), clip('emoji_mosquito', 'tropical', screen=[0.76, 0.3], size=220, loop=True), grade('danger', 0.3),
                scatter(GAP_PAN, 'art:tree', 'jungle', count=8, size=80, stagger=0.1)],
              cam=at_(7.9, -77.3, 20, duration=1.2), tr='flash',
              src=[src('Dangers include venomous wildlife and tropical diseases.', DG, 'venomous and deadly wildlife, tropical insects, parasites and diseases, and frequent heavy rains and flash floods')]),
            S("There is no police and no hospital, so violent crime is everywhere.", [
                clip('emoji_sos', 'police', 8.3, -76.35, size=240, loop=True), lab('NO POLICE', 8.95, -76.35, 'police', style='map', size=60), shake('violent'), grade('danger', 0.3),
                art('warning', 7.3, -76.5, 'violent', size=130), art('cross_mark', 6.6, -76.4, 'hospital', size=120), hl(GAP_PAN, '#ff3b3b', 'crime', fillOpacity=0.28)],
              src=[src('Law enforcement and medical support are nonexistent; violent crime is rampant.', DG, 'law enforcement and medical support are nonexistent, resulting in rampant violent crime')]),
            S("Still, in 2021, more than 130,000 people crossed it on foot. In 2022, about 250,000. And in 2023, more than 520,000.", [
                cnt_steps([('2021', '130,000+'), ('2022', '250,000'), ('2023', '520,000+')], size=170, color='#ff5a5f'),
                {'type': 'crowd', 'lat': 6.2, 'lon': -76.2, 'count': 52, 'cols': 13, 'size': 30, 'at': '2021', 'counts': [{'at': '2021', 'n': 13}, {'at': '2022', 'n': 25}, {'at': '2023', 'n': 52}], 'red': [{'at': '2023', 'n': 52}]},
                hl(GAP_PAN, '#ff5a5f', '2021', fillOpacity=0.3)],
              cam=at_(7.9, -77.4, 12, duration=1.0),
              src=[src('Crossings: more than 130,000 in 2021, about 250,000 in 2022, more than 520,000 in 2023.', DG, 'In 2023, more than 520,000 individuals passed through the gap'),
                   src('The 2021 and 2022 crossings.', DG, 'more than 130,000')]),
            S("The shortest gap on the road, and the most dangerous.", [
                clip('emoji_skull', 'dangerous', 8.4, -77.3, size=200)],
              cam=at_(10, -80, 1.3, duration=1.6), style='dark', no_claim=True),
            S("And that is the answer to the biggest question about this road:", [],
              cam=at_(HW_N[0][0], HW_N[0][1], 3.4, duration=1.8, loopIntro=True), no_claim=True),
        ],
        keywords={'darién': '#4ade80', 'gap': '#4ade80', 'panama': '#5ec8ff', 'colombia': '#ffd60a', '520,000': '#ff5a5f', 'venomous': '#ff5a5f'},
        captions={'theme': 'box'}, v2=True)

# =========================================================================================== CHIMBORAZO
if want('chimborazo'):
    CH = (-1.469, -78.817)
    EV = (27.988, 86.925)
    save('chimborazo', meta(
        'The Mountain Closest to Space Is NOT Everest 🏔️🚀🤯',
        "Everest 🇳🇵 is the highest mountain above sea level at 8,849 m, but it's not the point closest to space! 🚀 Earth isn't a perfect ball: it's thicker at the equator. Chimborazo in Ecuador 🇪🇨 is only 6,263 m high, but it sits just one degree south of the equator, on top of that bulge. Its summit is 6,384.4 km from Earth's center, about 2.1 km farther out than Everest's 🤯",
        ["The closest point to space is in Ecuador, not Nepal 🤯🇪🇨", "Did you know Earth is fatter at the equator? 👇", "Which record should we explain next? 🗺️"],
        ['chimborazo', 'everest', 'ecuador', 'highest mountain', 'closest to space', 'equatorial bulge', 'earth', 'andes', 'geography', 'maps', 'learn']),
        [
            S("Is Everest really the closest point on Earth to space?", [
                hook('CLOSEST POINT TO *SPACE*?', at=0.05, until='Earth'), ping(*EV, 'Everest', color='#ffd60a'), dot('Everest', *EV, 'Everest', dy=84),
                hl('NPL', 'flag:np', 'Everest', fillOpacity=0.6), arrow((20, 86.9), (26.6, 86.9), 'space', color='#ffd60a', width=10)],
              cam=at_(25, 80, 1.6), no_claim=True),
            S("No! That title belongs to Chimborazo, a volcano in Ecuador, which is only 6,263 meters high.", [
                ping(*CH, 'Chimborazo', color='#ff5a5f'), hl('ECU', 'flag:ec', 'Ecuador', fillOpacity=0.85), cnt('6,263 m', '6,263', size=170),
                dot('Quito', -0.18, -78.47, 'Ecuador', dy=-60, size=34)],
              cam=at_(-1.5, -78.8, 6.5),
              src=[src('Chimborazo is 6,263 m high.', 'Chimborazo', 'With an elevation of 6,263 m (20,548 ft), Chimborazo is the highest mountain in Ecuador')]),
            S("It's a glacier-covered volcano, and it last erupted around the year 550 AD.", [
                ping(*CH, 'volcano', color='#ff5a5f'),
                clip('emoji_volcano', 'erupted', *CH, size=240, dy=-175), cnt('~550 AD', '550', size=150),
                ],
              cam=at_(-1.5, -78.8, 7),
              src=[src('Chimborazo is a stratovolcano; the summit is covered by glaciers; last eruption around 550 AD.', 'Chimborazo',
                       'a dominantly andesitic-dacitic stratovolcano ... the last time around 550 AD ± 150 years')]),
            S("In 1802, Alexander von Humboldt climbed it to 5,875 meters, higher than any European ever had.", [
                year(1802, '1802'), cnt('5,875 m', '5,875', size=150), ping(*CH, 'Humboldt', color='#ff5a5f'),
                char('scientist', 'Humboldt', screen=(0.78, 0.6), size=290, name='Alexander von Humboldt'), lab('HIGHER THAN ANY EUROPEAN', -2.6, -78.8, 'European', style='map', size=40), ],
              cam=at_(-1.5, -78.8, 11, bearing=-3), tr='film',
              src=[src('In 1802 Humboldt reached 5,875 m, higher than any European in recorded history.', 'Chimborazo', 'they reached a point at 5,875 m, higher than previously attained by any European in recorded history')]),
            S("Everest is more than two and a half kilometers taller, so how can Chimborazo be closer to space?", [
                bars([('Everest', 8849, '8,849 m', '#ffd60a', 'np'), ('Chimborazo', 6263, '6,263 m', '#ff5a5f', 'ec')], 'taller', orient='v', shape='mountain', height=380), q(0, -60, 'how')],
              style='neon', cam=at_(0, -60, 1.0),
              src=[src('Chimborazo is 2,585 m lower than Everest above sea level.', 'Chimborazo', 'Despite being 2,585 m (8,481 ft) lower in elevation above sea level, it is 6,384.4 km')]),
            S("Because Earth isn't a perfect ball. It's thicker at the equator, like it's wearing a belt.", [
                route([(0, -180), (0, -90), (0, 0), (0, 90), (0, 180)], 'equator', rhumb=True, color='#ffd60a', width=10, drawDur=1.4), slam('EQUATOR', 6, -40, 'equator', size=70),
                ],
              cam=at_(10, -60, 1.0),
              src=[src('Earth is thicker at the equator than pole to pole.', 'Chimborazo', 'the Earth is thicker at the Equator than it is from pole to pole')]),
            S("And Chimborazo sits just one degree south of the equator, right on top of that bulge.", [
                route([(0, -90), (0, -68)], 'equator', rhumb=True, color='#ffd60a', width=8, drawDur=0.6), meas((0, -78.8), CH, '1°', 'degree', countUp=False), hl('ECU', 'flag:ec', 'Chimborazo', fillOpacity=0.55), ping(*CH, 'Chimborazo', color='#ff5a5f')],
              cam=at_(-0.5, -78.8, 5),
              src=[src('It lies one degree south of the equator.', 'Chimborazo', 'Chimborazo is one degree south of the Equator')]),
            S("Its summit is 6,384.4 kilometers from the center of the Earth.", [
                ping(*CH, 'summit', color='#ff5a5f'), cnt('6,384.4 km', '6,384.4', size=150), hl('ECU', 'flag:ec', 'summit', fillOpacity=0.55), beam(*CH, 'center'), ellipse(*CH, 'center', rx=170, ry=170)],
              cam=at_(-1.5, -78.8, 6, then=[{'at': 'center', 'lat': -1.5, 'lon': -78.8, 'zoom': 9, 'duration': 1.5}]),
              src=[src("Its summit is 6,384.4 km from Earth's center.", 'Chimborazo', "it is 6,384.4 km (3,967.1 mi) from the Earth's center")]),
            S("In fact, its summit is widely reported to be the farthest point on Earth's surface from the center of the planet.", [
                lab('FARTHEST FROM THE CENTER', 3.4, -74.2, 'farthest', style='map', size=44), ping(*CH, 'summit', color='#ff5a5f'), beam(*CH, 'farthest'), ring(*CH, 'surface', r=80)],
              cam=at_(-1.5, -78.8, 3.0),
              src=[src("Chimborazo's summit is widely reported to be the farthest point on the surface from Earth's center.", 'Chimborazo',
                       "the summit of Chimborazo is widely reported to be the farthest point on the surface from Earth's center")]),
            S("That's about 2.1 kilometers farther out than the top of Everest, so Chimborazo wins.", [
                ping(*CH, "That's", color='#ff5a5f'), dot('Chimborazo', *CH, "That's", dy=60), cnt('+2.1 km', '2.1', size=170, color='#ff5a5f'),
                ],
              cam=at_(0, -78.8, 2.2),
              src=[src("About 2.1 km farther than Everest's summit.", 'Chimborazo', "it is 6,384.4 km (3,967.1 mi) from the Earth's center, 2.1 km (1.3 mi) farther than")]),
            S("So the next time someone asks:", [],
              cam=at_(25, 80, 1.6, duration=1.6, loopIntro=True), no_claim=True),
        ],
        keywords={'chimborazo': '#ff5a5f', 'everest': '#ffd60a', 'equator': '#ffd60a', 'space': '#2de2e6'},
        style='globe', captions={'theme': 'impact'}, v2=True)
