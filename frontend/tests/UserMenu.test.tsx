import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { UserMenu } from '../src/components/UserMenu';
import { User } from '../src/types/models';

const mockUser: User = {
  id: 1,
  email: 'admin@test.com',
  full_name: 'Admin User',
  role: 'admin',
};

describe('UserMenu', () => {
  it('renders user information correctly', () => {
    const onLogout = vi.fn();
    render(<UserMenu user={mockUser} onLogout={onLogout} />);

    expect(screen.getByText('Admin User')).toBeDefined();
    expect(screen.getByText('admin')).toBeDefined();
    expect(screen.getByText('admin@test.com')).toBeDefined();
  });

  it('renders logout button', () => {
    const onLogout = vi.fn();
    render(<UserMenu user={mockUser} onLogout={onLogout} />);

    const logoutButton = screen.getByRole('button', { name: /logout/i });
    expect(logoutButton).toBeDefined();
  });

  it('calls onLogout when button is clicked', () => {
    const onLogout = vi.fn();
    render(<UserMenu user={mockUser} onLogout={onLogout} />);

    const logoutButton = screen.getByRole('button', { name: /logout/i });
    fireEvent.click(logoutButton);
    expect(onLogout).toHaveBeenCalledTimes(1);
  });

  it('displays different roles correctly', () => {
    const regularUser: User = {
      id: 2,
      email: 'user@test.com',
      full_name: 'Regular User',
      role: 'user',
    };
    const onLogout = vi.fn();
    render(<UserMenu user={regularUser} onLogout={onLogout} />);

    expect(screen.getByText('Regular User')).toBeDefined();
    expect(screen.getByText('user')).toBeDefined();
  });
});
