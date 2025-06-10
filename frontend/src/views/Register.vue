<template>
    <div class="container d-flex align-items-center justify-content-center min-vh-100">
      <div class="card shadow p-4" style="width: 100%; max-width: 500px;">
        <h3 class="text-center mb-4">Register</h3>
        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="alert alert-success mt-3">
          {{ successMessage }}
        </div>  
        <form @submit.prevent="register">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input v-model="username" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="fullName" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-success w-100">Create Account</button>
        </form>
        <div class="text-center mt-3">
          <span>Already have an account? </span>
          <router-link to="/login">Login</router-link>
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
    const email = ref('')
    const fullName = ref('')
    const password = ref('')
    
    const errorMessage = ref('')
    const successMessage = ref('')
    
    const register = async () => {
      try {
        const response = await axios.post('http://localhost:8000/register', {
          username: username.value,
          email: email.value,
          full_name: fullName.value,
          password: password.value
        })
        
        successMessage.value = response.data.message || 'Registration successful'
        setTimeout(() => {
          router.push('/login')
        }, 2000)
    
      } catch (error) {
        if (error.response) {
          errorMessage.value = error.response.data.detail || 'Registration failed'
        } else {
          errorMessage.value = 'Server error'
        }
        successMessage.value = ''
        console.error(error)
      }
    }
  </script>
  
  
  