<template>
  <label :class="cssClasses"><slot></slot></label>
</template>

<script>
import { ComponentMixin } from 'mixins'
export default {
  name: 'BLabel',
  mixins: [ ComponentMixin ],
  props: {
    size: String,
  },
  data() {
    return {
      sizes: ['xl', 'lg', 'sm', 'xs']
    }
  },
  computed: {
    cssClasses() {
      if (this.sizes.includes(this.size)) {
        return 'form-label mb-0 col-form-label-' + this.size
      }
      return 'form-label mb-0'
    }
  }
}
</script>