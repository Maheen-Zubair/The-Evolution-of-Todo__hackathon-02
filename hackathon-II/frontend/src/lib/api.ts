/**
 * Phase 2 Full-Stack Todo App - API Client
 *
 * Fetch wrapper for backend API calls with JWT authentication.
 * Gets JWT from Better Auth and sends as Bearer token.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ApiError {
  detail: string;
}

class ApiClientError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiClientError";
    this.status = status;
    this.detail = detail;
  }
}

// Cache the token to avoid fetching on every request
let cachedToken: string | null = null;
let tokenExpiry: number = 0;

/**
 * Get JWT token from Better Auth
 */
async function getAuthToken(): Promise<string | null> {
  // Return cached token if still valid (with 30s buffer)
  if (cachedToken && Date.now() < tokenExpiry - 30000) {
    return cachedToken;
  }

  try {
    const response = await fetch("/api/auth/token", {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      console.error("Failed to get auth token:", response.status, response.statusText);
      cachedToken = null;
      return null;
    }

    const data = await response.json();
    if (data.token) {
      cachedToken = data.token;
      // Cache for 5 minutes
      tokenExpiry = Date.now() + 5 * 60 * 1000;
      console.log("Auth token retrieved successfully");
      return data.token;
    }
    console.warn("Auth token endpoint returned no token");
    return null;
  } catch (error) {
    console.error("Error fetching auth token:", error);
    cachedToken = null;
    return null;
  }
}

/**
 * Clear cached token (call on logout)
 */
export function clearAuthToken(): void {
  cachedToken = null;
  tokenExpiry = 0;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = "An error occurred";

    try {
      const error: ApiError = await response.json();
      detail = error.detail || detail;
    } catch {
      // Response may not be JSON
      detail = response.statusText || detail;
    }

    console.error(`API Error ${response.status}:`, detail);
    throw new ApiClientError(response.status, detail);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * Build headers with JWT token
 */
async function buildHeaders(): Promise<Record<string, string>> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  const token = await getAuthToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return headers;
}

/**
 * API client with methods for all task operations.
 * Automatically includes JWT token for authentication.
 */
export const api = {
  /**
   * GET request
   */
  async get<T>(endpoint: string, params?: Record<string, string | number | undefined>): Promise<T> {
    const url = new URL(`${API_BASE_URL}${endpoint}`);

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          url.searchParams.append(key, String(value));
        }
      });
    }

    const headers = await buildHeaders();
    const response = await fetch(url.toString(), {
      method: "GET",
      credentials: "include",
      headers,
    });

    return handleResponse<T>(response);
  },

  /**
   * POST request
   */
  async post<T>(endpoint: string, data?: unknown): Promise<T> {
    const headers = await buildHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      credentials: "include",
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });

    return handleResponse<T>(response);
  },

  /**
   * PUT request
   */
  async put<T>(endpoint: string, data: unknown): Promise<T> {
    const headers = await buildHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "PUT",
      credentials: "include",
      headers,
      body: JSON.stringify(data),
    });

    return handleResponse<T>(response);
  },

  /**
   * PATCH request
   */
  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    const headers = await buildHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "PATCH",
      credentials: "include",
      headers,
      body: JSON.stringify(data),
    });

    return handleResponse<T>(response);
  },

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string): Promise<T> {
    const headers = await buildHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "DELETE",
      credentials: "include",
      headers,
    });

    return handleResponse<T>(response);
  },
};

export { ApiClientError };
