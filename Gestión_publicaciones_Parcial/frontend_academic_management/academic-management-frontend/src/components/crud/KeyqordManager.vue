<!-- src/components/crud/KeywordManager.vue -->
<template>
  <div class="keyword-manager">
    <!-- Header con botón para agregar -->
    <div class="manager-header">
      <h2>Gestión de Palabras Clave</h2>
      <BaseButton @click="openCreateModal" variant="primary">
        + Agregar Palabra Clave
      </BaseButton>
    </div>

    <!-- Barra de búsqueda -->
    <div class="search-bar">
      <BaseInput
        v-model="searchTerm"
        placeholder="Buscar palabras clave..."
        type="search"
      />
    </div>

    <!-- Loading spinner -->
    <LoadingSpinner v-if="loading" />

    <!-- Grid de palabras clave -->
    <div v-else-if="!loading && filteredKeywords.length > 0" class="keywords-grid">
      <div 
        v-for="keyword in filteredKeywords" 
        :key="keyword.id" 
        :class="['keyword-card', { inactive: !keyword.is_active }]"
      >
        <div class="keyword-content">
          <h3 class="keyword-name">{{ keyword.name }}</h3>
          <div class="keyword-meta">
            <span :class="['status-badge', keyword.is_active ? 'active' : 'inactive']">
              {{ keyword.is_active ? 'Activo' : 'Inactivo' }}
            </span>
            <span class="date">{{ formatDate(keyword.created_at) }}</span>
          </div>
        </div>
        
        <div class="keyword-actions">
          <BaseButton @click="openEditModal(keyword)" variant="secondary" size="small">
            Editar
          </BaseButton>
          <BaseButton 
            v-if="keyword.is_active" 
            @click="confirmDelete(keyword)" 
            variant="danger" 
            size="small"
          >
            Eliminar
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Mensaje cuando no hay datos -->
    <div v-else class="empty-state">
      <p v-if="searchTerm">No se encontraron palabras clave que coincidan con "{{ searchTerm }}"</p>
      <p v-else>No hay palabras clave registradas</p>
      <BaseButton v-if="!searchTerm" @click="openCreateModal" variant="primary">
        Agregar Primera Palabra Clave
      </BaseButton>
    </div>

    <!-- Modal para crear/editar -->
    <BaseModal :show="showModal" @close="closeModal" :title="modalTitle">
      <form @submit.prevent="submitForm" class="keyword-form">
        <BaseInput
          v-model="form.name"
          label="Nombre de la Palabra Clave"
          placeholder="Ingrese la palabra clave"
          :error="errors.name"
          required
        />
        
        <div class="form-help">
          <small>Las palabras clave ayudan a categorizar y encontrar publicaciones académicas.</small>
        </div>

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
        <p>¿Está seguro que desea eliminar la palabra clave <strong>{{ keywordToDelete?.name }}</strong>?</p>
        <p class="warning">Esta acción no se puede deshacer y puede afectar las publicaciones asociadas.</p>
        
        <div class="form-actions">
          <BaseButton @click="closeDeleteModal" variant="secondary">
            Cancelar
          </BaseButton>
          <BaseButton @click="deleteKeyword" variant="danger" :loading="formLoading">
            Eliminar
          </BaseButton>
        </div>
      </div>
    </BaseModal>

    <!-- Mostrar errores -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Contador de resultados -->
    <div v-if="keywords.length > 0" class="results-counter">
      Mostrando {{ filteredKeywords.length }} de {{ keywords.length }} palabras clave
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useKeywordsStore } from '@/stores/keywords'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const keywordsStore = useKeywordsStore()

// State
const showModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const formLoading = ref(false)
const keywordToDelete = ref(null)
const searchTerm = ref('')

// Form data
const form = reactive({
  name: ''
})

const errors = reactive({
  name: ''
})

// Computed
const keywords = computed(() => keywordsStore.keywords)
const loading = computed(() => keywordsStore.loading)
const error = computed(() => keywordsStore.error)

const filteredKeywords = computed(() => {
  if (!searchTerm.value) return keywords.value
  
  return keywords.value.filter(keyword =>
    keyword.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const modalTitle = computed(() => {
  return isEditing.value ? 'Editar Palabra Clave' : 'Agregar Palabra Clave'
})

// Methods
const fetchKeywords = async () => {
  try {
    await keywordsStore.fetchKeywords()
  } catch (err) {
    console.error('Error loading keywords:', err)
  }
}

const openCreateModal = () => {
  resetForm()
  isEditing.value = false
  showModal.value = true
}

const openEditModal = (keyword) => {
  resetForm()
  form.name = keyword.name
  form.id = keyword.id
  isEditing.value = true
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const confirmDelete = (keyword) => {
  keywordToDelete.value = keyword
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  keywordToDelete.value = null
}

const resetForm = () => {
  form.name = ''
  form.id = null
  errors.name = ''
}

const validateForm = () => {
  let isValid = true
  
  if (!form.name.trim()) {
    errors.name = 'El nombre es requerido'
    isValid = false
  } else if (form.name.trim().length < 2) {
    errors.name = 'El nombre debe tener al menos 2 caracteres'
    isValid = false
  } else if (form.name.trim().length > 50) {
    errors.name = 'El nombre no puede tener más de 50 caracteres'
    isValid = false
  } else {
    // Verificar duplicados (excluyendo el registro actual si es edición)
    const existingKeyword = keywords.value.find(k => 
      k.name.toLowerCase() === form.name.trim().toLowerCase() && 
      k.id !== form.id &&
      k.is_active
    )
    
    if (existingKeyword) {
      errors.name = 'Ya existe una palabra clave con este nombre'
      isValid = false
    } else {
      errors.name = ''
    }
  }
  
  return isValid
}

const submitForm = async () => {
  if (!validateForm()) return
  
  formLoading.value = true
  
  try {
    const keywordData = {
      name: form.name.trim()
    }
    
    if (isEditing.value) {
      await keywordsStore.updateKeyword(form.id, keywordData)
    } else {
      await keywordsStore.createKeyword(keywordData)
    }
    
    closeModal()
  } catch (err) {
    console.error('Error saving keyword:', err)
  } finally {
    formLoading.value = false
  }
}

const deleteKeyword = async () => {
  if (!keywordToDelete.value) return
  
  formLoading.value = true
  
  try {
    await keywordsStore.deleteKeyword(keywordToDelete.value.id)
    closeDeleteModal()
  } catch (err) {
    console.error('Error deleting keyword:', err)
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
  fetchKeywords()
})
</script>

<style scoped>
.keyword-manager {
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

.search-bar {
  margin-bottom: 20px;
  max-width: 400px;
}

.keywords-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.keyword-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.keyword-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.keyword-card.inactive {
  opacity: 0.6;
  background-color: #f8f9fa;
}

.keyword-content {
  margin-bottom: 12px;
}

.keyword-name {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.keyword-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
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

.date {
  color: #6c757d;
}

.keyword-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
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

.keyword-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-help {
  margin-top: -8px;
}

.form-help small {
  color: #6c757d;
  font-style: italic;
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

.results-counter {
  text-align: center;
  color: #6c757d;
  font-size: 14px;
  margin-top: 16px;
}

@media (max-width: 768px) {
  .keywords-grid {
    grid-template-columns: 1fr;
  }
  
  .manager-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .keyword-actions {
    justify-content: center;
  }
}
</style>