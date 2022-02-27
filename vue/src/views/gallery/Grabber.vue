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
            <b-input size="lg" v-model="extractPattern" placeholder="// . . ."></b-input>
          </b-col>
          <b-col cols="auto">
            <b-check size="lg" v-model="sourceCode">Source Code</b-check>
          </b-col>
          <b-col cols="auto">
            <b-check size="lg" v-model="savePin">Save</b-check>
          </b-col>
      </b-row>
      <b-row>
        <b-col class="text-700 mt-3">
          Pinterest
          <div class="text-muted mb-3">
            //head/link[@as="image"]/@href
          </div>
          Dribbble
          <div class="text-muted">
            //img[@data-animated-url]/@data-animated-url
          </div>
        </b-col>
      </b-row>
    </form>

    <b-row class="mt-5">
      <b-col cols="auto">
        <b-input v-model="message" placeholde="message..." />
      </b-col>
      <b-col cols="auto">
        <b-input v-model="duration" placeholde="duration... ms" type="number" />
      </b-col>
      <b-col cols="auto">
        <b-input v-model="type" placeholde="type..." />
      </b-col>
      <b-col cols="auto">
        <b-btn @click.stop.prevent="notify">Test</b-btn>
      </b-col>
    </b-row>

  </b-wrapper>
</template>

<script>
import { postApiCall } from 'services/http'
import { PageMixin } from 'mixins'

export default {
  name: 'Grabber',
  mixins: [ PageMixin ],
  data() {
    return {
      url: null,
      savePin: false,
      active: false,
      sourceCode: null,
      extractPattern: null,
      message: 'This is a test message !!',
      duration: 5000,
      type: 'dark',
    }
  },
  methods: {
    notify() {
      this.$store.dispatch('notify', {
        message: this.message,
        duration: parseInt(this.duration),
        type: this.type,
      })
    },
    submitGrab() {
      this.active = true
      const payload = {
        url: this.url,
        save: this.savePin,
        source: this.sourceCode,
        pattern: this.extractPattern,
      }
      postApiCall('/grab/html/', payload).then(data => {

        this.notify('Data received !!', 'success')
        console.log(data)

      }).finally(() => {

        this.active = false

      })
    }
  }
}
</script>