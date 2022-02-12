<template>
  <div class="container">
    <b-row class="mt-5 row-cols-1 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4">
      <b-col v-for="pin in items" :key="pin.uid">
        <div class="card bg-dark">
          <img :src="pin.url" class="card-img-top" alt="">
          <div class="card-body">
            <h6 class="card-title">{{ pin.name ? pin.name : '&nbsp;'}}</h6>
            <!--  <b-btn size="sm" variant="out-danger">delete</b-btn> -->
          </div>
        </div>
      </b-col>
    </b-row>
    <div style="height: 5rem;"></div>
  </div>
</template>

<script>
import { getApiCall } from 'services/http'

export default {
  name: 'Index',
  data() {
    return {
      items: [],
    }
  },
  methods: {
    removeFile() {

    },
    getFiles() {
      getApiCall('/gallery/').then(data => this.items = data)
    },
  },
  created() {
    this.getFiles()
  }
}
</script>
