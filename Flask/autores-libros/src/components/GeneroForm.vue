<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">
          {{ genero ? 'Editar Género' : 'Nuevo Género' }}
        </h3>
        <button @click="$emit('close')" class="modal-close">✕</button>
      </div>

      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <form @submit.prevent="saveGenero">
        <div class="form-group">
          <label class="form-label">Nombre del Género:</label>
          <input 
            v-model="form.nombre"
            type="text" 
            class="form-input"
            placeholder="Ej: Ficción, Drama, Ciencia Ficción, Romance"
            required
            maxlength="100"
          >
          <small style="color: #666; font-size: 0.9rem; margin-top: 5px; display: block;">
            Ingresa el nombre del género literario. Ejemplo: Ficción, No Ficción, Drama, Comedia, etc.
          </small>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancelar
          </button>
          <button 
            type="submit" 
            class="btn btn-success"
            :disabled="loading || !form.nombre.trim()"
          >
            {{ loading ? 'Guardando...' : (genero ? 'Actualizar' : 'Crear') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'GeneroForm',
  props: {
    genero: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: {
        nombre: ''
      },
      error: '',
      loading: false
    }
  },
  watch: {
    genero: {
      immediate: true,
      handler(newGenero) {
        if (newGenero) {
          this.form = {
            nombre: newGenero.nombre || ''
          }
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    async saveGenero() {
      // Validaciones
      if (!this.form.nombre.trim()) {
        this.error = 'El nombre del género es requerido'
        return
      }

      // Validar longitud mínima
      if (this.form.nombre.trim().length < 2) {
        this.error = 'El nombre del género debe tener al menos 2 caracteres'
        return
      }

      this.loading = true
      this.error = ''

      try {
        const data = {
          nombre: this.form.nombre.trim()
        }

        if (this.genero) {
          // Actualizar género existente
          data.genero_id = this.genero.genero_id
          await api.updateGenero(data)
        } else {
          // Crear nuevo género
          await api.createGenero(data)
        }
        
        this.$emit('saved')
        this.$emit('close')
      } catch (error) {
        console.error('Error al guardar género:', error)
        this.error = (error.response||error.response.data||error.response.data.error) || 'Error al guardar el género'
      } finally {
        this.loading = false
      }
    },

    resetForm() {
      this.form = {
        nombre: ''
      }
      this.error = ''
    }
  }
}
</script>