from helpers import *

MN = {'admin1': 'Minnesota', 'country': 'USA'}
MB = {'admin1': 'Manitoba', 'country': 'CAN'}
ANGLE = (49.34, -95.07)

# ------------------------------------------------------------------ NORTHWEST ANGLE
save('northwest_angle', meta(
    "Why This Piece of the USA Is Only Reachable Through Canada 🇺🇸🇨🇦🤯 Northwest Angle",
    "The Northwest Angle in Minnesota 🇺🇸 is the only place in the contiguous United States north of the 49th parallel, and you can only drive there through Canada 🇨🇦 Why? In 1783 the negotiators of the Treaty of Paris, including Benjamin Franklin, used John Mitchell's map, which got the Mississippi River and the Lake of the Woods wrong 🗺️ The treaty sent the border to the lake's northwesternmost point and then west to the Mississippi, but the river actually starts further south at Lake Itasca. Later treaties fixed the rest of the border, and this little corner stayed American. Only 149 people live there today 🤯",
    ["A piece of the USA you can only drive to through Canada 🤯🇺🇸🇨🇦", "Would you live in the Northwest Angle? 🎣👇", "Which weird border should we explain next? 🗺️"],
    ['northwest angle', 'minnesota', 'lake of the woods', 'canada', 'usa', 'border', '49th parallel', 'treaty of paris', 'benjamin franklin', 'map mistake', 'weird borders', 'geography', 'maps', 'learn']),
    [
        S("This tiny piece of Minnesota is the only place in the lower 48 states that sits north of the 49th parallel.", [
            hl(MN, '#1d4ed8', 'Minnesota', fillOpacity=0.35, hold=1), route([(49, -97.5), (49, -93)], '49th', rhumb=True, color='#ffd60a', width=6, dashed=True, dash=[16, 12], drawDur=1.0, hold=1),
            ping(*ANGLE, 'tiny', color='#ffd60a', hold=1), slam('NORTHWEST ANGLE', 49.55, -95.1, 'tiny', size=64)],
          cam=at_(49.1, -95.2, 26, bearing=-3),
          src=[src('The only place in the contiguous US north of the 49th parallel.', 'Northwest_Angle', 'the only place in the contiguous United States north of the 49th parallel')]),
        S("And if you want to drive there, you have to go through Canada.", [
            hl(MB, '#d52b1e', 'Canada', fillOpacity=0.4), flag('ca', 49.6, -95.9, 'Canada', size=90), mover_icon([(48.905, -95.314), (48.99, -95.55), (49.2, -95.62), (49.33, -95.35), ANGLE], 'drive', '🚗', size=90),
            dot('Warroad', 48.905, -95.314, 'drive', dy=46, size=40)],
          src=[src('It can be reached by land only through Canada, or across Lake of the Woods.', 'Northwest_Angle', 'accessible only through Canada or by crossing Lake of the Woods')]),
        S("So how did this happen? A map mistake from 1783.", [
            q(ANGLE[0], ANGLE[1], 'how'), year(1783, '1783'), stamp('MAP MISTAKE', 'mistake', size=84)],
          cam=at_(48, -95, 7), style='vintage', era='history',
          src=[src('It stems from a 1783 mapping mistake.', 'Northwest_Angle', "The region's existence stems from a 1783 mapping mistake.")]),
        S("The negotiators of the Treaty of Paris, including Benjamin Franklin, used a map that got the Mississippi River and this lake wrong.", [
            hl({'hist': 1783, 'name': 'United States of America'}, '#b08968', 0.05, fillOpacity=0.45), hl({'hist': 1783, 'names': ['Quebec', "Rupert's Land"]}, '#c9a27e', 0.05, fillOpacity=0.3), lab('USA', 46.6, -96.8, 0.05, style='serif', size=58), lab('BRITISH', 50.2, -96.8, 0.05, style='serif', size=50), char('franklin', 'Benjamin', name='Benjamin Franklin'),
            
            route([(47.24, -95.21), (47.45, -94.9), (47.3, -94.2), (46.4, -94.3), (45.6, -94.2), (44.98, -93.27)], 'Mississippi', color='#5ec8ff', width=7, drawDur=1.2, hold=2),
            lab('Lake of the Woods', 49.45, -94.3, 'lake', style='serif', size=48)],
          cam=at_(47.8, -94.8, 6), era='history', tr='film',
          src=[src("Negotiators incl. Benjamin Franklin relied on John Mitchell's inaccurate map.", 'Northwest_Angle',
                   "Negotiators of the Canada-U.S. border, including Benjamin Franklin, relied on John Mitchell's colonial map, which contained critical inaccuracies.")]),
        S("The treaty said the border runs to the lake's northwesternmost point, and then west to the Mississippi.", [
            hl({'hist': 1783, 'name': 'United States of America'}, '#b08968', 0.05, fillOpacity=0.45), hl({'hist': 1783, 'names': ['Quebec', "Rupert's Land"]}, '#c9a27e', 0.05, fillOpacity=0.3), lab('USA', 46.6, -96.8, 0.05, style='serif', size=58), lab('BRITISH', 50.2, -96.8, 0.05, style='serif', size=50),
            route([(48.7, -93.5), (49.2, -94.5), (49.38, -95.15)], 'northwesternmost', color='#c1121f', width=7, drawDur=1.2, hold=1),
            ping(49.38, -95.15, 'point', color='#c1121f'), arrow((49.38, -95.3), (49.38, -97.5), 'west', color='#c1121f')],
          era='history',
          src=[src('The treaty set the boundary through the lake to its "northwesternmost point," then westward to the Mississippi.', 'Northwest_Angle',
                   'The Treaty of Paris consequently set the boundary to run through the lake to its "northwesternmost point," then westward to the Mississippi.')]),
        S("But the Mississippi actually starts far to the south, at Lake Itasca. The line could never reach it.", [
            hl({'hist': 1783, 'name': 'United States of America'}, '#b08968', 0.05, fillOpacity=0.45), hl({'hist': 1783, 'names': ['Quebec', "Rupert's Land"]}, '#c9a27e', 0.05, fillOpacity=0.3), lab('USA', 46.6, -96.8, 0.05, style='serif', size=58), lab('BRITISH', 50.2, -96.8, 0.05, style='serif', size=50), ping(47.24, -95.21, 'Itasca', color='#5ec8ff'), dot('Lake Itasca', 47.24, -95.21, 'Itasca', dy=48),
            arrow((49.2, -97.3), (47.5, -95.5), 'south', color='#5ec8ff'), note('???', 48.3, -96.4, 'never', size=80)],
          cam=at_(48.0, -95.3, 6), era='history',
          src=[src("The Mississippi's actual source, Lake Itasca, lies south of Lake of the Woods.", 'Northwest_Angle',
                   "the river's actual source—Lake Itasca—lies south of Lake of the Woods, not northwest")]),
        S("Later treaties fixed the rest of the border, but this little corner stayed American.", [
            route([(49, -97.5), (49, -95.15), (49.38, -95.15)], 'fixed', rhumb=True, color='#ffd60a', width=7, drawDur=1.0),
            hl(MN, 'flag:us', 'American', fillOpacity=0.7), ping(*ANGLE, 'corner', color='#ffd60a')],
          cam=at_(49.1, -95.3, 18),
          src=[src('Later treaties (Jay Treaty, Treaty of Ghent, 1818 Convention, Webster–Ashburton) clarified the boundary.', 'Northwest_Angle',
                   'Subsequent treaties (Jay Treaty, Treaty of Ghent, Anglo-American Convention of 1818, and Webster-Ashburton Treaty) gradually clarified the boundary, cementing the Angle\'s unusual status.')]),
        S("Even getting in is unusual. There's a single gravel road, and you check in with US Customs using a kiosk.", [
            mover_icon([(48.905, -95.314), (48.99, -95.55), (49.2, -95.62), (49.33, -95.35), ANGLE], 'gravel', 'art:car', size=90, id='gr', nodes=True, drawDur=2.6),
            art('laptop', 49.34, -95.03, 'kiosk', size=120), dot('Customs kiosk', 49.34, -95.03, 'kiosk', dy=-62, size=34)],
          cam={'follow': 'gr', 'zoom': 40, 'zoomTo': 26, 'duration': 0.9},
          src=[src('Travelers use the single gravel road and an iPad kiosk to contact US Customs.', 'Northwest_Angle',
                   "Travelers using the single gravel road into the Angle are instructed to use an iPad kiosk at Jim's Corner, Young's Bay Marina, or Carlson's Landing to contact U.S. Customs.")]),
        S("In 1997, because of fishing rules, some residents even suggested leaving the United States and joining Canada.", [
            year(1997, '1997', light=True), art('fishing_boat', 49.22, -94.85, 'fishing', size=150), flag('ca', 49.62, -95.0, 'joining', size=110, wave=True),
            arrow((49.36, -95.08), (49.62, -95.0), 'leaving', color='#ffd60a'), react('art:emote_shock', (0.79, 0.3), 'suggested', size=160)],
          cam=at_(49.35, -95.1, 34, bearing=-3),
          src=[src('In 1997, some residents suggested leaving the US and joining Canada because of fishing laws.', 'Northwest_Angle',
                   'Because of laws restricting fishing, some residents of the Northwest Angle suggested leaving the United States and joining Canada in 1997.')]),
        S("Today, only 149 people live there, and about 79 percent of the area is water.", [
            hl(MN, '#1d4ed8', 0.05, fillOpacity=0.4), ping(*ANGLE, 0.05, color='#ffd60a'), cnt('149', '149', size=200), pill('people (2020)', '149'), icon('🎣', 49.25, -94.85, 'water', size=110)],
          cam=at_(*ANGLE, 40, bearing=-4), tr='flash',
          src=[src('149 residents in 2020; about 79% water.', 'Northwest_Angle', 'With just 149 residents as of the 2020 census ... though about 79% is water')]),
    ],
    keywords={'minnesota': '#5ec8ff', 'canada': '#ff5a5f', 'mississippi': '#5ec8ff', 'franklin': '#ffd60a', 'american': '#5ec8ff'},
    imagery=[{'bbox': [-95.9, 48.7, -94.5, 49.6], 'width': 3072}])

