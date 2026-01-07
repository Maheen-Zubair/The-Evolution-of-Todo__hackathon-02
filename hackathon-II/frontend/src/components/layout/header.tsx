"use client";

/**
 * Phase 2 Full-Stack Todo App - Header Component
 *
 * Application header with logo and user menu.
 */

import Link from "next/link";
import { CheckSquare } from "lucide-react";
import { UserMenu } from "./user-menu";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div className="container flex h-14 items-center justify-between px-4 mx-auto max-w-4xl">
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <CheckSquare className="h-6 w-6 text-blue-600" />
          <span className="font-bold text-xl">Todo App</span>
        </Link>

        {/* User Menu */}
        <UserMenu />
      </div>
    </header>
  );
}
