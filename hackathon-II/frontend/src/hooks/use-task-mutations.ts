/**
 * Phase 2 Full-Stack Todo App - Task Mutation Hooks
 *
 * React Query hooks for creating, updating, and deleting tasks.
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Task, TaskCreate, TaskUpdate, TaskPatch } from "@/lib/types";

/**
 * Hook to create a new task.
 */
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: TaskCreate): Promise<Task> => {
      return api.post<Task>("/api/tasks", data);
    },
    onSuccess: () => {
      // Invalidate tasks list to refetch
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}

/**
 * Hook to update a task (full update).
 */
export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      taskId,
      data,
    }: {
      taskId: number;
      data: TaskUpdate;
    }): Promise<Task> => {
      return api.put<Task>(`/api/tasks/${taskId}`, data);
    },
    onSuccess: (task) => {
      // Update cache for this specific task
      queryClient.setQueryData(["task", task.id], task);
      // Invalidate tasks list to refetch
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}

/**
 * Hook to partially update a task.
 */
export function usePatchTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      taskId,
      data,
    }: {
      taskId: number;
      data: TaskPatch;
    }): Promise<Task> => {
      return api.patch<Task>(`/api/tasks/${taskId}`, data);
    },
    onSuccess: (task) => {
      queryClient.setQueryData(["task", task.id], task);
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}

/**
 * Hook to toggle task completion status.
 * Includes optimistic update for better UX.
 */
export function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      taskId,
      isComplete,
    }: {
      taskId: number;
      isComplete: boolean;
    }): Promise<Task> => {
      return api.patch<Task>(`/api/tasks/${taskId}`, { is_complete: isComplete });
    },
    // Optimistic update
    onMutate: async ({ taskId, isComplete }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["tasks"] });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData(["tasks"]);

      // Optimistically update
      queryClient.setQueriesData({ queryKey: ["tasks"] }, (old: unknown) => {
        if (!old || typeof old !== "object") return old;
        const data = old as { tasks: Task[] };
        return {
          ...data,
          tasks: data.tasks.map((t: Task) =>
            t.id === taskId ? { ...t, is_complete: isComplete } : t
          ),
        };
      });

      return { previousTasks };
    },
    onError: (_err, _variables, context) => {
      // Rollback on error
      if (context?.previousTasks) {
        queryClient.setQueryData(["tasks"], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}

/**
 * Hook to delete a task.
 * Includes optimistic update for better UX.
 */
export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (taskId: number): Promise<void> => {
      return api.delete(`/api/tasks/${taskId}`);
    },
    // Optimistic update
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ["tasks"] });

      const previousTasks = queryClient.getQueryData(["tasks"]);

      queryClient.setQueriesData({ queryKey: ["tasks"] }, (old: unknown) => {
        if (!old || typeof old !== "object") return old;
        const data = old as { tasks: Task[]; total: number };
        return {
          ...data,
          tasks: data.tasks.filter((t: Task) => t.id !== taskId),
          total: data.total - 1,
        };
      });

      return { previousTasks };
    },
    onError: (_err, _variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(["tasks"], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}
