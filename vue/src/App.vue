<template>

  <router-view v-slot="{ Component, route }">
    <transition name="fade" mode="out-in">
        <component :is="Component" :key="route.fullPath" />
    </transition>
  </router-view>

  <b-loading />
  <b-toaster />

  <transition name="fade" mode="out-in">
    <b-navbar v-if="$store.state.user && $store.state.navbar" />
  </transition>

</template>
