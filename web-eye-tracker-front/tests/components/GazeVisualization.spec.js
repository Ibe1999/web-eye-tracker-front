// tests/components/GazeVisualization.spec.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render } from '@testing-library/vue';
import GazeVisualization from '@/components/GazeVisualization.vue';

// Mock canvas and context
const mockContext = {
  clearRect: vi.fn(),
  beginPath: vi.fn(),
  arc: vi.fn(),
  moveTo: vi.fn(),
  lineTo: vi.fn(),
  fill: vi.fn(),
  stroke: vi.fn()
};

// Mock canvas getContext
global.HTMLCanvasElement.prototype.getContext = () => mockContext;

// Mock requestAnimationFrame
global.requestAnimationFrame = vi.fn(cb => {
  cb();
  return 123; // Return a dummy ID
});

// Mock cancelAnimationFrame
global.cancelAnimationFrame = vi.fn();

describe('GazeVisualization', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders canvas element', () => {
    const { container } = render(GazeVisualization);
    
    const canvas = container.querySelector('canvas');
    expect(canvas).toBeDefined();
    expect(canvas.width).toBe(800);
    expect(canvas.height).toBe(600);
  });

  it('updates visualization when gaze data changes', async () => {
    const { rerender } = render(GazeVisualization, {
      props: {
        gazeData: { x: 0.5, y: 0.5 },
        width: 800,
        height: 600
      }
    });
    
    // Check if canvas methods were called
    expect(mockContext.clearRect).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeen