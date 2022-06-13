<template>
  <transition name="fade" mode="out-in">
    <b-navbar v-if="$store.state.user && $store.state.navbar" />
  </transition>

  <router-view v-slot="{ Component, route }">
    <transition name="fade" mode="out-in">
      <keep-alive>
        <component :is="Component" :key="route.fullPath" />
      </keep-alive>
    </transition>
  </router-view>

  <b-toaster />
  <b-loading />
</template>
