// src/utils/calibrationUtils.js

/**
 * Validates calibration data
 * @param {Object} calibrationData - The calibration data to validate
 * @returns {Object} - Validation results with valid flag and accuracy
 */
export function validateCalibration(calibrationData) {
    if (!calibrationData || !calibrationData.points || !calibrationData.points.length) {
      return { valid: false, accuracy: 0, failedPoints: [] };
    }
    
    const failedPoints = [];
    let totalPrecision = 0;
    
    for (const point of calibrationData.points) {
      if (point.precision < 0.7) {
        failedPoints.push(point);
      }
      totalPrecision += point.precision;
    }
    
    const averagePrecision = totalPrecision / calibrationData.points.length;
    const valid = averagePrecision > 0.8 && failedPoints.length <= 1;
    
    return {
      valid,
      accuracy: averagePrecision,
      failedPoints
    };
  }
  
  /**
   * Starts the calibration process
   */
  export function startCalibration() {
    // Implementation would connect to WebRTC and prepare calibration UI
    console.log('Starting calibration process');
  }
  
  /**
   * Stops the calibration process
   */
  export function stopCalibration() {
    // Implementation would stop the calibration process
    console.log('Stopping calibration process');
  }   