<!-- src/components/TrackerControls.vue -->
<template>
  <div class="tracker-controls">
    <button 
      @click="$emit('toggleTracking')" 
      class="tracking-button"
    >
      {{ isTracking ? 'Stop Tracking' : 'Start Tracking' }}
    </button>
    
    <button 
      @click="$emit('toggleRecording')" 
      class="recording-button"
      :disabled="!isTracking"
    >
      {{ isRecording ? 'Stop Recording' : 'Start Recording' }}
    </button>
    
    <button @click="$emit('openSettings')" class="settings-button">
      Settings
    </button>
  </div>
</template>

<script>
export default {
  name: 'TrackerControls',
  props: {
    isTracking: {
      type: Boolean,
      default: false
    },
    isRecording: {
      type: Boolean,
      default: false
    }
  },
  emits: ['toggleTracking', 'toggleRecording', 'openSettings']
};
</script>

<style scoped>
.tracker-controls {
  display: flex;
  gap: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tracking-button {
  background-color: #4caf50;
  color: white;
}

.recording-button {
  background-color: #f44336;
  color: white;
}

.settings-button {
  background-color: #2196f3;
  color: white;
}
</style>
