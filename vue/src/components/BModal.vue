<template>

  <transition name="fade" mode="out-in"
              @after-enter="dialogShown = true"
              @before-leave="dialogShown = false"
  >
  <div v-if="shown">
    <transition name="slideDown" mode="out-in">
    <div v-if="dialogShown"
         class="modal fade show"
         tabindex="-1"
         aria-modal="true"
         aria-hidden="false"
         style="display: block;"
         role="dialog">


          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 v-if="title" class="modal-title">{{ title }}</h5>
                <slot name="header"></slot>
                <button type="button" class="btn-close" @click="onClose"></button>
              </div>
              <div class="modal-body">
                <slot name="body"></slot>
              </div>
              <div class="modal-footer">
                <slot namer="footer"></slot>
                <button type="button" class="btn btn-secondary" @click="onClose">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
              </div>
            </div>
          </div>


    </div>
    </transition>

    <div class="modal-backdrop fade show"></div>
  </div>
  </transition>
</template>

<script>
export default {
  name: 'BModal',
  props: {
    shown: Boolean,
    title: String,
  },
  data() {
    return {
      dialogShown: false,
    }
  },
  computed: {
    cssClasses(){
      return 'modal fade' + (this.shown ? ' show': '')
    },
    cssStyle(){
      return this.shown ? 'display:block;' : 'display:none;'
    }
  },
  methods: {
    onClose() {
      this.$emit('close', this.shown)
    },
    beforeEnter() {

    }
  }
}
</script>