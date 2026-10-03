"""Test bench for the round-9 toolbox: one short scene per technique (video id _lab9, never published)."""
from helpers import *

save('_lab9', meta('lab', 'lab', ['a', 'b', 'c'], ['lab']), [
    S("Texas is big, and about twenty three of them would fit here.", [clone('USA', (0, -150), 'twenty', label='x23', color='#ffd60a')], cam=at_(10, -120, 1.4), no_claim=True),
    S("Sound reaches four hundred kilometers from the coast.", [wave(25, -90, 400, 0.3, color='#5ec8ff')], cam=at_(25, -90, 6), no_claim=True),
    S("The water creeps twenty kilometers inland along the coast.", [flood('NLD', 25, 52.3, 5.0, 0.3)], cam=at_(52.3, 5.0, 40), no_claim=True),
    S("Sixty meters below the sea, a tunnel carries a train.", [section(0.1, structure={'kind': 'tunnel', 'y': 0.76}, ref={'kind': 'tower', 'x': 0.5, 'base': 0.58, 'h': 0.16, 'label': 'Eiffel'}, dims=[{'x': 0.12, 'y0': 0.42, 'y1': 0.76, 'label': '60 m'}], coastLabels=['EUROPE', 'ASIA'])], cam=at_(41, 29, 20), no_claim=True),
    S("The poles are flatter than the equator.", [radii(0.1, radii=[{'angle': 90, 'label': '6,357 km', 'color': '#4ea1ff'}, {'angle': 0, 'label': '6,378 km', 'color': '#ff5a5f'}], marks=[{'angle': 25, 'label': 'Chimborazo'}])], cam=at_(0, -78, 3), no_claim=True),
    S("The crowd took to the streets in protest.", [protest(0.1, count=14), reason(1, 'Geography', 0.2, screen=[0.5, 0.18])], cam=at_(40.7, -74, 40), no_claim=True),
    S("Cars cannot cross, so it is no entry for vehicles.", [ban('art:car', 0.3, lat=8.2, lon=-77.5, size=200), banner('us', 8.4, -77.0, 0.5), retext('Holland', 'Netherlands', 0.4, screen=[0.5, 0.3])], cam=at_(8.2, -77.4, 10), no_claim=True),
    S("A swarm of flies, cut out of paper.", [swarm(0.1), hl('PAN', '#f97316', 0.1, cut=True)], cam=at_(8.5, -80, 8), no_claim=True, tr='curl'),
], v2=True)
