import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { feature } from 'topojson-client';
import * as turf from '@turf/turf';
// @ts-ignore
import world from 'world-atlas/countries-50m.json';
import { useMap, useFrameSync } from './useMap';

export type GlowBorderProps = { country: string; color: string; fill: number; pad: number };

/** Glowing country border on a transparent MapLibre map: 3 stacked layers (soft wide halo, mid halo, sharp core) + translucent fill. country = ISO numeric id ("792") or name. */
export const GlowBorder: React.FC<GlowBorderProps> = ({ country, color, fill, pad }) => {
  const frame = useCurrentFrame();
  const fc: any = feature(world as any, (world as any).objects.countries);
  const f = fc.features.find((x: any) => String(x.id) === country || x.properties.name?.toLowerCase() === country.toLowerCase());
  const style: any = {
    version: 8,
    sources: { c: { type: 'geojson', data: f } },
    layers: [
      { id: 'fill', type: 'fill', source: 'c', paint: { 'fill-color': color, 'fill-opacity': fill } },
      { id: 'halo2', type: 'line', source: 'c', paint: { 'line-color': color, 'line-width': 34, 'line-blur': 28, 'line-opacity': 0.35 } },
      { id: 'halo1', type: 'line', source: 'c', paint: { 'line-color': color, 'line-width': 14, 'line-blur': 10, 'line-opacity': 0.7 } },
      { id: 'core', type: 'line', source: 'c', paint: { 'line-color': '#ffffff', 'line-width': 3.5, 'line-opacity': 1 } },
    ],
  };
  const bb = turf.bbox(f) as [number, number, number, number];
  const { ref, map } = useMap(style, { bounds: bb, fitBoundsOptions: { padding: pad, animate: false }, canvasContextAttributes: { preserveDrawingBuffer: true } } as any);
  useFrameSync(map, (m) => {
    m.fitBounds(bb, { padding: pad, animate: false, maxZoom: 12 });
    const pulse = 1 + 0.18 * Math.sin(frame / 6);
    m.setPaintProperty('halo2', 'line-width', 34 * pulse);
    m.setPaintProperty('halo1', 'line-opacity', interpolate(pulse, [0.82, 1.18], [0.5, 0.85]));
  }, [map, frame]);
  return <AbsoluteFill><div ref={ref} style={{ width: 1080, height: 1920 }} /></AbsoluteFill>;
};
