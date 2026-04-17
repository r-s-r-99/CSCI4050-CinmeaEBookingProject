import { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router';

export function AdminRoute() {
  const [status, setStatus] = useState<'loading' | 'authorized' | 'unauthorized'>('loading');

  useEffect(() => {
    fetch('/api/me', { credentials: 'include' })
      .then(async res => {
        if (!res.ok) {
          setStatus('unauthorized');
          return;
        }

        const data = await res.json();

        // Check if user is admin
        if (data.role === 'admin') {
          setStatus('authorized');
        } else {
          setStatus('unauthorized');
        }
      })
      .catch(() => setStatus('unauthorized'));
  }, []);

  if (status === 'loading') return null;
  if (status === 'unauthorized') return <Navigate to="/" replace />;
  return <Outlet />;
}
