<template>
  <b-wrapper container>

    <b-row class="mt-7">
      <h4 class="text-info">DEBUG TOAST</h4>
    </b-row>

    <b-row>
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
        <b-btn @click.stop.prevent="notify(message, type)">Test</b-btn>
      </b-col>
    </b-row>

  </b-wrapper>
</template>

<script>
import { PageMixin } from 'mixins'

export default {
  name: 'Debug',
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
      type: 'success',
    }
  },
  methods: {
    notify(message, type) {
      this.$store.dispatch('notify', {
        message: message,
        duration: parseInt(this.duration),
        type: type,
      })
    },
  }
}
</script>