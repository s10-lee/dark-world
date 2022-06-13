<template>
  <header v-bind="$attrs" class="navbar navbar-dark bg-dark shadow-sm border-bottom navbar-expand-lg fixed-top px-3">
    <b-link class="navbar-brand" to="/" exact></b-link>
    <button class="navbar-toggler">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse">
      <div class="navbar-nav">
        <b-link class="nav-link" to="/" exact>#</b-link>
        <b-link class="nav-link ms-3" to="/n00b/" exact>Profile</b-link>
        <b-link class="nav-link ms-3" to="/n00b/gallery/">Gallery</b-link>
        <b-link class="nav-link ms-3" to="/n00b/upload/">Upload</b-link>
        <b-link class="nav-link ms-3" to="/n00b/grab/">Grab</b-link>
      </div>
      <div class="navbar-nav ms-auto">
        <b-link class="nav-link" @click.prevent="logout">logout</b-link>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'BNavbar',
  methods: {
    logout() {
      this.$store.dispatch('logoutToken')
    }
  }
}
</script>