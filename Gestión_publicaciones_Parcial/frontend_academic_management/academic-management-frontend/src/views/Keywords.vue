<!-- src/views/Keywords.vue -->
<template>
  <div class="keywords-view">
    <div class="header">
      <h1>Gestión de Palabras Clave</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        Agregar Palabra Clave
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="keywordsStore.loading" class="loading">
      <p>Cargando palabras clave...</p>
    </div>

    <!-- Error State -->
    <div v-if="keywordsStore.error" class="error">
      <p>Error: {{ keywordsStore.error }}</p>
      <button @click="keywordsStore.clearError" class="btn btn-secondary">
        Cerrar
      </button>
    </div>

    <!-- Keywords Table -->
    <div v-if="!keywordsStore.loading" class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Estado</th>
            <th>Fecha Creación</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="keyword in keywordsStore.activeKeywords" :key="keyword.id">
            <td>{{ keyword.name }}</td>
            <td>
              <span class="status active">Activo</span>
            </td>
            <td>{{ formatDate(keyword.created_at) }}</td>
            <td class="actions">
              <button @click="editKeyword(keyword)" class="btn btn-sm btn-secondary">
                Editar
              </button>
              <button @click="deleteKeyword(keyword.id)" class="btn btn-sm btn-danger">
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ showCreateModal ? 'Crear' : 'Editar' }} Palabra Clave</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="name">Nombre:</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                maxlength="50"
                class="form-input"
              />
            </div>
            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn btn-secondary">
                Cancelar
              </button>
              <button type="submit" class="btn btn-primary" :disabled="keywordsStore.loading">
                {{ showCreateModal ? 'Crear' : 'Actualizar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useKeywordsStore } from '@/stores/keywords'

const keywordsStore = useKeywordsStore()

// Modal states
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingKeyword = ref(null)

// Form data
const form = ref({
  name: ''
})

// Initialize
onMounted(() => {
  keywordsStore.fetchKeywords()
})

// Methods
const editKeyword = (keyword) => {
  editingKeyword.value = keyword
  form.value = {
    name: keyword.name
  }
  showEditModal.value = true
}

const deleteKeyword = async (id) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta palabra clave?')) {
    try {
      await keywordsStore.deleteKeyword(id)
    } catch (error) {
      console.error('Error deleting keyword:', error)
    }
  }
}

const submitForm = async () => {
  try {
    if (showCreateModal.value) {
      await keywordsStore.createKeyword(form.value)
    } else {
      await keywordsStore.updateKeyword(editingKeyword.value.id, form.value)
    }
    closeModal()
  } catch (error) {
    console.error('Error submitting form:', error)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingKeyword.value = null
  form.value = {
    name: ''
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}
</script>

<style scoped>
.keywords-view {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
  color: #333;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
  margin-right: 4px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  margin-bottom: 20px;
}

.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #495057;
}

.data-table tbody tr:hover {
  background-color: #f8f9fa;
}

.status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status.active {
  background-color: #d4edda;
  color: #155724;
}

.actions {
  white-space: nowrap;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>