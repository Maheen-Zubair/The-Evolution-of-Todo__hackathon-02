/**
 * Phase 2 Full-Stack Todo App - Empty State Component
 *
 * Contextual empty state messages based on current filter.
 */

import Link from "next/link";
import { CheckCircle2, Circle, ListTodo, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  filter?: "all" | "pending" | "complete";
}

export function EmptyState({ filter = "all" }: EmptyStateProps) {
  const config = {
    all: {
      icon: ListTodo,
      title: "No tasks yet",
      description: "Create your first task to get started!",
      showAction: true,
    },
    pending: {
      icon: Circle,
      title: "No pending tasks",
      description: "All tasks are complete! Great job!",
      showAction: false,
    },
    complete: {
      icon: CheckCircle2,
      title: "No completed tasks",
      description: "Complete some tasks to see them here.",
      showAction: false,
    },
  };

  const { icon: Icon, title, description, showAction } = config[filter];

  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="rounded-full bg-gray-100 p-4 mb-4">
        <Icon className="h-8 w-8 text-gray-400" />
      </div>
      <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-500 mb-4">{description}</p>
      {showAction && (
        <Button asChild>
          <Link href="/tasks/new">
            <Plus className="h-4 w-4 mr-2" />
            Create Task
          </Link>
        </Button>
      )}
    </div>
  );
}
