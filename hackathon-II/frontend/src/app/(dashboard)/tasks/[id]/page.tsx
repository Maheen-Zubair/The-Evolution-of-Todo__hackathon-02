"use client";

/**
 * Phase 2 Full-Stack Todo App - Edit Task Page
 *
 * Page for editing an existing task.
 */

import { use } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TaskForm } from "@/components/tasks/task-form";
import { useTask } from "@/hooks/use-tasks";

export default function EditTaskPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const router = useRouter();
  const resolvedParams = use(params);
  const taskId = parseInt(resolvedParams.id, 10);

  const { data: task, isLoading, error } = useTask(taskId);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
      </div>
    );
  }

  if (error || !task) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="p-6 rounded-lg border border-red-200 bg-red-50 text-center">
          <p className="font-medium text-red-700">Task not found</p>
          <p className="text-sm text-red-600 mt-1">
            The task you&apos;re looking for doesn&apos;t exist or you don&apos;t have access to it.
          </p>
          <Button
            variant="outline"
            onClick={() => router.push("/")}
            className="mt-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <TaskForm mode="edit" task={task} />
    </div>
  );
}
