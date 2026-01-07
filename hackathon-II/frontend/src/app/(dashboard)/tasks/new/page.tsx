/**
 * Phase 2 Full-Stack Todo App - New Task Page
 *
 * Page for creating a new task.
 */

import { TaskForm } from "@/components/tasks/task-form";

export default function NewTaskPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <TaskForm mode="create" />
    </div>
  );
}
