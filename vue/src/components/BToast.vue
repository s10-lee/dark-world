<template>
  <transition
      name="notification"
      mode="out-in"
  >
    <div
        v-show="isActive"
        :class="['b-toast', `b-toast--${type}`, `b-toast--${position}`]"
        @click="click"
        role="alert"
        v-html="message"
    />
  </transition>
</template>

<script>

const POSITIONS = {
  TOP_RIGHT: 'top-right',
  TOP: 'top',
  TOP_LEFT: 'top-left',
  BOTTOM_RIGHT: 'bottom-right',
  BOTTOM: 'bottom',
  BOTTOM_LEFT: 'bottom-left'
}

export default {
  name: 'BToast',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'secondary'
    },
    position: {
      type: String,
      default: POSITIONS.BOTTOM_RIGHT,
      validator(value) {
        return Object.values(POSITIONS).includes(value)
      }
    },
    maxToasts: {
      type: [Number, Boolean],
      default: false
    },
    duration: {
      type: Number,
      default: 5000
    },
    dismissible: {
      type: Boolean,
      default: true
    },
    queue: {
      type: Boolean,
      default: false
    },
    pauseOnHover: {
      type: Boolean,
      default: true
    },
    useDefaultCss: {
      type: Boolean,
      default: true
    },
    onClose: {
      type: Function,
      default: () => {
      }
    },
    onClick: {
      type: Function,
      default: () => {
      }
    },
  },
  data() {
    return {
      isActive: false,
      parentTop: null,
      parentBottom: null,
      isHovered: false,
      timer: null
    }
  },
  computed: {
    transition() {
      return {
        enter: 'slideUp',
        leave: 'fade',
      }
    }
  },
  methods: {
    showNotice() {
      this.isActive = true
      if (this.duration) {
        this.timer = setTimeout(() => this.close(), this.duration)
      }
    },
    click() {
      this.onClick.apply(null, arguments)
      if (this.dismissible) {
        this.close()
      }
    },
    stopTimer() {
      this.timer && clearTimeout(this.timer)
    },
    close() {
      this.stopTimer()
      this.isActive = false
      setTimeout(() => {
        this.onClose.apply(null, arguments)
      }, 150)
    }
  },
  mounted() {
    this.showNotice()
  }
}
</script>
