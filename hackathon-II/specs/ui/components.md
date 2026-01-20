---
title: UI Components and Pages for Responsive Todo Web Application
description: Component architecture and page layouts for Next.js App Router with TypeScript and Tailwind CSS.
version: "1.0"
status: draft
phase: 2
feature: ui-components
created: 2025-12-29
updated: 2025-12-29
authors:
  - Evolution of Todo Team
tags:
  - nextjs
  - react
  - typescript
  - tailwind
  - components
  - ui
dependencies:
  - next.js
  - react
  - tailwind-css
  - shadcn-ui
related:
  - specs/features/authentication.md
  - specs/api/rest-endpoints.md
---

# UI Components and Pages for Responsive Todo Web Application

## Overview

Component architecture and page layouts for Next.js App Router with TypeScript and Tailwind CSS.

**Target Audience**: Frontend developers building the React UI

**Focus**: Component hierarchy, state management, responsive design, accessibility

## Success Criteria

| ID | Criterion | Measurable Outcome |
|----|-----------|-------------------|
| SC-001 | Responsive design works | UI adapts to mobile/tablet/desktop |
| SC-002 | Auth flows complete | Users can signup, signin, signout |
| SC-003 | CRUD operations work | All task operations from UI |
| SC-004 | Loading states shown | Skeleton/spinner during async ops |
| SC-005 | Error handling visible | User-friendly error messages |
| SC-006 | Keyboard accessible | All actions reachable via keyboard |
| SC-007 | Fast initial load | LCP < 2.5s on 3G |

## Constraints

| Constraint | Requirement |
|------------|-------------|
| Framework | Next.js 16+ App Router |
| Language | TypeScript strict mode |
| Styling | Tailwind CSS v4 |
| Components | shadcn/ui library |
| State | React hooks + server actions |
| Forms | React Hook Form + Zod |
| Loading States | Skeleton loaders for lists, button spinners for actions |
| Error Display | Inline red text below forms/fields (no modals/toasts) |

## Out of Scope

- Dark mode toggle (future enhancement)
- Drag-and-drop task reordering
- Task categories/tags
- Due dates and reminders
- Offline support (PWA)

---

## Clarifications

### Session 2025-01-06

- Q: How should loading states and errors be displayed? → A: Inline feedback - skeleton loaders for lists, button spinners for actions, inline red text for errors (no modals/toasts)

---

## Page Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        PAGE STRUCTURE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  app/                                                            │
│  ├── (auth)/                    # Auth route group              │
│  │   ├── signin/page.tsx        # Sign in page                  │
│  │   ├── signup/page.tsx        # Sign up page                  │
│  │   └── layout.tsx             # Centered card layout          │
│  │                                                               │
│  ├── (dashboard)/               # Protected route group         │
│  │   ├── layout.tsx             # Dashboard layout with header  │
│  │   ├── page.tsx               # Task list (main dashboard)    │
│  │   └── tasks/                                                  │
│  │       ├── new/page.tsx       # Create task page              │
│  │       └── [id]/page.tsx      # Edit task page                │
│  │                                                               │
│  ├── layout.tsx                 # Root layout                   │
│  └── page.tsx                   # Landing/redirect              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPONENT HIERARCHY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  RootLayout                                                      │
│  └── AuthProvider                                                │
│      ├── (Auth Pages)                                            │
│      │   ├── SignInPage                                          │
│      │   │   └── AuthForm (mode="signin")                        │
│      │   └── SignUpPage                                          │
│      │       └── AuthForm (mode="signup")                        │
│      │                                                           │
│      └── (Dashboard)                                             │
│          └── DashboardLayout                                     │
│              ├── Header                                          │
│              │   ├── Logo                                        │
│              │   └── UserMenu                                    │
│              │       └── SignOutButton                           │
│              │                                                   │
│              └── TasksPage                                       │
│                  ├── TaskHeader                                  │
│                  │   ├── TaskCount                               │
│                  │   ├── FilterButtons                           │
│                  │   └── AddTaskButton                           │
│                  │                                               │
│                  ├── TaskList                                    │
│                  │   └── TaskItem (map)                          │
│                  │       ├── Checkbox                            │
│                  │       ├── TaskTitle                           │
│                  │       ├── EditButton                          │
│                  │       └── DeleteButton                        │
│                  │                                               │
│                  └── EmptyState                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### AuthForm

Authentication form for signin and signup.

```typescript
// components/auth/auth-form.tsx
interface AuthFormProps {
  mode: "signin" | "signup";
}

// Features:
// - Email and password fields
// - Name field (signup only)
// - Confirm password (signup only)
// - Form validation with Zod
// - Loading state during submission
// - Error message display
// - Link to alternate mode
```

**States**:
| State | Display |
|-------|---------|
| Idle | Form with submit button |
| Loading | Disabled form, spinner on button |
| Error | Red error message below form |
| Success | Redirect to dashboard |

---

### Header

Dashboard header with navigation and user menu.

