<template>
  <div class="row">
    <div class="col">
      <b-input :size="size" :placeholder="placeholderFirst" />
    </div>
    <div class="col">
      <b-input :size="size" :placeholder="placeholderLast" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'BInputPair',
  props: {
    size: String,
    placeholders: [Array],
    placeholderFirst: String,
    placeholderLast: String,
  },
  data() {
    return {
      sizes: ['xl', 'lg', 'md', 'sm', 'xl'],
    }
  },
}
</script>