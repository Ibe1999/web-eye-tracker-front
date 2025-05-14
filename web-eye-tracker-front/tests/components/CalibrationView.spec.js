// tests/components/CalibrationView.spec.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent } from '@testing-library/vue';
import CalibrationView from '@/views/CalibrationView.vue';

// Mock dependencies
vi.mock('@/utils/calibrationUtils', () => ({
  validateCalibration: vi.fn().mockReturnValue({ valid: true, accuracy: 0.95 }),
  startCalibration: vi.fn(),
  stopCalibration: vi.fn()
}));

describe('CalibrationView', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the calibration page correctly', () => {
    const { getByText } = render(CalibrationView);
    
    expect(getByText(/eye tracker calibration/i)).toBeDefined();
    expect(getByText(/start calibration/i)).toBeDefined();
  });

  it('starts calibration when button is clicked', async () => {
    const { getByText } = render(CalibrationView);
    
    const startButton = getByText(/start calibration/i);
    await fireEvent.click(startButton);
    
    // Check for calibration in progress text
    expect(getByText(/follow the dot/i)).toBeDefined();
  });

  it('shows success message after successful calibration', async () => {
    const { getByText } = render(CalibrationView);
    
    // Start calibration
    const startButton = getByText(/start calibration/i);
    await fireEvent.click(startButton);
    
    // Complete calibration
    const completeButton = getByText(/complete/i);
    await fireEvent.click(completeButton);
    
    // Check for success message
    expect(getByText(/calibration successful/i)).toBeDefined();
    expect(getByText(/accuracy: 95%/i)).toBeDefined();
  });
});