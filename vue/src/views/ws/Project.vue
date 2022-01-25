<template>
  <div class="container">
    <div class="row mt-3">
      <div class="col">
        <h3 class="border-bottom pb-3 mb-3">Projects</h3>

        <div v-if="item && pk">
          <pre>{{ item }}</pre>
        </div>

        <div v-else>
          <div class="row" v-for="item in items" :key="item.uid">
            <div class="col"><b-link :to="'/ws/project/' + item.uid">{{ item.uid }}</b-link></div>
            <div class="col">{{ item.name }}</div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { apiCrudMixin } from 'mixins'
export default {
  mixins: [apiCrudMixin],
  data() {
    return {
      endpoint: '/ws/project'
    }
  },
}
</script>