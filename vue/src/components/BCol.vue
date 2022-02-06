<template>
  <div :class="cssClasses">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'BCol',
  props: {
    cols: String
  },
  computed: {
    cssClasses() {
      let cls = ['col']
      if (this.cols) {
        cls = ['col-' + this.cols]
      }
      return cls
    }
  },
}
</script>