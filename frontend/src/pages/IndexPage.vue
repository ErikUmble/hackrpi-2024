<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Location {
  latitude: number
  longitude: number
}

// State
const mediaRecorder = ref<MediaRecorder | null>(null)
const isRecording = ref<boolean>(false)
const recordingStatus = ref<string>('Ready to record')
const locationStatus = ref<string>('Getting location...')
const currentLocation = ref<Location | null>(null)
const audioChunks = ref<Blob[]>([])
const watchPositionId = ref<number | null>(null)
const playingAudio = ref<HTMLAudioElement | null>(null)

// Location handling
const setupLocationWatcher = (): void => {
  if ('geolocation' in navigator) {
    watchPositionId.value = navigator.geolocation.watchPosition(
      (position: GeolocationPosition) => {
        currentLocation.value = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }
        locationStatus.value = 'Location ready'
      },
      (error: GeolocationPositionError) => {
        locationStatus.value = `Location error: ${error.message}`
      }
    )
  } else {
    locationStatus.value = 'Geolocation not available'
  }
}

// Recording functions
const initializeRecorder = async (): Promise<void> => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mimeType = MediaRecorder.isTypeSupported('audio/wav') ? 'audio/wav' : 'audio/webm';
    mediaRecorder.value = new MediaRecorder(stream, { mimeType })
    
    mediaRecorder.value.ondataavailable = (event: BlobEvent) => {
      audioChunks.value.push(event.data)
    }
    
    mediaRecorder.value.onstop = async () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' })
      await sendRecording(audioBlob)
      audioChunks.value = []
    }
  } catch (error) {
    recordingStatus.value = `Microphone error: ${error instanceof Error ? error.message : String(error)}`
  }
}

const startRecording = (): void => {
  if (mediaRecorder.value && mediaRecorder.value.state === 'inactive') {
    mediaRecorder.value.start()
    isRecording.value = true
    recordingStatus.value = 'Recording...'
    if (playingAudio.value) {
      playingAudio.value.pause()
    }
  }
}

const stopRecording = (): void => {
  if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
    mediaRecorder.value.stop()
    isRecording.value = false
    recordingStatus.value = 'Processing...'
  }
}

const playAudio = (blob: Blob): void => {
  const audioUrl = URL.createObjectURL(blob)
  const audio = new Audio(audioUrl)
  audio.play()
  playingAudio.value = audio;
}

const sendRecording = async (blob: Blob): Promise<void> => {
  try {
    const formData = new FormData()
    formData.append('audio', blob);
    formData.append('longitude', JSON.stringify(currentLocation.value?.longitude));
    formData.append('latitude', JSON.stringify(currentLocation.value?.latitude));

    // Replace with your API endpoint
    const response = await fetch('/api', {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      recordingStatus.value = 'Recording sent successfully'
      const contentType = response.headers.get('content-type');
      if (contentType?.includes("application/json")) {
        const jsonResponse = await response.json();
        console.log(`redirecting to ${jsonResponse.link}`);
        window.open(jsonResponse.link, '_blank');
      } else if (contentType?.includes("text/html")) {
        const audioBlob = await response.blob();
        playAudio(audioBlob);
      }
    } else {
      throw new Error('Failed to send recording')
    }
  } catch (error) {
    recordingStatus.value = `Error sending recording: ${error instanceof Error ? error.message : String(error)}`
  }
}

// Lifecycle hooks
onMounted(() => {
  initializeRecorder()
  setupLocationWatcher()
})

onUnmounted(() => {
  if (watchPositionId.value) {
    navigator.geolocation.clearWatch(watchPositionId.value)
  }
  if (mediaRecorder.value?.stream) {
    mediaRecorder.value.stream.getTracks().forEach(track => track.stop())
  }
})
</script>

<template>
  <q-page class="flex flex-center column q-pa-md">
    <!-- Recording Status -->
    <div class="text-h6 q-mb-md">
      {{ recordingStatus }}
    </div>

    <!-- Record Button -->
    <q-btn
      round
      size="xl"
      color="primary"
      :icon="isRecording ? 'stop' : 'mic'"
      :class="{ 'recording-pulse': isRecording }"
      @mousedown="startRecording"
      @mouseup="stopRecording"
      @touchstart="startRecording"
      @touchend="stopRecording"
    />

    <!-- Location Status -->
    <div class="text-caption q-mt-md">
      {{ locationStatus }}
    </div>
  </q-page>
</template>

<style scoped>
.recording-pulse {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2);
  }
  70% {
    transform: scale(1.1);
    box-shadow: 0 0 0 10px rgba(0, 0, 0, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  }
}
</style>