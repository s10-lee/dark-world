<template>
  <div class="fixed-container flex-center">
    <div class="file-upload">
      <h1>Choose file ...</h1>
      <b-file v-model="file" :disabled="active"/>
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
