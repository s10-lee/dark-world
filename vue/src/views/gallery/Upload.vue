<template>
  <div class="fixed-wrapper flex-center">
    <div class="gradient-border">
      <label class="file-upload">
        <b-file v-model="files" :disabled="active" multiple accept="image/*, audio/*, video/*"/>
        <span class="h1 fw-normal">Click to upload</span> <span class="h4 fw-normal">. . .</span>
      </label>
    </div>
  </div>
</template>

<script>
import { uploadApiCall } from 'services/http'
export default {
  name: 'Upload',
  data() {
    return {
      files: null,
      active: false,
    }
  },
  watch: {
    files(value, prevValue) {
      if (value && value !== prevValue) {
        this.submitUpload()
      }
    }
  },
  methods: {
    submitUpload() {
      this.active = true
      let formData = new FormData()
      for (let file of this.files){
        formData.append('files', file, file.name)
      }
      return uploadApiCall('/upload/', formData).then( data => {
        this.active = false
      })
    }
  }
}
</script>
