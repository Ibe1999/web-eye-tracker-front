// src/utils/timeUtils.js

/**
 * Formats a timestamp to HH:MM:SS format
 * @param {number|string|Date} timestamp - The timestamp to format
 * @returns {string} - Formatted time string
 */
export function formatTimestamp(timestamp) {
    if (!timestamp) return '--:--:--';
    
    let date;
    
    try {
      if (timestamp instanceof Date) {
        date = timestamp;
      } else if (typeof timestamp === 'number') {
        date = new Date(timestamp);
      } else if (typeof timestamp === 'string') {
        date = new Date(timestamp);
      }
      
      if (isNaN(date.getTime())) {
        return '--:--:--';
      }
      
      return date.toTimeString().split(' ')[0];
    } catch (error) {
      return '--:--:--';
    }
  }