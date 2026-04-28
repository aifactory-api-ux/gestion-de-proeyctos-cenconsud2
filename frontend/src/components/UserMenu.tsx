import React from 'react';
import { User } from '../types/models';

interface UserMenuProps {
  user: User;
  onLogout: () => void;
}

export function UserMenu({ user, onLogout }: UserMenuProps) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
      <div style={{ textAlign: 'right' }}>
        <strong>{user.full_name}</strong>
        <br />
        <small>{user.role}</small>
        <br />
        <small>{user.email}</small>
      </div>
      <button
        onClick={onLogout}
        style={{
          padding: '8px 16px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Logout
      </button>
    </div>
  );
}