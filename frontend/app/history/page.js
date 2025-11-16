'use client'
import React, { useEffect, useState, useCallback } from 'react';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Function to load history from backend
  const loadHistory = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const user = JSON.parse(localStorage.getItem('user') || 'null');
      if (!user || !user.user_id) {
        setError('You must be logged in to view history.');
        setLoading(false);
        return;
      }
      const res = await fetch(`http://localhost:5000/history/${user.user_id}`);
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error || 'Failed to fetch history');
      }
      const data = await res.json();
      setHistory(data.history || []);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
    
    // Listen for historyUpdated event from upload pages
    const handleHistoryUpdate = () => {
      console.log('History update event received, refreshing...');
      loadHistory();
    };
    
    window.addEventListener('historyUpdated', handleHistoryUpdate);
    return () => window.removeEventListener('historyUpdated', handleHistoryUpdate);
  }, [loadHistory]);

  if (loading) return <div className="container mt-4">Loading history...</div>;
  if (error) return <div className="container mt-4">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>Your Test History</h2>
      {history.length === 0 && <p>No history found.</p>}
      <ul className="list-group">
        {history.map((h) => (
          <li key={h._id} className="list-group-item">
            <div className="d-flex justify-content-between">
              <strong>{h.kind}</strong>
              <small>{h.created_at || ''}</small>
            </div>
            <div className="mt-2">
              <pre style={{whiteSpace: 'pre-wrap'}}>{JSON.stringify(h.input, null, 2)}</pre>
            </div>
            <div className="mt-2">
              <details>
                <summary>Result</summary>
                <pre style={{whiteSpace: 'pre-wrap'}}>{JSON.stringify(h.result, null, 2)}</pre>
              </details>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
