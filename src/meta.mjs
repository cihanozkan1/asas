// Upload text (.txt) and fact-check report (sources.md) for a video.
import fs from 'node:fs';

export function writeUploadText(script, file, extraCredits = []) {
  const m = script.meta || {};
  const tags = m.tags || [];
  const hashtags = (m.hashtags || tags.map((t) => '#' + t.replace(/\s+/g, ''))).join(' ');
  const credits = [...(m.credits || []), ...extraCredits];
  const lines = [
    'TITLE',
    m.title || '',
    '',
    'DESCRIPTION',
    (m.description || '').trim(),
    '',
    hashtags,
    ...(credits.length ? ['', ...credits] : []),
    '',
    'PINNED COMMENT',
    ...(m.pinnedComment || []),
    '',
    'TAGS',
    tags.join(', '),
    '',
  ];
  fs.writeFileSync(file, lines.join('\n'));
}

export function writeSources(script, file) {
  const out = [`# Sources: ${script.meta?.title || script.id}`, ''];
  script.scenes.forEach((s, i) => {
    out.push(`## Scene ${i + 1}`);
    out.push(`> ${s.text}`);
    out.push('');
    if (!s.sources?.length) out.push('_No factual claim / no source needed._');
    for (const src of s.sources || []) {
      out.push(`- **Claim:** ${src.claim}`);
      if (src.quote) out.push(`  - Quote: "${src.quote}"`);
      out.push(`  - Source: [${src.title || src.url}](${src.url})`);
    }
    out.push('');
  });
  fs.writeFileSync(file, out.join('\n'));
}
