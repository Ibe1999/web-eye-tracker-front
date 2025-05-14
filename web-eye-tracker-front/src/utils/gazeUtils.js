// src/utils/gazeUtils.js

/**
 * Calculates gaze position from eye data
 * @param {Object} eyeData - Object containing eye tracking data
 * @returns {Object|null} - The calculated gaze position or null
 */
export function calculateGaze(eyeData) {
    if (!eyeData) return null;
    
    // If we have both eyes, calculate average
    if (eyeData.leftEye && eyeData.rightEye) {
      return {
        x: (eyeData.leftEye.x + eyeData.rightEye.x) / 2,
        y: (eyeData.leftEye.y + eyeData.rightEye.y) / 2
      };
    }
    
    // If we only have one eye, use that
    if (eyeData.leftEye) {
      return {
        x: eyeData.leftEye.x,
        y: eyeData.leftEye.y
      };
    }
    
    if (eyeData.rightEye) {
      return {
        x: eyeData.rightEye.x,
        y: eyeData.rightEye.y
      };
    }
    
    // No valid eye data
    return null;
  }