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
        align: ['start', 'center', 'end', 'between', 'around', 'evenly']
    }
  },
  props: {
    alignV: String,
    alignH: String,
    gx: [String, Number],
    gy: [String, Number],
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
      if (this.gx) {
        cls.push(`gx-${this.gx}`)
      }
      if (this.gy) {
        cls.push(`gy-${this.gy}`)
      }
      return cls
    }
  },
}
</script>