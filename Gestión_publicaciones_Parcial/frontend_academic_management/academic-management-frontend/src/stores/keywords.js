// src/stores/keywords.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { keywordsService } from '@/services/crud'

export const useKeywordsStore = defineStore('keywords', () => {
  const keywords = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentKeyword = ref(null)

  // Getters
  const totalKeywords = computed(() => keywords.value.length)
  const activeKeywords = computed(() => keywords.value.filter(keyword => keyword.is_active))

  // Actions
  const fetchKeywords = async () => {
    loading.value = true
    error.value = null
    
    try {
      const data = await keywordsService.getAll()
      keywords.value = data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching keywords:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchKeywordById = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const data = await keywordsService.getById(id)
      currentKeyword.value = data
      return data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching keyword:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createKeyword = async (keywordData) => {
    loading.value = true
    error.value = null
    
    try {
      const newKeyword = await keywordsService.create(keywordData)
      keywords.value.push(newKeyword)
      return newKeyword
    } catch (err) {
      error.value = err.message
      console.error('Error creating keyword:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateKeyword = async (id, keywordData) => {
    loading.value = true
    error.value = null
    
    try {
      const updatedKeyword = await keywordsService.update(id, keywordData)
      const index = keywords.value.findIndex(k => k.id === id)
      if (index !== -1) {
        keywords.value[index] = updatedKeyword
      }
      return updatedKeyword
    } catch (err) {
      error.value = err.message
      console.error('Error updating keyword:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteKeyword = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await keywordsService.delete(id)
      const index = keywords.value.findIndex(k => k.id === id)
      if (index !== -1) {
        keywords.value[index].is_active = false
      }
    } catch (err) {
      error.value = err.message
      console.error('Error deleting keyword:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  const clearCurrentKeyword = () => {
    currentKeyword.value = null
  }

  return {
    // State
    keywords,
    loading,
    error,
    currentKeyword,
    
    // Getters
    totalKeywords,
    activeKeywords,
    
    // Actions
    fetchKeywords,
    fetchKeywordById,
    createKeyword,
    updateKeyword,
    deleteKeyword,
    clearError,
    clearCurrentKeyword
  }
})