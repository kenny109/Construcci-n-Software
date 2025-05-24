<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">
          {{ libro ? 'Editar Libro' : 'Nuevo Libro' }}
        </h3>
        <button @click="$emit('close')" class="modal-close">✕</button>
      </div>

      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <form @submit.prevent="saveLibro">
        <div class="form-group">
          <label class="form-label">Título:</label>
          <input 
            v-model="form.titulo"
            type="text" 
            class="form-input"
            placeholder="Título del libro"
            required
            maxlength="200"
          >
        </div>

        <div class="form-group">
          <label class="form-label">Año de Publicación:</label>
          <input 
            v-model.number="form.anio_publicacion"
            type="number" 
            class="form-input"
            placeholder="Año de publicación"
            :min="1000"
            :max="currentYear"
            required
          >
        </div>

        <div class="form-group">
          <label class="form-label">Autores:</label>
          <div v-if="loadingAutores" class="loading">Cargando autores...</div>
          <div v-else-if="autoresDisponibles.length === 0" class="alert alert-warning">
            No hay autores disponibles. Crea primero algunos autores.
          </div>
          <div v-else>
            <div 
              v-for="autor in autoresDisponibles" 
              :key="autor.autor_id"
              style="margin-bottom: 10px;"
            >
              <label style="display: flex; align-items: center; cursor: pointer;">
                <input 
                  type="checkbox" 
                  :value="autor.autor_id"
                  v-model="form.autores_ids"
                  class="form-checkbox"
                >
                {{ autor.nombre }} {{ autor.apellido }}
                <span v-if="autor.nacionalidad" style="color: #666; margin-left: 10px;">
                  ({{ autor.nacionalidad }})
                </span>
              </label>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Géneros:</label>
          <div v-if="loadingGeneros" class="loading">Cargando géneros...</div>
          <div v-else-if="generosDisponibles.length === 0" class="alert alert-warning">
            No hay géneros disponibles. Crea primero algunos géneros.
          </div>
          <div v-else>
            <div 
              v-for="genero in generosDisponibles" 
              :key="genero.genero_id"
              style="margin-bottom: 10px;"
            >
              <label style="display: flex; align-items: center; cursor: pointer;">
                <input 
                  type="checkbox" 
                  :value="genero.genero_id"
                  v-model="form.generos_ids"
                  class="form-checkbox"
                >
                {{ genero.nombre }}
              </label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancelar
          </button>
          <button 
            type="submit" 
            class="btn btn-success"
            :disabled="loading || !canSave"
          >
            {{ loading ? 'Guardando...' : (libro ? 'Actualizar' : 'Crear') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'LibroForm',
  props: {
    libro: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: {
        titulo: '',
        anio_publicacion: new Date().getFullYear(),
        autores_ids: [],
        generos_ids: []
      },
      autoresDisponibles: [],
      generosDisponibles: [],
      error: '',
      loading: false,
      loadingAutores: false,
      loadingGeneros: false
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    },
    canSave() {
      return this.form.titulo.trim() && 
             this.form.anio_publicacion && 
             this.form.autores_ids.length > 0 &&
             this.form.generos_ids.length > 0 &&
             this.autoresDisponibles.length > 0 &&
             this.generosDisponibles.length > 0
    }
  },
  watch: {
    libro: {
      immediate: true,
      handler(newLibro) {
        if (newLibro) {
          this.form = {
            titulo: newLibro.titulo || '',
            anio_publicacion: newLibro.anio_publicacion || new Date().getFullYear(),
            autores_ids: newLibro.autores ? newLibro.autores.map(a => a.autor_id) : [],
            generos_ids: newLibro.generos ? newLibro.generos.map(g => g.genero_id) : []
          }
        } else {
          this.resetForm()
        }
      }
    }
  },
  async created() {
    await Promise.all([
      this.loadAutores(),
      this.loadGeneros()
    ])
  },
  methods: {
    async loadAutores() {
      this.loadingAutores = true
      try {
        const response = await api.getAutores()
        this.autoresDisponibles = response.data
      } catch (error) {
        console.error('Error al cargar autores:', error)
        this.error = 'Error al cargar la lista de autores'
      } finally {
        this.loadingAutores = false
      }
    },

    async loadGeneros() {
      this.loadingGeneros = true
      try {
        const response = await api.getGeneros()
        this.generosDisponibles = response.data
      } catch (error) {
        console.error('Error al cargar géneros:', error)
        this.error = 'Error al cargar la lista de géneros'
      } finally {
        this.loadingGeneros = false
      }
    },

    async saveLibro() {
      // Validaciones
      if (!this.form.titulo.trim()) {
        this.error = 'El título es requerido'
        return
      }
      
      if (!this.form.anio_publicacion || this.form.anio_publicacion < 1000 || this.form.anio_publicacion > this.currentYear) {
        this.error = `El año de publicación debe estar entre 1000 y ${this.currentYear}`
        return
      }

      if (this.form.autores_ids.length === 0) {
        this.error = 'Debe seleccionar al menos un autor'
        return
      }

      if (this.form.generos_ids.length === 0) {
        this.error = 'Debe seleccionar al menos un género'
        return
      }

      this.loading = true
      this.error = ''

      try {
        const data = {
          titulo: this.form.titulo.trim(),
          anio_publicacion: this.form.anio_publicacion,
          autores_ids: this.form.autores_ids,
          generos_ids: this.form.generos_ids
        }

        if (this.libro) {
          // Actualizar libro existente
          data.libro_id = this.libro.libro_id
          await api.updateLibro(data)
        } else {
          // Crear nuevo libro
          await api.createLibro(data)
        }
        
        this.$emit('saved')
        this.$emit('close')
      } catch (error) {
        console.error('Error al guardar libro:', error)
this.error = (error.response && error.response.data && error.response.data.error) || 'Error al guardar el libro'
      } finally {
        this.loading = false
      }
    },

    resetForm() {
      this.form = {
        titulo: '',
        anio_publicacion: new Date().getFullYear(),
        autores_ids: [],
        generos_ids: []
      }
      this.error = ''
    }
  }
}
</script>