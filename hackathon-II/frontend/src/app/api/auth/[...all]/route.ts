/**
 * Phase 2 Full-Stack Todo App - Better Auth API Routes
 *
 * Catch-all route handler for Better Auth endpoints.
 * Handles: /api/auth/signin, /api/auth/signup, /api/auth/signout, etc.
 */

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
