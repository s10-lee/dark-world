<template>
  <b-loading />
  <b-navbar v-if="$store.state.user"></b-navbar>
  <router-view v-slot="{ Component, route }">
    <transition name="fade" mode="out-in">
      <component :is="Component" :key="route.fullPath" />
    </transition>
  </router-view>
</template>
