<template>
  <b-wrapper scroll container>

    <form @submit.prevent.stop="submitGrab">
      <b-row class="mb-5">
        <b-col class="position-relative">

          <div style="width: 30px;height:30px; position: absolute; top: 12px; left: -36px;">
            <transition name="fade" mode="out-in">
              <img v-if="grabber && grabber.icon" alt="" :src="icon" class="img-fluid"/>
            </transition>
          </div>
          <b-input size="lg" placeholder="https://" v-model="url" :disabled="active" @keyup="showIcon"/>
        </b-col>
        <b-col cols="auto">
          <b-btn size="lg" type="submit" :disabled="active">Grab</b-btn>
        </b-col>
      </b-row>

      <b-row v-if="endpoint === 'html'" class="mb-5">
          <b-col cols="6">
            <b-input size="lg" v-model="extractPattern" :disabled="active" placeholder="// . . ."></b-input>
          </b-col>
          <b-col cols="auto">
            <b-check size="lg" v-model="savePin">Save</b-check>
          </b-col>
          <b-col>
            <b-check size="lg" v-model="updateParse">Update</b-check>
          </b-col>
      </b-row>


      <b-row class="mb-5" v-if="foundElements">
        <b-col>
          <h3>Elements</h3>
          <div v-for="item in foundElements" class="mb-3 small">
            <div class="mono">{{ item.result }}</div>
          </div>
        </b-col>
      </b-row>

      <b-row v-if="htmlSource" class="mb-5">
        <b-col>
          <MonacoEditor
              width="100%"
              height="500"
              theme="vs-dark"
              language="text/html"
              :value="htmlSource"
              :options="editorOptions"
              @editorDidMount="editorDidMount"/>
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
import BRow from "../../components/BRow";
import BCol from "../../components/BCol";

export default {
  name: 'Grabber',
  mixins: [ PageMixin ],
  components: {BCol, BRow, MonacoEditor },
  data() {
    return {
      url: 'https://',
      icon: null,
      savePin: false,
      updateParse: false,
      active: false,
      extractPattern: null,
      grabberSettings: [],
      endpoint: null,
      foundElements: null,
      grabber: null,
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
      for (let grabber of this.grabberSettings) {
        for (let pattern of grabber.patterns) {
          let re = new RegExp(pattern, 'gi')
          if (re.test(this.url)) {
            this.icon = grabber.icon
            this.grabber = grabber
            this.endpoint = 'html'
            this.extractPattern = grabber.search_xpath
            return true
          }
        }
      }
      this.icon = null
      this.grabber = null
      this.endpoint = 'html'
      this.extractPattern = null
      this.itag = null
      this.foundElements = null
    },
    submitGrab() {
      this.active = true
      this.htmlSource = null
      let payload = {
        url: this.url,
        save: this.savePin,
        pattern: this.extractPattern,
        update_id: this.updateParse && this.grabber.id ? this.grabber.id : null,
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
          this.foundElements = !!data['elements'] ? data['elements'] : null
          this.htmlSource = body.replace(/\^\s+/, '')
          console.log(data)
        }
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
  },
  created() {
    getApiCall('/grab/').then(data => {
      this.grabberSettings = data
    })
  }
}
</script>