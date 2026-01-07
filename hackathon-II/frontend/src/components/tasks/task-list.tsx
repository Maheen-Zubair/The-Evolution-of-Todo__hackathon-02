"use client";

/**
 * Phase 2 Full-Stack Todo App - Task List Component
 *
 * Maps TaskItem components for a list of tasks.
 */

import { TaskItem } from "./task-item";
import { EmptyState } from "./empty-state";
import { TaskListSkeleton } from "./task-list-skeleton";
import type { Task } from "@/lib/types";

interface TaskListProps {
  tasks: Task[];
  isLoading?: boolean;
  filter?: "all" | "complete" | "pending";
  onToggle?: (taskId: number, isComplete: boolean) => void;
  onDelete?: (taskId: number) => void;
}

export function TaskList({
  tasks,
  isLoading,
  filter = "all",
  onToggle,
  onDelete,
}: TaskListProps) {
  if (isLoading) {
    return <TaskListSkeleton />;
  }

  if (tasks.length === 0) {
    return <EmptyState filter={filter} />;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
