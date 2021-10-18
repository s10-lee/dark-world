<template>
  <button type="button" :class="buttonCss"><slot></slot></button>
</template>

<script>
export default {
  name: 'BBtn',
  props: {
    size: String,
    variant: String,
  },
  data() {
    return {
      sizes: ['xl', 'lx', 'md', 'sm', 'xl'],
      variants: ['primary', 'secondary', 'success', 'warning', 'danger', 'info'],
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
      if (this.sizes.includes(this.size)) {
        styles.push('btn-' + this.size)
      }

      return styles
    }
  }
}
</script>