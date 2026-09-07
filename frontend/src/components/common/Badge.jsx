import React from 'react';

export default function Badge({ status }) {
  const normStatus = (status || 'queued').toLowerCase();
  return (
    <span className={`badge badge-${normStatus}`}>
      {status || 'Unknown'}
    </span>
  );
}
