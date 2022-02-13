<template>
  <div class="fixed-wrapper flex-center">
    <div class="gradient-border">
      <label class="file-upload">
        <b-file v-model="file" :disabled="active"/>
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
      file: null,
      active: false,
    }
  },
  watch: {
    file(value, prevValue) {
      console.log(value, prevValue)
      if (value && value !== prevValue) {
        this.submitUpload()
      }
    }
  },
  methods: {
    submitUpload() {
      this.active = true
      let formData = new FormData()
      formData.append('file', this.file, this.file.name)
      return uploadApiCall('/upload/', formData).then( () => this.active = false )
    }
  }
}
</script>
