<template>
    <div class="container">
      <div class="row">
        <div class="col">
          <h2 class="mt-5 fw-bold">Home Page</h2>
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
