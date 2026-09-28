// Hand-built SVG sprites (original artwork, no licences needed):
//  - portrait characters: bust-length, realistic proportions, shaded, in a framed
//    medallion like the channel's avatar cards. Eyes/mouth are in named groups so
//    the renderer can animate blinking and talking.
//  - sailing ships

const INK = '#1f1612';

export const CHARACTER_PRESETS = {
  pope: { skin: 'light', age: 'old', hair: 'short', hairColor: '#d8d8d8', hat: 'mitre', outfit: 'pope', bg: ['#7a1322', '#2a0509'], eyes: '#5b4a3a' },
  king: { skin: 'light', hair: 'wavy', hairColor: '#5a3a22', beard: 'full', hat: 'crown', outfit: 'royal', outfitColor: '#9e1b2b', bg: ['#3a2a6a', '#120a26'], eyes: '#4a6a8a' },
  queen: { skin: 'light', hair: 'long', hairColor: '#6b3e1e', hat: 'crown', outfit: 'royal', outfitColor: '#4b2a86', bg: ['#6a2a4a', '#20081a'], eyes: '#3f6a4a', female: true },
  explorer: { skin: 'tan', hair: 'short', hairColor: '#2e2016', beard: 'full', hat: 'beret', hatColor: '#1c1c1c', outfit: 'doublet', outfitColor: '#20304f', bg: ['#1d4a6b', '#07131f'], eyes: '#3b2a1c' },
  navigator: { skin: 'light', age: 'old', hair: 'long', hairColor: '#cfcac2', hat: 'beret', hatColor: '#7d1420', outfit: 'doublet', outfitColor: '#7d1420', bg: ['#6b4a1d', '#1f1407'], eyes: '#4a5a6a' },
  soldier: { skin: 'tan', hair: 'short', hairColor: '#2e2016', beard: 'goatee', hat: 'morion', outfit: 'armor', bg: ['#4a3a20', '#140e05'], eyes: '#3b2a1c' },
  sailor: { skin: 'tan', hair: 'short', hairColor: '#4a3020', beard: 'stubble', hat: 'bandana', hatColor: '#b3261e', outfit: 'shirt', outfitColor: '#e9e2d0', bg: ['#1d5a7a', '#061a26'], eyes: '#3b2a1c' },
  canadian: { skin: 'light', hair: 'short', hairColor: '#7a4a24', beard: 'full', hat: 'toque', hatColor: '#c8102e', outfit: 'plaid', outfitColor: '#b3121f', bg: ['#1f5a3a', '#07170f'], eyes: '#3f6a8a' },
  pharaoh: { skin: 'brown', hair: 'none', beard: 'pharaoh', hat: 'nemes', outfit: 'pharaoh', bg: ['#1f3f7a', '#081226'], eyes: '#2a1a10', eyeliner: true },
  farmer: { skin: 'brown', hair: 'short', hairColor: '#1a1410', beard: 'mustache', hat: 'turban', hatColor: '#f1ece0', outfit: 'galabeya', outfitColor: '#4f7fb5', bg: ['#b5782a', '#3a2008'], eyes: '#2a1a10' },
  engineer: { skin: 'brown', hair: 'short', hairColor: '#15100c', beard: 'stubble', hat: 'hardhat', hatColor: '#ffc21a', outfit: 'hivis', outfitColor: '#ff7a00', bg: ['#2f4f6f', '#0b1622'], eyes: '#2a1a10' },
  diplomat: { skin: 'light', age: 'old', hair: 'short', hairColor: '#9a9a9a', beard: 'mustache', hat: 'tophat', outfit: 'suit', outfitColor: '#20242c', bg: ['#4a4a4a', '#111111'], eyes: '#4a5a6a' },
};

const SKINS = {
  light: { base: '#f1c7a5', shade: '#d99e7c', deep: '#b97a5c', lip: '#c9716a', blush: '#f19a8c' },
  tan: { base: '#dca47a', shade: '#bd8058', deep: '#94593a', lip: '#a95a4c', blush: '#d97c66' },
  brown: { base: '#a9714b', shade: '#8a5634', deep: '#653a21', lip: '#7d3f2f', blush: '#b8664a' },
  dark: { base: '#7a4a2e', shade: '#5f361f', deep: '#442312', lip: '#5a2a1f', blush: '#8f4a34' },
};

