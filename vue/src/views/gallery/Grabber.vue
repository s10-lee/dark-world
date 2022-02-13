<template>
  <b-wrapper container>
    <form @submit.prevent.stop="submitGrab">
    <b-row>
      <b-col>
        <b-input size="lg" placeholder="https://" v-model="url" :disabled="active"/>
      </b-col>
      <b-col cols="auto">
        <b-btn size="lg" type="submit" :disabled="active">Grab</b-btn>
      </b-col>
    </b-row>
    </form>
  </b-wrapper>
</template>

<script>
import { postApiCall } from 'services/http'
export default {
  name: 'Grabber',
  data() {
    return {
      url: null,
      active: false,
    }
  },
  methods: {
    submitGrab() {
      this.active = true
      postApiCall('/grab/', {url: this.url})
          .then(() => {
            this.active = false
            this.url = null
          })
    },
  }
}
</script>