<template>
  <b-wrapper container>
    <form @submit.prevent.stop="submitGrab">
      <b-row class="mb-5">
        <b-col>
          <b-input size="lg" placeholder="https://www.youtube.com/watch..." v-model="url" :disabled="active"/>
        </b-col>
        <b-col cols="auto">
          <b-btn size="lg" type="submit" :disabled="active">Grab</b-btn>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <b-select size="lg" v-model="itag" :options="streams" :disabled="active || !streams"/>
        </b-col>
      </b-row>

      <b-row class="mt-3">
        <b-col>
          <h4 v-if="title">{{ title }}</h4>
          <div v-if="thumbnail">
            <img :src="thumbnail" :alt="title" />
          </div>
        </b-col>
      </b-row>

    </form>
  </b-wrapper>
</template>

<script>
import { postApiCall } from 'services/http'
import { PageMixin } from 'mixins'

export default {
  name: 'Youtube',
  mixins: [ PageMixin ],
  data() {
    return {
      url: null,
      itag: null,
      title: null,
      thumbnail: null,
      active: false,
      streams: null,
    }
  },
  methods: {
    notify(message, type) {
      this.$store.dispatch('notify', {
        message: message,
        duration: 5000,
        type: type,
      })
    },
    submitGrab() {
      this.active = true
      const payload = {
        url: this.url,
        itag: this.itag,
      }
      postApiCall('/grab/youtube/', payload).then(data => {
        this.notify('Data received !!', 'success')
        this.streams = data.result
        this.thumbnail = data.thumbnail
        this.title = data.title

        console.log(data)
      }).finally(() => {
        this.active = false
      })
    },
  }
}
</script>