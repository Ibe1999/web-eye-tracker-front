<!-- src/views/CalibrationView.vue -->
<template>
  <div class="calibration-container">
    <h1>Eye Tracker Calibration</h1>
    
    <div v-if="!isCalibrating && !isCompleted" class="start-section">
      <p>Please prepare for eye tracking calibration</p>
      <button @click="startCalibrationProcess">Start Calibration</button>
    </div>
    
    <div v-if="isCalibrating" class="calibration-area">
      <p>Follow the dot with your eyes</p>
      <div 
        v-for="(point, index) in calibrationPoints" 
        :key="index"
        class="calibration-point"
        :style="{ 
          left: `${point.x * 100}%`, 
          top: `${point.y * 100}%`,
          display: currentPointIndex === index ? 'block' : 'none'
        }"
      ></div>
      <button @click="completeCalibration">Complete</button>
    </div>
    
    <div v-if="isCompleted" class="results-section">
      <h2>Calibration {{ calibrationResult.valid ? 'Successful' : 'Failed' }}</h2>
      <p>Accuracy: {{ Math.round(calibrationResult.accuracy * 100) }}%</p>
      <button @click="resetCalibration">Recalibrate</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { validateCalibration, startCalibration, stopCalibration } from '@/utils/calibrationUtils';

export default {
  name: 'CalibrationView',
  setup() {
    const isCalibrating = ref(false);
    const isCompleted = ref(false);
    const currentPointIndex = ref(0);
    const calibrationResult = ref({ valid: false, accuracy: 0 });
    
    const calibrationPoints = [
      { x: 0.1, y: 0.1 },
      { x: 0.9, y: 0.1 },
      { x: 0.5, y: 0.5 },
      { x: 0.1, y: 0.9 },
      { x: 0.9, y: 0.9 }
    ];
    
    function startCalibrationProcess() {
      isCalibrating.value = true;
      currentPointIndex.value = 0;
      startCalibration();
    }
    
    function completeCalibration() {
      isCalibrating.value = false;
      isCompleted.value = true;
      stopCalibration();
      
      // Simulate calibration result
      calibrationResult.value = validateCalibration({
        points: calibrationPoints.map(point => ({
          ...point,
          precision: Math.random() * 0.3 + 0.7 // Random precision between 0.7 and 1.0
        }))
      });
    }
    
    function resetCalibration() {
      isCompleted.value = false;
    }
    
    return {
      isCalibrating,
      isCompleted,
      calibrationPoints,
      currentPointIndex,
      calibrationResult,
      startCalibrationProcess,
      completeCalibration,
      resetCalibration
    };
  }
};
</script>

<style scoped>
.calibration-container {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.calibration-area {
  position: relative;
  width: 100%;
  height: 80vh;
}

.calibration-point {
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: red;
  transform: translate(-50%, -50%);
}

button {
  padding: 10px 20px;
  margin: 10px;
  font-size: 16px;
  cursor: pointer;
}
</style>