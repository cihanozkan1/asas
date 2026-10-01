import React from 'react';
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import * as turf from '@turf/turf';
import { useMap, useFrameSync } from './useMap';

export type ArmyArrowProps = { points: [number, number][]; color: string; zoom: number; follow: boolean; width: number };

/** Growing army / migration arrow: Turf bezierSpline smooths the route, lineSliceAlong grows it over time, along() puts the arrow head and the follow-camera on the tip. */
export const ArmyArrow: React.FC<ArmyArrowProps> = ({ points, color, zoom, follow, width }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const full: any = turf.bezierSpline(turf.lineString(points), { resolution: 10000, sharpness: 0.6 });
  const len = turf.length(full);
  const style: any = {
    version: 8,
    sources: { line: { type: 'geojson', data: turf.lineString(points.slice(0, 2)) }, head: { type: 'geojson', data: turf.featureCollection([]) } },
    layers: [
      { id: 'glow', type: 'line', source: 'line', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': color, 'line-width': width * 3, 'line-blur': width * 2, 'line-opacity': 0.45 } },
      { id: 'core', type: 'line', source: 'line', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': color, 'line-width': width } },
      { id: 'head', type: 'fill', source: 'head', paint: { 'fill-color': color } },
    ],
  };
  const { ref, map } = useMap(style, { center: points[0], zoom, canvasContextAttributes: { preserveDrawingBuffer: true } } as any);
  useFrameSync(map, (m) => {
    const p = Easing.inOut(Easing.cubic)(interpolate(frame, [0, durationInFrames - 8], [0, 1], { extrapolateRight: 'clamp' }));
    const d = Math.max(0.001, p * len);
    const sliced = turf.lineSliceAlong(full, 0, d);
    (m.getSource('line') as any).setData(sliced);
    const tip = turf.along(full, d).geometry.coordinates;
    const back = turf.along(full, Math.max(0, d - len * 0.01)).geometry.coordinates;
    const brg = turf.bearing(back, tip);
    // arrow head triangle (size follows the line width in km at this zoom)
    const k = (width * 40000) / (512 * Math.pow(2, zoom));
    const a = turf.destination(tip, k * 2, brg, { units: 'kilometers' }).geometry.coordinates;
    const l = turf.destination(tip, k, brg - 90, { units: 'kilometers' }).geometry.coordinates;
    const r = turf.destination(tip, k, brg + 90, { units: 'kilometers' }).geometry.coordinates;
    (m.getSource('head') as any).setData(turf.polygon([[a, l, r, a]]));
    if (follow) m.jumpTo({ center: tip as [number, number], zoom });
  }, [map, frame]);
  return <AbsoluteFill><div ref={ref} style={{ width: 1080, height: 1920 }} /></AbsoluteFill>;
};
