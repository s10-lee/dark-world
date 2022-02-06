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
          <b-link class="nav-link" to="/n00b" exact>Profile</b-link>
          <b-link class="nav-link" to="/n00b/gallery">Gallery</b-link>
          <!--
          <b-link class="nav-link" to="/ws/project">wScrap</b-link>
          <b-link class="nav-link" to="/m1r0">m1r0</b-link>
          -->
        </template>
        <template v-else>
          <b-link class="nav-link" to="/sux0r">Sux0r</b-link>
        </template>
      </div>
    </div>
  </header>
  <div style="height:56px;"></div>
</template>

<script>
import BLink from "./BLink";
export default {
  name: 'BNavbar',
  components: {BLink}
}
</script>