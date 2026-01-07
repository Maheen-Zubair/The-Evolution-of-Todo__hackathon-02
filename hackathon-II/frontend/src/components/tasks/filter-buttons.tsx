"use client";

/**
 * Phase 2 Full-Stack Todo App - Filter Buttons Component
 *
 * Toggle buttons for All/Pending/Complete task filters.
 */

import { Button } from "@/components/ui/button";

type Filter = "all" | "pending" | "complete";

interface FilterButtonsProps {
  value: Filter;
  onChange: (filter: Filter) => void;
  counts?: {
    all: number;
    pending: number;
    complete: number;
  };
}

export function FilterButtons({ value, onChange, counts }: FilterButtonsProps) {
  const filters: { key: Filter; label: string }[] = [
    { key: "all", label: "All" },
    { key: "pending", label: "Pending" },
    { key: "complete", label: "Complete" },
  ];

  return (
    <div className="flex items-center gap-2">
      {filters.map(({ key, label }) => (
        <Button
          key={key}
          variant={value === key ? "default" : "outline"}
          size="sm"
          onClick={() => onChange(key)}
          className="min-w-[80px]"
        >
          {label}
          {counts && (
            <span className="ml-1 text-xs opacity-70">({counts[key]})</span>
          )}
        </Button>
      ))}
    </div>
  );
}
