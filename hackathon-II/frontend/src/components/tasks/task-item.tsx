"use client";

/**
 * Phase 2 Full-Stack Todo App - Task Item Component
 *
 * Single task display with checkbox, title, and action buttons.
 */

import { useState } from "react";
import Link from "next/link";
import { Pencil, Trash2 } from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import type { Task } from "@/lib/types";

interface TaskItemProps {
  task: Task;
  onToggle?: (taskId: number, isComplete: boolean) => void;
  onDelete?: (taskId: number) => void;
}

export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    if (!onToggle || isToggling) return;
    setIsToggling(true);
    try {
      await onToggle(task.id, !task.is_complete);
    } finally {
      setIsToggling(false);
    }
  };

  return (
    <div
      className={`group flex items-start gap-3 p-4 rounded-lg border bg-white transition-all ${
        task.is_complete ? "opacity-60" : ""
      }`}
    >
      {/* Checkbox */}
      <Checkbox
        id={`task-${task.id}`}
        checked={task.is_complete}
        onCheckedChange={handleToggle}
        disabled={isToggling}
        className="mt-1"
      />

      {/* Content */}
      <div className="flex-1 min-w-0">
        <label
          htmlFor={`task-${task.id}`}
          className={`block font-medium cursor-pointer ${
            task.is_complete ? "line-through text-gray-500" : "text-gray-900"
          }`}
        >
          {task.title}
        </label>
        {task.description && (
          <p
            className={`mt-1 text-sm ${
              task.is_complete ? "text-gray-400" : "text-gray-600"
            }`}
          >
            {task.description}
          </p>
        )}
        <p className="mt-2 text-xs text-gray-400">
          {new Date(task.created_at).toLocaleDateString()}
        </p>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
        <Button variant="ghost" size="sm" asChild>
          <Link href={`/tasks/${task.id}`}>
            <Pencil className="h-4 w-4" />
            <span className="sr-only">Edit</span>
          </Link>
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onDelete?.(task.id)}
          className="text-red-500 hover:text-red-600 hover:bg-red-50"
        >
          <Trash2 className="h-4 w-4" />
          <span className="sr-only">Delete</span>
        </Button>
      </div>
    </div>
  );
}
