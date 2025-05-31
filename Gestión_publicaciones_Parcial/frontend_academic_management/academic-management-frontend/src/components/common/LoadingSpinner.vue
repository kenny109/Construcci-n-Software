<!-- src/components/common/LoadingSpinner.vue -->
<template>
  <div :class="containerClasses">
    <div :class="spinnerClasses">
      <svg
        class="animate-spin"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
    </div>
    <p v-if="text" :class="textClasses">{{ text }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['blue', 'gray', 'white', 'green', 'red'].includes(value)
  },
  centered: {
    type: Boolean,
    default: false
  },
  overlay: {
    type: Boolean,
    default: false
  }
})

const containerClasses = computed(() => {
  const baseClasses = ['flex', 'flex-col', 'items-center', 'justify-center']
  
  const centerClasses = props.centered ? ['w-full', 'h-full'] : []
  
  const overlayClasses = props.overlay
    ? [
        'fixed',
        'inset-0',
        'bg-white',
        'bg-opacity-75',
        'z-50'
      ]
    : []

  return [
    ...baseClasses,
    ...centerClasses,
    ...overlayClasses
  ].join(' ')
})

const spinnerClasses = computed(() => {
  const sizeClasses = {
    xs: ['w-4', 'h-4'],
    sm: ['w-6', 'h-6'],
    md: ['w-8', 'h-8'],
    lg: ['w-12', 'h-12'],
    xl: ['w-16', 'h-16']
  }

  const colorClasses = {
    blue: ['text-blue-600'],
    gray: ['text-gray-600'],
    white: ['text-white'],
    green: ['text-green-600'],
    red: ['text-red-600']
  }

  return [
    ...sizeClasses[props.size],
    ...colorClasses[props.color]
  ].join(' ')
})

const textClasses = computed(() => {
  const colorClasses = {
    blue: ['text-blue-600'],
    gray: ['text-gray-600'],
    white: ['text-white'],
    green: ['text-green-600'],
    red: ['text-red-600']
  }

  return [
    'mt-2',
    'text-sm',
    'font-medium',
    ...colorClasses[props.color]
  ].join(' ')
})
</script>