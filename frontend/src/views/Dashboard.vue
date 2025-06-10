<template>
  <div class="container mt-5">
    <div class="card mx-auto shadow-lg border-0" style="max-width: 500px;">
      <div class="card-body text-center">
        <div class="mb-4">
          <img 
            v-if="actualPhotoUrl"
            :src="actualPhotoUrl"
            alt="Profile" 
            class="rounded-circle border"
            style="width: 150px; height: 150px; object-fit: cover;"
          />
          <span v-else class="bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center mx-auto mb-4" 
                style="width: 150px; height: 150px; font-size: 48px;">
            {{ initials }}
          </span>
        </div>
        <h5><strong>Login:</strong> {{ username }}</h5>
        <h5><strong>Email:</strong> {{ email }}</h5>
        <h5><strong>Full Name:</strong> {{ full_name }}</h5>
        <form class="mt-4" @submit.prevent="updateProfile()">
            <div class="mb-3">
              <label class="form-label">Full Name</label>
              <input v-model="full_name" type="text" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="email" type="email" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label">New Password (optional)</label>
              <input v-model="password" type="password" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label">Profile Photo</label>
              <input type="file" @change="uploadPhoto" accept="image/*" class="form-control" />
            </div>
            <button type="submit" class="btn btn-primary">Update Profile</button>
        </form>
        <button class="btn btn-outline-danger mt-4" @click="logout">
          <i class="fas fa-sign-out-alt me-2"></i> Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { useRouter } from 'vue-router'
  import { ref, onMounted, computed} from 'vue'
  import axios from 'axios'
  
  const router = useRouter()
  const username = ref('')
  const email = ref('')
  const full_name = ref('')
  const photo_url = ref('')
  const password = ref('')
  const photo_file = ref(null)
  const upp = ref('')

  const actualPhotoUrl = computed(() => {
    if (!photo_url.value || photo_url.value === "null" || photo_url.value.includes("NULL")) {
      return null
    }
    return photo_url.value
  })
  
  onMounted(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
    } else {
        username.value = localStorage.getItem('username')
        email.value = localStorage.getItem('email')
        full_name.value = localStorage.getItem('full_name')
        photo_url.value = localStorage.getItem('photo_url')
      }
  })

    const initials = computed(() => {
    if (!full_name.value) return '?'
    const parts = full_name.value.trim().split(' ')
    return parts.map(p => p[0]?.toUpperCase()).join('').slice(0, 2)
  })

  const photoOrInitials = computed(() => {
    return photo_url.value ? photo_url.value : initials.value
  })

  const logout = () => {
    localStorage.removeItem('access_token')
    
    router.push('/login')
  }

  const uploadPhoto = (event) => {
  photo_file.value = event.target.files[0]
}


const updateProfile = async () => {
  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('email', email.value)
    formData.append('full_name', full_name.value)
    if (password.value) formData.append('password', password.value)
    if (photo_file.value) formData.append('file', photo_file.value)

    const response = await axios.patch('http://localhost:8000/update-profile', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    if (response.data.user.photo_url) {
      const fullUrl = `http://localhost:8000/${response.data.user.photo_url}`
      photo_url.value = fullUrl
      localStorage.setItem('photo_url', fullUrl)
    } else {
      photo_url.value = ''
      localStorage.removeItem('photo_url')
    }

    localStorage.setItem('full_name', response.data.user.full_name)
    full_name.value = response.data.user.full_name
    localStorage.setItem('email', response.data.user.email)
    email.value = response.data.user.email


  } catch (error) {
    console.error("Update failed:", error)
  }
}
</script>
  
<style scoped>
  .card-header {
    font-size: 1.2rem;
  }
</style>
  