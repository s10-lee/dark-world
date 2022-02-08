<template>
  <button type="button" :class="buttonCss" v-bind="$attrs"><slot></slot></button>
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

      if (!this.variant) {
        styles = ['btn', 'btn-secondary']
      } else if (this.variants.includes(this.variant)) {
        styles = ['btn', 'btn-' + this.variant]
      } else if (this.variants2.includes(this.variant)) {
        styles = ['btn-' + this.variant]
      } else if (this.variant.indexOf('out-') === 0) {
        let cls = this.variant.substring(4)
        if (this.variants.includes(cls)) {
          styles = ['btn', 'btn-outline-' + cls]
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