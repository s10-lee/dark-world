<template>
  <b-wrapper scroll container>

    <form @submit.prevent.stop="submitGrab">
      <b-row class="mb-5">
        <b-col class="position-relative">

          <div style="width: 30px;height:30px; position: absolute; top: 12px; left: -36px;">
            <transition name="fade" mode="out-in">
              <img v-if="icon" alt="" :src="icon" class="img-fluid"/>
            </transition>
          </div>

          <b-input size="lg" placeholder="https://" v-model="url" :disabled="active" @keyup="showIcon"/>
        </b-col>
        <b-col cols="auto">
          <b-btn size="lg" type="submit" :disabled="active">Grab</b-btn>
        </b-col>
      </b-row>

      <b-row v-if="endpoint === 'html'" class="mt-3">
          <b-col cols="6">
            <b-input size="lg" v-model="extractPattern" :disabled="active" placeholder="// . . ."></b-input>
          </b-col>
          <b-col cols="auto">
            <b-check size="lg" v-model="savePin">Save</b-check>
          </b-col>
      </b-row>

      <b-row v-if="htmlSource" class="mt-5">
        <b-col>
          <h3>Source code</h3>

          <MonacoEditor
              width="100%"
              height="500"
              theme="vs-dark"
              language="text/html"
              :value="htmlSource"
              :options="editorOptions"
              @editorDidMount="editorDidMount"
              @change="onChange"
          ></MonacoEditor>
        </b-col>
      </b-row>

      <b-row class="mt-3" v-if="endpoint === 'youtube' && thumbnail && title">
        <b-col cols="3">
          <h4 class="text-secondary" v-if="title">{{ title }}</h4>
          <div v-if="thumbnail" class="mt-4">
            <img :src="thumbnail" :alt="title" style="width: 100%;"/>
          </div>
          <div class="mt-3" v-if="streams">
            <b-select size="lg" v-model="itag" :options="streams" :disabled="active"/>
          </div>
        </b-col>
      </b-row>
    </form>

  </b-wrapper>
</template>

<script>
import { getApiCall, postApiCall } from 'services/http'
import { PageMixin } from 'mixins'
import MonacoEditor from 'monaco-editor-vue3'

export default {
  name: 'Grabber',
  mixins: [ PageMixin ],
  components: { MonacoEditor },
  data() {
    return {
      url: 'https://',
      icon: null,
      savePin: false,
      active: false,
      extractPattern: null,
      iconSettings: [],
      endpoint: null,

      editor: null,

      // Youtube
      itag: null,
      title: null,
      thumbnail: null,
      streams: null,

      // HTML
      htmlSource: null,
      editorOptions: {
        minimap: { enabled: false },
        // autoIndent: 'full',
        // wrappingIndent: 'none',
        formatOnPaste: true,
        formatOnType: true,
        // automaticLayout: true,
        quickSuggestions: true,
      },
    }
  },
  methods: {
    showIcon() {
      for (let { icon, patterns, type, search_xpath } of this.iconSettings) {
        for (let pattern of patterns) {
          let re = new RegExp(pattern, 'gi')
          if (re.test(this.url)) {
            this.icon = icon
            this.endpoint = type
            this.extractPattern = search_xpath
            return true
          }
        }
      }
      this.icon = null
      this.endpoint = 'html'
      this.extractPattern = null
      this.itag = null
    },
    submitGrab() {
      this.active = true
      this.htmlSource = null
      let payload = {
        url: this.url,
        save: this.savePin,
        pattern: this.extractPattern,
      }

      if (this.endpoint === 'youtube') {
        payload = {url: this.url, itag: this.itag}
      }

      postApiCall(`/grab/${this.endpoint}/`, payload).then(data => {
        this.notify('Data received !!', 'success')
        if (this.endpoint === 'youtube') {
          this.title = data['title']
          this.thumbnail = data['thumbnail']
          this.streams = data['streams']
        } else {
          let { body = '' } = data['response']
          body = body.replace(/\^\s+/, '')
          this.htmlSource = body
        }
        console.log(data)
      }).catch(e => {
        this.notify('Server Error', 'danger')
        console.log(e.response)
      }).finally(() => {
        this.active = false
      })
    },
    editorDidMount(editor) {
      this.editor = editor
      console.log('editor mounted !')
    },
    onChange(value) {
      // console.log(this.editor)
    },
  },
  created() {
    getApiCall('/grab/').then(data => {
      this.iconSettings = data
    })
  }
}
</script>