```typescript
// components/layout/header.tsx
interface HeaderProps {
  user: {
    name: string;
    email: string;
  };
}

// Features:
// - App logo/title (links to dashboard)
// - User avatar or initials
// - Dropdown with user email
// - Sign out button
```

**Responsive Behavior**:
| Breakpoint | Layout |
|------------|--------|
| Mobile (< 640px) | Hamburger menu, stacked |
| Tablet (640-1024px) | Condensed header |
| Desktop (> 1024px) | Full header with all elements |

---

### TaskList

Container for task items with filtering.

```typescript
// components/tasks/task-list.tsx
interface TaskListProps {
  tasks: Task[];
  filter: "all" | "pending" | "complete";
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
}

// Features:
// - Maps over tasks to render TaskItems
// - Shows EmptyState when no tasks
// - Skeleton loading state
// - Optimistic updates
```

---

### TaskItem

Individual task display with actions.

```typescript
// components/tasks/task-item.tsx
interface TaskItemProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
}

// Features:
// - Checkbox for completion toggle
// - Task title (strikethrough when complete)
// - Optional description (truncated)
// - Edit button (pencil icon)
// - Delete button (trash icon) with confirmation
```

**Visual States**:
| State | Appearance |
|-------|------------|
| Pending | Normal text, unchecked |
| Complete | Strikethrough, checked, muted |
| Hovering | Highlighted background |
| Deleting | Fade out animation |

---

### TaskForm

Form for creating and editing tasks.

```typescript
// components/tasks/task-form.tsx
interface TaskFormProps {
  task?: Task;  // undefined for create, defined for edit
  onSubmit: (data: TaskFormData) => void;
  onCancel: () => void;
}

interface TaskFormData {
  title: string;
  description?: string;
}

// Features:
// - Title input (required, max 500 chars)
// - Description textarea (optional, max 2000 chars)
// - Character count indicators
// - Submit and Cancel buttons
// - Form validation with Zod
```

---

### EmptyState

Display when no tasks exist.

```typescript
// components/tasks/empty-state.tsx
interface EmptyStateProps {
  filter: "all" | "pending" | "complete";
}

// Messages:
// - all: "No tasks yet. Create your first task!"
// - pending: "All tasks complete! Great job!"
// - complete: "No completed tasks yet."
```

---

### FilterButtons

Toggle between task filters.

```typescript
// components/tasks/filter-buttons.tsx
interface FilterButtonsProps {
  current: "all" | "pending" | "complete";
  onChange: (filter: "all" | "pending" | "complete") => void;
  counts: {
    all: number;
    pending: number;
    complete: number;
  };
}

// Features:
// - Three toggle buttons: All, Pending, Complete
// - Shows count badge on each
// - Highlights active filter
```

---

### DeleteConfirmDialog

Confirmation modal for task deletion.

```typescript
// components/tasks/delete-confirm-dialog.tsx
interface DeleteConfirmDialogProps {
  taskTitle: string;
  isOpen: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

// Features:
// - Modal overlay
// - Warning icon
// - Task title in message
// - Cancel and Delete buttons
// - Delete button is destructive (red)
```

---

## Page Specifications

### Sign In Page (`/signin`)

```
┌────────────────────────────────────────────┐
│                                            │
│              [ Logo ]                      │
│                                            │
│         ┌──────────────────────┐          │
│         │   Sign In            │          │
│         │                      │          │
│         │   Email              │          │
│         │   ┌────────────────┐ │          │
│         │   │                │ │          │
│         │   └────────────────┘ │          │
│         │                      │          │
│         │   Password           │          │
│         │   ┌────────────────┐ │          │
│         │   │ ●●●●●●●●       │ │          │
│         │   └────────────────┘ │          │
│         │                      │          │
│         │   [ Sign In ]        │          │
│         │                      │          │
│         │   Don't have an      │          │
│         │   account? Sign up   │          │
│         └──────────────────────┘          │
│                                            │
└────────────────────────────────────────────┘
```

---

### Sign Up Page (`/signup`)

```
┌────────────────────────────────────────────┐
│                                            │
│              [ Logo ]                      │
│                                            │
│         ┌──────────────────────┐          │
│         │   Create Account     │          │
│         │                      │          │
│         │   Name               │          │
│         │   ┌────────────────┐ │          │
│         │   │                │ │          │
│         │   └────────────────┘ │          │
│         │                      │          │
│         │   Email              │          │
│         │   ┌────────────────┐ │          │
│         │   │                │ │          │
│         │   └────────────────┘ │          │
│         │                      │          │
│         │   Password           │          │
│         │   ┌────────────────┐ │          │
│         │   │ ●●●●●●●●       │ │          │
│         │   └────────────────┘ │          │
│         │                      │          │
│         │   [ Create Account ] │          │
│         │                      │          │
│         │   Already have an    │          │
│         │   account? Sign in   │          │
│         └──────────────────────┘          │
│                                            │
└────────────────────────────────────────────┘
```

---

### Dashboard Page (`/`)

