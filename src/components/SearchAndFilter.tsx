import { useState, useMemo } from 'react';
import { Search, X } from 'lucide-react';
import RuleCard from './RuleCard';
import { cn } from '../lib/utils';

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

const toolFilters = [
  { value: 'claude-code', label: 'CLAUDE.md', class: 'badge-claude' },
  { value: 'cursor', label: '.cursorrules', class: 'badge-cursor' },
  { value: 'agents-md', label: 'AGENTS.md', class: 'badge-agents' },
];

const categoryFilters = [
  { value: 'web-frontend', label: 'Frontend' },
  { value: 'backend', label: 'Backend' },
  { value: 'cli', label: 'CLI' },
  { value: 'devops', label: 'DevOps' },
  { value: 'security', label: 'Security' },
];

type SortOption = 'stars' | 'newest' | 'title';

export default function SearchAndFilter({ rules, initialQuery = '', initialTool = '', initialLanguage = '' }: { rules: Rule[], initialQuery?: string, initialTool?: string, initialLanguage?: string }) {
  const [query, setQuery] = useState(initialQuery);
  const [activeTool, setActiveTool] = useState(initialTool);
  const [activeCategory, setActiveCategory] = useState('');
  const [activeLanguage, setActiveLanguage] = useState(initialLanguage);
  const [sort, setSort] = useState<SortOption>('stars');

  const languages = useMemo(() => [...new Set(rules.map(r => r.language))], [rules]);

  const filtered = useMemo(() => {
    let result = [...rules];

    if (query) {
      const q = query.toLowerCase();
      result = result.filter(r =>
        r.title.toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        r.tags.some(t => t.includes(q)) ||
        r.content.toLowerCase().includes(q)
      );
    }

    if (activeTool) result = result.filter(r => r.tool === activeTool);
    if (activeCategory) result = result.filter(r => r.category === activeCategory);
    if (activeLanguage) result = result.filter(r => r.language === activeLanguage);

    result.sort((a, b) => {
      if (sort === 'stars') return b.stars - a.stars;
      if (sort === 'title') return a.title.localeCompare(b.title);
      return 0;
    });

    return result;
  }, [rules, query, activeTool, activeCategory, activeLanguage, sort]);

  const hasFilters = query || activeTool || activeCategory || activeLanguage;

  function clearAll() {
    setQuery('');
    setActiveTool('');
    setActiveCategory('');
    setActiveLanguage('');
  }

  return (
    <div>
      {/* Search */}
      <div className="search-glow relative rounded-xl bg-[--color-surface] mb-6">
        <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-[--color-text-muted]" />
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search rules, frameworks, languages..."
          className="w-full pl-12 pr-12 py-3.5 bg-transparent text-[--color-text] placeholder:text-[--color-text-muted]/50 outline-none text-sm"
        />
        {query && (
          <button onClick={() => setQuery('')} className="absolute right-4 top-1/2 -translate-y-1/2 text-[--color-text-muted] hover:text-[--color-text]">
            <X size={16} />
          </button>
        )}
      </div>

      {/* Filter bar */}
      <div className="flex flex-wrap items-center gap-2 mb-8">
        {/* Tool filters */}
        {toolFilters.map(f => (
          <button
            key={f.value}
            onClick={() => setActiveTool(activeTool === f.value ? '' : f.value)}
            className={cn(
              "px-3 py-1.5 text-[12px] font-medium rounded-lg border transition-all",
              activeTool === f.value
                ? f.class + " ring-1 ring-current/20"
                : "bg-[--color-surface] border-[--color-border] text-[--color-text-muted] hover:text-[--color-text] hover:border-[--color-border-hover]"
            )}
          >
            {f.label}
          </button>
        ))}

        <span className="w-px h-5 bg-[--color-border] mx-1" />

        {/* Category filters */}
        {categoryFilters.map(f => (
          <button
            key={f.value}
            onClick={() => setActiveCategory(activeCategory === f.value ? '' : f.value)}
            className={cn(
              "px-3 py-1.5 text-[12px] rounded-lg border transition-all",
              activeCategory === f.value
                ? "bg-[--color-accent-dim] border-[--color-accent]/30 text-[--color-accent]"
                : "bg-[--color-surface] border-[--color-border] text-[--color-text-muted] hover:text-[--color-text] hover:border-[--color-border-hover]"
            )}
          >
            {f.label}
          </button>
        ))}

        <span className="w-px h-5 bg-[--color-border] mx-1" />

        {/* Language dropdown */}
        <select
          value={activeLanguage}
          onChange={e => setActiveLanguage(e.target.value)}
          className="px-3 py-1.5 text-[12px] rounded-lg bg-[--color-surface] border border-[--color-border] text-[--color-text-muted] outline-none cursor-pointer hover:border-[--color-border-hover]"
        >
          <option value="">All Languages</option>
          {languages.map(l => <option key={l} value={l}>{l}</option>)}
        </select>

        {/* Sort */}
        <div className="ml-auto flex items-center gap-2">
          {hasFilters && (
            <button onClick={clearAll} className="text-[12px] text-[--color-accent] hover:underline">
              Clear filters
            </button>
          )}
          <select
            value={sort}
            onChange={e => setSort(e.target.value as SortOption)}
            className="px-3 py-1.5 text-[12px] rounded-lg bg-[--color-surface] border border-[--color-border] text-[--color-text-muted] outline-none cursor-pointer"
          >
            <option value="stars">Most Popular</option>
            <option value="title">Alphabetical</option>
          </select>
        </div>
      </div>

      {/* Results count */}
      <div className="flex items-center justify-between mb-5">
        <p className="text-sm text-[--color-text-muted]">
          <span className="text-[--color-text] font-medium stat-number">{filtered.length}</span> rules
          {hasFilters && <span> matching</span>}
        </p>
      </div>

      {/* Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map(rule => (
            <RuleCard key={rule.id} rule={rule} />
          ))}
        </div>
      ) : (
        <div className="text-center py-24">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-[--color-surface] border border-[--color-border] mb-4">
            <Search size={24} className="text-[--color-text-muted]" />
          </div>
          <h3 className="text-lg font-medium mb-2">No rules found</h3>
          <p className="text-[--color-text-muted] text-sm mb-4">Try adjusting your search or filters</p>
          <button onClick={clearAll} className="text-sm text-[--color-accent] hover:underline">Clear all filters</button>
        </div>
      )}
    </div>
  );
}
