<template>
  <div>
    <h3 class="border-bottom pb-3 mb-3">Projects: </h3>
    <div class="row" v-for="item in items">
      <div class="col">{{ item.uid }}</div>
      <div class="col">{{ item.name }}</div>

    </div>
  </div>
</template>

<script>
import { getApiCall } from 'services/http'
export default {
  data() {
    return {
      items: [],
    }
  },
  async mounted() {
    this.items = await getApiCall('/ws/project/')
  }
}
</script>