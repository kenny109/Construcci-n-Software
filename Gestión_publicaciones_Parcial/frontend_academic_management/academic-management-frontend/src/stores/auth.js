// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const userRole = computed(() => user.value?.role || 'user')
  const isAdmin = computed(() => userRole.value === 'admin')

  // Actions
  const initializeAuth = () => {
    const storedUser = authService.getStoredUser()
    if (storedUser && authService.isAuthenticated()) {
      user.value = storedUser
    }
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await authService.login(credentials)
      user.value = result.user
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await authService.register(userData)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    loading.value = true
    
    try {
      await authService.logout()
      user.value = null
      error.value = null
    } catch (err) {
      console.error('Error during logout:', err)
    } finally {
      loading.value = false
    }
  }

  const refreshUser = async () => {
    try {
      const userData = await authService.getCurrentUser()
      user.value = userData
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (err) {
      console.error('Error refreshing user:', err)
      await logout()
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    user,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    userRole,
    isAdmin,
    
    // Actions
    initializeAuth,
    login,
    register,
    logout,
    refreshUser,
    clearError
  }
})