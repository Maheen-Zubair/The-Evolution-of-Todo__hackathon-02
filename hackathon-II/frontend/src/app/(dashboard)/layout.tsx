"use client";

/**
 * Phase 2 Full-Stack Todo App - Dashboard Layout
 *
 * Protected layout with header and auth check.
 */

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/auth-client";
import { Header } from "@/components/layout/header";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  // Redirect to signin if not authenticated
  useEffect(() => {
    if (!isPending && !session) {
      router.replace("/signin");
    }
  }, [session, isPending, router]);

  // Show loading state while checking auth
  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    );
  }

  // Don't render dashboard if not authenticated
  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto max-w-4xl px-4 py-8">{children}</main>
    </div>
  );
}
