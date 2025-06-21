<!-- src/components/PublicationsCrud.vue -->
<template>
  <div class="publications-crud">
    <div class="header">
      <h2>Gestión de Publicaciones</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        Nueva Publicación
      </button>
    </div>

    <!-- Publications List -->
    <div class="publications-grid">
      <div v-for="publication in publications" :key="publication.id" class="publication-card">
        <div class="publication-header">
          <h3>{{ publication.title }}</h3>
          <div class="publication-actions">
            <button @click="editPublication(publication)" class="btn-edit">
              Editar
            </button>
            <button @click="deletePublication(publication.id)" class="btn-delete">
              Eliminar
            </button>
          </div>
        </div>
        
        <div class="publication-details">
          <p><strong>DOI:</strong> {{ publication.doi || 'N/A' }}</p>
          <p><strong>Fecha:</strong> {{ formatDate(publication.publication_date) }}</p>
          <p><strong>Tipo:</strong> {{ getPublicationTypeName(publication.publication_type_id) }}</p>
          <p v-if="publication.journal_id"><strong>Revista:</strong> {{ getJournalName(publication.journal_id) }}</p>
          <p v-if="publication.conference_id"><strong>Conferencia:</strong> {{ getConferenceName(publication.conference_id) }}</p>
          <p><strong>Citas:</strong> {{ publication.citation_count || 0 }}</p>
        </div>
        
        <div v-if="publication.abstract" class="publication-abstract">
          <p><strong>Resumen:</strong></p>
          <p>{{ publication.abstract.substring(0, 200) }}{{ publication.abstract.length > 200 ? '...' : '' }}</p>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ showCreateModal ? 'Nueva Publicación' : 'Editar Publicación' }}</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>

        <form @submit.prevent="submitForm" class="modal-body">
          <!-- Basic Information -->
          <div class="form-section">
            <h4>Información Básica</h4>
            
            <div class="form-group">
              <label>Título *</label>
              <input v-model="form.title" type="text" required>
            </div>

            <div class="form-group">
              <label>Resumen</label>
              <textarea v-model="form.abstract" rows="4"></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>DOI</label>
                <input v-model="form.doi" type="text">
              </div>
              
              <div class="form-group">
                <label>URL</label>
                <input v-model="form.url" type="url">
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Fecha de Publicación</label>
                <input v-model="form.publication_date" type="date">
              </div>
              
              <div class="form-group">
                <label>Número de Citas</label>
                <input v-model="form.citation_count" type="number" min="0">
              </div>
            </div>
          </div>

          <!-- Publication Type -->
          <div class="form-section">
            <h4>Tipo de Publicación</h4>
            
            <div class="form-row">
              <div class="form-group">
                <label>Tipo de Publicación *</label>
                <select v-model="form.publication_type_id" required>
                  <option value="">Seleccionar tipo</option>
                  <option v-for="type in publicationTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
              
              <div class="form-group">
                <label>Nuevo Tipo</label>
                <div class="input-with-button">
                  <input v-model="newPublicationType.name" type="text" placeholder="Nombre del nuevo tipo">
                  <button type="button" @click="createPublicationType" class="btn-add">+</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Journal or Conference -->
          <div class="form-section">
            <div class="form-tabs">
              <button type="button" :class="['tab', { active: publicationVenue === 'journal' }]" 
                      @click="publicationVenue = 'journal'">
                Revista
              </button>
              <button type="button" :class="['tab', { active: publicationVenue === 'conference' }]" 
                      @click="publicationVenue = 'conference'">
                Conferencia
              </button>
            </div>

            <!-- Journal Section -->
            <div v-if="publicationVenue === 'journal'">
              <div class="form-row">
                <div class="form-group">
                  <label>Revista</label>
                  <select v-model="form.journal_id">
                    <option value="">Seleccionar revista</option>
                    <option v-for="journal in journals" :key="journal.id" :value="journal.id">
                      {{ journal.name }}
                    </option>
                  </select>
                </div>
                
                <div class="form-group">
                  <label>País de la Revista</label>
                  <select v-model="newJournal.country_id">
                    <option value="">Seleccionar país</option>
                    <option v-for="country in countries" :key="country.id" :value="country.id">
                      {{ country.name }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- New Journal Form -->
              <div class="new-item-form">
                <h5>Crear Nueva Revista</h5>
                <div class="form-row">
                  <div class="form-group">
                    <input v-model="newJournal.name" type="text" placeholder="Nombre de la revista">
                  </div>
                  <div class="form-group">
                    <input v-model="newJournal.issn" type="text" placeholder="ISSN">
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <input v-model="newJournal.publisher" type="text" placeholder="Editorial">
                  </div>
                  <div class="form-group">
                    <select v-model="newJournal.quartile">
                      <option value="">Cuartil</option>
                      <option value="Q1">Q1</option>
                      <option value="Q2">Q2</option>
                      <option value="Q3">Q3</option>
                      <option value="Q4">Q4</option>
                    </select>
                  </div>
                </div>
                <button type="button" @click="createJournal" class="btn-secondary">
                  Crear Revista
                </button>
              </div>
            </div>

            <!-- Conference Section -->
            <div v-if="publicationVenue === 'conference'">
              <div class="form-row">
                <div class="form-group">
                  <label>Conferencia</label>
                  <select v-model="form.conference_id">
                    <option value="">Seleccionar conferencia</option>
                    <option v-for="conference in conferences" :key="conference.id" :value="conference.id">
                      {{ conference.name }} ({{ conference.year }})
                    </option>
                  </select>
                </div>
                
                <div class="form-group">
                  <label>País de la Conferencia</label>
                  <select v-model="newConference.country_id">
                    <option value="">Seleccionar país</option>
                    <option v-for="country in countries" :key="country.id" :value="country.id">
                      {{ country.name }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- New Conference Form -->
              <div class="new-item-form">
                <h5>Crear Nueva Conferencia</h5>
                <div class="form-row">
                  <div class="form-group">
                    <input v-model="newConference.name" type="text" placeholder="Nombre de la conferencia">
                  </div>
                  <div class="form-group">
                    <input v-model="newConference.year" type="number" placeholder="Año">
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <input v-model="newConference.location" type="text" placeholder="Ubicación">
                  </div>
                  <div class="form-group">
                    <input v-model="newConference.website" type="url" placeholder="Sitio web">
                  </div>
                </div>
                <button type="button" @click="createConference" class="btn-secondary">
                  Crear Conferencia
                </button>
              </div>
            </div>
          </div>

          <!-- Authors Section -->
          <div class="form-section">
            <h4>Autores</h4>
            
            <div class="authors-list">
              <div v-for="(author, index) in selectedAuthors" :key="index" class="author-item">
                <select v-model="author.author_id" required>
                  <option value="">Seleccionar autor</option>
                  <option v-for="a in authors" :key="a.id" :value="a.id">
                    {{ a.first_name }} {{ a.last_name }}
                  </option>
                </select>
                <input v-model="author.author_order" type="number" placeholder="Orden" min="1">
                <label>
                  <input type="checkbox" v-model="author.is_corresponding">
                  Correspondiente
                </label>
                <button type="button" @click="removeAuthor(index)" class="btn-remove">-</button>
              </div>
            </div>
            
            <button type="button" @click="addAuthor" class="btn-secondary">
              Agregar Autor
            </button>

            <!-- New Author Form -->
            <div class="new-item-form">
              <h5>Crear Nuevo Autor</h5>
              <div class="form-row">
                <div class="form-group">
                  <input v-model="newAuthor.first_name" type="text" placeholder="Nombre">
                </div>
                <div class="form-group">
                  <input v-model="newAuthor.last_name" type="text" placeholder="Apellido">
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <input v-model="newAuthor.email" type="email" placeholder="Email">
                </div>
                <div class="form-group">
                  <input v-model="newAuthor.institution" type="text" placeholder="Institución">
                </div>
              </div>
              <button type="button" @click="createAuthor" class="btn-secondary">
                Crear Autor
              </button>
            </div>
          </div>

          <!-- Keywords Section -->
          <div class="form-section">
            <h4>Palabras Clave</h4>
            
            <div class="keywords-container">
              <div class="selected-keywords">
                <span v-for="keyword in selectedKeywords" :key="keyword.id" class="keyword-tag">
                  {{ keyword.name }}
                  <button type="button" @click="removeKeyword(keyword.id)" class="remove-keyword">&times;</button>
                </span>
              </div>
              
              <div class="keyword-selector">
                <select v-model="selectedKeywordId" @change="addKeyword">
                  <option value="">Seleccionar palabra clave</option>
                  <option v-for="keyword in availableKeywords" :key="keyword.id" :value="keyword.id">
                    {{ keyword.name }}
                  </option>
                </select>
              </div>

              <div class="new-keyword">
                <input v-model="newKeywordName" type="text" placeholder="Nueva palabra clave">
                <button type="button" @click="createKeyword" class="btn-add">+</button>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Guardando...' : (showCreateModal ? 'Crear' : 'Actualizar') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="loading">Cargando...</div>

    <!-- Error message -->
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'PublicationsCrud',
  data() {
    return {
      publications: [],
      publicationTypes: [],
      journals: [],
      conferences: [],
      authors: [],
      keywords: [],
      countries: [],
      
      selectedAuthors: [],
      selectedKeywords: [],
      selectedKeywordId: '',
      newKeywordName: '',
      
      showCreateModal: false,
      showEditModal: false,
      loading: false,
      error: '',
      
      publicationVenue: 'journal', // 'journal' or 'conference'
      
      form: {
        title: '',
        abstract: '',
        doi: '',
        url: '',
        publication_date: '',
        citation_count: 0,
        publication_type_id: '',
        journal_id: '',
        conference_id: ''
      },
      
      newPublicationType: {
        name: '',
        description: ''
      },
      
      newJournal: {
        name: '',
        issn: '',
        publisher: '',
        quartile: '',
        country_id: ''
      },
      
      newConference: {
        name: '',
        year: new Date().getFullYear(),
        location: '',
        website: '',
        country_id: ''
      },
      
      newAuthor: {
        first_name: '',
        last_name: '',
        email: '',
        institution: '',
        orcid_id: ''
      }
    }
  },
  
  computed: {
    availableKeywords() {
      return this.keywords.filter(k => !this.selectedKeywords.find(sk => sk.id === k.id))
    }
  },
  
  async created() {
    await this.loadData()
  },
  
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [publications, publicationTypes, journals, conferences, authors, keywords, countries] = await Promise.all([
          api.getItems('publications'),
          api.getItems('publication-types'),
          api.getItems('journals'),
          api.getItems('conferences'),
          api.getItems('authors'),
          api.getItems('keywords'),
          api.getItems('countries')
        ])
        
        this.publications = publications.data || publications
        this.publicationTypes = publicationTypes.data || publicationTypes
        this.journals = journals.data || journals
        this.conferences = conferences.data || conferences
        this.authors = authors.data || authors
        this.keywords = keywords.data || keywords
        this.countries = countries.data || countries
        
      } catch (error) {
        this.error = 'Error cargando datos: ' + error.message
      } finally {
        this.loading = false
      }
    },
    
    async createPublicationType() {
      if (!this.newPublicationType.name.trim()) return
      
      try {
        const response = await api.createItem('publication-types', this.newPublicationType)
        this.publicationTypes.push(response.data || response)
        this.form.publication_type_id = (response.data || response).id
        this.newPublicationType = { name: '', description: '' }
      } catch (error) {
        this.error = 'Error creando tipo de publicación: ' + error.message
      }
    },
    
    async createJournal() {
      if (!this.newJournal.name.trim()) return
      
      try {
        const response = await api.createItem('journals', this.newJournal)
        this.journals.push(response.data || response)
        this.form.journal_id = (response.data || response).id
        this.newJournal = { name: '', issn: '', publisher: '', quartile: '', country_id: '' }
      } catch (error) {
        this.error = 'Error creando revista: ' + error.message
      }
    },
    
    async createConference() {
      if (!this.newConference.name.trim()) return
      
      try {
        const response = await api.createItem('conferences', this.newConference)
        this.conferences.push(response.data || response)
        this.form.conference_id = (response.data || response).id
        this.newConference = { name: '', year: new Date().getFullYear(), location: '', website: '', country_id: '' }
      } catch (error) {
        this.error = 'Error creando conferencia: ' + error.message
      }
    },
    
    async createAuthor() {
      if (!this.newAuthor.first_name.trim() || !this.newAuthor.last_name.trim()) return
      
      try {
        const response = await api.createItem('authors', this.newAuthor)
        this.authors.push(response.data || response)
        this.newAuthor = { first_name: '', last_name: '', email: '', institution: '', orcid_id: '' }
      } catch (error) {
        this.error = 'Error creando autor: ' + error.message
      }
    },
    
    async createKeyword() {
      if (!this.newKeywordName.trim()) return
      
      try {
        const response = await api.createItem('keywords', { name: this.newKeywordName })
        this.keywords.push(response.data || response)
        this.newKeywordName = ''
      } catch (error) {
        this.error = 'Error creando palabra clave: ' + error.message
      }
    },
    
    addAuthor() {
      this.selectedAuthors.push({
        author_id: '',
        author_order: this.selectedAuthors.length + 1,
        is_corresponding: false
      })
    },
    
    removeAuthor(index) {
      this.selectedAuthors.splice(index, 1)
    },
    
    addKeyword() {
      if (!this.selectedKeywordId) return
      
      const keyword = this.keywords.find(k => k.id === this.selectedKeywordId)
      if (keyword && !this.selectedKeywords.find(sk => sk.id === keyword.id)) {
        this.selectedKeywords.push(keyword)
        this.selectedKeywordId = ''
      }
    },
    
    removeKeyword(keywordId) {
      this.selectedKeywords = this.selectedKeywords.filter(k => k.id !== keywordId)
    },
    
    editPublication(publication) {
      this.form = { ...publication }
      
      // Load publication authors and keywords
      this.selectedAuthors = publication.authors || []
      this.selectedKeywords = publication.keywords || []
      
      this.showEditModal = true
    },
    
    async submitForm() {
      this.loading = true
      this.error = ''
      
      try {
        // Clean form data
        const publicationData = { ...this.form }
        
        // Set venue based on selection
        if (this.publicationVenue === 'journal') {
          publicationData.conference_id = null
        } else {
          publicationData.journal_id = null
        }
        
        let publicationResponse
        
        if (this.showCreateModal) {
          publicationResponse = await api.createItem('publications', publicationData)
        } else {
          publicationResponse = await api.updateItem('publications', this.form.id, publicationData)
        }
        
        const publication = publicationResponse.data || publicationResponse
        
        // Handle authors
        if (this.selectedAuthors.length > 0) {
          for (const authorData of this.selectedAuthors) {
            if (authorData.author_id) {
              const publicationAuthorData = {
                publication_id: publication.id,
                author_id: authorData.author_id,
                author_order: authorData.author_order,
                is_corresponding: authorData.is_corresponding
              }
              
              await api.addAuthorToPublication(publication.id, {
  author_id: authorData.author_id,
  order: authorData.author_order,
  is_corresponding: authorData.is_corresponding
})

            }
          }
        }
        
        // Handle keywords
        if (this.selectedKeywords.length > 0) {
          for (const keyword of this.selectedKeywords) {
            const publicationKeywordData = {
              publication_id: publication.id,
              keyword_id: keyword.id
            }
            
            await api.createItem('publication-keywords', publicationKeywordData)
          }
        }
        
        await this.loadData()
        this.closeModal()
        
      } catch (error) {
        this.error = 'Error guardando publicación: ' + error.message
      } finally {
        this.loading = false
      }
    },
    
    async deletePublication(id) {
      if (!confirm('¿Está seguro de eliminar esta publicación?')) return
      
      try {
        await api.deleteItem('publications', id)
        await this.loadData()
      } catch (error) {
        this.error = 'Error eliminando publicación: ' + error.message
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.resetForm()
    },
    
    resetForm() {
      this.form = {
        title: '',
        abstract: '',
        doi: '',
        url: '',
        publication_date: '',
        citation_count: 0,
        publication_type_id: '',
        journal_id: '',
        conference_id: ''
      }
      
      this.selectedAuthors = []
      this.selectedKeywords = []
      this.selectedKeywordId = ''
      this.newKeywordName = ''
      this.publicationVenue = 'journal'
      this.error = ''
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },
    
    getPublicationTypeName(typeId) {
      const type = this.publicationTypes.find(t => t.id === typeId)
      return type ? type.name : 'N/A'
    },
    
    getJournalName(journalId) {
      const journal = this.journals.find(j => j.id === journalId)
      return journal ? journal.name : 'N/A'
    },
    
    getConferenceName(conferenceId) {
      const conference = this.conferences.find(c => c.id === conferenceId)
      return conference ? `${conference.name} (${conference.year})` : 'N/A'
    }
  }
}
</script>

