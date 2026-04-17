import { useEffect, useState } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router';

interface ProtectedRouteProps {
  requiredRole?: string; // e.g., 'admin' - if not specified, only auth is required
}

export function ProtectedRoute({ requiredRole }: ProtectedRouteProps) {
  const [status, setStatus] = useState<'loading' | 'auth' | 'unauth' | 'unauthorized'>('loading');
  const location = useLocation();

  useEffect(() => {
    fetch('/api/me', { credentials: 'include' })
      .then(async res => {
        if (!res.ok) {
          setStatus('unauth');
          return;
        }

        const data = await res.json();

        // If a specific role is required, check the user's role
        if (requiredRole && data.role !== requiredRole) {
          setStatus('unauthorized');
          return;
        }

        setStatus('auth');
      })
      .catch(() => setStatus('unauth'));
  }, [requiredRole]);

  if (status === 'loading') return null; // or a spinner
  if (status === 'unauth') return <Navigate to="/login" replace state={{ from: location }} />;
  if (status === 'unauthorized') return <Navigate to="/" replace />; // Redirect to home if unauthorized
  return <Outlet />;
}