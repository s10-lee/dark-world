<template>
  <router-link
      :to="toHref"
      custom
      v-slot="{ href, route, navigate, isActive, isExactActive }"
  >
    <a :href="href"
       @click="navigate"
       v-bind="$attrs"
       :data-exact-active="isExactActive ? 'true' : 'false'"
       :data-active="isActive ? 'true' : 'false'"
       :class="[
           ($route.fullPath === route.fullPath || isExactActive) && exact && $router.options.linkExactActiveClass,
           ($route.fullPath.indexOf(route.fullPath) === 0 || isActive) && !exact && $router.options.linkActiveClass
           ]">
      <slot></slot>
    </a>
  </router-link>
</template>

<script>
export default {
  name: 'BLink',
  props: {
    to: String,
    exact: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    toHref() {
      return this.to ? this.to : '#'
    }
  }
}
</script>