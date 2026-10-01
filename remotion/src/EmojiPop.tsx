import React from 'react';
import { AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { AnimatedEmoji, type EmojiName } from '@remotion/animated-emoji';

export type EmojiPopProps = { emoji: string; size: number; x: number; y: number; start: number };

/** Noto animated emoji (💥🔥🌋 ...) popped in at a screen position. Use map.project([lon,lat]) to get x,y from a coordinate. */
export const EmojiPop: React.FC<EmojiPopProps> = ({ emoji, size, x, y, start }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - start, fps, config: { damping: 12 } });
  return (
    <AbsoluteFill>
      <div style={{ position: 'absolute', left: x - size / 2, top: y - size / 2, width: size, height: size, transform: `scale(${s})`, opacity: interpolate(frame - start, [0, 3], [0, 1], { extrapolateRight: 'clamp' }) }}>
        <AnimatedEmoji emoji={emoji as EmojiName} scale="1" calculateSrc={({ emoji: e }) => staticFile(`animated-emoji/${e}-1x.webm`)} style={{ width: size, height: size }} />
      </div>
    </AbsoluteFill>
  );
};
