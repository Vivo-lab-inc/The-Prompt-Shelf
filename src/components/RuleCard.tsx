import { useState, useEffect } from 'react';

export interface Rule {
  id: string;
  title: string;
  title_ja?: string;
  description: string;
  description_ja?: string;
  tool: string;
  format: string;
  language: string;
  framework: string;
  category: string;
  tags: string[];
  author: string;
  source: string;
  sourceUrl?: string;
  stars: number;
  content: string;
}

const toolAccent: Record<string, { hover: string; spine: string; glow: string }> = {
  'cursor':      { hover: 'group-hover:border-blue-500/15', spine: 'group-hover:bg-blue-500/60',  glow: 'group-hover:shadow-[0_0_20px_rgba(59,130,246,0.06)]' },
  'claude-code': { hover: 'group-hover:border-orange-500/15', spine: 'group-hover:bg-orange-500/60', glow: 'group-hover:shadow-[0_0_20px_rgba(249,115,22,0.06)]' },
  'agents-md':   { hover: 'group-hover:border-emerald-500/15', spine: 'group-hover:bg-emerald-500/60', glow: 'group-hover:shadow-[0_0_20px_rgba(16,185,129,0.06)]' },
  'image-prompt': { hover: 'group-hover:border-pink-500/15', spine: 'group-hover:bg-pink-500/60', glow: 'group-hover:shadow-[0_0_20px_rgba(236,72,153,0.06)]' },
};

function useLang() {
  const [lang, setLang] = useState('ja');
  useEffect(() => {
    setLang(localStorage.getItem('lang') || 'ja');
    const handler = () => setLang(localStorage.getItem('lang') || 'ja');
    window.addEventListener('lang-changed', handler);
    return () => window.removeEventListener('lang-changed', handler);
  }, []);
  return lang;
}

export default function RuleCard({ rule }: { rule: Rule }) {
  const [copied, setCopied] = useState(false);
  const lang = useLang();
  const accent = toolAccent[rule.tool] || toolAccent['agents-md'];

  const title = lang === 'ja' && rule.title_ja ? rule.title_ja : rule.title;
  const description = lang === 'ja' && rule.description_ja ? rule.description_ja : rule.description;

  // Derive avatar and display name from source
  // Only show real avatars for known, verified authors
  const isGitHub = rule.sourceUrl?.includes('github.com');
  const isKnownAuthor = rule.author && !['awesome-cursorrules', 'Community'].includes(rule.author);
  const avatarUrl = isKnownAuthor && isGitHub ? `https://github.com/${rule.author}.png?size=32`
    : null;
  const displayAuthor = isKnownAuthor ? (rule.source || rule.author)
    : rule.source === 'cursor.directory' ? 'cursor.directory'
    : rule.source === 'awesome-cursorrules' ? 'awesome-cursorrules'
    : rule.source || rule.author;

  async function handleCopy(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    await navigator.clipboard.writeText(rule.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="relative group">
      {/* Shelf line - gets a hint of color on hover */}
      <div className={`absolute -bottom-px -left-3 -right-3 h-px bg-border-subtle z-0 pointer-events-none transition-colors duration-500`} />

      {/* Card */}
      <a
        href={`/rules/${rule.id}`}
        className={`relative z-10 flex flex-col bg-surface border border-border-subtle rounded-[3px] transition-all duration-500 hover:bg-surface-hover hover:-translate-y-[2px] ${accent.hover} ${accent.glow} cursor-pointer overflow-hidden block`}
      >
        {/* Spine - monochrome at rest, colored on hover */}
        <div className={`absolute left-0 top-0 bottom-0 w-1 bg-[#1a1a1a] transition-colors duration-500 ${accent.spine} z-20`} />

        <div className="p-5 pl-7 flex flex-col z-10">
          {/* Title */}
          <h3 className="text-text-main font-medium tracking-tight text-[15px] leading-snug mb-1.5">
            {title}
          </h3>

          {/* Description */}
          <p className="text-text-muted text-[13px] leading-relaxed mb-4 line-clamp-2">
            {description}
          </p>

          {/* Preview */}
          <div className="mb-5 relative mt-auto">
            {rule.tool === 'image-prompt' ? (
              <div className="rounded-sm border border-white/[0.02] overflow-hidden">
                <img
                  src={`/previews/${rule.id}.webp`}
                  alt={rule.title}
                  className="w-full h-auto"
                  loading="lazy"
                />
              </div>
            ) : (
              <>
                <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-surface group-hover:to-surface-hover z-10 pointer-events-none transition-colors duration-500" />
                <pre className="text-[10px] leading-relaxed text-text-faint font-mono bg-[#080808] p-3 rounded-sm border border-white/[0.02] overflow-hidden h-28">
                  <code>{rule.content.substring(0, 300)}...</code>
                </pre>
              </>
            )}
          </div>

          {/* Author row */}
          <div className="flex items-center gap-2 mb-3">
            {avatarUrl ? (
              <img
                src={avatarUrl}
                alt={displayAuthor}
                className="w-5 h-5 rounded-full border border-border-subtle"
                loading="lazy"
                onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
              />
            ) : isGitHub ? (
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-text-faint shrink-0"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            ) : (
              <div className="w-5 h-5 rounded-full bg-white/[0.05] border border-border-subtle flex items-center justify-center shrink-0">
                <span className="text-[8px] text-text-faint font-medium">{displayAuthor.charAt(0).toUpperCase()}</span>
              </div>
            )}
            <span className="text-[11px] text-text-faint truncate">{displayAuthor}</span>
            {rule.stars > 0 && (
              <span className="text-[10px] text-yellow-500/60 flex items-center gap-1 ml-auto shrink-0">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                {rule.stars.toLocaleString()}
              </span>
            )}
          </div>

          {/* Footer */}
          <div className="flex flex-wrap items-center gap-2 pt-3 border-t border-border-subtle/40">
            <span className="px-2 py-[2px] text-[10px] font-medium text-text-main/80 bg-white/[0.05] rounded-full border border-white/[0.06] tracking-wider uppercase">
              {rule.format}
            </span>
            {rule.framework !== 'Any' && (
              <span className="px-2 py-[2px] text-[10px] text-text-faint rounded-full border border-border-subtle tracking-wide">
                {rule.framework}
              </span>
            )}

            <div className="ml-auto flex items-center gap-3">
              <span className="text-[10px] text-text-faint tracking-wide">
                {rule.language}
              </span>

              <button
                onClick={handleCopy}
                className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-text-faint hover:text-text-muted"
                title="Copy rule"
              >
                {copied ? (
                  <svg width="13" height="13" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                ) : (
                  <svg width="13" height="13" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Bottom resting shadow */}
        <div className="absolute bottom-0 left-0 right-0 h-px bg-black shadow-[0_1px_4px_rgba(0,0,0,0.8)] z-20" />
      </a>
    </div>
  );
}
