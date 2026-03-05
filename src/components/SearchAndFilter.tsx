import { useState, useMemo, useEffect } from 'react';
import RuleCard from './RuleCard';
import type { Rule } from './RuleCard';

const toolFilters = [
  { value: '', label: 'All' },
  { value: 'claude-code', label: 'Claude Code' },
  { value: 'cursor', label: 'Cursor' },
  { value: 'agents-md', label: 'Agents.md' },
];

const categoryFilters = [
  { value: 'web-frontend', label: 'Frontend' },
  { value: 'backend', label: 'Backend' },
  { value: 'cli', label: 'CLI' },
  { value: 'devops', label: 'DevOps' },
  { value: 'security', label: 'Security' },
];

function getParams() {
  if (typeof window === 'undefined') return { q: '', tool: '', category: '' };
  const p = new URLSearchParams(window.location.search);
  return {
    q: p.get('q') || '',
    tool: p.get('tool') || '',
    category: p.get('category') || '',
  };
}

export default function SearchAndFilter({ rules }: { rules: Rule[] }) {
  const [query, setQuery] = useState('');
  const [activeTool, setActiveTool] = useState('');
  const [activeCategory, setActiveCategory] = useState('');

  // Read URL params on mount
  useEffect(() => {
    const { q, tool, category } = getParams();
    if (q) setQuery(q);
    if (tool) setActiveTool(tool);
    if (category) setActiveCategory(category);
  }, []);

  const filtered = useMemo(() => {
    let result = [...rules];
    if (query) {
      const q = query.toLowerCase();
      result = result.filter(r =>
        r.title.toLowerCase().includes(q) ||
        (r.title_ja || '').toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        (r.description_ja || '').toLowerCase().includes(q) ||
        r.tool.toLowerCase().includes(q) ||
        r.format.toLowerCase().includes(q) ||
        r.tags.some(t => t.includes(q)) ||
        r.language.toLowerCase().includes(q) ||
        r.framework.toLowerCase().includes(q) ||
        r.content.toLowerCase().includes(q)
      );
    }
    if (activeTool) result = result.filter(r => r.tool === activeTool);
    if (activeCategory) result = result.filter(r => r.category === activeCategory);
    return result.sort((a, b) => b.stars - a.stars);
  }, [rules, query, activeTool, activeCategory]);

  const hasFilters = query || activeTool || activeCategory;

  return (
    <div>
      {/* Search */}
      <div className="relative mb-8">
        <svg className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-faint" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search rules..."
          className="w-full pl-11 pr-4 py-3 bg-surface border border-border-subtle rounded-[3px] text-text-main placeholder:text-text-faint outline-none focus:border-border-strong text-[14px] transition-colors"
        />
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-2 mb-10">
        {toolFilters.map(f => (
          <button
            key={f.value}
            onClick={() => setActiveTool(activeTool === f.value ? '' : f.value)}
            className={`px-4 py-1.5 rounded-full text-[13px] tracking-wide transition-all duration-200 border ${
              activeTool === f.value
                ? 'bg-white/[0.08] text-text-main border-white/10'
                : 'bg-transparent text-text-muted border-transparent hover:text-text-main hover:bg-white/[0.03]'
            }`}
          >
            {f.label}
          </button>
        ))}

        <span className="w-px h-4 bg-border-subtle mx-2" />

        {categoryFilters.map(f => (
          <button
            key={f.value}
            onClick={() => setActiveCategory(activeCategory === f.value ? '' : f.value)}
            className={`px-4 py-1.5 rounded-full text-[13px] tracking-wide transition-all duration-200 border ${
              activeCategory === f.value
                ? 'bg-white/[0.08] text-text-main border-white/10'
                : 'bg-transparent text-text-muted border-transparent hover:text-text-main hover:bg-white/[0.03]'
            }`}
          >
            {f.label}
          </button>
        ))}

        {hasFilters && (
          <button
            onClick={() => { setQuery(''); setActiveTool(''); setActiveCategory(''); }}
            className="ml-auto text-[12px] text-text-faint hover:text-text-muted transition-colors"
          >
            Clear
          </button>
        )}
      </div>

      {/* Count */}
      <p className="text-[13px] text-text-faint mb-8 tracking-wide">
        {filtered.length} rules
      </p>

      {/* Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-6 gap-y-14">
          {filtered.map(rule => (
            <RuleCard key={rule.id} rule={rule} />
          ))}
        </div>
      ) : (
        <div className="text-center py-32">
          <p className="text-text-muted mb-2">No rules found</p>
          <button
            onClick={() => { setQuery(''); setActiveTool(''); setActiveCategory(''); }}
            className="text-[13px] text-text-faint hover:text-text-muted transition-colors"
          >
            Clear filters
          </button>
        </div>
      )}
    </div>
  );
}
