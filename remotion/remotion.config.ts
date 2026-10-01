import { Config } from '@remotion/cli/config';
// Deterministic WebGL map rendering (rules from remotion-dev/maplibre-example): angle (software ANGLE/SwiftShader, gives WebGL2 on a GPU-less server), one tab at a time, PNG frames.
Config.setChromiumOpenGlRenderer('angle');
Config.setConcurrency(1);
Config.setVideoImageFormat('png');
Config.setOverwriteOutput(true);
