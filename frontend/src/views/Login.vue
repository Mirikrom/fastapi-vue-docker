<template>
  <div class="container d-flex align-items-center justify-content-center min-vh-100">
    <div class="card shadow p-4" style="width: 100%; max-width: 400px;">
      <h3 class="text-center mb-4">Login</h3>

      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="username" required />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" required />
        </div>

        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
      <div class="text-center mt-3">
        <span>Don't have an account? </span>
        <router-link to="/register">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const router = useRouter()

  const username = ref('')
  const password = ref('')
  const errorMessage = ref('')

  const login = async () => {
    try {
      const response = await axios.post('http://localhost:8000/login', {
        username: username.value,
        password: password.value
      })

      const token = response.data.token
      const user = response.data.user
      localStorage.setItem('access_token', token)
      localStorage.setItem('username', user.username)
      localStorage.setItem('email', user.email)
      localStorage.setItem('full_name', user.full_name)
      localStorage.setItem('photo_url', user.photo_url)
      if (user.photo_url && !user.photo_url.startsWith('http')) {
        user.photo_url = `http://localhost:8000/${user.photo_url}`
        localStorage.setItem('photo_url', user.photo_url)
      }
      router.push('/dashboard')
    } catch (error) {
      errorMessage.value = error.response?.data?.detail || 'Login failed'
      console.error(error)
    }
  }
</script>
