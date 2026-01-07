# Phase 2 Todo App - Frontend

Next.js 16+ frontend with TypeScript, Tailwind CSS, shadcn/ui, and Better Auth.

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **State Management**: React Query (TanStack Query)
- **Authentication**: Better Auth
- **Form Handling**: React Hook Form + Zod
- **Icons**: Lucide React

## Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running on `http://localhost:8000`

## Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.local.example .env.local
   ```

   Edit `.env.local`:
   ```
   DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/todoapp?sslmode=require
   BETTER_AUTH_SECRET=your-256-bit-secret
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/             # Auth pages (signin, signup)
│   │   ├── (dashboard)/        # Protected dashboard pages
│   │   ├── api/auth/           # Better Auth API routes
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── auth/               # Auth components
│   │   ├── layout/             # Header, UserMenu
│   │   ├── tasks/              # Task components
│   │   └── ui/                 # shadcn/ui components
│   ├── hooks/                  # React Query hooks
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   ├── auth.ts             # Better Auth config
│   │   ├── auth-client.ts      # Client-side auth
│   │   ├── schemas.ts          # Zod validation
│   │   ├── types.ts            # TypeScript types
│   │   └── utils.ts            # Utilities
│   └── ...
├── public/                     # Static assets
├── .env.local                  # Environment variables
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Features

### Authentication
- Email/password signup and signin
- Session management via Better Auth
- Protected routes with automatic redirect

### Task Management
- Create, view, edit, and delete tasks
- Toggle completion status
- Filter by All/Pending/Complete
- Optimistic updates for better UX

### UI/UX
- Responsive design (mobile-first)
- Loading skeletons
- Inline error messages
- Character count indicators

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | Secret for JWT signing |
| `NEXT_PUBLIC_APP_URL` | Yes | Frontend URL |
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |

## API Integration

The frontend communicates with the FastAPI backend via:
- Cookie-based authentication (httpOnly JWT)
- REST API calls through `src/lib/api.ts`
- React Query for caching and state management
