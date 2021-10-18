<template>
  <label :class="cssClasses"><slot></slot></label>
</template>

<script>
export default {
  name: 'BLabel',
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
        return 'form-label-' + this.size
      }
      return 'form-label fw-bold'
    }
  }
}
</script>