let uid = 0;

// ------------------------------------------------------------------ parts

function face(c, S, id) {
  const hairCol = c.hairColor || '#3a2a1c';
  const brow = c.hair === 'none' ? '#2a1a10' : c.age === 'old' ? '#bdbdbd' : hairCol;
  const irisCol = c.eyes || '#4a3a2a';
  const lashW = c.female ? 3.4 : 2.6;
  const eye = (cx, flip) => {
    const d = flip ? -1 : 1;
    return `
      <path d="M${cx - 15} 158 Q${cx - 2 * d} ${147} ${cx + 15} 157 Q${cx + 2 * d} 166 ${cx - 15} 158Z" fill="#fbf7f2"/>
      <g clip-path="url(#eye${id}${flip ? 'r' : 'l'})">
        <circle cx="${cx + d}" cy="158" r="7" fill="${irisCol}"/>
        <circle cx="${cx + d}" cy="158" r="7" fill="url(#iris${id})"/>
        <circle cx="${cx + d}" cy="158" r="3.2" fill="#120c08"/>
        <circle cx="${cx - 2 + d}" cy="155.5" r="1.9" fill="#fff"/>
        <path d="M${cx - 16} 150 Q${cx} 146 ${cx + 16} 150 L${cx + 16} 156 Q${cx} 151 ${cx - 16} 156Z" fill="rgba(0,0,0,.18)"/>
      </g>
      <path d="M${cx - 16} 158.5 Q${cx - 2 * d} 145.5 ${cx + 16} 157" fill="none" stroke="${INK}" stroke-width="${lashW}" stroke-linecap="round"/>
      <path d="M${cx - 12} 163 Q${cx} 166.5 ${cx + 12} 162.5" fill="none" stroke="${S.deep}" stroke-width="1.1" opacity=".6"/>
      ${c.age === 'old' ? `<path d="M${cx + 14 * d} 163 l${6 * d} 3 M${cx + 14 * d} 159 l${7 * d} 0" stroke="${S.deep}" stroke-width="1" opacity=".55"/>` : ''}
      ${c.eyeliner ? `<path d="M${cx + 15 * d} 157 L${cx + 26 * d} 153" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>` : ''}`;
  };
  return `
  <defs>
    <clipPath id="eye${id}l"><path d="M109 158 Q122 147 139 157 Q126 166 109 158Z"/></clipPath>
    <clipPath id="eye${id}r"><path d="M161 157 Q178 147 191 158 Q174 166 161 157Z"/></clipPath>
    <radialGradient id="iris${id}" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>
    <radialGradient id="skinhi${id}" cx=".42" cy=".38" r=".68"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="${S.deep}" stop-opacity=".35"/></radialGradient>
  </defs>
  <!-- ears -->
  <g>
    <path d="M90 148 C76 144 74 176 92 184 Z" fill="${S.base}"/><path d="M88 156 C82 158 83 170 90 174" fill="none" stroke="${S.deep}" stroke-width="2" opacity=".6"/>
    <path d="M210 148 C224 144 226 176 208 184 Z" fill="${S.base}"/><path d="M212 156 C218 158 217 170 210 174" fill="none" stroke="${S.deep}" stroke-width="2" opacity=".6"/>
  </g>
  <!-- head -->
  <path d="M150 80 C190 80 212 106 212 148 C212 176 206 198 194 214 C182 230 166 238 150 238 C134 238 118 230 106 214 C94 198 88 176 88 148 C88 106 110 80 150 80Z" fill="${S.base}"/>
  <path d="M150 80 C190 80 212 106 212 148 C212 176 206 198 194 214 C182 230 166 238 150 238 C134 238 118 230 106 214 C94 198 88 176 88 148 C88 106 110 80 150 80Z" fill="url(#skinhi${id})"/>
  <path d="M100 200 C112 226 132 236 150 236 C168 236 188 226 200 200 C190 222 170 232 150 232 C130 232 110 222 100 200Z" fill="${S.shade}" opacity=".55"/>
  <ellipse cx="118" cy="186" rx="14" ry="8" fill="${S.blush}" opacity="${c.female ? 0.45 : 0.25}"/>
  <ellipse cx="182" cy="186" rx="14" ry="8" fill="${S.blush}" opacity="${c.female ? 0.45 : 0.25}"/>
  ${c.age === 'old' ? `<path d="M112 120 Q150 112 188 120 M118 130 Q150 124 182 130" fill="none" stroke="${S.deep}" stroke-width="1.3" opacity=".4"/><path d="M122 196 Q128 206 132 212 M178 196 Q172 206 168 212" fill="none" stroke="${S.deep}" stroke-width="1.6" opacity=".45"/>` : ''}
  <!-- brows -->
  <path d="M106 143 Q121 132 140 139 Q122 137 108 146Z" fill="${brow}" stroke="${brow}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M194 143 Q179 132 160 139 Q178 137 192 146Z" fill="${brow}" stroke="${brow}" stroke-width="3" stroke-linejoin="round"/>
  <!-- eyes -->
  <g class="eyes-open">${eye(124, false)}${eye(176, true)}</g>
  <g class="eyes-closed" style="display:none">
    <path d="M108 159 Q124 164 140 158 M160 158 Q176 164 192 159" fill="none" stroke="${INK}" stroke-width="2.8" stroke-linecap="round"/>
    <path d="M110 156 Q124 150 138 155 L140 158 Q124 164 108 159Z M162 155 Q176 150 190 156 L192 159 Q176 164 160 158Z" fill="${S.shade}"/>
  </g>
  <!-- nose -->
  <path d="M152 162 C154 176 158 186 160 192 C156 197 146 197 141 193" fill="none" stroke="${S.deep}" stroke-width="2.4" stroke-linecap="round" opacity=".75"/>
  <path d="M150 170 C147 180 146 188 147 192" fill="none" stroke="#fff" stroke-width="3" opacity=".18" stroke-linecap="round"/>
  <ellipse cx="143" cy="194" rx="3.2" ry="1.8" fill="${S.deep}" opacity=".7"/><ellipse cx="158" cy="194" rx="3.2" ry="1.8" fill="${S.deep}" opacity=".7"/>`;
}

