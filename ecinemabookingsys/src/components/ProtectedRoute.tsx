import { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router';

export function ProtectedRoute() {
  const [status, setStatus] = useState<'loading' | 'auth' | 'unauth'>('loading');

  useEffect(() => {
    fetch('/api/me', { credentials: 'include' })
      .then(res => setStatus(res.ok ? 'auth' : 'unauth'))
      .catch(() => setStatus('unauth'));
  }, []);

  if (status === 'loading') return null; // or a spinner
  if (status === 'unauth') return <Navigate to="/login" replace />;
  return <Outlet />;
}