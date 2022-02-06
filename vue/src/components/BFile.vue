<template>
  <label class="file-upload">
    <input type="file"
           @change="$emit('update:modelValue', $event.target.value)"
           :value="modelValue"
           v-bind="$attrs">
    <slot></slot>
  </label>
</template>

<script>
export default {
  name: 'BFile',
  props: ['modelValue'],
  emits: ['update:modelValue'],
}
</script>