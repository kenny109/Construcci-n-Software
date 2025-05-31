<template>
  <div class="countries-view">
    <!-- Header Section -->
    <div class="view-header">
      <div class="header-info">
        <h2>Gestión de Países</h2>
        <p>Administra los países disponibles en el sistema</p>
      </div>
      <button @click="openCreateModal" class="btn-primary">
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
        </svg>
        Nuevo País
      </button>
    </div>

    <!-- Search and Filters -->
    <div class="filters-section">
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24">
          <path fill="currentColor" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"/>
        </svg>
        <input 
          v-model="searchTerm"
          type="text" 
          placeholder="Buscar países..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Cargando países...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path fill="currentColor" d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
      </svg>
      <p>{{ error }}</p>
      <button @click="fetchCountries" class="btn-secondary">Reintentar</button>
    </div>

    <!-- Countries Table -->
    <div v-else class="table-container">
      <div class="table-header">
        <h3>Países Registrados ({{ filteredCountries.length }})</h3>
      </div>
      
      <div class="table-wrapper">
        <table class="countries-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Código</th>
              <th>Estado</th>
              <th>Creado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="country in filteredCountries" :key="country.id" class="table-row">
              <td>
                <div class="country-info">
                  <div class="country-flag">{{ getFlagEmoji(country.code) }}</div>
                  <span class="country-name">{{ country.name }}</span>
                </div>
              </td>
              <td>
                <span class="country-code">{{ country.code }}</span>
              </td>
              <td>
                <span class="status-badge" :class="{ 'status-active': country.is_active, 'status-inactive': !country.is_active }">
                  {{ country.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td>
                <span class="date-text">{{ formatDate(country.created_at) }}</span>
              </td>
              <td>
                <div class="actions-group">
                  <button @click="openEditModal(country)" class="btn-icon btn-edit" title="Editar">
                    <svg viewBox="0 0 24 24" width="16" height="16">
                      <path fill="currentColor" d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"/>
                    </svg>
                  </button>
                  <button @click="confirmDelete(country)" class="btn-icon btn-delete" title="Eliminar">
                    <svg viewBox="0 0 24 24" width="16" height="16">
                      <path fill="currentColor" d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="filteredCountries.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" width="48" height="48">
            <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"/>
          </svg>
          <h3>No se encontraron países</h3>
          <p>{{ searchTerm ? 'No hay países que coincidan con tu búsqueda' : 'Aún no hay países registrados' }}</p>
        </div>
      </div>
    </div>

    <!-- Modal for Create/Edit -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ isEditing ? 'Editar País' : 'Nuevo País' }}</h3>
          <button @click="closeModal" class="btn-close">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="modal-form">
          <div class="form-group">
            <label for="name">Nombre del País *</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              placeholder="Ej: Perú"
              :disabled="formLoading"
            />
          </div>

          <div class="form-group">
            <label for="code">Código ISO (2 letras) *</label>
            <input
              id="code"
              v-model="form.code"
              type="text"
              required
              placeholder="Ej: PE"
              maxlength="2"
              pattern="[A-Z]{2}"
              :disabled="formLoading"
              @input="form.code = form.code.toUpperCase()"
            />
            <small class="form-help">Código de 2 letras en mayúsculas (ISO 3166-1)</small>
          </div>

          <div v-if="formError" class="error-message">
            {{ formError }}
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" :disabled="formLoading" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" :disabled="formLoading" class="btn-primary">
              <span v-if="formLoading" class="loading-spinner"></span>
              {{ isEditing ? 'Actualizar' : 'Crear' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useCountriesStore } from '@/stores/countries'

const countriesStore = useCountriesStore()

// Reactive state
const searchTerm = ref('')
const showModal = ref(false)
const isEditing = ref(false)
const currentCountry = ref(null)
const formLoading = ref(false)
const formError = ref('')

const form = reactive({
  name: '',
  code: ''
})

// Computed properties
const loading = computed(() => countriesStore.loading)
const error = computed(() => countriesStore.error)
const countries = computed(() => countriesStore.activeCountries)

const filteredCountries = computed(() => {
  if (!searchTerm.value) return countries.value
  
  const term = searchTerm.value.toLowerCase()
  return countries.value.filter(country => 
    country.name.toLowerCase().includes(term) ||
    country.code.toLowerCase().includes(term)
  )
})

// Methods
const fetchCountries = async () => {
  await countriesStore.fetchCountries()
}

const openCreateModal = () => {
  isEditing.value = false
  currentCountry.value = null
  resetForm()
  showModal.value = true
}

const openEditModal = (country) => {
  isEditing.value = true
  currentCountry.value = country
  form.name = country.name
  form.code = country.code
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
  formError.value = ''
}

const resetForm = () => {
  form.name = ''
  form.code = ''
}

const handleSubmit = async () => {
  formLoading.value = true
  formError.value = ''
  
  try {
    if (isEditing.value) {
      await countriesStore.updateCountry(currentCountry.value.id, {
        name: form.name,
        code: form.code
      })
    } else {
      await countriesStore.createCountry({
        name: form.name,
        code: form.code
      })
    }
    closeModal()
  } catch (err) {
    formError.value = err.message
  } finally {
    formLoading.value = false
  }
}

const confirmDelete = async (country) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el país "${country.name}"?`)) {
    try {
      await countriesStore.deleteCountry(country.id)
    } catch (err) {
      alert('Error al eliminar el país: ' + err.message)
    }
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getFlagEmoji = (countryCode) => {
  // Simple flag emoji mapping for common countries
  const flags = {
    'PE': '🇵🇪', 'US': '🇺🇸', 'ES': '🇪🇸', 'MX': '🇲🇽', 
    'AR': '🇦🇷', 'BR': '🇧🇷', 'CL': '🇨🇱', 'CO': '🇨🇴',
    'EC': '🇪🇨', 'BO': '🇧🇴', 'UY': '🇺🇾', 'PY': '🇵🇾'
  }
  return flags[countryCode] || '🏳️'
}

// Lifecycle
onMounted(() => {
  fetchCountries()
})
</script>

<style scoped>
.countries-view {
  max-width: 1200px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.header-info h2 {
  margin: 0 0 8px 0;
  color: #2d3748;
  font-size: 28px;
  font-weight: 600;
}

.header-info p {
  margin: 0;
  color: #718096;
  font-size: 16px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.filters-section {
  margin-bottom: 24px;
}

.search-box {
  position: relative;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #a0aec0;
}

.search-input {
  width: 100%;
  padding: 12px 12px 12px 44px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.loading-container, .error-container {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-color: rgb(175, 25, 25)}

</style>