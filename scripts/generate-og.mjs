import sharp from 'sharp';

const width = 1200;
const height = 630;

// Build SVG with embedded text (no external fonts needed)
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" fill="none">
  <rect width="${width}" height="${height}" fill="#0a0a0a"/>

  <!-- Grid pattern -->
  <g opacity="0.05" stroke="#fff" stroke-width="1">
    ${Array.from({length: 10}, (_, i) => `<line x1="${(i+1)*120}" y1="0" x2="${(i+1)*120}" y2="${height}"/>`).join('\n    ')}
    ${Array.from({length: 5}, (_, i) => `<line x1="0" y1="${(i+1)*120}" x2="${width}" y2="${(i+1)*120}"/>`).join('\n    ')}
  </g>

  <!-- Grid dots -->
  <g opacity="0.1" fill="#fff">
    ${Array.from({length: 10}, (_, i) =>
      Array.from({length: 5}, (_, j) =>
        `<circle cx="${(i+1)*120}" cy="${(j+1)*120}" r="2"/>`
      ).join('\n    ')
    ).join('\n    ')}
  </g>

  <!-- Subtle top ambient -->
  <ellipse cx="600" cy="0" rx="500" ry="300" fill="url(#ambient)"/>
  <defs>
    <radialGradient id="ambient">
      <stop offset="0%" stop-color="#fff" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Book shelf icon -->
  <g transform="translate(510, 140)" stroke="#555" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <rect x="8" y="10" width="18" height="65" rx="3"/>
    <rect x="30" y="3" width="14" height="72" rx="3"/>
    <rect x="48" y="18" width="12" height="57" rx="2"/>
    <rect x="64" y="7" width="18" height="68" rx="3"/>
    <rect x="86" y="13" width="12" height="62" rx="2" transform="rotate(6 92 75)"/>
    <line x1="2" y1="78" x2="106" y2="78" stroke-width="3.5"/>
  </g>

  <!-- Title -->
  <text x="600" y="310" text-anchor="middle" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="52" font-weight="600" letter-spacing="-1">The-Prompt-Shelf</text>

  <!-- Subtitle -->
  <text x="600" y="370" text-anchor="middle" fill="#888888" font-family="system-ui, -apple-system, sans-serif" font-size="22">Curated AI Coding Rules &amp; Prompts</text>

  <!-- Tags -->
  <g transform="translate(600, 420)" text-anchor="middle" font-family="monospace" font-size="14" fill="#4a4a4a">
    <text x="-200" y="0">CLAUDE.md</text>
    <text x="-60" y="0">·</text>
    <text x="0" y="0">.cursorrules</text>
    <text x="80" y="0">·</text>
    <text x="170" y="0">AGENTS.md</text>
  </g>

  <!-- Stats line -->
  <text x="600" y="480" text-anchor="middle" fill="#555" font-family="system-ui, sans-serif" font-size="16">39 rules · 14 languages · 7 categories</text>

  <!-- URL -->
  <text x="600" y="560" text-anchor="middle" fill="#333" font-family="monospace" font-size="17">thepromptshelf.dev</text>

  <!-- Bottom shelf line -->
  <line x1="200" y1="590" x2="1000" y2="590" stroke="#1a1a1a" stroke-width="2"/>
</svg>`;

await sharp(Buffer.from(svg))
  .resize(width, height)
  .png()
  .toFile('public/og-default.png');

console.log('Generated public/og-default.png (1200x630)');
