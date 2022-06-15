<template>
  <b-wrapper scroll container>

    <b-row class="row-cols-1 row-cols-md-3 row-cols-lg-4 row-cols-xl-5" align-h="end">
      <b-col cols="1" class="position-relative">
        <label class="file-upload-btn">
          &plus;
          <b-file v-model="files" :disabled="active" multiple accept="image/*, audio/*, video/*"/>
        </label>
      </b-col>
    </b-row>

    <b-row v-if="items.length" class="row-cols-1 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4">
      <b-col v-for="pin in items" :key="pin.id">
        <div class="box-image-fit with-toolbar" style="max-height:18rem;">

          <b-light-box :src="pin.url" v-if="pin.type === 'image'">
            <img :src="pin.url"  alt="">
          </b-light-box>

          <div class="p-3" v-else-if="pin.type === 'video'">
            <video controls style="width:100%;height:100%;object-fit:cover;">
              <source :src="pin.url" type="video/mp4">
            </video>
          </div>

          <div class="p-3" v-else>
            <h5 class="text-300">{{ pin.name ? pin.name : '' }}</h5>
            <b class="text-500">{{ pin.content_type }}</b>
          </div>

          <b-toolbar>
            <b-btn class="px-3" variant="out-danger" @click.stop.prevent="removeFile(pin.id)">
              <i class="bi bi-trash-fill"></i>
            </b-btn>
          </b-toolbar>

        </div>
      </b-col>
    </b-row>
    <b-row align-h="center" v-else>
      <b-col cols="auto">
        <h1 class="mt-9 text-center text-muted">No Media</h1>
      </b-col>
    </b-row>
  </b-wrapper>
</template>

<script>
import {getApiCall, deleteApiCall, uploadApiCall} from 'services/http'
import { PageMixin } from 'mixins'

export default {
  name: 'List',
  mixins: [ PageMixin ],
  data() {
    return {
      items: [],
      active: null,
      files: null,
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
    removeFile(primaryKey) {
      if ( window.confirm('Delete ?') && primaryKey ) {
        this.loading(true )
        deleteApiCall( `/gallery/${primaryKey}/` ).then( () => {
          this.getFiles().then(() => this.loading(false ))
        })
      }
    },
    getFiles() {
      return getApiCall('/gallery/').then(data => this.items = data)
    },
    submitUpload() {
      this.active = true
      let formData = new FormData()
      for (let file of this.files){
        formData.append('files', file, file.name)
      }
      return uploadApiCall('/upload/', formData).then( data => {
        this.active = false
        this.getFiles()
      })
    }
  },
  mounted() {
    this.getFiles()
  }
}
</script>
