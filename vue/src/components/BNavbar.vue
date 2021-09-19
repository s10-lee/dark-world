<template>
  <header v-bind="$attrs" class="navbar navbar-dark navbar-expand-lg fixed-top px-3">
    <b-link class="navbar-brand" to="/" exact><small class="moon-text">D4RKVV0R1D</small></b-link>
    <button class="navbar-toggler">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse">
      <div class="navbar-nav">
<!--        <b-link class="nav-link" to="/project/">get out</b-link>-->
      </div>
    </div>
  </header>
  <div style="min-height:4rem;">&nbsp;</div>
</template>

<script>
export default {
  name: 'BNavbar'
}
</script>