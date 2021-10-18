<template>
  <b-label v-if="label" :size="size">{{ label }}</b-label>
  <input type="text" :class="inputCss" v-bind="$attrs">
</template>

<script>
import BLabel from './BLabel';
export default {
  name: 'BInput',
  components: {BLabel},
  props: {
    size: String,
    label: String
  },
  data() {
    return {
      sizes: ['xl', 'lg', 'md', 'sm', 'xl'],
    }
  },
  computed: {
    inputCss(){
      if (this.sizes.includes(this.size)) {
        return 'form-control-' + this.size
      }
      return 'form-control'
    },
  }
}
</script>