"use client";

/**
 * Root Page - Redirects to signin or dashboard
 *
 * This page handles the initial routing:
 * - Unauthenticated users -> /signin
 * - Authenticated users -> dashboard (shows task list)
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TaskList } from "@/components/tasks/task-list";
import { FilterButtons } from "@/components/tasks/filter-buttons";
import { DeleteConfirmDialog } from "@/components/tasks/delete-confirm-dialog";
import { useTasks } from "@/hooks/use-tasks";
import { useToggleTask, useDeleteTask } from "@/hooks/use-task-mutations";
import type { Task } from "@/lib/types";

type Filter = "all" | "pending" | "complete";

export default function HomePage() {
  const router = useRouter();
  const [filter, setFilter] = useState<Filter>("all");
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);
  const [mutationError, setMutationError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  const { data, isLoading, error } = useTasks({
    status: filter,
    sort: "created_at",
    order: "desc",
  });

  const toggleMutation = useToggleTask();
  const deleteMutation = useDeleteTask();

  // Check authentication on mount
  useEffect(() => {
    // If we get a 401 error, redirect to signin
    if (error && error.message?.includes("401")) {
      setIsAuthenticated(false);
      router.push("/signin");
      return;
    }

    // If data loads successfully, user is authenticated
    if (data) {
      setIsAuthenticated(true);
    }
  }, [data, error, router]);

  // Show loading state while checking auth
  if (isAuthenticated === null && isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  // If not authenticated, show redirect message
  if (isAuthenticated === false) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-500">Redirecting to sign in...</div>
      </div>
    );
  }

  // Calculate counts for filter buttons
  const counts = data
    ? {
        all: data.total,
        pending: data.tasks.filter((t) => !t.is_complete).length,
        complete: data.tasks.filter((t) => t.is_complete).length,
      }
    : undefined;

  // Handle toggle completion
  const handleToggle = async (taskId: number, isComplete: boolean) => {
    setMutationError(null);
    try {
      await toggleMutation.mutateAsync({ taskId, isComplete });
    } catch (err) {
      setMutationError(
        err instanceof Error ? err.message : "Failed to update task"
      );
    }
  };

  // Handle delete with confirmation
  const handleDeleteClick = (taskId: number) => {
    const task = data?.tasks.find((t) => t.id === taskId);
    if (task) {
      setTaskToDelete(task);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!taskToDelete) return;
    await deleteMutation.mutateAsync(taskToDelete.id);
    setTaskToDelete(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
              <p className="text-sm text-gray-500">
                {data?.total ?? 0} task{(data?.total ?? 0) !== 1 ? "s" : ""} total
              </p>
            </div>

            <Button asChild>
              <Link href="/tasks/new">
                <Plus className="h-4 w-4 mr-2" />
                New Task
              </Link>
            </Button>
          </div>

          {/* Filters */}
          <FilterButtons value={filter} onChange={setFilter} counts={counts} />

          {/* Error States */}
          {error && !error.message?.includes("401") && (
            <div className="p-4 rounded-lg border border-red-200 bg-red-50 text-red-700">
              <p className="font-medium">Failed to load tasks</p>
              <p className="text-sm mt-1">
                {error instanceof Error ? error.message : "An error occurred"}
              </p>
            </div>
          )}

          {mutationError && (
            <div className="p-4 rounded-lg border border-red-200 bg-red-50 text-red-700">
              <p className="font-medium">Operation failed</p>
              <p className="text-sm mt-1">{mutationError}</p>
              <button
                onClick={() => setMutationError(null)}
                className="text-sm underline mt-2"
              >
                Dismiss
              </button>
            </div>
          )}

          {/* Task List */}
          <TaskList
            tasks={data?.tasks ?? []}
            isLoading={isLoading}
            filter={filter}
            onToggle={handleToggle}
            onDelete={handleDeleteClick}
          />

          {/* Delete Confirmation Dialog */}
          <DeleteConfirmDialog
            isOpen={taskToDelete !== null}
            taskTitle={taskToDelete?.title ?? ""}
            onConfirm={handleDeleteConfirm}
            onCancel={() => setTaskToDelete(null)}
          />
        </div>
      </div>
    </div>
  );
}
