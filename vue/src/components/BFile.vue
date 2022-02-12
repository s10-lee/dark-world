<template>
    <input type="file" @change="onChange" v-bind="$attrs">
</template>

<script>
export default {
  name: 'BFile',
  props: ['modelValue'],
  emits: ['update:modelValue'],
  methods: {
    onChange(event) {
      this.$emit('update:modelValue', event.target.files[0])
    }
  }
}
</script>