function mouth(c, S) {
  return `
  <g class="mouth-closed">
    <path d="M133 210 Q141 206 150 208 Q159 206 167 210 Q158 213 150 212 Q142 213 133 210Z" fill="${S.lip}"/>
    <path d="M135 211 Q150 222 165 211 Q158 218 150 218 Q142 218 135 211Z" fill="${S.lip}" opacity=".8"/>
    <path d="M133 210.5 Q150 214 167 210.5" fill="none" stroke="${S.deep}" stroke-width="1.8" stroke-linecap="round"/>
    <path d="M143 217 Q150 219 157 217" fill="none" stroke="#fff" stroke-width="1.5" opacity=".3"/>
  </g>
  <g class="mouth-open" style="display:none">
    <path d="M132 208 Q150 204 168 208 Q164 230 150 231 Q136 230 132 208Z" fill="#4a1414"/>
    <path d="M136 209 Q150 206 164 209 L162 214 Q150 212 138 214Z" fill="#f6f1ea"/>
    <path d="M140 225 Q150 219 160 225 Q155 230 150 230 Q145 230 140 225Z" fill="#c75b5b"/>
    <path d="M132 208 Q150 204 168 208" fill="none" stroke="${S.lip}" stroke-width="3" stroke-linecap="round"/>
  </g>`;
}

function hairBack(c) {
  const col = c.hairColor || '#3a2a1c';
  if (c.hair === 'long') return `<path d="M84 150 C78 96 112 70 150 70 C190 70 222 96 216 150 L224 262 C206 270 196 258 194 240 L192 150 Z M84 150 L76 262 C94 270 104 258 106 240 L108 150Z" fill="${col}"/>`;
  if (c.hair === 'wavy') return `<path d="M86 150 C80 100 112 72 150 72 C188 72 220 100 214 150 C224 170 222 196 206 210 L196 160 Z M86 150 C76 170 78 196 94 210 L104 160Z" fill="${col}"/>`;
  return '';
}

