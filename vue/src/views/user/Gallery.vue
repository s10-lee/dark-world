<template>
  <div class="fixed-container-scroll pt-6">
  <div class="container">
    <b-row align-v="center">
      <b-col>
        <h1>Gallery</h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <pin-create-form/>
      </b-col>
    </b-row>
    <b-row class="mt-3 row-cols-1 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4">
      <b-col v-for="item in items" :key="item.uid">
        <div class="card bg-dark">
          <img :src="item.url" class="card-img-top" alt="">
          <div class="card-body">
            <h6 class="card-title">{{ item.name ? item.name : '&nbsp;'}}</h6>
            <b-btn size="sm" variant="out-danger">delete</b-btn>
          </div>
        </div>
      </b-col>
    </b-row>
    <div style="height: 5rem;"></div>
  </div>
  </div>
</template>

<script>
import {uploadApiCall, getApiCall, deleteApiCall} from 'services/http'
import PinCreateForm from "./PinCreateForm"

export default {
  name: 'Gallery',
  components: {
    PinCreateForm
  },
  data() {
    return {
      file: '',
      items: [],
    }
  },
  methods: {
    removeFile() {

    },
    onChange(event) {
      this.file = event.target.files[0]
    },
    uploadFile(event) {
      this.file = event.target.files[0]
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
