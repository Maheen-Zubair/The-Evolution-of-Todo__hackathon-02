/**
 * Phase 2 Full-Stack Todo App - JWT Token Endpoint
 *
 * Returns the JWT token for the current authenticated session.
 * The frontend API client calls this to get the Bearer token for backend requests.
 */

import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const headersList = await headers();

    // Get the session using Better Auth
    const session = await auth.api.getSession({
      headers: headersList,
    });

    if (!session) {
      return NextResponse.json(
        { error: "Not authenticated" },
        { status: 401 }
      );
    }

    // Get the JWT token using Better Auth's JWT plugin
    // The JWT plugin provides a getToken method that returns { token: string }
    const result = await auth.api.getToken({
      headers: headersList,
    });

    if (!result || !result.token) {
      return NextResponse.json(
        { error: "Could not generate token" },
        { status: 500 }
      );
    }

    return NextResponse.json({ token: result.token });
  } catch (error) {
    console.error("Error getting auth token:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
