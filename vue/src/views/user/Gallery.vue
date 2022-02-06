<template>
  <div class="container">
    <b-row align-v="center">
      <b-col>
        <h1>Gallery</h1>
      </b-col>
      <b-col cols="auto">
        <div class="file-upload">
          <input type="file" accept="image/*" @change="onChange"/>
          Choose File
        </div>
        <div v-if="file" class="ps-5">
          <b>{{ file.name }}</b>
          <b-btn variant="secondary" @click="uploadFile">Submit</b-btn>
        </div>
      </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col>
        <div v-for="item in items" :key="item.uid" class="pin-preview">
          {{ item.name ? item.name : item.uid}}
          <img :src="`/media/${item.user_id}/${item.uid}.${item.name.split('.').pop()}`">
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import {uploadApiCall, getApiCall} from 'services/http'

export default {
  name: 'Gallery',
  data() {
    return {
      file: '',
      items: [],
    }
  },
  methods: {
    onChange(event) {
      this.file = event.target.files[0]
    },
    uploadFile() {
      let formData = new FormData()
      formData.append('file', this.file, this.file.name)
      uploadApiCall('/pin/upload/', formData).then(data => {
        console.log(data)
        this.getFiles()
        this.file = ''
      }).catch(e => {
        console.log(e)
      })
    },
    getFiles() {
      getApiCall('/pin/').then(data => {
        this.items = data
      }).catch(e => {
        console.log(e)
      })
    },
    inputFile(newFile, oldFile) {
      if (newFile && oldFile && !newFile.active && oldFile.active) {
        // Get response data
        console.log('response', newFile.response)
        if (newFile.xhr) {
          //  Get the response status code
          console.log('status', newFile.xhr.status)
        }
      }
    },
    inputFilter(newFile, oldFile, prevent) {
      newFile.blob = ''
      let URL = window.URL || window.webkitURL
      if (URL && URL.createObjectURL) {
        newFile.blob = URL.createObjectURL(newFile.file)
      }
    }
  },
  created() {
    this.getFiles()
  }
}
</script>
