<template>
    <a href="#" @click.stop.prevent="onOpen" class="light-box-preview">
      <slot></slot>
    </a>
    <transition name="fade" mode="out-in" @after-enter="shown = true">
      <div v-if="display" class="light-box-backdrop">
        <transition name="slideUp" mode="out-in" @after-leave="onClose" appear>
          <div class="light-box-container" v-if="shown" @click="shown = false">
            <div class="light-box-body">
              <a v-focus @keydown.esc="shown = false" href="#"><img :src="src" alt=""/></a>
            </div>
          </div>
        </transition>
      </div>
    </transition>
</template>

<script>
import { SET_NAVBAR_DISPLAY } from 'store/types'

export default {
  name: "BLightBox",
  data() {
    return {
      shown: false,
      display: false
    }
  },
  props: ['w', 'h', 'src'],
  methods: {
    onClose() {
      this.display = false
      this.$store.commit(SET_NAVBAR_DISPLAY, true)
    },

    onOpen() {
      this.$store.commit(SET_NAVBAR_DISPLAY, false)
      this.display = true
    },
  },
}
</script>
