<template>
  <div class="container-fluid">
    <div class="row justify-content-center">
      <div class="col-6 col-lg-6 col-md-10 col-sm-12">
        <transition name="fade" mode="out-in">
        <div v-if="error" class="alert alert-danger text-center" role="alert">
          <h2 class="fw-bold">{{ error.response.status }}</h2>
          <h3 class="fw-bolder">{{ error.response.statusText }}</h3>
        </div>
        <div v-else-if="done" class="mt-5 text-center">
          <a href="#" @click="onCopy" class="color-text copy-link fs-3 fw-bold">{{ origin + '/1/' + done.code }}</a>
        </div>
        <form @submit.prevent.stop="onSubmit" v-else>
          <div class="mb-5">
            <input type="text" v-model="fullurl" class="form-control p-3 form-control-lg d-block w-100" placeholder="https://" autocomplete="Off" spellcheck="false">
          </div>
          <button class="btn mx-auto px-6 btn-lg btn-green d-block" type="submit">
            Make Short
          </button>
        </form>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import {xhr} from 'services'

export default {
  name: "Link",
  data() {
    return {
      error: null,
      done: null,
      fullurl: null,
      origin: null,
    }
  },
  methods: {
    onSubmit() {
      let parsedUrl = ''
      if (this.fullurl) {

        try {
          parsedUrl = new URL(this.fullurl)
        } catch (e) {
          console.log(e)
          return false
        }

        if (parsedUrl) {
          const expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi
          const re = new RegExp(expression);

          if (re.test(this.fullurl)) {
            xhr.post('/link/', {url: parsedUrl}).then(r => r.data).then(data => {this.done = data
            }).catch(e => {
              this.error = e
            })
          }
        }
      }
    },
    onCopy(e) {
      const text = e.target.innerText
      navigator.clipboard.writeText(text)
      e.preventDefault()
      e.stopPropagation()
    }
  },
  created() {
    this.origin = new URL(location.href).origin
  }
}
</script>
