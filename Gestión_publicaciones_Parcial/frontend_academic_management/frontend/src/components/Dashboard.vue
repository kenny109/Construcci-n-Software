<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
      <p>Bienvenido al sistema de gestión académica</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="icon-users">👥</i>
        </div>
        <div class="stat-content">
          <h3>{{ stats.authors }}</h3>
          <p>Autores</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="icon-publications">📚</i>
        </div>
        <div class="stat-content">
          <h3>{{ stats.publications }}</h3>
          <p>Publicaciones</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="icon-users-admin">👤</i>
        </div>
        <div class="stat-content">
          <h3>{{ stats.users }}</h3>
          <p>Usuarios</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="icon-active">✅</i>
        </div>
        <div class="stat-content">
          <h3>{{ stats.active }}</h3>
          <p>Registros Activos</p>
        </div>
      </div>
    </div>
    
    <div class="dashboard-actions">
      <h2>Acciones Rápidas</h2>
      <div class="actions-grid">
        <router-link to="/authors" class="action-card">
          <div class="action-icon">👥</div>
          <h3>Gestionar Autores</h3>
          <p>Crear, editar y eliminar autores</p>
        </router-link>
        
        <router-link to="/publications" class="action-card">
          <div class="action-icon">📚</div>
          <h3>Gestionar Publicaciones</h3>
          <p>Administrar publicaciones académicas</p>
        </router-link>
        
        <router-link to="/users" class="action-card">
          <div class="action-icon">👤</div>
          <h3>Gestionar Usuarios</h3>
          <p>Administrar usuarios del sistema</p>
        </router-link>
      </div>
    </div>
    
    <div v-if="recentActivities.length > 0" class="recent-activities">
      <h2>Actividad Reciente</h2>
      <div class="activities-list">
        <div
          v-for="activity in recentActivities"
          :key="activity.id"
          class="activity-item"
        >
          <div class="activity-content">
            <h4>{{ activity.title }}</h4>
            <p>{{ activity.description }}</p>
            <span class="activity-date">{{ formatDate(activity.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiService from '../services/api'

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({
      authors: 0,
      publications: 0,
      users: 0,
      active: 0
    })
    
    const recentActivities = ref([])
    const isLoading = ref(false)
    
    const loadStats = async () => {
      isLoading.value = true
      
      try {
        const [authorsData, publicationsData, usersData] = await Promise.all([
          apiService.getAuthors(),
          apiService.getPublications(),
          apiService.getUsers()
        ])
        
        stats.value = {
          authors: authorsData.length || 0,
          publications: publicationsData.length || 0,
          users: usersData.length || 0,
          active: (authorsData.length || 0) + (publicationsData.length || 0) + (usersData.length || 0)
        }
        
        // Simular actividades recientes
        recentActivities.value = [
          {
            id: 1,
            title: 'Nuevo autor registrado',
            description: 'Se ha registrado un nuevo autor en el sistema',
            created_at: new Date().toISOString()
          },
          {
            id: 2,
            title: 'Publicación actualizada',
            description: 'Se ha actualizado una publicación existente',
            created_at: new Date(Date.now() - 86400000).toISOString()
          }
        ]
      } catch (error) {
        console.error('Error loading dashboard stats:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      stats,
      recentActivities,
      isLoading,
      formatDate
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem 0;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  font-size: 1.2rem;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 3rem;
  margin-right: 1.5rem;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.stat-content p {
  color: #666;
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
}

.dashboard-actions {
  margin-bottom: 3rem;
}

.dashboard-actions h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.action-card p {
  color: #666;
  margin: 0;
}

.recent-activities {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.recent-activities h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  padding: 1rem;
  border-left: 4px solid #667eea;
  background-color: #f8f9fa;
  border-radius: 0 8px 8px 0;
}

.activity-content h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.activity-content p {
  margin: 0 0 0.5rem 0;
  color: #666;
}

.activity-date {
  font-size: 0.9rem;
  color: #999;
}
</style>