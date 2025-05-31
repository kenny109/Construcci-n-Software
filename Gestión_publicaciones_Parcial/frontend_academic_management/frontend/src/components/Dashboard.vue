<template>
    <div class="dashboard">
        <div class="dashboard-header">
            <h1>Dashboard</h1>
            <p>Bienvenido al Sistema de Gestión de Publicaciones</p>
        </div>

        <div class="stats-grid grid grid-4">
            <div class="stat-card card">
                
                
                <div class="stat-content">
                    <h3>{{ stats.authors }}</h3>
                    <p>Autores</p>
                </div>
            </div>

            <div class="stat-card card">
                <div class="stat-icon">
                    📚
                </div>
                <div class="stat-content">
                    <h3>{{ stats.publications }}</h3>
                    <p>Publicaciones</p>
                </div>
            </div>

            <div class="stat-card card">
                <div class="stat-icon">
                    📖
                </div>
                <div class="stat-content">
                    <h3>{{ stats.journals }}</h3>
                    <p>Revistas</p>
                </div>
            </div>

            <div class="stat-card card">
                <div class="stat-icon">
                    👤
                </div>
                <div class="stat-content">
                    <h3>{{ stats.users }}</h3>
                    <p>Usuarios</p>
                </div>
            </div>
        </div>

        <div class="dashboard-content grid grid-2">
            <div class="recent-publications card">
                <div class="card-header">
                    <h2>Publicaciones Recientes</h2>
                    <router-link to="/publications" class="btn btn-sm btn-primary">
                        Ver todas
                    </router-link>
                </div>
                <div class="publications-list">
                    <div v-if="loading.publications" class="loading">
                        <div class="spinner"></div>
                    </div>
                    <div v-else-if="recentPublications.length === 0" class="empty-state">
                        No hay publicaciones recientes
                    </div>
                    <div v-else>
                        <div v-for="publication in recentPublications" :key="publication.id" class="publication-item">
                            <h4>{{ publication.title }}</h4>
                            <p class="publication-meta">
                                {{ formatDate(publication.publication_date) }} •
                                {{ publication.publication_type?.name }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="top-authors card">
                <div class="card-header">
                    <h2>Autores Más Activos</h2>
                    <router-link to="/authors" class="btn btn-sm btn-primary">
                        Ver todos
                    </router-link>
                </div>
                <div class="authors-list">
                    <div v-if="loading.authors" class="loading">
                        <div class="spinner"></div>
                    </div>
                    <div v-else-if="topAuthors.length === 0" class="empty-state">
                        No hay autores registrados
                    </div>
                    <div v-else>
                        <div v-for="author in topAuthors" :key="author.id" class="author-item">
                            <div class="author-info">
                                <h4>{{ author.first_name }} {{ author.last_name }}</h4>
                                <p>{{ author.institution }}</p>
                            </div>
                            <div class="author-stats">
                                <span class="publication-count">{{ author.publication_count || 0 }} pub.</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
    name: 'Dashboard',
    setup() {
        const stats = ref({
            authors: 0,
            publications: 0,
            journals: 0,
            users: 0
        })

        const recentPublications = ref([])
        const topAuthors = ref([])

        const loading = ref({
            stats: false,
            publications: false,
            authors: false
        })

        const loadStats = async () => {
            loading.value.stats = true
            try {
                // Cargar estadísticas básicas
                const [authorsRes, publicationsRes, journalsRes, usersRes] = await Promise.all([
                    api.get('/authors'),
                    api.get('/publications'),
                    api.get('/journals'),
                    api.get('/users')
                ])

                stats.value = {
                    authors: authorsRes.data.length,
                    publications: publicationsRes.data.length,
                    journals: journalsRes.data.length,
                    users: usersRes.data.length
                }
            } catch (error) {
                console.error('Error loading stats:', error)
            } finally {
                loading.value.stats = false
            }
        }

        const loadRecentPublications = async () => {
            loading.value.publications = true
            try {
                const response = await api.get('/publications?limit=5')
                recentPublications.value = response.data.slice(0, 5)
            } catch (error) {
                console.error('Error loading recent publications:', error)
            } finally {
                loading.value.publications = false
            }
        }

        const loadTopAuthors = async () => {
            loading.value.authors = true
            try {
                const response = await api.get('/authors?limit=5')
                topAuthors.value = response.data.slice(0, 5)
            } catch (error) {
                console.error('Error loading top authors:', error)
            } finally {
                loading.value.authors = false
            }
        }

        const formatDate = (dateString) => {
            if (!dateString) return 'Sin fecha'
            return new Date(dateString).toLocaleDateString('es-ES')
        }

        onMounted(() => {
            loadStats()
            loadRecentPublications()
            loadTopAuthors()
        })

        return {
            stats,
            recentPublications,
            topAuthors,
            loading,
            formatDate
        }
    }
}
</script>

<style scoped>
.dashboard-header {
    margin-bottom: 2rem;
}

.dashboard-header h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: #1f2937;
}

.dashboard-header p {
    color: #6b7280;
    font-size: 1.1rem;
}

.stats-grid {
    margin-bottom: 2rem;
}

.stat-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
}

.stat-icon {
    font-size: 2rem;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
}

.stat-content h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.25rem;
}

.stat-content p {
    color: #6b7280;
    font-size: 0.9rem;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
}

.card-header h2 {
    font-size: 1.25rem;
    color: #1f2937;
}

.publications-list,
.authors-list {
    max-height: 400px;
    overflow-y: auto;
}

.publication-item {
    padding: 1rem 0;
    border-bottom: 1px solid #f3f4f6;
}

.publication-item:last-child {
    border-bottom: none;
}

.publication-item h4 {
    font-size: 1rem;
    color: #1f2937;
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.publication-meta {
    font-size: 0.85rem;
    color: #6b7280;
}

.author-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #f3f4f6;
}

.author-item:last-child {
    border-bottom: none;
}

.author-info h4 {
    font-size: 1rem;
    color: #1f2937;
    margin-bottom: 0.25rem;
}

.author-info p {
    font-size: 0.85rem;
    color: #6b7280;
}

.publication-count {
    background-color: #f3f4f6;
    color: #374151;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 500;
}

.empty-state {
    text-align: center;
    color: #6b7280;
    padding: 2rem;
    font-style: italic;
}

@media (max-width: 768px) {
    .dashboard-content {
        grid-template-columns: 1fr;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .stat-card {
        padding: 1rem;
    }

    .stat-icon {
        width: 50px;
        height: 50px;
        font-size: 1.5rem;
    }
}
</style>