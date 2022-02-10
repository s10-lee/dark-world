<template>
  <div class="fixed-container-scroll" style="padding-top: 56px;">
  <div class="container">
    <b-row align-v="center" class="mt-3">
      <b-col>
        <h3>Gallery</h3>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <gallery-form />
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
import Form from "./Form"

export default {
  name: 'Index',
  components: {
    GalleryForm: Form,
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
  },
  created() {
    this.getFiles()
  }
}
</script>
