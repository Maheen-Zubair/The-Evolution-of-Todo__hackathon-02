"use client";

/**
 * Phase 2 Full-Stack Todo App - Task Form Component
 *
 * Form for creating and editing tasks with validation.
 */

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { taskCreateSchema, taskUpdateSchema } from "@/lib/schemas";
import { useCreateTask, useUpdateTask } from "@/hooks/use-task-mutations";
import type { Task, TaskCreate, TaskUpdate } from "@/lib/types";

interface TaskFormProps {
  mode: "create" | "edit";
  task?: Task;
}

export function TaskForm({ mode, task }: TaskFormProps) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  const createMutation = useCreateTask();
  const updateMutation = useUpdateTask();

  const isCreate = mode === "create";
  const schema = isCreate ? taskCreateSchema : taskUpdateSchema;
  const isLoading = createMutation.isPending || updateMutation.isPending;

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<TaskCreate | TaskUpdate>({
    resolver: zodResolver(schema),
    defaultValues: task
      ? {
          title: task.title,
          description: task.description || "",
          is_complete: task.is_complete,
        }
      : {
          title: "",
          description: "",
          is_complete: false,
        },
  });

  // Watch for character counts
  const title = watch("title") || "";
  const description = watch("description") || "";

  // Update form when task changes (for edit mode)
  useEffect(() => {
    if (task && mode === "edit") {
      setValue("title", task.title);
      setValue("description", task.description || "");
      setValue("is_complete", task.is_complete);
    }
  }, [task, mode, setValue]);

  const onSubmit = async (data: TaskCreate | TaskUpdate) => {
    setError(null);

    try {
      if (isCreate) {
        await createMutation.mutateAsync(data as TaskCreate);
      } else if (task) {
        await updateMutation.mutateAsync({
          taskId: task.id,
          data: data as TaskUpdate,
        });
      }

      router.push("/");
      router.refresh();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An error occurred. Please try again."
      );
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{isCreate ? "Create Task" : "Edit Task"}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Title */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="title">Title</Label>
              <span
                className={`text-xs ${
                  title.length > 500 ? "text-red-500" : "text-gray-500"
                }`}
              >
                {title.length}/500
              </span>
            </div>
            <Input
              id="title"
              placeholder="Enter task title..."
              disabled={isLoading}
              {...register("title")}
            />
            {errors.title && (
              <p className="text-sm text-red-500">{errors.title.message}</p>
            )}
          </div>

          {/* Description */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="description">Description (optional)</Label>
              <span
                className={`text-xs ${
                  description.length > 2000 ? "text-red-500" : "text-gray-500"
                }`}
              >
                {description.length}/2000
              </span>
            </div>
            <textarea
              id="description"
              placeholder="Add more details..."
              disabled={isLoading}
              className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              {...register("description")}
            />
            {errors.description && (
              <p className="text-sm text-red-500">{errors.description.message}</p>
            )}
          </div>

          {/* Is Complete (edit mode only) */}
          {!isCreate && (
            <div className="flex items-center space-x-2">
              <Checkbox
                id="is_complete"
                checked={watch("is_complete")}
                onCheckedChange={(checked) =>
                  setValue("is_complete", checked === true)
                }
                disabled={isLoading}
              />
              <Label htmlFor="is_complete" className="cursor-pointer">
                Mark as complete
              </Label>
            </div>
          )}

          {/* Error display */}
          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 border border-red-200 rounded-md">
              {error}
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center gap-3 pt-4">
            <Button type="submit" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  {isCreate ? "Creating..." : "Saving..."}
                </>
              ) : isCreate ? (
                "Create Task"
              ) : (
                "Save Changes"
              )}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => router.back()}
              disabled={isLoading}
            >
              Cancel
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
