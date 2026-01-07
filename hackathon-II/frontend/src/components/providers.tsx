"use client";

/**
 * Phase 2 Full-Stack Todo App - Application Providers
 *
 * Global providers for React Query and other context providers.
 */

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  // Create QueryClient instance only once per client session
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Stale time: 1 minute - data considered fresh for this duration
            staleTime: 60 * 1000,
            // Retry failed requests up to 3 times
            retry: 3,
            // Refetch on window focus for fresh data
            refetchOnWindowFocus: true,
          },
          mutations: {
            // Retry mutations once on failure
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
