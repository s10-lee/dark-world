<template>
  <div :class="cssClasses">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'BCol',
  props: {
    cols: [String, Number],
    offset: [String, Number]
  },
  computed: {
    cssClasses() {
      let cls = ['col']
      if (this.cols) {
        cls = ['col-' + this.cols]
      }
      if (this.offset) {
        cls.push('offset-' + this.offset)
      }
      return cls
    }
  },
}
</script>