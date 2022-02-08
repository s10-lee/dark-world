<template>
  <label :class="cssClasses"><slot></slot></label>
</template>

<script>
import { Component } from 'mixins'
export default {
  name: 'BLabel',
  mixins: [Component],
  props: {
    size: String,
  },
  data() {
    return {
      sizes: ['xl', 'lg', 'md', 'sm', 'xs']
    }
  },
  computed: {
    cssClasses() {
      if (this.sizes.includes(this.size)) {
        return 'form-label form-label-' + this.size
      }
      return 'form-label fw-bold'
    }
  }
}
</script>