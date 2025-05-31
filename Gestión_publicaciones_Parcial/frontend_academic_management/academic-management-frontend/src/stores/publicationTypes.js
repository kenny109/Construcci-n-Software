// src/stores/publicationTypes.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { publicationTypesService } from '@/services/crud'

export const usePublicationTypesStore = defineStore('publicationTypes', () => {
  const publicationTypes = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentPublicationType = ref(null)

  // Getters
  const totalPublicationTypes = computed(() => publicationTypes.value.length)
  const activePublicationTypes = computed(() => publicationTypes.value.filter(type => type.is_active))

  // Actions
  const fetchPublicationTypes = async () => {
    loading.value = true
    error.value = null
    
    try {
      const data = await publicationTypesService.getAll()
      publicationTypes.value = data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching publication types:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPublicationTypeById = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const data = await publicationTypesService.getById(id)
      currentPublicationType.value = data
      return data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching publication type:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createPublicationType = async (publicationTypeData) => {
    loading.value = true
    error.value = null
    
    try {
      const newPublicationType = await publicationTypesService.create(publicationTypeData)
      publicationTypes.value.push(newPublicationType)
      return newPublicationType
    } catch (err) {
      error.value = err.message
      console.error('Error creating publication type:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updatePublicationType = async (id, publicationTypeData) => {
    loading.value = true
    error.value = null
    
    try {
      const updatedPublicationType = await publicationTypesService.update(id, publicationTypeData)
      const index = publicationTypes.value.findIndex(pt => pt.id === id)
      if (index !== -1) {
        publicationTypes.value[index] = updatedPublicationType
      }
      return updatedPublicationType
    } catch (err) {
      error.value = err.message
      console.error('Error updating publication type:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deletePublicationType = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await publicationTypesService.delete(id)
      const index = publicationTypes.value.findIndex(pt => pt.id === id)
      if (index !== -1) {
        publicationTypes.value[index].is_active = false
      }
    } catch (err) {
      error.value = err.message
      console.error('Error deleting publication type:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  const clearCurrentPublicationType = () => {
    currentPublicationType.value = null
  }

  return {
    // State
    publicationTypes,
    loading,
    error,
    currentPublicationType,
    
    // Getters
    totalPublicationTypes,
    activePublicationTypes,
    
    // Actions
    fetchPublicationTypes,
    fetchPublicationTypeById,
    createPublicationType,
    updatePublicationType,
    deletePublicationType,
    clearError,
    clearCurrentPublicationType
  }
})