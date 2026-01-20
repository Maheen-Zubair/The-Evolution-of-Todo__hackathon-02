/**
 * Phase 2 Full-Stack Todo App - Task List Skeleton
 *
 * Loading skeleton for task list.
 */

export function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {[...Array(5)].map((_, i) => (
        <div
          key={i}
          className="flex items-start gap-3 p-4 rounded-lg border bg-white animate-pulse"
        >
          {/* Checkbox skeleton */}
          <div className="w-5 h-5 rounded bg-gray-200 mt-1" />

          {/* Content skeleton */}
          <div className="flex-1 space-y-2">
            <div className="h-5 bg-gray-200 rounded w-3/4" />
            <div className="h-4 bg-gray-100 rounded w-1/2" />
            <div className="h-3 bg-gray-100 rounded w-24" />
          </div>

          {/* Actions skeleton */}
          <div className="flex items-center gap-1">
            <div className="w-8 h-8 rounded bg-gray-100" />
            <div className="w-8 h-8 rounded bg-gray-100" />
          </div>
        </div>
      ))}
    </div>
  );
}