function hairFront(c) {
  const col = c.hairColor || '#3a2a1c';
  const hl = `<path d="M118 92 Q140 84 168 90" fill="none" stroke="#fff" stroke-width="3" opacity=".18" stroke-linecap="round"/>`;
  switch (c.hair) {
    case 'short':
      return `<path d="M88 146 C84 100 112 76 150 76 C190 76 218 100 212 146 C206 124 196 110 180 104 C164 112 132 112 118 104 C104 112 94 126 88 146Z" fill="${col}"/>${hl}`;
    case 'wavy':
    case 'long':
      return `<path d="M88 150 C82 102 112 74 150 74 C190 74 220 102 212 150 C204 122 190 104 170 100 C160 112 140 116 122 112 C106 118 94 132 88 150Z" fill="${col}"/>${hl}`;
    default:
      return '';
  }
}

function beard(c, S) {
  const col = c.age === 'old' ? '#d6d6d6' : c.beardColor || c.hairColor || '#3a2a1c';
  switch (c.beard) {
    case 'full':
      return `<path d="M90 168 C92 206 108 244 150 250 C192 244 208 206 210 168 C204 190 194 204 176 206 C168 200 132 200 124 206 C106 204 96 190 90 168Z" fill="${col}"/>
        <path d="M126 204 Q138 196 150 199 Q162 196 174 204 Q162 206 150 205 Q138 206 126 204Z" fill="${col}"/>
        <path d="M120 222 Q126 234 132 240 M150 226 L150 246 M180 222 Q174 234 168 240" stroke="rgba(0,0,0,.18)" stroke-width="2" fill="none"/>`;
    case 'goatee':
      return `<path d="M128 204 Q150 196 172 204 Q164 208 150 207 Q136 208 128 204Z M140 222 Q150 244 160 222 Q150 226 140 222Z" fill="${col}"/>`;
    case 'mustache':
      return `<path d="M126 206 Q138 196 150 201 Q162 196 174 206 Q162 204 150 207 Q138 204 126 206Z" fill="${col}"/>`;
    case 'stubble':
      return `<path d="M98 186 C104 220 126 236 150 236 C174 236 196 220 202 186 C196 214 176 230 150 230 C124 230 104 214 98 186Z" fill="${S.deep}" opacity=".28"/><path d="M128 205 Q150 199 172 205" stroke="${S.deep}" stroke-width="6" opacity=".22" fill="none"/>`;
    case 'pharaoh':
      return `<path d="M141 232 L159 232 L156 276 L144 276Z" fill="#23407a"/><path d="M142 244 H158 M143 256 H157 M144 268 H156" stroke="#d9b13b" stroke-width="3"/>`;
    default:
      return '';
  }
}

