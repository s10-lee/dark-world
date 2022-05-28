<template>
  <div class="dropdown">
    <button :class="'btn border-secondary bg-dark block fw-normal w-100 dropdown-toggle' + (shown ? ' show' : '') + ' ' + getSize"
            type="button"
            style="text-align: left;"
            data-bs-toggle="dropdown"
            :disabled="disabled"
            @click.prevent.stop="onToggle">
      {{ displayTitle }}
    </button>
    <ul :class="'dropdown-menu dropdown-menu-dark block w-100'  + (shown ? ' show' : '')">
      <li v-for="item in options" :key="item.value">
        <button :class="'dropdown-item block w-100 ' + (item.value === modelValue ? ' active': '')"
                :disabled="disabled"
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
    disabled: Boolean,
  },
  emits: ['update:modelValue'],
  data() {
    return {
      sizes: ['xl', 'lg', 'md', 'sm', 'xs'],
      shown: false,
    }
  },
  computed: {
    getSize() {
      if (this.size && this.sizes.indexOf(this.size) > -1) {
        return 'btn-' + this.size
      }
      return ''
    },
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