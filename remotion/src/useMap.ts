import { useEffect, useRef, useState } from 'react';
import { continueRender, delayRender } from 'remotion';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

/** One MapLibre map per composition. Deterministic: no interaction, no fade; every frame waits until the map is idle. */
export function useMap(style: any, opts: Partial<maplibregl.MapOptions> = {}) {
  const ref = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<maplibregl.Map | null>(null);
  const [handle] = useState(() => delayRender('map load'));
  useEffect(() => {
    const m = new maplibregl.Map({ container: ref.current!, style, interactive: false, fadeDuration: 0, attributionControl: false, ...opts } as any);
    m.on('error', (e) => console.warn('MAPERR', String((e as any)?.error?.message || e)));
    m.on('load', () => { m.resize(); setMap(m); continueRender(handle); });
    return () => m.remove();
  }, []);
  return { ref, map };
}

/** Run `apply` (set camera / paint props) for the current frame, then wait for the map to settle. */
export function useFrameSync(map: maplibregl.Map | null, apply: (m: maplibregl.Map) => void, deps: any[]) {
  useEffect(() => {
    if (!map) return;
    const h = delayRender('map frame');
    apply(map);
    const done = () => continueRender(h);
    if (map.loaded() && !map.isMoving()) map.once('idle', done); else map.once('idle', done);
    map.triggerRepaint();
  }, deps);
}
