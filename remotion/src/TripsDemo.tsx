import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { TripsLayer } from '@deck.gl/geo-layers';
import { ArcLayer } from '@deck.gl/layers';
import { useMap, useFrameSync } from './useMap';

export type Trip = { path: [number, number][]; timestamps: number[]; color: [number, number, number] };
export type TripsDemoProps = { trips: Trip[]; arcs: { from: [number, number]; to: [number, number]; color: [number, number, number] }[]; center: [number, number]; zoom: number; trail: number; fps: number };

/** Several armies / ships at once: deck.gl TripsLayer (glowing fading trails) + ArcLayer (curved links) over a transparent MapLibre map. currentTime is the Remotion frame. */
export const TripsDemo: React.FC<TripsDemoProps> = ({ trips, arcs, center, zoom, trail }) => {
  const frame = useCurrentFrame();
  const style: any = { version: 8, sources: {}, layers: [] };
  const { ref, map } = useMap(style, { center, zoom, canvasContextAttributes: { preserveDrawingBuffer: true } } as any);
  const overlay = React.useRef<any>(null);
  useFrameSync(map, (m) => {
    if (!overlay.current) { overlay.current = new MapboxOverlay({ interleaved: false, layers: [] } as any); m.addControl(overlay.current); }
    overlay.current.setProps({
      layers: [
        new TripsLayer({ id: 'trips', data: trips, getPath: (d: Trip) => d.path, getTimestamps: (d: Trip) => d.timestamps, getColor: (d: Trip) => d.color, widthMinPixels: 10, capRounded: true, jointRounded: true, trailLength: trail, currentTime: frame }),
        new ArcLayer({ id: 'arcs', data: arcs, getSourcePosition: (d: any) => d.from, getTargetPosition: (d: any) => d.to, getSourceColor: (d: any) => d.color, getTargetColor: [255, 255, 255], getWidth: 4, greatCircle: true }),
      ],
    });
  }, [map, frame]);
  return <AbsoluteFill><div ref={ref} style={{ width: 1080, height: 1920 }} /></AbsoluteFill>;
};
