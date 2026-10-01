import React, { useEffect, useState } from 'react';
import { AbsoluteFill, continueRender, delayRender, staticFile } from 'remotion';
import { Lottie, type LottieAnimationData } from '@remotion/lottie';

export type LottieBurstProps = { file: string; size: number; x: number; y: number };

/** Any Lottie JSON from public/lottie/ (LottieFiles Simple License files, After Effects exports) locked to the Remotion timeline. */
export const LottieBurst: React.FC<LottieBurstProps> = ({ file, size, x, y }) => {
  const [data, setData] = useState<LottieAnimationData | null>(null);
  const [handle] = useState(() => delayRender('lottie'));
  useEffect(() => {
    fetch(staticFile('lottie/' + file)).then((r) => r.json()).then((j) => { setData(j); continueRender(handle); });
  }, [file]);
  if (!data) return null;
  return (
    <AbsoluteFill>
      <div style={{ position: 'absolute', left: x - size / 2, top: y - size / 2, width: size, height: size }}>
        <Lottie animationData={data} style={{ width: size, height: size }} />
      </div>
    </AbsoluteFill>
  );
};
