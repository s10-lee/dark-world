<template>
  <button type="button" :class="buttonCss"><slot></slot></button>
</template>

<script>
export default {
  name: 'BBtn',
  props: {
    block: Boolean,
    size: String,
    variant: String,
  },
  data() {
    return {
      sizes: ['xs', 'md', 'sm', 'lg', 'xl'],
      variants: ['primary', 'secondary', 'success', 'warning', 'danger', 'info', 'dark'],
      variants2: ['green', 'yellow', 'out']
    }
  },
  computed: {
    buttonCss() {
      let styles = []
      if (this.variants.includes(this.variant)) {
        styles.push('btn')
        styles.push('btn-' + this.variant)
      } else if (this.variants2.includes(this.variant)) {
        styles.push('btn-' + this.variant)
      }

      if (this.variant.indexOf('out-') === 0) {
        let cls = this.variant.substring(4)
        if (this.variants.includes(cls)) {
          styles.push('btn')
          styles.push('btn-outline-' + cls)
        }
      }

      if (this.sizes.includes(this.size)) {
        styles.push('btn-' + this.size)
      }
      if (this.block) {
        styles.push('btn-block')
      }

      return styles
    }
  }
}
</script>