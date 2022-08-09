<template>
  <div>
    <button :class="cssButton" type="button">{{ title }}</button>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'BTab',
  props: {
    isActive: Boolean,
  },
  data() {
    return {
      title: null,
    }
  },
  computed: {
    cssButton() {
      return this.isActive ? 'nav-link active' : 'nav-link'
    }
  }
}
</script>