# ------------------------------------------------------------------ POINT ROBERTS
PR = (48.975, -123.06)
# the real road: north out of Point Roberts through Tsawwassen, around the top of Boundary Bay
# (Hwy 17 / Hwy 99 through Delta and Surrey) and south to the Peace Arch crossing into Blaine
PR_ROAD = [(48.975, -123.06), (49.002, -123.068), (49.04, -123.07), (49.085, -123.04), (49.115, -122.97),
           (49.11, -122.88), (49.06, -122.80), (49.03, -122.775), (49.002, -122.757), (48.993, -122.75)]
PRB = {'box': [-123.1, 48.955, -123.0, 49.0]}
PRW = 'Point_Roberts,_Washington'
BLAINE = (48.993, -122.75)
save('point_roberts', meta(
    "The US Town You Can Only Drive to Through Canada 🇺🇸🇨🇦🤯 Point Roberts",
    "Point Roberts 🇺🇸 is a piece of Washington State on the tip of a Canadian peninsula south of Vancouver 🇨🇦 To reach the rest of the USA by land you have to drive about 40 km through Canada 🚗 Why? The 1846 Oregon Treaty set the US–Canada border at the 49th parallel, and the line cut straight across the tip of the Tsawwassen peninsula 📏 About 1,191 people live there, older kids cross the border four times on every school trip, and when the border closed in 2020 the town lost about 80% of its business 🤯",
    ["Kids here cross an international border 4 times to go to school 🤯🚌", "Would you live in Point Roberts? 👇", "Which weird border should we explain next? 🗺️"],
    ['point roberts', 'washington', 'canada', 'usa', 'border', '49th parallel', 'oregon treaty', 'vancouver', 'exclave', 'weird borders', 'geography', 'maps', 'learn']),
    [
        S("This little town is in the USA, but you can only drive there through Canada. Otherwise, you need a boat or a plane.", [
            trace(PRB, '#1d4ed8', 'town', neon='#6aa5ff', fillOpacity=0.5), ping(*PR, 'town', color='#ffd60a', hold=1), flag('us', 48.972, -123.03, 'USA', pin=True, size=110, wave=True),
            hl('CAN', '#d52b1e', 'Canada', fillOpacity=0.35), flag('ca', 49.06, -122.96, 'Canada', size=100, wave=True)],
          cam=at_(49.0, -123.0, 120, bearing=-3),
          src=[src('Point Roberts is a US pene-exclave reachable by land only through Canada (or by boat/plane).', PRW, 'a pene-exclave of the US state of Washington ... "25 mi (40 km) through Canada, or without passing through Canada by boat or private airplane."')]),
        S("It's Point Roberts, on the tip of a Canadian peninsula just south of Vancouver.", [
            giant('POINT ROBERTS', 48.945, -123.06, 'Point', size=70), dot('Vancouver', 49.25, -123.1, 'Vancouver', dy=-46), pathtext('Tsawwassen peninsula', [(49.02, -123.13), (49.05, -123.07), (49.09, -123.03)], 'peninsula', size=40)],
          cam=at_(49.08, -123.05, 60),
          src=[src('On the southern tip of the Tsawwassen peninsula, south of Vancouver.', PRW, 'on the southernmost tip of the Tsawwassen peninsula, south of Vancouver, British Columbia, Canada')]),
        S("It was named in 1792 by the explorer George Vancouver, after his friend Henry Roberts.", [
            year(1792, '1792', light=True),
            rider_ship([(49.3, -124.1), (49.12, -123.5), (49.0, -123.16), (48.985, -123.09)], 'explorer', 'sea', 'british_officer', (48.984, -123.055), style='caravel', emblem='#c1121f', drawDur=2.6, rider_size=115),
            react('art:emote_cool', (0.76, 0.3), 'Henry', size=170)],
          era='history', tr='film', cam=at_(49.06, -123.3, 26),
          src=[src('Point Roberts was named by George Vancouver after his friend Henry Roberts (1792 expedition).', PRW, 'Point Roberts acquired its present name from George Vancouver, who named it after his friend Henry Roberts')]),
        S("So why is it American?", [q(PR[0], PR[1], 'why'), react('art:emote_think', (0.3, 0.32), 'why', size=170)], cam=at_(49.0, -123.0, 90), style='dark', no_claim=True, tr='flash'),
        S("In 1846, the Oregon Treaty set the border between the US and British Canada along the 49th parallel.", [
            year(1846, '1846'), route([(49, -125), (49, -120)], '49th', rhumb=True, color='#ffd60a', width=7, drawDur=1.3, hold=1, laser=True),
            lab('BRITISH', 49.5, -122.0, 'British', style='serif', size=56), lab('UNITED STATES', 48.5, -122.0, 'US', style='serif', size=52)],
          cam=at_(49.0, -122.5, 12), era='history', tr='film',
          src=[src('The 1846 Oregon Treaty fixed the boundary at the 49th parallel.', PRW, 'the 1846 Oregon Treaty, which established "the 49th parallel would define the boundary between their respective territories"')]),
        S("But this perfectly straight line cut right across the peninsula, leaving its tip on the American side.", [
            route([(49.0, -123.3), (49.0, -122.8)], 'line', rhumb=True, color='#ffd60a', width=7, drawDur=0.8, laser=True),
            lab('CANADA', 49.03, -123.07, 'perfectly', style='pill', bg='#d52b1e', size=46), lab('USA', 48.975, -123.06, 'tip', style='pill', bg='#1d4ed8', size=46),
            trace(PRB, '#1d4ed8', 'tip', neon='#6aa5ff', fillOpacity=0.5)],
          cam=at_(49.0, -123.05, 140), tr='flash',
          src=[src('The 49th parallel left the southern peninsula tip on the US side.', PRW, 'leaving this southern peninsula on the American side')]),
        S("To reach the rest of the USA by land, you drive about 40 kilometers through Canada.", [
            route(PR_ROAD, 'drive', color='#ffffff', width=5, dashed=True, dash=[14, 12], glow=False, id='road', mover={'kind': 'icon', 'icon': 'art:car', 'size': 90}, nodes=True, drawDur=3.6),
            dot('Blaine, USA', *BLAINE, 'Canada', dy=50, dx=-110), cnt('40 km', '40', size=160)],
          cam={'follow': 'road', 'zoom': 60, 'zoomTo': 24, 'duration': 1.0},
          src=[src('Residents travel about 25 mi (40 km) through Canada.', PRW, 'traveling "25 mi (40 km) through Canada, or without passing through Canada by boat or private airplane."')]),
        S("Older kids go to school in Blaine, so they cross the border four times on every round trip.", [
            route(PR_ROAD, 'school', color='#ffffff', width=5, dashed=True, dash=[14, 12], glow=False, id='bus', mover={'kind': 'icon', 'icon': 'art:bus', 'size': 100}, nodes=True, drawDur=2.6),
            cnt_steps([('school', '1'), ('cross', '2'), ('four', '4')], size=200), react('art:emote_sweat', (0.76, 0.28), 'four', size=160)],
          cam={'follow': 'bus', 'zoom': 40, 'zoomTo': 24, 'duration': 0.9},
          src=[src('Students in grade 4 and above commute to Blaine, crossing the border four times.', PRW,
                   'Students attending grades 4 and above must commute to Blaine, Washington. This journey requires them to "cross the US–Canada border four times, two on the trip to Blaine and two on the trip back."')]),
        S("In March 2020, the border closed to non-essential travel, and the town lost about eighty percent of its business.", [
            year('2020', 'March', light=True), handstamp('BORDER CLOSED', 'closed', size=92, screen=[0.5, 0.36]), grade('cold', 'March', until=5.5),
            cnt('-80%', 'eighty', size=200, color='#ff5a5f'), react('art:emote_cry', (0.78, 0.3), 'lost', size=170)],
          cam=at_(48.99, -123.05, 100, bearing=3), tr='flash',
          src=[src('The border closed to non-essential travel in March 2020; Point Roberts lost 80 percent of its business.', PRW,
                   'In 2020, a study found that Point Roberts had lost 80 percent of its business and hundreds of seasonal residents as a result of the pandemic and border shutdown.')]),
        S("So a temporary passenger ferry carried people from Point Roberts to Blaine, over the water.", [
            route([(48.985, -123.06), (48.965, -123.0), (48.945, -122.92), (48.96, -122.84), (48.985, -122.775)], 'ferry', color='#ffffff', width=5, dashed=True, dash=[14, 12], glow=False, id='ferry', mover={'kind': 'ship', 'size': 170, 'style': 'ferry'}, drawDur=3.0),
            dot('Blaine', 48.99, -122.77, 'Blaine', dy=50, dx=-50)],
          cam={'follow': 'ferry', 'zoom': 50, 'zoomTo': 28, 'duration': 1.0},
          src=[src('A temporary passenger ferry ran from Point Roberts to Blaine.', PRW, 'A temporary passenger ferry service from Point Roberts to Blaine operated by the Port of Bellingham')]),
        S("Today, Canadians drive in for cheaper American gas, alcohol and food.", [
            scatter(PRB, 'art:beer_glass', 'alcohol', count=3, size=120, stagger=0.25), scatter(PRB, 'art:oil_barrel', 'gas', count=3, size=110, stagger=0.25),
            flag('ca', 49.02, -123.0, 'Canadians', size=110, wave=True)],
          cam=at_(48.98, -123.05, 110),
          src=[src('Canadians visit Point Roberts for cheaper American gasoline, alcohol and food.', PRW, 'Canadians visit for cheaper American gasoline, alcohol, and food when the Canadian dollar is strong')]),
        S("Forty times more Canadians have mailboxes in Point Roberts than the number of residents.", [
            {'type': 'crowd', 'lat': 48.985, 'lon': -123.065, 'count': 40, 'cols': 10, 'size': 30, 'color': '#ffffff', 'red': [{'at': 'Canadians', 'n': 40}], 'redColor': '#e11d2e', 'at': 'Forty'},
            cnt('40x', 'Forty', size=190, color='#ff5a5f')],
          cam=at_(48.985, -123.05, 130),
          src=[src('Forty times more Canadians have mailboxes in Point Roberts than there are residents.', PRW, 'Forty times more Canadians have mailboxes in Point Roberts than the number of residents')]),
        S("Today, about 1,191 people live in this American island on land.", [
            trace(PRB, '#1d4ed8', 0.05, neon='#6aa5ff', fillOpacity=0.5), lab('POINT ROBERTS', 48.99, -123.06, 0.05, style='map', size=54),
            cnt('1,191', '1,191', size=180), pill('people (2020)', '1,191'), ping(*PR, 'American', color='#ffd60a')],
          cam=at_(48.99, -123.05, 150, bearing=-4), tr='flash',
          src=[src('Population 1,191 (2020 census).', PRW, 'The 2020 census recorded 1,191 residents across 4.884 square miles of territory.')]),
    ],
    keywords={'canada': '#ff5a5f', 'usa': '#5ec8ff', 'american': '#5ec8ff', 'blaine': '#ffd60a', 'vancouver': '#ffd60a'},
    imagery=[{'bbox': [-123.35, 48.85, -122.6, 49.35], 'width': 4096}])

