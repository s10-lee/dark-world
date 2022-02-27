<template>
  <div class="b-toast-container b-toast-container--bottom">
    <b-toast v-for="item in notifications"
             :message="item.message"
             :type="item.type"
             :duration="item.duration"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'BToaster',
  computed: mapState([
      'notifications'
  ])
}
</script>