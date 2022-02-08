<template>
  <div class="container">
    <b-row class="my-3" gx="0">
        <b-label>Username</b-label>
        <h3 class="text-warning">{{ name }}</h3>
    </b-row>
    <b-row align-v="end" class="mb-3">
      <b-col cols="auto">
        <b-input size="lg" v-model="email" label="Email"/>
      </b-col>
      <b-col cols="auto">
        <b-btn size="lg" @click="saveForm">Save</b-btn>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { getApiCall, putApiCall } from 'services/http'
export default {
  name: 'Profile',
  data() {
    return {
      name: null,
      email: null,
    }
  },
  methods: {
    saveForm() {
      putApiCall('/profile/email/', {email: this.email}).then(data => {
        console.log(data)
      })
    }
  },
  mounted() {
    getApiCall('/profile/').then(data => {
      this.name = data['name']
      this.email = data['email']
    })
  }
}
</script>