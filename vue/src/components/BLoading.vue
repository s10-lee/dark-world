<template>
  <transition name="fade">
    <div id="page-loading" v-if="$store.state.loading">
      <div style="position: absolute; top: 40%; left:50%; transform: translateX(-50%)">
        <h1 class="text-600">Loading...</h1>
        <!--
        <div class="spinner-border text-light" style="width: 4rem; height: 4rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        -->
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'BLoading',
}
</script>