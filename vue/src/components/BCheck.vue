<template>
  <label class="check">
    <slot></slot>
    <input type="checkbox"
           @change="$emit('update:modelValue', $event.target.checked)"
           :checked="modelValue">
    <span class="mark"></span>
  </label>
</template>

<script>
import BLabel from './BLabel';
export default {
  name: 'BCheck',
  components: { BLabel },
  emits: ['update:modelValue'],
  props: {
    modelValue: String,
    size: String
  },
  data() {
    return {
      sizes: ['xl', 'lg', 'md', 'sm', 'xl'],
    }
  },
  computed: {
    inputCss() {
      const styles = ['form-control']
      if (this.sizes.includes(this.size)) {
        styles.push('form-control-' + this.size)
      }
      return styles
    },
  }
}
</script>