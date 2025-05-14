// tests/utils/test-utils.js
import { render } from '@testing-library/vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia } from 'pinia';
import { vi } from 'vitest';

// Create a custom render function that includes router and store setup
export function renderWithSetup(component, options = {}) {
  // Create router instance
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/',
        component: () => import('@/views/HomeView.vue')
      },
      {
        path: '/calibration',
        component: () => import('@/views/CalibrationView.vue')
      },
      {
        path: '/tracking',
        component: () => import('@/views/TrackingView.vue')
      },
      {
        path: '/settings',
        component: () => import('@/views/SettingsView.vue')
      }
    ]
  });

  // Create pinia store
  const pinia = createPinia();

  // Custom render with plugins
  return render(component, {
    global: {
      plugins: [router, pinia],
      ...options?.global
    },
    ...options
  });
}

// Mock eye tracking data generator
export function mockEyeTrackingData(options = {}) {
  const defaults = {
    sampleCount: 10,
    noiseLevel: 0.05,
    baseX: 0.5,
    baseY: 0.5
  };
  
  const config = { ...defaults, ...options };
  
  return Array.from({ length: config.sampleCount }, (_, i) => {
    const noise = () => (Math.random() * 2 - 1) * config.noiseLevel;
    
    return {
      timestamp: Date.now() + i * 16, // ~60fps
      leftEye: {
        x: config.baseX + noise(),
        y: config.baseY + noise(),
        pupilSize: 0.3 + noise() * 0.1
      },
      rightEye: {
        x: config.baseX + noise(),
        y: config.baseY + noise(),
        pupilSize: 0.3 + noise() * 0.1
      },
      gaze: {
        x: config.baseX + noise(),
        y: config.baseY + noise()
      }
    };
  });
}

// Mock function for media stream
export function mockMediaStream() {
  return {
    getTracks: () => [{
      stop: vi.fn()
    }]
  };
}

// Mock WebRTC
export function setupWebRTCMocks() {
  global.MediaStream = vi.fn().mockImplementation(() => ({
    getTracks: () => [{
      stop: vi.fn()
    }]
  }));
  
  global.navigator.mediaDevices = {
    getUserMedia: vi.fn().mockResolvedValue(mockMediaStream())
  };
}