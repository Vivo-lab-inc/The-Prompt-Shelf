import { cn } from '../lib/utils';
import { Star, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface Rule {
  id: string;
  title: string;
  description: string;
  tool: string;
  format: string;
  language: string;
  framework: string;
  category: string;
  tags: string[];
  author: string;
  source: string;
  stars: number;
  content: string;
}

const toolConfig: Record<string, { label: string; class: string; icon: string }> = {
  'cursor': { label: '.cursorrules', class: 'badge-cursor', icon: '>' },
  'claude-code': { label: 'CLAUDE.md', class: 'badge-claude', icon: '#' },
  'agents-md': { label: 'AGENTS.md', class: 'badge-agents', icon: '@' },
};

function highlightCode(text: string): string {
  return text
    .replace(/(#.*)/g, '<span class="cm">$1</span>')
    .replace(/(".*?")/g, '<span class="str">$1</span>')
    .replace(/\b(import|from|export|const|let|var|function|return|if|else|async|await|class|interface|type)\b/g, '<span class="kw">$1</span>')
    .replace(/\b(true|false|null|undefined)\b/g, '<span class="num">$1</span>')
    .replace(/(\/\/.*)/g, '<span class="cm">$1</span>')
    .replace(/(-\s)/g, '<span class="op">$1</span>');
}

export default function RuleCard({ rule }: { rule: Rule }) {
  const [copied, setCopied] = useState(false);
  const config = toolConfig[rule.tool] || toolConfig['agents-md'];

  const codeLines = rule.content.split('\n').slice(0, 6);

  async function handleCopy(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    await navigator.clipboard.writeText(rule.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <a href={`/rules/${rule.id}`} className="glow-card group block p-0 overflow-hidden">
      {/* Shelf spine accent */}
      <div className={cn(
        "h-1 w-full",
        rule.tool === 'cursor' ? 'bg-gradient-to-r from-blue-500/60 to-blue-400/20' :
        rule.tool === 'claude-code' ? 'bg-gradient-to-r from-orange-500/60 to-orange-400/20' :
        'bg-gradient-to-r from-green-500/60 to-green-400/20'
      )} />

      <div className="p-5">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className={cn("px-2.5 py-1 text-[11px] font-semibold rounded-md border uppercase tracking-wider", config.class)}>
              {config.label}
            </span>
            <span className="px-2 py-0.5 text-[11px] rounded bg-[--color-bg] border border-[--color-border] text-[--color-text-muted]">
              {rule.language}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleCopy}
              className="opacity-0 group-hover:opacity-100 transition-opacity p-1.5 rounded-md hover:bg-[--color-surface-hover] text-[--color-text-muted] hover:text-[--color-text]"
              title="Copy to clipboard"
            >
              {copied ? <Check size={14} className="text-[--color-green]" /> : <Copy size={14} />}
            </button>
            <span className="flex items-center gap-1 text-xs text-[--color-text-muted]">
              <Star size={12} className="fill-[--color-yellow]/30 text-[--color-yellow]" />
              {rule.stars.toLocaleString()}
            </span>
          </div>
        </div>

        {/* Title */}
        <h3 className="font-semibold text-[15px] mb-1.5 group-hover:text-[--color-accent] transition-colors leading-snug">
          {rule.title}
        </h3>
        <p className="text-[13px] text-[--color-text-muted] leading-relaxed mb-4 line-clamp-2">
          {rule.description}
        </p>

        {/* Code Preview - the "spine" of the shelf */}
        <div className="code-preview rounded-lg bg-[--color-bg] border border-[--color-border] p-3 overflow-hidden">
          <div className="flex items-center gap-1.5 mb-2.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#ff5f57]/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-[#febc2e]/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-[#28c840]/80" />
            <span className="ml-2 text-[10px] text-[--color-text-muted]/50 font-mono">{rule.format}</span>
          </div>
          <pre className="!bg-transparent !border-0 !p-0 !m-0 !rounded-none">
            <code
              className="text-[11px] leading-[1.6] !font-mono block"
              dangerouslySetInnerHTML={{
                __html: codeLines.map(line => highlightCode(line)).join('\n')
              }}
            />
          </pre>
          {rule.content.split('\n').length > 6 && (
            <div className="mt-1 text-[10px] text-[--color-text-muted]/40 font-mono">
              ... {rule.content.split('\n').length - 6} more lines
            </div>
          )}
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5 mt-4">
          {rule.tags.slice(0, 4).map(tag => (
            <span key={tag} className="px-2 py-0.5 text-[10px] rounded-full bg-[--color-surface-hover] text-[--color-text-muted] border border-[--color-border]/50">
              {tag}
            </span>
          ))}
          {rule.tags.length > 4 && (
            <span className="px-2 py-0.5 text-[10px] text-[--color-text-muted]/50">
              +{rule.tags.length - 4}
            </span>
          )}
        </div>
      </div>
    </a>
  );
}
