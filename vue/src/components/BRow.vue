<template>
  <div :class="cssClasses">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'BRow',
  data() {
    return {
        align: ['start', 'center', 'end', 'between']
    }
  },
  props: {
    alignV: String,
    alignH: String,
  },
  computed: {
    cssClasses() {
      let cls = ['row']
      if (this.align.indexOf(this.alignH) > -1) {
        cls.push('justify-content-' + this.alignH)
      }
      if (this.align.indexOf(this.alignV) > -1) {
        cls.push('align-items-' + this.alignV)
      }
      return cls
    }
  },
}
</script>