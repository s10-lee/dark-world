<template>
  <label :class="cssClasses">
    <slot></slot>
    <input type="checkbox"
           @change="$emit('update:modelValue', $event.target.checked)"
           :checked="modelValue">
    <span class="mark"></span>
  </label>
</template>

<script>
export default {
  name: 'BCheck',
  emits: ['update:modelValue'],
  props: {
    modelValue: [String, Boolean],
    size: [String, Number],
  },
  data() {
    return {
      sizes: ['xs', 'sm', 'lg', 'xl'],
    }
  },
  computed: {
    cssClasses() {
      const styles = ['check']
      if (this.sizes.includes(this.size)) {
        styles.push(`check-${this.size}`)
      }
      return styles
    },
  }
}
</script>