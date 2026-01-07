"use client";

/**
 * Phase 2 Full-Stack Todo App - Auth Form Component
 *
 * Reusable authentication form for signup and signin.
 * Features:
 * - Email/password/name fields
 * - Zod validation (min 8 char password)
 * - Loading state with spinner
 * - Inline error display (409 duplicate email, 401 invalid credentials)
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { signIn, signUp } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import Link from "next/link";

// Validation schemas
const signInSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

const signUpSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type SignInFormData = z.infer<typeof signInSchema>;
type SignUpFormData = z.infer<typeof signUpSchema>;

interface AuthFormProps {
  mode: "signin" | "signup";
}

export function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const isSignUp = mode === "signup";
  const schema = isSignUp ? signUpSchema : signInSchema;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpFormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: SignUpFormData) => {
    setError(null);
    setIsLoading(true);

    try {
      if (isSignUp) {
        const result = await signUp.email({
          email: data.email,
          password: data.password,
          name: data.name,
        });

        if (result.error) {
          // Handle duplicate email (409)
          if (result.error.status === 409) {
            setError("An account with this email already exists.");
          } else {
            setError(result.error.message || "Failed to create account.");
          }
          return;
        }
      } else {
        const result = await signIn.email({
          email: data.email,
          password: data.password,
        });

        if (result.error) {
          // Handle invalid credentials (401)
          if (result.error.status === 401) {
            setError("Invalid email or password.");
          } else {
            setError(result.error.message || "Failed to sign in.");
          }
          return;
        }
      }

      // Redirect to dashboard on success
      router.push("/");
      router.refresh();
    } catch {
      setError("An unexpected error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold">
          {isSignUp ? "Create an account" : "Sign in"}
        </CardTitle>
        <CardDescription>
          {isSignUp
            ? "Enter your details to create your account"
            : "Enter your credentials to access your tasks"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Name field (signup only) */}
          {isSignUp && (
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="John Doe"
                disabled={isLoading}
                {...register("name")}
              />
              {errors.name && (
                <p className="text-sm text-red-500">{errors.name.message}</p>
              )}
            </div>
          )}

          {/* Email field */}
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="john@example.com"
              disabled={isLoading}
              {...register("email")}
            />
            {errors.email && (
              <p className="text-sm text-red-500">{errors.email.message}</p>
            )}
          </div>

          {/* Password field */}
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder={isSignUp ? "Min. 8 characters" : "Enter your password"}
              disabled={isLoading}
              {...register("password")}
            />
            {errors.password && (
              <p className="text-sm text-red-500">{errors.password.message}</p>
            )}
          </div>

          {/* Error display */}
          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 border border-red-200 rounded-md">
              {error}
            </div>
          )}

          {/* Submit button with loading state */}
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                {isSignUp ? "Creating account..." : "Signing in..."}
              </>
            ) : isSignUp ? (
              "Create account"
            ) : (
              "Sign in"
            )}
          </Button>

          {/* Link to other auth page */}
          <p className="text-center text-sm text-gray-600">
            {isSignUp ? (
              <>
                Already have an account?{" "}
                <Link href="/signin" className="text-blue-600 hover:underline">
                  Sign in
                </Link>
              </>
            ) : (
              <>
                Don&apos;t have an account?{" "}
                <Link href="/signup" className="text-blue-600 hover:underline">
                  Sign up
                </Link>
              </>
            )}
          </p>
        </form>
      </CardContent>
    </Card>
  );
}
