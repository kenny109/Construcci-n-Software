<template>
  <div class="config-container">
    <div class="config-header">
      <h2>⚙️ Configuración del Sistema</h2>
      <p>Gestiona los elementos básicos del sistema académico</p>
    </div>

    <!-- Navegación de tabs -->
    <div class="config-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
      >
        {{ tab.icon }} {{ tab.name }}
      </button>
    </div>

    <!-- Contenido de cada tab -->
    <div class="config-content">
      
      <!-- Países -->
      <div v-if="activeTab === 'countries'" class="config-section">
        <div class="section-header">
          <h3>🌍 Gestión de Países</h3>
          <button @click="showCreateModal('countries')" class="btn-create">
            ➕ Nuevo País
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            v-model="searchTerms.countries"
            @input="handleSearch('countries')"
            placeholder="Buscar países..."
            class="search-input"
          >
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Código</th>
                <th>Fecha Creación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading.countries">
                <td colspan="4" class="loading">Cargando...</td>
              </tr>
              <tr v-else-if="!data.countries.length">
                <td colspan="4" class="no-data">No hay países registrados</td>
              </tr>
              <tr v-else v-for="country in data.countries" :key="country.id">
                <td>{{ country.name }}</td>
                <td>{{ country.code }}</td>
                <td>{{ formatDate(country.created_at) }}</td>
                <td class="actions">
                  <button @click="editItem('countries', country)" class="btn-edit">
                    ✏️ Editar
                  </button>
                  <button @click="deleteItem('countries', country.id)" class="btn-delete">
                    🗑️ Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Autores -->
      <div v-if="activeTab === 'authors'" class="config-section">
        <div class="section-header">
          <h3>👥 Gestión de Autores</h3>
          <button @click="showCreateModal('authors')" class="btn-create">
            ➕ Nuevo Autor
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            v-model="searchTerms.authors"
            @input="handleSearch('authors')"
            placeholder="Buscar autores..."
            class="search-input"
          >
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>Email</th>
                <th>ORCID</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading.authors">
                <td colspan="5" class="loading">Cargando...</td>
              </tr>
              <tr v-else-if="!data.authors.length">
                <td colspan="5" class="no-data">No hay autores registrados</td>
              </tr>
              <tr v-else v-for="author in data.authors" :key="author.id">
                <td>{{ author.first_name }}</td>
                <td>{{ author.last_name }}</td>
                <td>{{ author.email || 'N/A' }}</td>
                <td>{{ author.orcid_id || 'N/A' }}</td>
                <td class="actions">
                  <button @click="editItem('authors', author)" class="btn-edit">
                    ✏️ Editar
                  </button>
                  <button @click="deleteItem('authors', author.id)" class="btn-delete">
                    🗑️ Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tipos de Publicación -->
      <div v-if="activeTab === 'publication-types'" class="config-section">
        <div class="section-header">
          <h3>📑 Gestión de Tipos de Publicación</h3>
          <button @click="showCreateModal('publication-types')" class="btn-create">
            ➕ Nuevo Tipo
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            v-model="searchTerms.publicationTypes"
            @input="handleSearch('publication-types')"
            placeholder="Buscar tipos de publicación..."
            class="search-input"
          >
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Fecha Creación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading.publicationTypes">
                <td colspan="4" class="loading">Cargando...</td>
              </tr>
              <tr v-else-if="!data.publicationTypes.length">
                <td colspan="4" class="no-data">No hay tipos de publicación registrados</td>
              </tr>
              <tr v-else v-for="type in data.publicationTypes" :key="type.id">
                <td>{{ type.name }}</td>
                <td>{{ type.description || 'N/A' }}</td>
                <td>{{ formatDate(type.created_at) }}</td>
                <td class="actions">
                  <button @click="editItem('publication-types', type)" class="btn-edit">
                    ✏️ Editar
                  </button>
                  <button @click="deleteItem('publication-types', type.id)" class="btn-delete">
                    🗑️ Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Palabras Clave -->
      <div v-if="activeTab === 'keywords'" class="config-section">
        <div class="section-header">
          <h3>🏷️ Gestión de Palabras Clave</h3>
          <button @click="showCreateModal('keywords')" class="btn-create">
            ➕ Nueva Palabra Clave
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            v-model="searchTerms.keywords"
            @input="handleSearch('keywords')"
            placeholder="Buscar palabras clave..."
            class="search-input"
          >
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Fecha Creación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading.keywords">
                <td colspan="3" class="loading">Cargando...</td>
              </tr>
              <tr v-else-if="!data.keywords.length">
                <td colspan="3" class="no-data">No hay palabras clave registradas</td>
              </tr>
              <tr v-else v-for="keyword in data.keywords" :key="keyword.id">
                <td>{{ keyword.name }}</td>
                <td>{{ formatDate(keyword.created_at) }}</td>
                <td class="actions">
                  <button @click="editItem('keywords', keyword)" class="btn-edit">
                    ✏️ Editar
                  </button>
                  <button @click="deleteItem('keywords', keyword.id)" class="btn-delete">
                    🗑️ Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- Modal para crear/editar -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveItem">
            
            <!-- Formulario para países -->
            <div v-if="modalType === 'countries'">
              <div class="form-group">
                <label>Nombre del País *</label>
                <input 
                  v-model="currentItem.name" 
                  type="text" 
                  required 
                  class="form-input"
                  placeholder="Ej: Perú"
                >
              </div>
              <div class="form-group">
                <label>Código del País *</label>
                <input 
                  v-model="currentItem.code" 
                  type="text" 
                  required 
                  class="form-input"
                  placeholder="Ej: PE"
                  maxlength="3"
                >
              </div>
            </div>

            <!-- Formulario para autores -->
            <div v-if="modalType === 'authors'">
              <div class="form-group">
                <label>Nombre *</label>
                <input 
                  v-model="currentItem.first_name" 
                  type="text" 
                  required 
                  class="form-input"
                  placeholder="Nombre del autor"
                >
              </div>
              <div class="form-group">
                <label>Apellido *</label>
                <input 
                  v-model="currentItem.last_name" 
                  type="text" 
                  required 
                  class="form-input"
                  placeholder="Apellido del autor"
                >
              </div>
              <div class="form-group">
                <label>Email</label>
                <input 
                  v-model="currentItem.email" 
                  type="email" 
                  class="form-input"
                  placeholder="email@ejemplo.com"
                >
              </div>
              <div class="form-group">
                <label>ORCID ID</label>
                <input 
                  v-model="currentItem.orcid_id" 
                  type="text" 
                  class="form-input"
                  placeholder="0000-0000-0000-0000"
                >
              </div>
              <div class="form-group">
                <label>Afiliación</label>
                <input 
                  v-model="currentItem.affiliation" 
                  type="text" 
                  class="form-input"
                  placeholder="Universidad o institución"
                >
              </div>
            </div>

            <!-- Formulario para tipos de publicación -->
            <div v-if="modalType === 'publication-types'">
              <div class="form-group">
                <label>Nombre del Tipo *</label>
                <input 
                  v-model="currentItem.name" 
                  type="text" 
                  required 
                  class="form-input"
                  placeholder="Ej: Artículo de Journal"
                >
              </div>
              <div class="form-group">
                <label>Descripción *</label>
                <textarea 
                  v-model="currentItem.description" 
                  required 
                  class="form-input"
                  placeholder="Descripción del tipo de publicación"
                  rows="3"
                ></textarea>
              </div>
            </div>

            <!-- Formulario para palabras clave -->
            <div v-if="modalType === 'keywords'">
              <div class="form-group">
                <label>Nombre de la Palabra Clave *</label>
                <input 
                  v-model="currentItem.name" 
                  type="text" 
                  required 
                  class="form-input"
                  placeholder="Ej: Machine Learning"
                >
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn-cancel">
                Cancelar
              </button>
              <button type="submit" class="btn-save" :disabled="saving">
                {{ saving ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ConfigComponent',
  data() {
    return {
      activeTab: 'countries',
      showModal: false,
      modalType: null,
      modalTitle: '',
      currentItem: {},
      saving: false,
      isEditing: false,
      
      tabs: [
        { id: 'countries', name: 'Países', icon: '🌍' },
        { id: 'authors', name: 'Autores', icon: '👥' },
        { id: 'publication-types', name: 'Tipos de Publicación', icon: '📑' },
        { id: 'keywords', name: 'Palabras Clave', icon: '🏷️' }
      ],
      
      data: {
        countries: [],
        authors: [],
        publicationTypes: [],
        keywords: []
      },
      
      loading: {
        countries: false,
        authors: false,
        publicationTypes: false,
        keywords: false
      },
      
      searchTerms: {
        countries: '',
        authors: '',
        publicationTypes: '',
        keywords: ''
      },
      
      searchTimeouts: {}
    }
  },
  
  async mounted() {
    await this.loadData(this.activeTab)
  },
  
  methods: {
    async loadData(type) {
      this.loading[type] = true
      
      try {
        let response
        const searchTerm = this.searchTerms[type] || ''
        
        switch (type) {
          case 'countries':
            response = await api.getCountries({ search: searchTerm })
            this.data.countries = response.data || []
            break
          case 'authors':
            response = await api.getAuthors({ search: searchTerm })
            this.data.authors = response.data || []
            break
          case 'publication-types':
            response = await api.getPublicationTypes({ search: searchTerm })
            this.data.publicationTypes = response.data || []
            break
          case 'keywords':
            response = await api.getKeywords({ search: searchTerm })
            this.data.keywords = response.data || []
            break
        }
      } catch (error) {
        console.error(`Error cargando ${type}:`, error)
        this.$emit('show-error', `Error al cargar ${type}`)
      } finally {
        this.loading[type] = false
      }
    },
    
    showCreateModal(type) {
      this.modalType = type
      this.isEditing = false
      this.currentItem = {}
      this.modalTitle = `Crear ${this.getTypeTitle(type)}`
      this.showModal = true
    },
    
    editItem(type, item) {
      this.modalType = type
      this.isEditing = true
      this.currentItem = { ...item }
      this.modalTitle = `Editar ${this.getTypeTitle(type)}`
      this.showModal = true
    },
    
    async saveItem() {
      this.saving = true
      
      try {
        if (this.isEditing) {
          await this.updateItem()
        } else {
          await this.createItem()
        }
        
        this.closeModal()
        await this.loadData(this.modalType)
        this.$emit('show-success', 
          `${this.getTypeTitle(this.modalType)} ${this.isEditing ? 'actualizado' : 'creado'} exitosamente`
        )
      } catch (error) {
        console.error('Error guardando:', error)
        this.$emit('show-error', error.message)
      } finally {
        this.saving = false
      }
    },
    
    async createItem() {
      switch (this.modalType) {
        case 'countries':
          await api.createCountry(this.currentItem)
          break
        case 'authors':
          await api.createAuthor(this.currentItem)
          break
        case 'publication-types':
          await api.createPublicationType(this.currentItem)
          break
        case 'keywords':
          await api.createKeyword(this.currentItem)
          break
      }
    },
    
    async updateItem() {
      switch (this.modalType) {
        case 'countries':
          await api.updateCountry(this.currentItem.id, this.currentItem)
          break
        case 'authors':
          await api.updateAuthor(this.currentItem.id, this.currentItem)
          break
        case 'publication-types':
          await api.updatePublicationType(this.currentItem.id, this.currentItem)
          break
        case 'keywords':
          await api.updateKeyword(this.currentItem.id, this.currentItem)
          break
      }
    },
    
    async deleteItem(type, id) {
      if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
        return
      }
      
      try {
        switch (type) {
          case 'countries':
            await api.deleteCountry(id)
            break
          case 'authors':
            await api.deleteAuthor(id)
            break
          case 'publication-types':
            await api.deletePublicationType(id)
            break
          case 'keywords':
            await api.deleteKeyword(id)
            break
        }
        
        await this.loadData(type)
        this.$emit('show-success', `${this.getTypeTitle(type)} eliminado exitosamente`)
      } catch (error) {
        console.error('Error eliminando:', error)
        this.$emit('show-error', error.message)
      }
    },
    
    handleSearch(type) {
      // Debounce search
      if (this.searchTimeouts[type]) {
        clearTimeout(this.searchTimeouts[type])
      }
      
      this.searchTimeouts[type] = setTimeout(() => {
        this.loadData(type)
      }, 500)
    },
    
    closeModal() {
      this.showModal = false
      this.modalType = null
      this.currentItem = {}
      this.isEditing = false
      this.saving = false
    },
    
    getTypeTitle(type) {
      const titles = {
        'countries': 'País',
        'authors': 'Autor',
        'publication-types': 'Tipo de Publicación',
        'keywords': 'Palabra Clave'
      }
      return titles[type] || 'Elemento'
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }
  },
  
  watch: {
    activeTab(newTab) {
      this.loadData(newTab)
    }
  }
}
</script>

<style scoped>
/* Los estilos se añadirán después */
</style>