```
┌────────────────────────────────────────────────────────────────┐
│  [ Logo ]  Todo App                          [ User ▼ ]        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   My Tasks (5)                              [ + Add Task ]     │
│                                                                │
│   [ All (5) ] [ Pending (3) ] [ Complete (2) ]                │
│                                                                │
│   ┌────────────────────────────────────────────────────────┐  │
│   │ ☐  Buy groceries                          [ ✏️ ] [ 🗑️ ] │  │
│   │    Get milk, eggs, and bread                            │  │
│   ├────────────────────────────────────────────────────────┤  │
│   │ ☐  Finish project report                  [ ✏️ ] [ 🗑️ ] │  │
│   ├────────────────────────────────────────────────────────┤  │
│   │ ☐  Call dentist                           [ ✏️ ] [ 🗑️ ] │  │
│   ├────────────────────────────────────────────────────────┤  │
│   │ ☑  Complete todo app spec    ────────     [ ✏️ ] [ 🗑️ ] │  │
│   ├────────────────────────────────────────────────────────┤  │
│   │ ☑  Review pull request       ────────     [ ✏️ ] [ 🗑️ ] │  │
│   └────────────────────────────────────────────────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

### Create/Edit Task Page (`/tasks/new`, `/tasks/[id]`)

```
┌────────────────────────────────────────────────────────────────┐
│  [ Logo ]  Todo App                          [ User ▼ ]        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   ← Back                                                       │
│                                                                │
│   Create New Task  /  Edit Task                                │
│                                                                │
│   Title *                                                      │
│   ┌────────────────────────────────────────────────────────┐  │
│   │                                                        │  │
│   └────────────────────────────────────────────────────────┘  │
│   0/500 characters                                             │
│                                                                │
│   Description                                                  │
│   ┌────────────────────────────────────────────────────────┐  │
│   │                                                        │  │
│   │                                                        │  │
│   │                                                        │  │
│   └────────────────────────────────────────────────────────┘  │
│   0/2000 characters                                            │
│                                                                │
│   [ Cancel ]  [ Save Task ]                                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## State Management

### Auth State (Better Auth Client)

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
});

// Hook usage in components:
const { user, session, signIn, signUp, signOut } = useSession();
```

### Task State (React Query / Server Actions)

```typescript
// hooks/use-tasks.ts
export function useTasks(filter: string) {
  return useQuery({
    queryKey: ["tasks", filter],
    queryFn: () => fetchTasks(filter),
  });
}

export function useCreateTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}
```

---

## Styling Guidelines

### Tailwind Theme

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: "hsl(var(--primary))",
        secondary: "hsl(var(--secondary))",
        destructive: "hsl(var(--destructive))",
        muted: "hsl(var(--muted))",
        accent: "hsl(var(--accent))",
      },
    },
  },
};
```

### Component Classes

| Component | Base Classes |
|-----------|-------------|
| Button Primary | `bg-primary text-primary-foreground hover:bg-primary/90` |
| Button Secondary | `bg-secondary text-secondary-foreground hover:bg-secondary/80` |
| Button Destructive | `bg-destructive text-destructive-foreground hover:bg-destructive/90` |
| Input | `border border-input bg-background px-3 py-2 text-sm` |
| Card | `rounded-lg border bg-card text-card-foreground shadow-sm` |

---

## Accessibility Requirements

| Requirement | Implementation |
|-------------|----------------|
| Keyboard Navigation | All interactive elements focusable |
| Focus Indicators | Visible focus ring on all buttons/inputs |
| Screen Reader Labels | aria-label on icon-only buttons |
| Color Contrast | WCAG AA minimum (4.5:1) |
| Error Announcements | aria-live regions for form errors |
| Skip Links | Skip to main content link |

---

## Testing Requirements

### Unit Tests (Vitest)

- [ ] AuthForm validates required fields
- [ ] TaskItem renders correct state
- [ ] FilterButtons updates on click
- [ ] EmptyState shows correct message

### Integration Tests (Playwright)

- [ ] User can sign up
- [ ] User can sign in
- [ ] User can create task
- [ ] User can toggle task completion
- [ ] User can edit task
- [ ] User can delete task with confirmation
- [ ] Filter buttons work correctly

### Accessibility Tests

- [ ] axe-core audit passes
- [ ] Keyboard-only navigation works
- [ ] Screen reader announcements correct

---

## Implementation Checklist

- [ ] Set up Next.js 16+ with App Router
- [ ] Configure Tailwind CSS v4
- [ ] Install shadcn/ui components
- [ ] Set up Better Auth client
- [ ] Create auth layout and pages
- [ ] Create dashboard layout
- [ ] Implement Header component
- [ ] Implement TaskList component
- [ ] Implement TaskItem component
- [ ] Implement TaskForm component
- [ ] Implement FilterButtons
- [ ] Implement EmptyState
- [ ] Implement DeleteConfirmDialog
- [ ] Add loading skeletons
- [ ] Add error boundaries
- [ ] Write component tests
- [ ] Write E2E tests
- [ ] Audit accessibility
