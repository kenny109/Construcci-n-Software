// src/stores/countries.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { countriesService } from '@/services/crud'

export const useCountriesStore = defineStore('countries', () => {
  const countries = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentCountry = ref(null)

  // Getters
  const totalCountries = computed(() => countries.value.length)
  const activeCountries = computed(() => countries.value.filter(country => country.is_active))

  // Actions
  const fetchCountries = async () => {
    loading.value = true
    error.value = null
    
    try {
      const data = await countriesService.getAll()
      countries.value = data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching countries:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCountryById = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const data = await countriesService.getById(id)
      currentCountry.value = data
      return data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching country:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createCountry = async (countryData) => {
    loading.value = true
    error.value = null
    
    try {
      const newCountry = await countriesService.create(countryData)
      countries.value.push(newCountry)
      return newCountry
    } catch (err) {
      error.value = err.message
      console.error('Error creating country:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateCountry = async (id, countryData) => {
    loading.value = true
    error.value = null
    
    try {
      const updatedCountry = await countriesService.update(id, countryData)
      const index = countries.value.findIndex(c => c.id === id)
      if (index !== -1) {
        countries.value[index] = updatedCountry
      }
      return updatedCountry
    } catch (err) {
      error.value = err.message
      console.error('Error updating country:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteCountry = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await countriesService.delete(id)
      const index = countries.value.findIndex(c => c.id === id)
      if (index !== -1) {
        countries.value[index].is_active = false
      }
    } catch (err) {
      error.value = err.message
      console.error('Error deleting country:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  const clearCurrentCountry = () => {
    currentCountry.value = null
  }

  return {
    // State
    countries,
    loading,
    error,
    currentCountry,
    
    // Getters
    totalCountries,
    activeCountries,
    
    // Actions
    fetchCountries,
    fetchCountryById,
    createCountry,
    updateCountry,
    deleteCountry,
    clearError,
    clearCurrentCountry
  }
})