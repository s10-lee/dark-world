<template>
  <div class="dropdown">
    <button :class="'btn bg-white border block fw-normal w-100 dropdown-toggle' + (shown ? ' show' : '') "
            type="button"
            style="text-align: left;"
            data-bs-toggle="dropdown"
            @click.prevent.stop="onToggle">
      {{ displayTitle }}
    </button>
    <ul :class="'dropdown-menu block w-100'  + (shown ? ' show' : '')">
      <li v-for="item in options" :key="item.value">
        <button :class="'dropdown-item block w-100 ' + (item.value === modelValue ? ' active': '')"
                @click="onSelect(item.value)"
                type="button">{{ item.text }}</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'BSelect',
  props: {
    modelValue: String,
    size: String,
    label: String,
    options: [Array, Object],
    emptyTitle: String,
  },
  emits: ['update:modelValue'],
  data() {
    return {
      sizes: ['xl', 'lg', 'md', 'sm', 'xl'],
      shown: false,
    }
  },
  computed: {
    displayTitle() {
      if (this.modelValue && this.options) {
        return this.options.find(item => this.modelValue === item.value).text
      }
      return this.emptyTitle || ' --- '
    }
  },
  methods: {
    onSelect(value) {
      this.$emit('update:modelValue', value)
      this.shown = false
    },
    onToggle() {
      this.shown = !this.shown
    }
  }
}
</script>