<template>
    <div class="container h-100">
      <div class="row justify-content-center align-items-end h-100">
        <div class="col-auto h-100">
          <img src="../assets/icon/moon.png" class="moon-img">
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'Home',
  mounted() {
    this.$store.commit('loaded')
  }
}
</script>