function hat(c) {
  const col = c.hatColor;
  const gold = '#e2b43c', goldD = '#a87a14';
  switch (c.hat) {
    case 'crown':
      return `<defs><linearGradient id="gold${c._id}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ffe58a"/><stop offset=".5" stop-color="${gold}"/><stop offset="1" stop-color="${goldD}"/></linearGradient></defs>
        <path d="M94 104 L100 50 L124 80 L150 38 L176 80 L200 50 L206 104Z" fill="url(#gold${c._id})" stroke="${goldD}" stroke-width="2"/>
        <path d="M92 98 Q150 88 208 98 L208 116 Q150 106 92 116Z" fill="url(#gold${c._id})" stroke="${goldD}" stroke-width="2"/>
        <circle cx="150" cy="104" r="7" fill="#c1121f" stroke="#fff" stroke-width="1.5"/><circle cx="118" cy="106" r="5" fill="#1d6fd6"/><circle cx="182" cy="106" r="5" fill="#1d6fd6"/>
        <circle cx="100" cy="50" r="5" fill="#fff4c2"/><circle cx="150" cy="38" r="6" fill="#fff4c2"/><circle cx="200" cy="50" r="5" fill="#fff4c2"/>`;
    case 'mitre':
      return `<defs><linearGradient id="mit${c._id}" x1="0" x2="1"><stop offset="0" stop-color="#e9e4d8"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="#d8d1c2"/></linearGradient></defs>
        <path d="M100 112 C98 70 120 36 150 14 C180 36 202 70 200 112Z" fill="url(#mit${c._id})" stroke="#b9ad92" stroke-width="2"/>
        <path d="M150 20 V108" stroke="${gold}" stroke-width="10"/><path d="M100 104 Q150 94 200 104" stroke="${gold}" stroke-width="10" fill="none"/>
        <path d="M138 52 H162 M150 40 V66" stroke="#c1121f" stroke-width="5"/>`;
    case 'beret':
      return `<path d="M82 118 C78 84 112 64 154 66 C196 68 226 86 222 112 C200 100 110 100 82 118Z" fill="${col || '#1c1c1c'}"/>
        <path d="M86 116 Q150 96 220 110" stroke="rgba(255,255,255,.15)" stroke-width="3" fill="none"/>
        <path d="M188 80 C214 40 250 30 262 46 C240 48 220 62 202 86Z" fill="#f4efe4"/><path d="M196 82 C220 56 244 44 258 46" stroke="#cfc6b4" stroke-width="2" fill="none"/>`;
    case 'morion':
      return `<defs><linearGradient id="st${c._id}" x1="0" x2="1"><stop offset="0" stop-color="#8d949c"/><stop offset=".45" stop-color="#e8ecf0"/><stop offset="1" stop-color="#7a828a"/></linearGradient></defs>
        <path d="M60 126 Q150 96 240 126 Q226 138 206 134 Q150 118 94 134 Q74 138 60 126Z" fill="url(#st${c._id})" stroke="#5b636b" stroke-width="2"/>
        <path d="M98 122 C98 70 202 70 202 122Z" fill="url(#st${c._id})" stroke="#5b636b" stroke-width="2"/>
        <path d="M150 40 C140 64 138 84 150 92 C162 84 160 64 150 40Z" fill="url(#st${c._id})" stroke="#5b636b" stroke-width="2"/>`;
    case 'toque':
      return `<path d="M88 124 C84 72 216 72 212 124Z" fill="${col || '#c8102e'}"/>
        ${[0, 1, 2, 3, 4, 5, 6].map((i) => `<path d="M${104 + i * 16} 84 V122" stroke="rgba(0,0,0,.12)" stroke-width="3"/>`).join('')}
        <rect x="84" y="108" width="132" height="26" rx="10" fill="#f3efe6"/><path d="M90 116 H210 M90 126 H210" stroke="#d9d2c4" stroke-width="2"/>
        <circle cx="150" cy="66" r="20" fill="#f3efe6"/><circle cx="144" cy="60" r="7" fill="#fff" opacity=".7"/>`;
    case 'bandana':
      return `<path d="M86 132 C84 84 216 84 214 132 C190 118 110 118 86 132Z" fill="${col || '#b3261e'}"/><circle cx="120" cy="108" r="3" fill="#fff" opacity=".7"/><circle cx="160" cy="100" r="3" fill="#fff" opacity=".7"/><circle cx="190" cy="112" r="3" fill="#fff" opacity=".7"/>`;
    case 'nemes':
      return `<defs><linearGradient id="nm${c._id}" x1="0" x2="1"><stop offset="0" stop-color="#b58a1c"/><stop offset=".5" stop-color="#f3cf5a"/><stop offset="1" stop-color="#b58a1c"/></linearGradient></defs>
        <path d="M70 290 L86 130 C90 70 210 70 214 130 L230 290 L196 290 L190 150 C170 128 130 128 110 150 L104 290Z" fill="url(#nm${c._id})"/>
        ${[0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<path d="M${80 + i * 1.6} ${150 + i * 18} L${106 - i * 0.4} ${152 + i * 18} M${220 - i * 1.6} ${150 + i * 18} L${194 + i * 0.4} ${152 + i * 18}" stroke="#1f3a8a" stroke-width="7"/>`).join('')}
        <path d="M100 118 Q150 98 200 118" stroke="#1f3a8a" stroke-width="9" fill="none"/><path d="M96 124 Q150 106 204 124" stroke="#f3cf5a" stroke-width="4" fill="none"/>
        <path d="M150 88 C142 96 142 108 150 114 C158 108 158 96 150 88Z" fill="#e2b43c" stroke="#8a6410" stroke-width="2"/>`;
    case 'turban':
      return `<path d="M84 132 C74 76 226 76 216 132 C196 114 104 114 84 132Z" fill="${col || '#f1ece0'}"/>
        <path d="M90 118 C120 96 184 94 212 116 M88 126 C124 104 180 104 214 124 M100 100 C130 84 176 84 204 100" stroke="#d6cfbf" stroke-width="4" fill="none"/>`;
    case 'hardhat':
      return `<defs><linearGradient id="hh${c._id}" x1="0" x2="1"><stop offset="0" stop-color="#d99a00"/><stop offset=".45" stop-color="${col || '#ffc21a'}"/><stop offset="1" stop-color="#c98800"/></linearGradient></defs>
        <path d="M92 126 C92 66 208 66 208 126Z" fill="url(#hh${c._id})"/><rect x="76" y="118" width="148" height="16" rx="8" fill="url(#hh${c._id})"/>
        <path d="M150 70 V120" stroke="rgba(0,0,0,.15)" stroke-width="10"/><path d="M110 88 Q124 76 142 74" stroke="#fff" stroke-width="4" opacity=".45" fill="none" stroke-linecap="round"/>`;
    case 'tophat':
      return `<rect x="106" y="18" width="88" height="92" rx="6" fill="#16181c"/><rect x="106" y="80" width="88" height="14" fill="#6b1420"/>
        <path d="M76 112 Q150 96 224 112 Q150 124 76 112Z" fill="#16181c"/><path d="M118 28 V100" stroke="#fff" stroke-width="3" opacity=".12"/>`;
    default:
      return '';
  }
}

function outfit(c, S) {
  const col = c.outfitColor || '#2d4a7a';
  const torso = 'M24 360 C28 300 70 268 124 256 L176 256 C230 268 272 300 276 360Z';
  const shade = `<path d="${torso}" fill="url(#cloth${c._id})"/>`;
  const defs = `<defs><linearGradient id="cloth${c._id}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".35" stop-color="#000" stop-opacity="0"/><stop offset=".65" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></linearGradient></defs>`;
  const neck = `<path d="M128 220 L172 220 L176 262 Q150 276 124 262Z" fill="${S.base}"/><path d="M128 222 Q150 244 172 222 L172 236 Q150 252 128 236Z" fill="${S.deep}" opacity=".45"/>`;
  let body = '';
  switch (c.outfit) {
    case 'pope':
      body = `<path d="${torso}" fill="#f6f2e8"/>
        <path d="M40 330 C60 288 100 266 150 262 C200 266 240 288 260 330 C220 318 190 312 150 312 C110 312 80 318 40 330Z" fill="#b3122a"/>
        <path d="M118 262 Q150 280 182 262" stroke="#f6f2e8" stroke-width="8" fill="none"/>
        <path d="M150 282 V334 M136 298 H164" stroke="#e2b43c" stroke-width="7" stroke-linecap="round"/><path d="M122 262 Q150 330 178 262" stroke="#e2b43c" stroke-width="2.5" fill="none"/>`;
      break;
    case 'royal':
      body = `<path d="${torso}" fill="${col}"/>
        <path d="M30 336 C44 294 84 266 130 258 L150 300 L170 258 C216 266 256 294 270 336 C240 322 200 312 180 312 L150 330 L120 312 C100 312 60 322 30 336Z" fill="#f7f3ea"/>
        ${[[70, 300], [96, 288], [120, 300], [180, 300], [204, 288], [230, 300], [150, 320]].map(([x, y]) => `<path d="M${x} ${y} l-3 8 h6z" fill="#1a1a1a"/>`).join('')}
        <path d="M112 300 Q150 352 188 300" stroke="#e2b43c" stroke-width="6" fill="none"/><circle cx="150" cy="340" r="10" fill="#e2b43c" stroke="#a87a14" stroke-width="2"/>`;
      break;
    case 'doublet':
      body = `<path d="${torso}" fill="${col}"/>
        <path d="M150 262 V360" stroke="rgba(0,0,0,.35)" stroke-width="4"/>${[280, 302, 324, 346].map((y) => `<circle cx="150" cy="${y}" r="4.5" fill="#e2b43c"/>`).join('')}
        <path d="M60 300 Q76 330 70 360 M240 300 Q224 330 230 360" stroke="rgba(255,255,255,.12)" stroke-width="3" fill="none"/>
        <path d="M112 252 Q150 276 188 252 Q196 266 186 272 Q150 290 114 272 Q104 266 112 252Z" fill="#fbf8f1" stroke="#d8d0c0" stroke-width="2"/>
        ${[0, 1, 2, 3, 4, 5, 6].map((i) => `<path d="M${118 + i * 11} 262 q5 12 10 0" stroke="#d8d0c0" stroke-width="1.6" fill="none"/>`).join('')}`;
      break;
    case 'armor':
      body = `<defs><linearGradient id="ar${c._id}" x1="0" x2="1"><stop offset="0" stop-color="#6e767e"/><stop offset=".4" stop-color="#dfe4e9"/><stop offset="1" stop-color="#5f676f"/></linearGradient></defs>
        <path d="${torso}" fill="#7a1a1a"/>
        <path d="M70 360 C72 312 100 280 150 276 C200 280 228 312 230 360Z" fill="url(#ar${c._id})" stroke="#4a5058" stroke-width="2"/>
        <path d="M150 280 V360" stroke="#4a5058" stroke-width="2"/><path d="M96 318 Q150 300 204 318" stroke="#4a5058" stroke-width="2" fill="none"/>`;
      break;
    case 'plaid':
      body = `<defs><pattern id="pl${c._id}" width="36" height="36" patternUnits="userSpaceOnUse"><rect width="36" height="36" fill="${col}"/><rect x="0" y="12" width="36" height="10" fill="#1a1a1a" opacity=".55"/><rect x="12" y="0" width="10" height="36" fill="#1a1a1a" opacity=".55"/><rect x="0" y="16" width="36" height="2" fill="#fff" opacity=".18"/></pattern></defs>
        <path d="${torso}" fill="url(#pl${c._id})"/><path d="M122 256 L150 292 L178 256 L190 262 L150 310 L110 262Z" fill="#a50f1c"/><path d="M150 292 V360" stroke="rgba(0,0,0,.4)" stroke-width="3"/>`;
      break;
    case 'pharaoh':
      body = `<path d="${torso}" fill="${S.base}"/>
        ${[0, 1, 2, 3].map((i) => `<path d="M${64 + i * 6} ${330 - i * 18} Q150 ${372 - i * 24} ${236 - i * 6} ${330 - i * 18}" stroke="${['#1f3a8a', '#e2b43c', '#2a8a6a', '#e2b43c'][i]}" stroke-width="12" fill="none"/>`).join('')}`;
      break;
    case 'galabeya':
      body = `<path d="${torso}" fill="${col}"/><path d="M136 258 L150 300 L164 258" stroke="#f4efe4" stroke-width="5" fill="none"/><path d="M150 300 V360" stroke="rgba(0,0,0,.2)" stroke-width="3"/>`;
      break;
    case 'hivis':
      body = `<path d="${torso}" fill="#35506e"/><path d="M58 360 C62 316 90 284 126 270 L136 360Z M242 360 C238 316 210 284 174 270 L164 360Z" fill="${col}"/>
        <path d="M84 300 L130 300 M170 300 L216 300 M76 330 L132 330 M168 330 L224 330" stroke="#e9ecef" stroke-width="9"/>`;
      break;
    case 'suit':
      body = `<path d="${torso}" fill="${col}"/><path d="M124 258 L150 320 L176 258Z" fill="#f6f4ef"/><path d="M150 272 L142 292 L150 350 L158 292Z" fill="#8b1e2d"/>
        <path d="M124 258 L150 330 L112 290 Z M176 258 L150 330 L188 290Z" fill="#15181e"/>`;
      break;
    case 'shirt':
      body = `<path d="${torso}" fill="${col}"/><path d="M130 258 L150 300 L170 258" stroke="#bdb5a0" stroke-width="4" fill="none"/>`;
      break;
    default:
      body = `<path d="${torso}" fill="${col}"/>`;
  }
  return `${defs}${neck}${body}${shade}`;
}

