<template>
  <b-wrapper container>
    <b-row gx="0">
        <b-label size="lg">USERNAME</b-label>
        <h1>{{ name }}</h1>
    </b-row>
    <b-row align-v="end" class="mb-3">
      <b-col cols="auto">
        <b-input size="lg" v-model="email" label="EMAIL"/>
      </b-col>
      <b-col cols="auto">
        <b-btn size="lg" @click="saveForm">Save</b-btn>
      </b-col>
    </b-row>
  </b-wrapper>
</template>

<script>
import { getApiCall, putApiCall } from 'services/http'
import { PageMixin } from 'mixins'


export default {
  name: 'Profile',
  mixins: [ PageMixin ],
  data() {
    return {
      name: null,
      email: null,
    }
  },
  methods: {
    saveForm() {
      this.loading(true)
      putApiCall('/profile/email/', {email: this.email}).then(data => {
        this.notify('Email was updated !', 'success')
        this.loading(false)
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