import React from 'react';
import { Composition } from 'remotion';
import { EmojiPop } from './EmojiPop';
import { LottieBurst } from './LottieBurst';
import { GlowBorder } from './GlowBorder';
import { ArmyArrow } from './ArmyArrow';
import { TripsDemo } from './TripsDemo';
import { GlobeArcs } from './GlobeArcs';
import { GifLayer } from './GifLayer';

const W = 1080, H = 1920, FPS = 30;
const C = (id: string, component: any, frames: number, props: any, w = W, h = H) => <Composition id={id} component={component} durationInFrames={frames} fps={FPS} width={w} height={h} defaultProps={props} />;

export const Root: React.FC = () => (
  <>
    {C('EmojiPop', EmojiPop, 75, { emoji: 'collision', size: 700, x: 540, y: 900, start: 2 })}
    {C('LottieBurst', LottieBurst, 45, { file: 'burst.json', size: 900, x: 540, y: 900 })}
    {C('GlowBorder', GlowBorder, 90, { country: '792', color: '#ffd60a', fill: 0.25, pad: 120 })}
    {C('ArmyArrow', ArmyArrow, 120, { points: [[28.9, 41.0], [26.5, 40.2], [24.0, 38.5], [22.5, 36.0], [20.0, 33.5]], color: '#ff3b3b', zoom: 5, follow: true, width: 16 })}
    {C('TripsDemo', TripsDemo, 150, {
      center: [20, 41], zoom: 4, trail: 60, fps: FPS,
      trips: [
        { path: [[28.9, 41.0], [26.5, 40.2], [24.0, 38.5], [22.5, 37.0]], timestamps: [0, 40, 80, 120], color: [255, 60, 60] },
        { path: [[12.5, 41.9], [15.0, 40.5], [18.0, 39.5], [22.0, 37.5]], timestamps: [10, 50, 90, 130], color: [90, 200, 255] },
      ],
      arcs: [{ from: [28.9, 41.0], to: [12.5, 41.9], color: [255, 214, 10] }],
    })}
    {C('GlobeArcs', GlobeArcs, 120, {
      arcs: [{ startLat: 41, startLng: 29, endLat: 38.9, endLng: -77, color: '#ffd60a' }, { startLat: 41, startLng: 29, endLat: 35.7, endLng: 139.7, color: '#ff3b3b' }],
      rings: [{ lat: 41, lng: 29 }], lat: 30, lng: 20, altitude: 2.2,
    })}
    {C('GifLayer', GifLayer, 60, { file: 'test_collision.gif', size: 600, x: 540, y: 900, useGif: false })}
  </>
);
