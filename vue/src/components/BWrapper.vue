<template>
  <div :class="cssWrapper">
    <div :class="cssContainer">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BWrapper',
  props: {
    scroll: {
      type: Boolean,
      default: false,
    },
    container: {
      type: Boolean,
      default: false,
    },
    fluid: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    cssWrapper() {
      return this.scroll ? 'fixed-wrapper-scroll' : 'fixed-wrapper'
    },
    cssContainer() {
      if (this.container) {
        return this.fluid ? 'container-fluid' : 'container'
      }
      return ''
    }
  }
}
</script>