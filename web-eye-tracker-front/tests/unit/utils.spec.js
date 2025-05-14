// tests/unit/utils.spec.js
import { describe, it, expect } from 'vitest';
import { calculateGaze } from '@/utils/gazeUtils';
import { formatTimestamp } from '@/utils/timeUtils';
import { validateCalibration } from '@/utils/calibrationUtils';

// Example unit test for gaze calculation utility
describe('Gaze Utils', () => {
  it('calculates gaze position correctly', () => {
    const eyeData = {
      leftEye: { x: 0.2, y: 0.3 },
      rightEye: { x: 0.4, y: 0.3 }
    };
    
    const result = calculateGaze(eyeData);
    
    expect(result).toBeDefined();
    expect(result.x).toBeCloseTo(0.3);
    expect(result.y).toBeCloseTo(0.3);
  });

  it('handles missing eye data gracefully', () => {
    const incompleteData = {
      leftEye: { x: 0.2, y: 0.3 }
      // Right eye data missing
    };
    
    const result = calculateGaze(incompleteData);
    
    // Should use available data or return a default
    expect(result).toBeDefined();
    expect(result.x).toBeCloseTo(0.2);
    expect(result.y).toBeCloseTo(0.3);
  });

  it('returns null for invalid input', () => {
    expect(calculateGaze(null)).toBeNull();
    expect(calculateGaze(undefined)).toBeNull();
    expect(calculateGaze({})).toBeNull();
  });
});

// Example unit test for time formatting utility
describe('Time Utils', () => {
  it('formats timestamps correctly', () => {
    const timestamp = 1650000000000; // Example timestamp
    const formatted = formatTimestamp(timestamp);
    
    expect(formatted).toMatch(/^\d{2}:\d{2}:\d{2}$/); // HH:MM:SS format
  });

  it('handles different timestamp formats', () => {
    expect(formatTimestamp(1650000000000)).toBeDefined();
    expect(formatTimestamp('2023-04-15T12:00:00')).toBeDefined();
    expect(formatTimestamp(new Date(2023, 3, 15))).toBeDefined();
  });

  it('returns placeholder for invalid timestamps', () => {
    expect(formatTimestamp(null)).toBe('--:--:--');
    expect(formatTimestamp('invalid')).toBe('--:--:--');
  });
});

// Example unit test for calibration validation utility
describe('Calibration Utils', () => {
  it('validates successful calibration', () => {
    const calibrationData = {
      points: [
        { x: 0.1, y: 0.1, precision: 0.95 },
        { x: 0.9, y: 0.1, precision: 0.92 },
        { x: 0.5, y: 0.5, precision: 0.98 },
        { x: 0.1, y: 0.9, precision: 0.94 },
        { x: 0.9, y: 0.9, precision: 0.93 }
      ]
    };
    
    const result = validateCalibration(calibrationData);
    
    expect(result.valid).toBe(true);
    expect(result.accuracy).toBeGreaterThan(0.9);
  });

  it('identifies failed calibration', () => {
    const poorCalibrationData = {
      points: [
        { x: 0.1, y: 0.1, precision: 0.95 },
        { x: 0.9, y: 0.1, precision: 0.92 },
        { x: 0.5, y: 0.5, precision: 0.4 },
        { x: 0.1, y: 0.9, precision: 0.3 }, 
        { x: 0.9, y: 0.9, precision: 0.93 }
      ]
    };
    
    const result = validateCalibration(poorCalibrationData);
    
    expect(result.valid).toBe(false);
    expect(result.accuracy).toBeLessThan(0.8);
    expect(result.failedPoints.length).toBe(2);
  });

  it('handles edge cases', () => {
    expect(validateCalibration(null)).toEqual({ valid: false, accuracy: 0, failedPoints: [] });
    expect(validateCalibration({ points: [] })).toEqual({ valid: false, accuracy: 0, failedPoints: [] });
  });
});