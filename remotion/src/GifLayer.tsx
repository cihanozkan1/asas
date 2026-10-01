import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { AnimatedImage } from 'remotion';
import { Gif } from '@remotion/gif';

export type GifLayerProps = { file: string; size: number; x: number; y: number; useGif: boolean };

/** GIF / APNG / WebP / AVIF overlay locked to the timeline: <AnimatedImage> (Chrome) or <Gif> (Safari-safe). File in public/. */
export const GifLayer: React.FC<GifLayerProps> = ({ file, size, x, y, useGif }) => (
  <AbsoluteFill>
    <div style={{ position: 'absolute', left: x - size / 2, top: y - size / 2, width: size, height: size }}>
      {useGif ? <Gif src={staticFile(file)} width={size} height={size} /> : <AnimatedImage src={staticFile(file)} width={size} height={size} />}
    </div>
  </AbsoluteFill>
);