<style scoped>
.publications-crud {
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  margin: 0;
  color: #333;
}

.publications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.publication-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.publication-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.publication-header h3 {
  margin: 0;
  color: #333;
  flex: 1;
  margin-right: 1rem;
}

.publication-actions {
  display: flex;
  gap: 0.5rem;
}

.publication-details p {
  margin: 0.5rem 0;
  color: #666;
}

.publication-abstract {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.publication-abstract p {
  margin: 0.5rem 0;
  color: #555;
  line-height: 1.4;
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
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.form-section:last-child {
  border-bottom: none;
}

.form-section h4 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.1rem;
}

.form-section h5 {
  margin: 1rem 0 0.5rem 0;
  color: #555;
  font-size: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.form-group textarea {
  resize: vertical;
}

.input-with-button {
  display: flex;
  gap: 0.5rem;
}

.input-with-button input {
  flex: 1;
}

.form-tabs {
  display: flex;
  margin-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.tab {
  padding: 0.75rem 1.5rem;
  border: none;
  background: #f8f9fa;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tab.active {
  background: white;
  border-bottom-color: #007bff;
  color: #007bff;
}

.new-item-form {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.authors-list {
  margin-bottom: 1rem;
}

.author-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.author-item select {
  flex: 2;
}

.author-item input[type="number"] {
  width: 80px;
}

.author-item label {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  white-space: nowrap;
}

.keywords-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}


.selected-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.keyword-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.5rem;
  border-radius: 16px;
  font-size: 0.85rem;
}

.remove-keyword {
  background: none;
  border: none;
  color: #1976d2;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
}

.keyword-selector {
  margin-bottom: 1rem;
}

.new-keyword {
  display: flex;
  gap: 0.5rem;
}

.new-keyword input {
  flex: 1;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.btn-edit {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.btn-add {
  background-color: #17a2b8;
  color: white;
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-remove {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  margin: 1rem 0;
}

.btn-primary:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>