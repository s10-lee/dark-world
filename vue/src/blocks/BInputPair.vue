<template>
  <div class="row">
    <div class="col">
      <b-input :size="size" v-model="valueFirst" :placeholder="placeholderFirst" />
    </div>
    <div class="col">
      <b-input :size="size" v-model="valueSecond" :placeholder="placeholderLast" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'BInputPair',
  props: {
    valueFirst: String,
    valueSecond: String,
    size: String,
    placeholderFirst: String,
    placeholderLast: String,
  },
  emits: ['update:valueFirst', 'update:valueSecond'],
  data() {
    return {
      sizes: ['xl', 'lg', 'md', 'sm', 'xl'],
    }
  },
}
</script>