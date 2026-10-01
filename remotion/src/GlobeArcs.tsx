import React, { useEffect, useRef, useState } from 'react';
import { AbsoluteFill, continueRender, delayRender, useCurrentFrame } from 'remotion';
import Globe from 'react-globe.gl';
import { feature } from 'topojson-client';
// @ts-ignore
import world from 'world-atlas/countries-110m.json';

export type GlobeArcsProps = { arcs: { startLat: number; startLng: number; endLat: number; endLng: number; color: string }[]; rings: { lat: number; lng: number }[]; lat: number; lng: number; altitude: number };

/** three.js globe (globe.gl): flying arcs + pulse rings, camera aimed per frame. Transparent background. */
export const GlobeArcs: React.FC<GlobeArcsProps> = ({ arcs, rings, lat, lng, altitude }) => {
  const frame = useCurrentFrame();
  const ref = useRef<any>(null);
  const [handle] = useState(() => delayRender('globe'));
  useEffect(() => { const t = setTimeout(() => continueRender(handle), 1500); return () => clearTimeout(t); }, []);
  useEffect(() => { ref.current?.pointOfView({ lat, lng: lng + frame * 0.2, altitude }, 0); }, [frame]);
  return (
    <AbsoluteFill>
      <Globe ref={ref} width={1080} height={1920} backgroundColor="rgba(0,0,0,0)" showGlobe={false} showAtmosphere={false} polygonsData={(feature(world as any, (world as any).objects.countries) as any).features} polygonCapColor={() => "rgba(120,200,255,0.18)"} polygonSideColor={() => "rgba(0,0,0,0)"} polygonStrokeColor={() => "rgba(255,255,255,0.7)"} polygonAltitude={0.004} atmosphereColor="#5ec8ff"
        arcsData={arcs} arcColor="color" arcDashLength={0.4} arcDashGap={1} arcDashInitialGap={(d: any) => 1 - ((frame / 45) % 1)} arcDashAnimateTime={0} arcStroke={0.6}
        ringsData={rings} ringColor={() => '#ffd60a'} ringMaxRadius={6} ringPropagationSpeed={3} ringRepeatPeriod={900} />
    </AbsoluteFill>
  );
};