// ------------------------------------------------------------------ public

export function characterSvg(spec) {
  const base = CHARACTER_PRESETS[spec.preset] || {};
  const c = { ...base };
  for (const [k, v] of Object.entries(spec)) if (v !== undefined) c[k] = v;
  c._id = 'p' + uid++;
  const S = SKINS[c.skin] || SKINS.light;
  const [bg1, bg2] = c.bg || ['#2f4f6f', '#0b1622'];
  const id = c._id;
  const frame = c.frame || 'hex';
  const hexPts = '150,6 290,86 290,274 150,354 10,274 10,86';
  const clip = frame === 'round' ? `<circle cx="150" cy="180" r="172"/>` : frame === 'none' ? `<rect x="-40" y="-40" width="380" height="440"/>` : `<polygon points="${hexPts}"/>`;
  const border = frame === 'round'
    ? `<circle cx="150" cy="180" r="172" fill="none" stroke="#fff" stroke-width="10"/><circle cx="150" cy="180" r="178" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="3"/>`
    : frame === 'none' ? '' : `<polygon points="${hexPts}" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round"/><polygon points="150,-2 297,82 297,278 150,362 3,278 3,82" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="3" stroke-linejoin="round"/>`;
  return `<svg viewBox="0 0 300 360" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">
  <defs>
    <clipPath id="fr${id}">${clip}</clipPath>
    <radialGradient id="bg${id}" cx=".5" cy=".35" r=".8"><stop offset="0" stop-color="${bg1}"/><stop offset="1" stop-color="${bg2}"/></radialGradient>
  </defs>
  <g clip-path="url(#fr${id})">
    ${frame === 'none' ? '' : `<rect x="-10" y="-10" width="320" height="380" fill="url(#bg${id})"/><circle cx="150" cy="150" r="120" fill="#fff" opacity=".06"/>`}
    <g class="breathe" transform="translate(150 196) scale(1.1) translate(-150 -186)">
      ${hairBack(c)}
      ${outfit(c, S)}
      ${face(c, S, id)}
      ${hairFront(c)}
      ${beard(c, S)}
      ${mouth(c, S)}
      ${hat(c)}
    </g>
  </g>
  ${border}
</svg>`;
}

