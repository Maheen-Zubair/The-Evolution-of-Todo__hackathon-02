/**
 * Phase 2 Full-Stack Todo App - Tasks Hooks
 *
 * React Query hooks for fetching tasks data.
 */

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Task, TaskListResponse } from "@/lib/types";

interface UseTasksParams {
  status?: "all" | "complete" | "pending";
  limit?: number;
  offset?: number;
  sort?: "created_at" | "title";
  order?: "asc" | "desc";
}

/**
 * Hook to fetch all tasks for the current user.
 */
export function useTasks(params: UseTasksParams = {}) {
  const { status = "all", limit = 50, offset = 0, sort = "created_at", order = "desc" } = params;

  return useQuery({
    queryKey: ["tasks", { status, limit, offset, sort, order }],
    queryFn: async (): Promise<TaskListResponse> => {
      return api.get<TaskListResponse>("/api/tasks", {
        status,
        limit,
        offset,
        sort,
        order,
      });
    },
  });
}

/**
 * Hook to fetch a single task by ID.
 */
export function useTask(taskId: number | null) {
  return useQuery({
    queryKey: ["task", taskId],
    queryFn: async (): Promise<Task> => {
      if (taskId === null) {
        throw new Error("Task ID is required");
      }
      return api.get<Task>(`/api/tasks/${taskId}`);
    },
    enabled: taskId !== null,
  });
}
