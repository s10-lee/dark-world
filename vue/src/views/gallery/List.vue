<template>
  <b-wrapper scroll container>
    <b-row class="row-cols-1 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4">
      <b-col v-for="pin in items" :key="pin.uid">
        <div class="box-image-fit"
             @click.prevent.stop="removeFile(pin.id)"
             style="max-height:18rem;">
          <img :src="pin.url"  alt="">
        </div>
      </b-col>
    </b-row>
  </b-wrapper>
</template>

<script>
import { getApiCall, deleteApiCall } from 'services/http'
import { PageMixin } from 'mixins'

export default {
  name: 'Index',
  mixins: [ PageMixin ],
  data() {
    return {
      items: [],
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
  },
  created() {
    this.getFiles()
  }
}
</script>
