<template>
  <header v-bind="$attrs" class="navbar navbar-dark bg-dark shadow-sm navbar-expand-lg fixed-top px-3">
    <b-link class="navbar-brand" to="/" exact></b-link>
    <button class="navbar-toggler">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse">
      <div class="navbar-nav">
        <b-link class="nav-link" to="/" exact>#</b-link>
        <template v-if="$store.state.user">
          <b-link class="nav-link ms-3" to="/n00b" exact>Profile</b-link>
          <b-link class="nav-link ms-3" to="/n00b/gallery">Gallery</b-link>
          <b-link class="nav-link ms-3" to="/n00b/upload">Upload</b-link>
          <slot></slot>
        </template>
        <template v-else>
          <b-link class="nav-link" to="/sux0r">Sux0r</b-link>
        </template>
      </div>
      <div class="d-flex ms-auto" v-if="$store.state.user">
        <b-link class="nav-link text-danger" @click.prevent.stop="$store.dispatch('logoutToken')">logout</b-link>
      </div>
    </div>
  </header>
  <div style="height:60px;"></div>
</template>

<script>
export default {
  name: 'BNavbar',
}
</script>