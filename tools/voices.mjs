// Lists English Edge neural voices: npm run voices
import { listVoices } from '../src/tts.mjs';

const voices = await listVoices(process.argv[2] || 'en-');
for (const v of voices) console.log(`${v.ShortName.padEnd(36)} ${v.Gender.padEnd(7)} ${v.Locale}`);