# ------------------------------------------------------------------ AUSTRALIA
AUS = 'AUS'
CITIES = [('Sydney', -33.87, 151.21), ('Melbourne', -37.81, 144.96), ('Brisbane', -27.47, 153.03), ('Perth', -31.95, 115.86), ('Adelaide', -34.93, 138.6)]
save('australia', meta(
    'Why Almost Nobody Lives in the Middle of Australia 🇦🇺🤯',
    "Australia 🇦🇺 is a giant continent, but almost 80% of Australians live within 25 km of the coast 🏖️ Why? 80% of the land gets less than 600 mm of rain a year and half gets less than 300 mm 🏜️ The Great Dividing Range runs almost 4,000 km along the east coast, and the interior, the Outback, is desert and semi-desert. That's why Australia has only about 3.5 people per km², with 27 million people living mostly on the edges 🤯",
    ["80% of Australians live near the coast 🤯🇦🇺", "Aussies: coast or Outback, where do you live? 👇", "Which country's population map next? 🗺️"],
    ['australia', 'outback', 'population', 'desert', 'great dividing range', 'sydney', 'melbourne', 'coast', 'geography', 'maps', 'learn']),
    [
        S("Australia is a giant continent. But almost 80 percent of Australians live within 25 kilometers of the coast.", [
            hl(AUS, 'flag:au', 'Australia', hold=0), cnt('80%', '80', size=190), pill('live near the coast', 'coast'),
            *[ping(la, lo, 'coast', color='#ffd60a') for _, la, lo in CITIES]],
          cam=at_(-26, 134, 2.7, bearing=-3),
          src=[src('Almost 80% of Australians live within 25 km of the coast.', 'Geography_of_Australia', 'Almost 80% of the Australian population live within 25 km (16 mi) of the coast')]),
        S("It's the sixth largest country in the world, with about 7.7 million square kilometers of land.", [
            hl(AUS, 'flag:au', 0.05, fillOpacity=0.85), cnt('#6', 'sixth', size=200), pill('7.7M km²', 'million', bg='#0f766e')],
          cam=at_(-26, 134, 2.7, bearing=3),
          src=[src('Sixth-largest country by land area: 7,688,287 km².', 'Geography_of_Australia',
                   'making it the sixth-largest country in the world by land area of jurisdiction, which comprises 7,688,287 km2')]),
        S("The big cities are all on the edges: Sydney, Melbourne, Brisbane, Perth and Adelaide.", [
            *[dot(n, la, lo, n, dy=-46, size=40) for n, la, lo in CITIES], blob(AUS, '#2a2b2f', '#ffd60a', 0.05, softness=4, fillOpacity=0.0)],
          style='dark', cam=at_(-26, 134, 2.7),
          src=[src('73% live in major coastal urban centres.', 'Geography_of_Australia', 'with 73% inhabiting major coastal urban centers')]),
        S("So why is the middle almost empty?", [q(-25, 134, 'why'), hl(AUS, '#e76f51', 0.05, fillOpacity=0.85)], cam=at_(-26, 134, 2.7), style='dark', no_claim=True),
        S("Water. 80 percent of the land gets less than 600 millimeters of rain a year, and half gets less than 300.", [
            hl({'admin1s': ['Northern Territory', 'South Australia', 'Western Australia'], 'country': 'AUS'}, '#c2703d', 'rain', fillOpacity=0.55), lab('OUTBACK', -24, 131, 'rain', style='map', size=64), cnt_steps([('80', '80%'), ('half', '50%')], size=180),
            pill('< 600 mm rain', 'rain', bg='#b45309')],
          cam=at_(-26, 134, 2.7),
          src=[src('80% of the land gets <600 mm of rain a year, 50% gets <300 mm.', 'Geography_of_Australia',
                   '80% of the land area receives less than 600 mm (24 in) of annual rainfall and 50% less than 300 mm (12 in)')]),
        S("That makes Australia the driest inhabited continent on Earth. Even its lowest point, the bed of Lake Eyre, is just 15 meters below sea level.", [
            ping(-28.4, 137.35, 'lowest', color='#ffd60a'), dot('Lake Eyre', -28.4, 137.35, 'Lake', dy=-50, size=38), cnt('-15 m', '15', size=170, color='#ff9f1c'),
            art('sun', -24.5, 129.5, 'driest', size=150), react('art:emote_sweat', (0.79, 0.3), 'driest', size=160)],
          cam=at_(-27.5, 135.5, 4.5),
          src=[src('Australia is the driest inhabited continent.', 'Geography_of_Australia', 'As Australia is the driest inhabited continent, such droughts can limit the streamflow'),
               src("The country's lowest point is on the bed of Lake Eyre, 15 m below sea level.", 'Geography_of_Australia', "the country's lowest point is found on the bed of the Lake Eyre (15 m (49 ft) below sea level)")]),
        S("The Great Dividing Range runs almost 4,000 kilometers along the east coast, separating the rainy coast from the dry interior.", [
            route([(-11, 142.5), (-17, 145.3), (-23, 148), (-28, 152), (-33, 150.3), (-37, 148.5)], 'Great', color='#c8a46e', width=14, drawDur=1.6),
            slam('GREAT DIVIDING RANGE', -30, 150, 'Range', size=44, rotate=-3), cnt('4,000 km', '4,000', size=150)],
          cam=at_(-26, 146, 1.9),
          src=[src('The Great Dividing Range runs almost 4,000 km parallel to the east coast, separating coastal rainfall from interior dryness.', 'Geography_of_Australia',
                   'runs parallel to the east coast from the tip of the Cape York Peninsula in Queensland almost 4,000 km (2,500 mi) south')]),
        S("And the heart of the country, the Outback, is desert and semi-desert, with very few people.", [
            slam('OUTBACK', -25, 133, 'Outback', size=110), icon('🐪', -23, 128, 'desert', size=120), icon('☀️', -21, 137, 'semi-desert', size=120)],
          cam=at_(-26, 134, 2.7, bearing=3),
          src=[src('The Outback is sparsely populated and semi-arid/desert.', 'Geography_of_Australia', 'sparsely populated and characterised by semi-arid and desert landscapes')]),
        S("That's why Australia has only about 3.5 people per square kilometer.", [
            cnt('3.5', '3.5', size=210), pill('people per km²', 'people'), punch('only')],
          src=[src('Mean population density 3.5/km² (2024).', 'Geography_of_Australia', 'a mean population density of 3.5/km2 (9.1/sq mi) as of 2024')]),
        S("27 million people, living mostly on the edges of a huge, dry continent.", [
            cnt('27M', '27', size=200), blob(AUS, '#b45309', '#ffd60a', 'edges', softness=6, fillOpacity=0.35),
            *[ping(la, lo, 'edges', color='#ffd60a') for _, la, lo in CITIES]],
          cam=at_(-26, 134, 2.7, bearing=-3), tr='flash',
          src=[src('Total population 27.2 million.', 'Geography_of_Australia', 'its substantial total population of 27.2 million')]),
    ],
    keywords={'australia': '#ffd60a', 'australians': '#ffd60a', 'outback': '#f4a261', 'coast': '#5ec8ff', 'water': '#5ec8ff'})

