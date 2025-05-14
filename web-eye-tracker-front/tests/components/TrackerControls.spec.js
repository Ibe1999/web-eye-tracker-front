// tests/components/TrackerControls.spec.js
import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/vue';
import TrackerControls from '@/components/TrackerControls.vue';

describe('TrackerControls', () => {
  it('renders all control buttons', () => {
    const { getByText } = render(TrackerControls, {
      props: {
        isTracking: false,
        isRecording: false
      }
    });
    
    expect(getByText(/start tracking/i)).toBeDefined();
    expect(getByText(/start recording/i)).toBeDefined();
    expect(getByText(/settings/i)).toBeDefined();
  });

  it('toggles tracking state when tracking button is clicked', async () => {
    const mockToggleTracking = vi.fn();
    
    const { getByText, rerender } = render(TrackerControls, {
      props: {
        isTracking: false,
        isRecording: false
      },
      global: {
        mocks: {},
        stubs: {},
        plugins: []
      }
    });
    
    const trackingButton = getByText(/start tracking/i);
    await fireEvent.click(trackingButton);
    
    // Rerender with updated props to simulate state change
    await rerender({ isTracking: true });
    
    expect(getByText(/stop tracking/i)).toBeDefined();
  });

  it('disables recording button when not tracking', () => {
    const { getByText } = render(TrackerControls, {
      props: {
        isTracking: false,
        isRecording: false
      }
    });
    
    const recordingButton = getByText(/start recording/i);
    expect(recordingButton.disabled).toBe(true);
  });

  it('enables recording button when tracking', () => {
    const { getByText } = render(TrackerControls, {
      props: {
        isTracking: true,
        isRecording: false
      }
    });
    
    const recordingButton = getByText(/start recording/i);
    expect(recordingButton.disabled).toBe(false);
  });
});