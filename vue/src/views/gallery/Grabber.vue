<template>
  <b-wrapper container>
    <form @submit.prevent.stop="submitGrab">
      <b-row class="mb-5">
        <b-col>
          <b-input size="lg" placeholder="https://" v-model="url" :disabled="active"/>
        </b-col>
        <b-col cols="auto">
          <b-btn size="lg" type="submit" :disabled="active">Grab</b-btn>
        </b-col>
      </b-row>
      <b-row>
          <b-col cols="6">
            <b-input size="lg" v-model="extractPattern" placeholder="xpath . . ."></b-input>
          </b-col>
          <b-col cols="auto">
            <b-check size="lg" v-model="sourceCode">Source Code</b-check>
          </b-col>
          <b-col cols="auto">
            <b-check v-model="savePin">Save</b-check>
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
      savePin: false,
      active: false,
      sourceCode: null,
      extractPattern: null,
    }
  },
  methods: {
    submitGrab() {
      this.active = true
      const payload = {
        url: this.url,
        save: this.savePin,
        source: this.sourceCode,
        pattern: this.extractPattern,
      }
      postApiCall('/grab/html/', payload).then(data => {

        console.log(data)

      }).finally(() => {

        this.active = false

      })
    }
  }
}
</script>