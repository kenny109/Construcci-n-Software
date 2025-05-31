<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          📚 Gestión Académica
        </router-link>
      </div>

      <div class="nav-menu" :class="{ 'nav-menu-active': isMenuOpen }">
        <router-link
          to="/"
          class="nav-link"
          @click="closeMenu"
        >
          Dashboard
        </router-link>
        <router-link
          to="/authors"
          class="nav-link"
          @click="closeMenu"
        >
          Autores
        </router-link>
        <router-link
          to="/publications"
          class="nav-link"
          @click="closeMenu"
        >
          Publicaciones
        </router-link>
      </div>

      <div class="nav-user">
        <div class="user-info">
          <span class="user-name">{{ userDisplayName }}</span>
          <button @click="handleLogout" class="logout-btn">
            Cerrar Sesión
          </button>
        </div>
        
        <button
          class="mobile-menu-btn"
          @click="toggleMenu"
        >
          <span class="hamburger"></span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'NavBar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const isMenuOpen = ref(false)

    const userDisplayName = computed(() => {
      const user = authStore.currentUser
      if (user) {
        return user.first_name && user.last_name
          ? `${user.first_name} ${user.last_name}`
          : user.username
      }
      return 'Usuario'
    })

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value
    }

    const closeMenu = () => {
      isMenuOpen.value = false
    }

    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }

    return {
      isMenuOpen,
      userDisplayName,
      toggleMenu,
      closeMenu,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.nav-brand .brand-link {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  color: white;
  font-weight: 500;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger {
  display: block;
  width: 24px;
  height: 3px;
  background: white;
  border-radius: 3px;
  position: relative;
  transition: all 0.3s ease;
}

.hamburger::before,
.hamburger::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 3px;
  background: white;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.hamburger::before {
  top: -8px;
}

.hamburger::after {
  bottom: -8px;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .nav-menu {
    position: fixed;
    top: 60px;
    left: -100%;
    width: 100%;
    height: calc(100vh - 60px);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    gap: 0;
    padding-top: 2rem;
    transition: left 0.3s ease;
  }

  .nav-menu-active {
    left: 0;
  }

  .nav-link {
    width: 90%;
    text-align: center;
    padding: 1rem;
    margin-bottom: 0.5rem;
  }

  .mobile-menu-btn {
    display: block;
  }

  .user-info {
    display: none;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 0.5rem;
  }

  .nav-brand .brand-link {
    font-size: 1.2rem;
  }
}
</style>