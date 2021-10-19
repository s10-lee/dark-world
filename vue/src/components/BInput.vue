<template>
  <b-label v-if="label" :size="size">{{ label }}</b-label>
  <input :class="inputCss"
         :value="modelValue"
         @input="$emit('update:modelValue', $event.target.value)"
         v-bind="$attrs">
</template>

<script>
import BLabel from './BLabel';
export default {
  name: 'BInput',
  components: { BLabel },
  props: {
    modelValue: String,
    size: String,
    label: String
  },
  emits: ['update:modelValue'],
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