# ------------------------------------------------------------------ BOLIVIA
BOL = 'BOL'
ANTO = {'admin1': 'Antofagasta', 'country': 'CHL'}
TITI = (-15.9, -69.35)
save('bolivia_navy', meta(
    'Why Bolivia Has a Navy but No Sea 🇧🇴🤯 The Lost Coast',
    "Bolivia 🇧🇴 is landlocked, yet it has a navy of about 5,000 personnel ⚓ patrolling Lake Titicaca and rivers. Why? Bolivia used to have a Pacific coast 🌊 In 1879 a tax dispute with a Chilean mining company started the War of the Pacific 🇨🇱 Chile defeated Bolivia and Peru, Bolivia lost its coastal Litoral Department, and Peru lost Tarapacá. Every 23 March Bolivia still marks the Day of the Sea, keeping hope of a coast alive 🤯",
    ["A navy with no sea 🤯🇧🇴⚓", "Should Bolivia get its coast back? 👇", "Which lost territory should we explain next? 🗺️"],
    ['bolivia', 'bolivian navy', 'lake titicaca', 'landlocked', 'chile', 'peru', 'war of the pacific', 'day of the sea', 'south america', 'history', 'geography', 'maps', 'learn']),
    [
        S("Bolivia is completely landlocked, with no coast at all. And yet, it has a navy, with about 5,000 personnel.", [
            hl(BOL, 'flag:bo', 'Bolivia'), cnt('5,000', '5,000', size=190), icon('⚓', -17, -62, 'navy', size=150), note('NO SEA?!', -12, -66, 'coast', size=66)],
          cam=fit(BOL, pad=0.9, bearing=-3),
          src=[src('Bolivia is landlocked but has a navy of about 5,000 personnel (2018).', 'Bolivian_Navy', 'As of 2018, the force comprised "approximately 5,000 personnel."')]),
        S("It patrols Lake Titicaca, the highest navigable lake in the world, and the rivers of the Amazon.", [
            ping(*TITI, 'Titicaca', color='#5ec8ff'), dot('Lake Titicaca', *TITI, 'Titicaca', dy=-120), mover_icon([(-16.40, -68.72), (-16.22, -68.84), (-16.05, -69.2), (-15.85, -69.4)], 'patrols', 'art:speedboat', size=75)],
          cam=at_(-16.0, -69.3, 14),
          src=[src('It operates on Lake Titicaca, the highest navigable lake, and Amazon tributaries.', 'Bolivian_Navy', 'Lake Titicaca, described as "the highest navigable lake in the world," and patrols Amazon tributaries')]),
        S("So why does a landlocked country need a navy?", [q(-17, -65, 'why')], cam=fit(BOL, pad=0.9), style='dark', no_claim=True),
        S("Because until the 1880s, Bolivia had its own coast on the Pacific Ocean, right here.", [
            hl({'hist': 1880, 'name': 'Bolivia'}, 'flag:bo', 0.05), ping(-23.65, -70.4, 'coast', color='#ffd60a')],
          cam=fit(BOL, ANTO, pad=0.9), era='history', tr='film',
          src=[src('Bolivia ceded its coastal Litoral Department to Chile.', 'War_of_the_Pacific', 'Bolivia ceded its coastal Litoral Department to Chile, making it landlocked')]),
        S("In 1879, Bolivia raised a tax on a Chilean mining company, breaking an earlier treaty, and it started the War of the Pacific.", [
            year(1879, '1879'), hl(ANTO, 'flag:bo', 'Bolivia', fillOpacity=0.75), icon('⛏️', -23.0, -69.5, 'mining', size=120), stamp('10¢ TAX', 'tax', size=90), shake('War')],
          era='history',
          src=[src("Bolivia's 10 cents per quintal tax on the Chilean company CSFA triggered the war (1879–1884).", 'War_of_the_Pacific',
                   'Bolivia imposed a controversial "10 cents per quintal tax" on the Chilean mining company CSFA, violating the 1874 boundary treaty ... 1 March 1879 – 4 April 1884')]),
        S("Peru fought alongside Bolivia, but after five years of war, Chile won.", [
            hl({'hist': 1880, 'name': 'Peru'}, 'flag:pe', 'Peru', fillOpacity=0.8), hl({'hist': 1880, 'name': 'Chile'}, 'flag:cl', 'Chile', fillOpacity=0.8),
            char('soldier_chile', 'Chile', name='Chile'), char('soldier_bolivia', 'Bolivia', screen=(0.74, 0.6), name='Bolivia', flip=True)],
          cam=at_(-20, -68, 2.6), era='history',
          src=[src('Chile fought an alliance of Bolivia and Peru and emerged victorious.', 'War_of_the_Pacific', 'between Chile against an alliance of Bolivia and Peru ... Chile emerged victorious')]),
        S("Bolivia lost its entire coastline, and Peru lost the Tarapacá region.", [
            hl(ANTO, '#c1121f', 'Bolivia'), hl({'admin1': 'Tarapacá', 'country': 'CHL'}, '#c1121f', 'Tarapacá'),
            lab('Tarapacá', -20.2, -69.3, 'Tarapacá', style='serif', size=52), note('LANDLOCKED', -16, -63, 'coastline', size=64)],
          cam=fit(BOL, ANTO, pad=0.9), era='history',
          src=[src('Peru ceded Tarapacá; Bolivia lost its coast (confirmed by the 1904 treaty).', 'War_of_the_Pacific', '"Peru formally cedes the Tarapacá Department to Chile" ... In 1904, Chile and Bolivia signed the Treaty of Peace and Friendship')]),
        S("Bolivia even took Chile to the International Court of Justice. But in 2018, the judges ruled that Chile has no obligation to negotiate a sea access for Bolivia.", [
            year(2018, '2018', light=True), art('gavel', -23.65, -70.4, 'judges', size=150), handstamp('NO DEAL', 'ruled', size=90, screen=[0.5, 0.34]),
            flag('bo', -17, -64, 'Bolivia', size=110, wave=True), flag('cl', -23.0, -70.3, 'Chile', size=100, wave=True)],
          cam=fit(BOL, ANTO, pad=0.9), tr='flash',
          src=[src('On 1 October 2018 the ICJ ruled Chile had no obligation to negotiate sovereign access to the Pacific for Bolivia.', 'Obligation_to_Negotiate_Access_to_the_Pacific_Ocean',
                   'On 1 October 2018, a twelve-judge majority ruled that Chile did not have an obligation to negotiate with Bolivia towards an access to the Pacific Ocean')]),
        S("But Bolivia never gave up. Its navy partly exists to keep the dream of the sea alive, and every March 23, the country celebrates the Day of the Sea.", [
            cnt('23 March', 'March', size=150), pill('Día del Mar', 'Sea', bg='#1d4ed8'), icon('🌊', -22, -72, 'Sea', size=130), hl(BOL, 'flag:bo', 0.05)],
          cam=fit(BOL, ANTO, pad=0.9, bearing=-3), tr='flash',
          src=[src('Bolivia marks Día del Mar every 23 March; the navy partly exists to keep hopes of a coast alive.', 'Bolivian_Navy', 'Bolivia commemorates its lost coast annually through "Día del Mar" (Day of the Sea) on March 23 ... the navy exists partly to preserve maritime consciousness and keep hopes of coastal recovery alive')]),
    ],
    keywords={'bolivia': '#4ade80', 'chile': '#ff5a5f', 'peru': '#ff5a5f', 'navy': '#5ec8ff', 'sea': '#5ec8ff', 'titicaca': '#5ec8ff'})

