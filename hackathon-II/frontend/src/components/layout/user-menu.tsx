"use client";

/**
 * Phase 2 Full-Stack Todo App - User Menu Component
 *
 * Dropdown menu with user info and signout button.
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import { LogOut, User, ChevronDown } from "lucide-react";
import { useSession, signOut } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";

export function UserMenu() {
  const router = useRouter();
  const { data: session } = useSession();
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSignOut = async () => {
    setIsLoading(true);
    try {
      await signOut();
      router.push("/signin");
      router.refresh();
    } catch (error) {
      console.error("Sign out error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!session?.user) {
    return null;
  }

  return (
    <div className="relative">
      <Button
        variant="ghost"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2"
      >
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
          <User className="h-4 w-4" />
        </div>
        <span className="hidden sm:inline-block max-w-[150px] truncate">
          {session.user.name || session.user.email}
        </span>
        <ChevronDown className="h-4 w-4" />
      </Button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown */}
          <div className="absolute right-0 mt-2 w-56 rounded-md border bg-white shadow-lg z-20">
            <div className="p-2 border-b">
              <p className="text-sm font-medium truncate">
                {session.user.name || "User"}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {session.user.email}
              </p>
            </div>

            <div className="p-1">
              <button
                onClick={handleSignOut}
                disabled={isLoading}
                className="flex w-full items-center space-x-2 rounded-md px-2 py-2 text-sm text-red-600 hover:bg-red-50 disabled:opacity-50"
              >
                <LogOut className="h-4 w-4" />
                <span>{isLoading ? "Signing out..." : "Sign out"}</span>
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
