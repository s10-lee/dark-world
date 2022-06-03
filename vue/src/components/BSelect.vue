<template>
  <div class="dropdown">
    <button :class="'btn dropdown-toggle' + (shown ? ' show' : '') + ' ' + getSize"
            type="button"
            style="text-align: left;"
            data-bs-toggle="dropdown"
            :disabled="disabled"
            @click.prevent.stop="onToggle">
      {{ displayTitle }}
    </button>
    <ul :class="'dropdown-menu dropdown-menu-dark block w-100'  + (shown ? ' show' : '')">
      <li v-for="item in getOptions" :key="item.value">
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
    modelValue: [String, Number],
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
    getOptions() {
      if (this.options && !Array.isArray(this.options)) {
        const options = []
        for (const [value, text] of Object.entries(this.options)) {
          options.push({'value': value, 'text': text})
        }
        return options
      }
      return this.options
    },
    displayTitle() {
      if (this.modelValue && this.options) {

        if (Array.isArray(this.options)) {
          return this.options.find(item => this.modelValue === item.value).text
        }
        return this.options[this.modelValue]
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