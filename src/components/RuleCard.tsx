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

  async function handleCopy(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    await navigator.clipboard.writeText(rule.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="relative group h-full">
      {/* Shelf line - gets a hint of color on hover */}
      <div className={`absolute -bottom-px -left-3 -right-3 h-px bg-border-subtle z-0 pointer-events-none transition-colors duration-500`} />

      {/* Card */}
      <a
        href={`/rules/${rule.id}`}
        className={`relative z-10 h-full flex flex-col bg-surface border border-border-subtle rounded-[3px] transition-all duration-500 hover:bg-surface-hover hover:-translate-y-[2px] ${accent.hover} ${accent.glow} cursor-pointer overflow-hidden block`}
      >
        {/* Spine - monochrome at rest, colored on hover */}
        <div className={`absolute left-0 top-0 bottom-0 w-1 bg-[#1a1a1a] transition-colors duration-500 ${accent.spine} z-20`} />

        <div className="p-5 pl-7 flex flex-col h-full z-10">
          {/* Title */}
          <h3 className="text-text-main font-medium tracking-tight text-[15px] leading-snug mb-1.5">
            {title}
          </h3>

          {/* Description */}
          <p className="text-text-muted text-[13px] leading-relaxed mb-4 line-clamp-2">
            {description}
          </p>

          {/* Code Preview */}
          <div className="mb-5 relative mt-auto">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-surface group-hover:to-surface-hover z-10 pointer-events-none transition-colors duration-500" />
            <pre className="text-[10px] leading-relaxed text-text-faint font-mono bg-[#080808] p-3 rounded-sm border border-white/[0.02] overflow-hidden h-14">
              <code>{rule.content.substring(0, 100)}...</code>
            </pre>
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
              {rule.stars > 0 && (
                <span className="text-[10px] text-text-faint flex items-center gap-1">
                  <svg width="9" height="9" viewBox="0 0 24 24" fill="currentColor" className="opacity-50">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  {rule.stars}
                </span>
              )}

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
