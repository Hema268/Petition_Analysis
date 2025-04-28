import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

test('renders petition submission form', () => {
  render(<App />);
  const linkElement = screen.getByText(/Submit a Petition/i);
  expect(linkElement).toBeInTheDocument();
});