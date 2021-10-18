<template>
  <b-label v-if="label" :size="size">{{ label }}</b-label>
  <textarea :class="inputCss" v-bind="$attrs"></textarea>
</template>

<script>
import BLabel from './BLabel';
export default {
  name: 'BTextArea',
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