// Sailing ship: sails carry a coloured band and the mast flies a pennant.
export function shipSvg(spec = {}) {
  const hull = spec.hull || '#6e4322';
  const sail = spec.sail || '#f3ead2';
  const emblem = spec.emblem || '#c1121f';
  // neutral sails: a coloured band, no religious or national symbol
  const cross = `<path d="M-22 -4 Q0 -8 22 -4 L22 5 Q0 1 -22 5Z" fill="${emblem}" opacity=".85"/>`;
  return `<svg viewBox="0 0 240 220" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">
  <defs>
    <linearGradient id="hull" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#8a5a32"/><stop offset="1" stop-color="${hull}"/></linearGradient>
    <linearGradient id="sailg" x1="0" x2="1"><stop offset="0" stop-color="#d9cfb3"/><stop offset=".5" stop-color="${sail}"/><stop offset="1" stop-color="#d9cfb3"/></linearGradient>
  </defs>
  <g stroke="${INK}" stroke-width="3" stroke-linejoin="round">
    <path d="M86 36 V168 M146 54 V168 M186 94 V168" stroke-width="5"/>
    <path d="M58 50 C84 46 110 46 120 52 C126 90 120 118 114 134 C94 130 72 130 54 134 C62 110 64 80 58 50Z" fill="url(#sailg)"/>
    <path d="M124 68 C142 64 162 64 172 70 C176 98 172 118 168 128 C152 126 136 126 122 128 C126 110 128 90 124 68Z" fill="url(#sailg)"/>
    <path d="M186 98 L224 150 L186 150Z" fill="url(#sailg)"/>
    <path d="M86 36 L114 24 L86 14Z" fill="${emblem}"/>
    <path d="M8 158 L232 158 C224 196 196 208 120 208 C58 208 24 196 8 158Z" fill="url(#hull)"/>
    <path d="M8 158 L2 136 L46 144 L46 158Z" fill="url(#hull)"/>
    <path d="M18 174 H218" stroke="#3e2410" stroke-width="2.5"/>
  </g>
  <g transform="translate(88 92)">${cross}</g>
  <g transform="translate(146 98) scale(.8)">${cross}</g>
  ${[60, 96, 132, 168].map((x) => `<circle cx="${x}" cy="186" r="5" fill="#2a1f1a"/>`).join('')}
  <path d="M-6 204 Q20 196 40 206 T90 206 T140 206 T190 206 T246 204" stroke="#fff" stroke-width="4" fill="none" opacity=".8"/>
</svg>`;
}
