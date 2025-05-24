<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">
          {{ autor ? 'Editar Autor' : 'Nuevo Autor' }}
        </h3>
        <button @click="$emit('close')" class="modal-close">✕</button>
      </div>

      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <form @submit.prevent="saveAutor">
        <div class="form-group">
          <label class="form-label">Nombre:</label>
          <input 
            v-model="form.nombre"
            type="text" 
            class="form-input"
            placeholder="Nombre del autor"
            required
            maxlength="100"
          >
        </div>

        <div class="form-group">
          <label class="form-label">Apellido:</label>
          <input 
            v-model="form.apellido"
            type="text" 
            class="form-input"
            placeholder="Apellido del autor"
            required
            maxlength="100"
          >
        </div>

        <div class="form-group">
          <label class="form-label">Nacionalidad:</label>
          <input 
            v-model="form.nacionalidad"
            type="text" 
            class="form-input"
            placeholder="País de origen"
            maxlength="100"
          >
        </div>

        <div class="form-group">
          <label class="form-label">Fecha de Nacimiento:</label>
          <input 
            v-model="form.fecha_nacimiento"
            type="date" 
            class="form-input"
            :max="maxDate"
          >
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancelar
          </button>
          <button 
            type="submit" 
            class="btn btn-success"
            :disabled="loading"
          >
            {{ loading ? 'Guardando...' : (autor ? 'Actualizar' : 'Crear') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'AutorForm',
  props: {
    autor: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: {
        nombre: '',
        apellido: '',
        nacionalidad: '',
        fecha_nacimiento: ''
      },
      error: '',
      loading: false
    }
  },
  computed: {
    maxDate() {
      // La fecha máxima es hoy
      return new Date().toISOString().split('T')[0]
    }
  },
  watch: {
    autor: {
      immediate: true,
      handler(newAutor) {
        if (newAutor) {
          this.form = {
            nombre: newAutor.nombre || '',
            apellido: newAutor.apellido || '',
            nacionalidad: newAutor.nacionalidad || '',
            fecha_nacimiento: newAutor.fecha_nacimiento || ''
          }
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    async saveAutor() {
      // Validaciones
      if (!this.form.nombre.trim()) {
        this.error = 'El nombre es requerido'
        return
      }
      
      if (!this.form.apellido.trim()) {
        this.error = 'El apellido es requerido'
        return
      }

      // Validar fecha de nacimiento si se proporciona
      if (this.form.fecha_nacimiento) {
        const fechaNacimiento = new Date(this.form.fecha_nacimiento)
        const hoy = new Date()
        
        if (fechaNacimiento > hoy) {
          this.error = 'La fecha de nacimiento no puede ser futura'
          return
        }
      }

      this.loading = true
      this.error = ''

      try {
        const data = {
          nombre: this.form.nombre.trim(),
          apellido: this.form.apellido.trim(),
          nacionalidad: this.form.nacionalidad.trim() || null,
          fecha_nacimiento: this.form.fecha_nacimiento || null
        }

        if (this.autor) {
          // Actualizar autor existente
          data.autor_id = this.autor.autor_id
          await api.updateAutor(data)
        } else {
          // Crear nuevo autor
          await api.createAutor(data)
        }
        
        this.$emit('saved')
        this.$emit('close')
      } catch (error) {
        console.error('Error al guardar autor:', error)
this.error = (error.response && error.response.data && error.response.data.error) || 'Error al guardar el autor'
      } finally {
        this.loading = false
      }
    },

    resetForm() {
      this.form = {
        nombre: '',
        apellido: '',
        nacionalidad: '',
        fecha_nacimiento: ''
      }
      this.error = ''
    }
  }
}
</script>