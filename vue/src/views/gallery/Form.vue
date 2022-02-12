<template>
  <div class="pin-create">
    <b-row align-v="end">
      <b-col>
        <b-input placeholder="https://" size="lg" v-model="url" :disabled="active"/>
      </b-col>
      <b-col cols="auto">
        <b-btn size="lg" variant="secondary" @click="submitGrab" :disabled="active">GO</b-btn>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import {postApiCall, uploadApiCall} from 'services/http'
export default {
  name: 'Form',
  data() {
    return {
      url: null,
      file: null,
      progress: 0,
      active: false,
    }
  },
  methods: {
    submitGrab() {
      this.active = true
      postApiCall('/pin/grab/', {url: this.url})
          .then(() => {
            this.active = false
            this.url = null
          })
    },
    submitUpload() {
      if (!this.file) {
        return console.log('Empty file')
      }
      this.active = true
      let formData = new FormData()
      formData.append('file', this.file, this.file.name)
      uploadApiCall('/pin/upload/', formData)
          .then(() => {
            this.active = false
            this.file = null
          })
    }
  }
}
</script>