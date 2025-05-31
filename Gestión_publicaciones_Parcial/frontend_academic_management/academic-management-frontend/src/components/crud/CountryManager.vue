<!-- src/components/crud/CountryManager.vue -->
<template>
  <div class="country-manager">
    <!-- Header con botón para agregar -->
    <div class="manager-header">
      <h2>Gestión de Países</h2>
      <BaseButton @click="openCreateModal" variant="primary">
        + Agregar País
      </BaseButton>
    </div>

    <!-- Loading spinner -->
    <LoadingSpinner v-if="loading" />

    <!-- Tabla de países -->
    <div v-else-if="!loading && countries.length > 0" class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Código</th>
            <th>Estado</th>
            <th>Fecha Creación</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="country in countries" :key="country.id" :class="{ inactive: !country.is_active }">
            <td>{{ country.name }}</td>
            <td>{{ country.code }}</td>
            <td>
              <span :class="['status-badge', country.is_active ? 'active' : 'inactive']">
                {{ country.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td>{{ formatDate(country.created_at) }}</td>
            <td class="actions">
              <BaseButton @click="openEditModal(country)" variant="secondary" size="small">
                Editar
              </BaseButton>
              <BaseButton 
                v-if="country.is_active" 
                @click="confirmDelete(country)" 
                variant="danger" 
                size="small"
              >
                Eliminar
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mensaje cuando no hay datos -->
    <div v-else class="empty-state">
      <p>No hay países registrados</p>
      <BaseButton @click="openCreateModal" variant="primary">
        Agregar Primer País
      </BaseButton>
    </div>

    <!-- Modal para crear/editar -->
    <BaseModal :show="showModal" @close="closeModal" :title="modalTitle">
      <form @submit.prevent="submitForm" class="country-form">
        <BaseInput
          v-model="form.name"
          label="Nombre del País"
          placeholder="Ingrese el nombre del país"
          :error="errors.name"
          required
        />
        
        <BaseInput
          v-model="form.code"
          label="Código del País"
          placeholder="PE, US, BR, etc."
          :error="errors.code"
          maxlength="2"
          required
        />

        <div class="form-actions">
          <BaseButton type="button" @click="closeModal" variant="secondary">
            Cancelar
          </BaseButton>
          <BaseButton type="submit" variant="primary" :loading="formLoading">
            {{ isEditing ? 'Actualizar' : 'Crear' }}
          </BaseButton>
        </div>
      </form>
    </BaseModal>

    <!-- Modal de confirmación para eliminar -->
    <BaseModal :show="showDeleteModal" @close="closeDeleteModal" title="Confirmar Eliminación">
      <div class="delete-confirmation">
        <p>¿Está seguro que desea eliminar el país <strong>{{ countryToDelete?.name }}</strong>?</p>
        <p class="warning">Esta acción no se puede deshacer.</p>
        
        <div class="form-actions">
          <BaseButton @click="closeDeleteModal" variant="secondary">
            Cancelar
          </BaseButton>
          <BaseButton @click="deleteCountry" variant="danger" :loading="formLoading">
            Eliminar
          </BaseButton>
        </div>
      </div>
    </BaseModal>

    <!-- Mostrar errores -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useCountriesStore } from '@/stores/countries'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const countriesStore = useCountriesStore()

// State
const showModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const formLoading = ref(false)
const countryToDelete = ref(null)

// Form data
const form = reactive({
  name: '',
  code: ''
})

const errors = reactive({
  name: '',
  code: ''
})

// Computed
const countries = computed(() => countriesStore.countries)
const loading = computed(() => countriesStore.loading)
const error = computed(() => countriesStore.error)

const modalTitle = computed(() => {
  return isEditing.value ? 'Editar País' : 'Agregar País'
})

// Methods
const fetchCountries = async () => {
  try {
    await countriesStore.fetchCountries()
  } catch (err) {
    console.error('Error loading countries:', err)
  }
}

const openCreateModal = () => {
  resetForm()
  isEditing.value = false
  showModal.value = true
}

const openEditModal = (country) => {
  resetForm()
  form.name = country.name
  form.code = country.code
  form.id = country.id
  isEditing.value = true
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const confirmDelete = (country) => {
  countryToDelete.value = country
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  countryToDelete.value = null
}

const resetForm = () => {
  form.name = ''
  form.code = ''
  form.id = null
  errors.name = ''
  errors.code = ''
}

const validateForm = () => {
  let isValid = true
  
  if (!form.name.trim()) {
    errors.name = 'El nombre es requerido'
    isValid = false
  } else {
    errors.name = ''
  }
  
  if (!form.code.trim()) {
    errors.code = 'El código es requerido'
    isValid = false
  } else if (form.code.length !== 2) {
    errors.code = 'El código debe tener exactamente 2 caracteres'
    isValid = false
  } else {
    errors.code = ''
  }
  
  return isValid
}

const submitForm = async () => {
  if (!validateForm()) return
  
  formLoading.value = true
  
  try {
    const countryData = {
      name: form.name.trim(),
      code: form.code.trim().toUpperCase()
    }
    
    if (isEditing.value) {
      await countriesStore.updateCountry(form.id, countryData)
    } else {
      await countriesStore.createCountry(countryData)
    }
    
    closeModal()
  } catch (err) {
    console.error('Error saving country:', err)
  } finally {
    formLoading.value = false
  }
}

const deleteCountry = async () => {
  if (!countryToDelete.value) return
  
  formLoading.value = true
  
  try {
    await countriesStore.deleteCountry(countryToDelete.value.id)
    closeDeleteModal()
  } catch (err) {
    console.error('Error deleting country:', err)
  } finally {
    formLoading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('es-ES')
}

// Lifecycle
onMounted(() => {
  fetchCountries()
})
</script>

<style scoped>
.country-manager {
  padding: 20px;
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.manager-header h2 {
  margin: 0;
  color: #333;
}

.table-container {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #555;
}

.data-table tr:hover {
  background-color: #f8f9fa;
}

.data-table tr.inactive {
  opacity: 0.6;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  margin-bottom: 20px;
  color: #666;
}

.country-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.delete-confirmation {
  text-align: center;
}

.delete-confirmation p {
  margin-bottom: 16px;
}

.delete-confirmation .warning {
  color: #dc3545;
  font-size: 14px;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
  margin-top: 16px;
}
</style>