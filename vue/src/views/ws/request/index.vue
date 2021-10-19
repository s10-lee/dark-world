<template>
  <div>
    <h3 class="border-bottom mb-3">Requests: </h3>
    <div class="text-center text-pre">
      {{ items }}


    </div>

  </div>
</template>

<script>
import { getApiCall } from 'services/http'

export default {
  data() {
    return {
      items: null
    }
  },
  created() {
    getApiCall('/ws/request/').then(data => {
      // this.items = data
      console.log(data);
    })
  }
}
</script>