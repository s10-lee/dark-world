<template>
  <transition name="fade">
    <div id="page-loading" v-if="$store.state.loading">
      <div style="position: absolute; top: 40%; left:50%; transform: translateX(-50%)">
        <h1 class="text-600">...</h1>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'BLoading',
}
</script>