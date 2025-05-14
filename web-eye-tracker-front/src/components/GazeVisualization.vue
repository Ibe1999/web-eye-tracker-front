<!-- src/components/GazeVisualization.vue -->
<template>
  <div class="gaze-visualization">
    <canvas ref="canvas" :width="width" :height="height"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue';

export default {
  name: 'GazeVisualization',
  props: {
    gazeData: {
      type: Object,
      default: null
    },
    width: {
      type: Number,
      default: 800
    },
    height: {
      type: Number,
      default: 600
    }
  },
  setup(props) {
    const canvas = ref(null);
    let context = null;
    let animationFrameId = null;
    
    onMounted(() => {
      if (canvas.value) {
        context = canvas.value.getContext('2d');
        drawGaze();
      }
    });
    
    onUnmounted(() => {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    });
    
    watch(() => props.gazeData, () => {
      drawGaze();
    });
    
    function drawGaze() {
      if (!context) return;
      
      // Clear canvas
      context.clearRect(0, 0, props.width, props.height);
      
      // Draw gaze point if data exists
      if (props.gazeData) {
        const x = props.gazeData.x * props.width;
        const y = props.gazeData.y * props.height;
        
        // Draw gaze point
        context.beginPath();
        context.arc(x, y, 10, 0, Math.PI * 2);
        context.fillStyle = 'rgba(255, 0, 0, 0.5)';
        context.fill();
        
        // Draw crosshair
        context.beginPath();
        context.moveTo(x - 15, y);
        context.lineTo(x + 15, y);
        context.moveTo(x, y - 15);
        context.lineTo(x, y + 15);
        context.strokeStyle = 'rgba(255, 0, 0, 0.8)';
        context.lineWidth = 2;
        context.stroke();
      }
      
      // Request next frame
      animationFrameId = requestAnimationFrame(drawGaze);
    }
    
    return { canvas };
  }
};
</script>

<style scoped>
.gaze-visualization {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

canvas {
  border: 1px solid #ccc;
  background-color: #f8f8f8;
}
</style> 
