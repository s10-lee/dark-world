<template>
  <b-wrapper container>

    <form @submit.prevent.stop="submitGrab">
      <b-row class="mb-5">
        <b-col cols="auto" class="align-self-center">
          <div style="width: 30px;height:30px; text-align: right; margin-left: auto;">
            <transition name="fade" mode="out-in">
              <img v-if="icon" alt="" :src="icon" class="img-fluid"/>
            </transition>
          </div>
        </b-col>
        <b-col>
          <b-input size="lg" placeholder="https://" v-model="url" :disabled="active" @keyup="showIcon"/>
        </b-col>
        <b-col cols="auto">
          <b-btn size="lg" type="submit" :disabled="active">Grab</b-btn>
        </b-col>
      </b-row>

      <b-row v-if="endpoint === 'html'" class="mt-3">
          <b-col cols="6">
            <b-input size="lg" v-model="extractPattern" :disabled="active" placeholder="// . . ."></b-input>
          </b-col>
          <b-col cols="auto">
            <b-check size="lg" v-model="savePin">Save</b-check>
          </b-col>
      </b-row>

      <b-row class="mt-3" v-if="endpoint === 'youtube' && thumbnail && title">
        <b-col cols="3">
          <h4 class="text-secondary" v-if="title">{{ title }}</h4>
          <div v-if="thumbnail" class="mt-4">
            <img :src="thumbnail" :alt="title" style="width: 100%;"/>
          </div>
          <div class="mt-3" v-if="streams">
            <b-select size="lg" v-model="itag" :options="streams" :disabled="active"/>
          </div>
        </b-col>
      </b-row>
    </form>

  </b-wrapper>
</template>

<script>
import { getApiCall, postApiCall } from 'services/http'
import { PageMixin } from 'mixins'

export default {
  name: 'Grabber',
  mixins: [ PageMixin ],
  data() {
    return {
      url: null,
      icon: null,
      savePin: false,
      active: false,
      extractPattern: null,
      iconSettings: [],
      endpoint: null,

      // Youtube
      itag: null,
      title: null,
      thumbnail: null,
      streams: null,
    }
  },
  methods: {
    showIcon() {
      for (let { icon, patterns, type, search_xpath } of this.iconSettings) {
        for (let pattern of patterns) {
          let re = new RegExp(pattern, 'gi')
          if (re.test(this.url)) {
            this.icon = icon
            this.endpoint = type
            this.extractPattern = search_xpath
            return true
          }
        }
      }
      this.icon = null
      this.endpoint = null
      this.extractPattern = null
      this.itag = null
    },
    submitGrab() {
      this.active = true
      let payload = {
        url: this.url,
        save: this.savePin,
        pattern: this.extractPattern,
      }

      if (this.endpoint === 'youtube') {
        payload = {url: this.url, itag: this.itag}
      }

      postApiCall(`/grab/${this.endpoint}/`, payload).then(data => {
        this.notify('Data received !!', 'success')
        if (this.endpoint === 'youtube') {
          this.title = data['title']
          this.thumbnail = data['thumbnail']
          this.streams = data['streams']
        }
        console.log(data)
      }).catch(e => {
        this.notify('Server Error', 'danger')
        console.log(e.response)
      }).finally(() => {
        this.active = false
      })
    },
  },
  created() {
    getApiCall('/grab/').then(data => {
      this.iconSettings = data
    })
  }
}
</script>