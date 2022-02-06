<template>
  <b-navbar/>
  <div class="fixed-container-scroll pt-6">
    <router-view v-slot="{ Component, route }">
      <transition name="fade" mode="out-in">
        <component :is="Component" :key="route.fullPath"/>
      </transition>
    </router-view>
  </div>
</template>

<script>
export default {
  name: 'Index'
}
</script>