# ------------------------------------------------------------------ PANAMA
NY, SF = (40.55, -73.95), (37.75, -122.6)
AROUND = [NY, (30, -68), (10, -45), (-10, -33), (-30, -45), (-45, -60), (-56.3, -67.3), (-50, -78), (-30, -76), (-10, -82), (10, -95), (25, -113), SF]
CANAL = [NY, (28, -74), (19, -75.5), (12, -79), (9.36, -79.92), (8.9, -79.53), (7.5, -80.5), (12, -92), (25, -113), SF]
save('panama_canal', meta(
    'How the Panama Canal Saves Ships 13,000 km 🇵🇦🚢🤯',
    "Before 1914, a ship going from New York to San Francisco had to sail all the way around South America, about 22,500 km 🌎 Then the Panama Canal opened, cutting through this thin strip of land and shrinking the trip to about 9,500 km 🚢 The canal is just 82 km long, and locks lift ships 26 meters up to Gatun Lake and back down again ⬆️⬇️ Around 14,000 ships pass through every year. The US ran it for decades, but in 1999 Panama took control 🇵🇦🤯",
    ["82 km of canal saves ships 13,000 km 🤯🚢", "Would you rather sail around Cape Horn or through Panama? 👇", "Which canal should we explain next? 🗺️"],
    ['panama canal', 'panama', 'cape horn', 'ships', 'shipping', 'gatun lake', 'locks', 'new york', 'san francisco', 'geography', 'history', 'maps', 'learn']),
    [
        S("Before 1914, a ship sailing from New York to San Francisco had to go all the way around South America, past Cape Horn at the very bottom.", [
            ship(AROUND, 'sailing', 'horn', drawDur=8.0, hold=1, style='steamer'), dot('New York', *NY, 'New', dy=-46), dot('San Francisco', *SF, 'San', dy=-50, dx=-40)],
          cam={'follow': 'horn', 'zoom': 1.6, 'zoomTo': 0.95},
          src=[src('Around Cape Horn the voyage is about 22,500 km.', 'Panama_Canal', 'Instead of traveling approximately 22,500 kilometers around South America\'s Cape Horn')]),
        S("That's about 22,500 kilometers.", [cnt('22,500 km', '22,500', size=170), ping(-56.3, -67.3, 'about', color='#ff3b3b'), dot('Cape Horn', -56.3, -67.3, 'kilometers', dy=46)],
          cam=at_(0, -80, 0.8),
          src=[src('About 22,500 km around Cape Horn.', 'Panama_Canal', 'approximately 22,500 kilometers around South America\'s Cape Horn')]),
        S("Then in 1914, the Panama Canal opened, cutting right through this thin strip of land.", [
            year(1914, '1914', light=True), hl('PAN', 'flag:pa', 'Panama', hold=1), ping(9.1, -79.7, 'cutting', color='#ffd60a')],
          cam=at_(9.0, -79.7, 12, bearing=-3), tr='flash',
          src=[src('Formally opened on 15 August 1914.', 'Panama_Canal', 'was formally opened on 15 August 1914')]),
        S("It's only 82 kilometers long.", [meas((9.36, -79.92), (8.9, -79.53), '82 km', '82'), route([(9.36, -79.92), (9.2, -79.87), (9.05, -79.7), (8.9, -79.53)], 'long', color='#5ec8ff', width=9, drawDur=1.2)],
          cam=at_(9.13, -79.72, 45),
          src=[src('The canal is 82 km long.', 'Panama_Canal', 'The Panama Canal spans "82 kilometers (51 miles)"')]),
        S("Giant locks lift ships 26 meters up to Gatun Lake, a man-made lake created by damming a river, and then lower them back down on the other side.", [
            cnt('26 m', '26', size=190), ping(9.2, -79.9, 'Gatun', color='#5ec8ff'), dot('Gatun Lake', 9.2, -79.9, 'Gatun', dy=-48),
            art('canal_lock', 9.272, -79.921, 'lift', size=150), art('canal_lock', 9.017, -79.593, 'lower', size=150), arrow((9.22, -80.05), (9.32, -80.05), 'lift', color='#4ade80'), arrow((8.98, -79.45), (8.9, -79.45), 'lower', color='#ff5a5f')],
          cam=at_(9.13, -79.75, 50),
          src=[src('Ships are raised 26 m to Gatun Lake (an artificial lake made by damming the Chagres River) and lowered at the other end.', 'Panama_Canal', 'Vessels are raised 26 meters to Gatun Lake, an artificial freshwater body created by damming the Chagres River. The locks then lower ships at the opposite end.')]),
        S("The United States spent almost 500 million dollars building it, and about 5,600 workers died from disease and accidents.", [
            cnt_steps([('500', '$500M'), ('5,600', '5,600')], size=170), art('banknotes', 9.35, -79.78, 'spent', size=140), art('skull', 9.0, -79.6, 'died', size=130)],
          cam=at_(9.1, -79.75, 40, bearing=-3), style='dark',
          src=[src('The US spent almost $500 million on construction.', 'Panama_Canal', 'The United States spent almost $500 million (roughly equivalent to $16.1 billion in 2025).'),
               src('About 5,600 workers died from disease and accidents during US construction.', 'Panama_Canal', 'about 5,600 workers died from disease and accidents during the US construction phase')]),
        S("Now the New York to San Francisco trip is only about 9,500 kilometers.", [
            ship(CANAL, 'trip', 'canalroute', emblem='#1d4ed8', drawDur=3.0, style='cargo'), cnt_steps([('trip', '22,500 km'), ('9,500', '9,500 km')], size=160)],
          cam={'follow': 'canalroute', 'zoom': 1.2, 'zoomTo': 0.95},
          src=[src('Through the canal the voyage is roughly 9,500 km.', 'Panama_Canal', 'ships now transit roughly 9,500 kilometers through the canal')]),
        S("Around 14,000 ships pass through every year, and by 2012, more than 815,000 ships had used it.", [cnt_steps([('14,000', '14,000'), ('815,000', '815,000')], size=190), pill('ships per year', 'ships', until='2012'), pill('ships by 2012', '815,000', bg='#0f766e'), scatter({'circle': {'lat': 9.1, 'lon': -79.7, 'km': 60}}, '🚢', 'pass', count=4, size=70, stagger=0.15, along=[(9.36, -79.92), (9.2, -79.83), (9.05, -79.66), (8.9, -79.53)])],
          cam=at_(9.1, -79.7, 16),
          src=[src('About 14,702 transits a year; over 815,000 by 2012.', 'Panama_Canal', 'The canal handles approximately 14,702 vessel transits yearly, with over 815,000 ships having passed through by 2012')]),
        S("And in 2016, a third, wider lane of locks began operating.", [
            art('canal_lock', 9.272, -79.921, 'third', size=170), art('canal_lock', 9.017, -79.593, 'wider', size=170), year(2016, '2016', light=True)],
          cam=at_(9.13, -79.75, 45),
          src=[src('A third, wider lane of locks was built 2007–2016 and began commercial operation on 26 June 2016.', 'Panama_Canal',
                   'A third, wider lane of locks was constructed between September 2007 and May 2016. The expanded waterway began commercial operation on 26 June 2016.')]),
        S("The United States ran the canal for most of the century, but in 1999, Panama finally took control.", [
            year(1999, '1999', light=True), hl({'geojson': 'canal_zone.geojson'}, 'flag:us', 'United', until='Panama'), lab('CANAL ZONE', 9.35, -79.5, 'United', style='pill', bg='#1d4ed8', size=44, until='Panama', fixed=True), hl('PAN', 'flag:pa', 'Panama')],
          cam=at_(9.1, -79.7, 55, bearing=-3),
          src=[src('Panama took control in 1999 under the Torrijos–Carter Treaties.', 'Panama_Canal', 'the Panamanian government took control in 1999 following the Torrijos–Carter Treaties of 1977')]),
    ],
    keywords={'panama': '#ff5a5f', 'canal': '#5ec8ff', 'ships': '#5ec8ff', 'america': '#ffd60a'},
    )
