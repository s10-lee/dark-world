<template>
  <b-wrapper scroll container>
    <b-row class="mb-3">
      <b-col>
        <h3 class="text-800 text-uppercase">{{ title }}</h3>
      </b-col>
    </b-row>

    <b-row v-if="item">
      <b-col>

        <form @submit.prevent.stop="saveFormItem">
          <b-row class="mb-3" v-if="collections">
            <b-col>
              <b-select label="Collection" :options="collections" v-model="item['collection_id']"/>
            </b-col>
            <b-col cols="1">
              <b-input label="Position" v-model="item.position" type="number"/>
            </b-col>
          </b-row>
          <b-row align-h="start" align-v="end" class="mb-5">
            <b-col cols="auto">
              <div style="min-width: 9rem;">
                <b-select v-if="methods" label="Method" :options="methods" v-model="item.method "/>
              </div>
            </b-col>
            <b-col>
              <b-input label="URL" v-model="item.url" spellcheck="false" />
            </b-col>
          </b-row>

          <!--
          <b-row>
            <b-col cols="10">
              <nav class="nav nav-pills nav-justified">
                <button class="nav-link active" type="button">Params</button>
                <button class="nav-link" type="button">Headers</button>
                <button class="nav-link" type="button">Body</button>
              </nav>
              <div>
                ...
              </div>
            </b-col>
          </b-row>
          -->


          <b-row class="mb-5">
            <b-col>
              <b-label size="lg">Params</b-label>
              <b-row v-for="(p, index) in item.params" class="mb-3" align-v="start">
                <b-col cols="3" class="d-flex">
                  <b-check size="lg" v-model="item.params[index].is_active" class="mr-2 dark"/>
                  <b-input v-model="item.params[index].name" />
                </b-col>
                <b-col cols="3">
                  <b-input v-model="item.params[index].value" />
                </b-col>
                <b-col cols="auto">
                  <b-btn @click.stop.prevent="item.params.splice(index, 1);">&minus;</b-btn>
                </b-col>
              </b-row>
              <b-row>
                <b-col>
                  <b-btn variant="out-info" @click.stop.prevent="addParam">&plus;</b-btn>
                </b-col>
              </b-row>
            </b-col>
          </b-row>

          <b-row class="mb-3">
            <b-col>
              <b-label size="lg">Headers</b-label>
              <b-row v-for="(h, index) in item.headers" class="mb-3" align-v="center">
                <b-col cols="3" class="d-flex">
                  <b-check size="lg" v-model="item.headers[index].is_active" class="mr-2 dark"/>
                  <b-input v-model="item.headers[index].name" />
                </b-col>
                <b-col cols="3">
                  <b-input v-model="item.headers[index].value" />
                </b-col>
                <b-col cols="auto">
                  <b-btn @click.stop.prevent="item.headers.splice(index, 1);">&minus;</b-btn>
                </b-col>
              </b-row>

              <b-row>
                <b-col>
                  <b-btn variant="out-info" @click.stop.prevent="addHeader">&plus;</b-btn>
                </b-col>
              </b-row>

            </b-col>
          </b-row>

          <b-row class="mb-5">
            <b-col>
              <b-label size="lg">Data</b-label>
              <b-text-area rows="15" class="mono" v-model="item.data" spellcheck="false" />
            </b-col>
          </b-row>


          <b-row class="mb-7" align-h="end">
            <b-col>
              <b-btn size="lg" type="submit" class="me-5">Save</b-btn>
              <b-btn size="lg" variant="out-success" @click.prevent.stop="executeRequest">RUN</b-btn>
            </b-col>
            <b-col cols="auto">
              <b-btn v-if="'add' === pk" size="lg" variant="out-secondary" @click.prevent.stop="$router.push(routePath)">
                Cancel
              </b-btn>
              <b-btn v-else size="lg" variant="out-danger"  @click.prevent.stop="destroyItem(pk)">
                Delete
              </b-btn>
            </b-col>
          </b-row>
        </form>

        <b-row v-if="item.last_response">
          <b-col>

            <h3 class="text-500 mb-3">
              <span class="pe-3">{{ item.last_response.method }}</span>
              <span :class="statusColor">{{ item.last_response.status }}</span>
              <span class="ps-3 text-300">{{ item.last_response.url }}</span>
            </h3>

            <div class="p-3 mono fs-7 rounded-5 mb-3"
                 style="max-height: 400px; background: #14283b; color: #dee2e6; overflow: scroll; font-family: SFMono-Regular, Menlo, Monaco, 'Courier New', monospace">
              <div v-for="(value, key) in item.last_response.headers">
                <span>{{ key }}:</span> <span style="color: #00dcff;">{{ value }}</span>
              </div>
            </div>

            <div class="p-3 mono fs-7 rounded-5 mb-3" style="background: #2b3035; overflow: scroll;max-height: 400px;">
              <pre><code>{{ item.last_response.body ? item.last_response.body : 'EMPTY' }}</code></pre>
            </div>

          </b-col>
        </b-row>

        <b-row v-if="parsers" align-v="end" class="mb-3">
          <b-col>
            <b-select size="lg"
                      label="Choose Parser"
                      v-model="currentParser"
                      :options="parsers.map(p => { return {'text': p.name, 'value': p.id} })" />
          </b-col>
          <b-col cols="auto">
            <b-btn size="lg" variant="secondary" @click.prevent.stop="applyParser">Apply</b-btn>
          </b-col>
        </b-row>

        <b-row v-if="parsers && currentParser" class="mb-7">
          <b-col>
            <div class="p-3 bg-dark mono">{{ parsers.find(p => p.id === currentParser ).search_pattern }}</div>
          </b-col>
        </b-row>

      </b-col>
    </b-row>

    <b-row v-else>
      <b-col>
        <div class="text-end mb-5">
          <b-btn variant="out-info"
                 @click="$router.push(routePath + '/add')">Create</b-btn>
        </div>
        <b-table bordered
                 :pk-name="pkName"
                 :fields="fields"
                 :items="items"
                 :route-path="routePath" />
      </b-col>
    </b-row>

  </b-wrapper>
</template>

<script>
import Collection from 'views/scrape/Collection';
import {getApiCall, postApiCall} from 'services/http'
import MonacoEditor from 'monaco-editor-vue3'

export default {
  name: 'Request',
  components: { MonacoEditor },
  extends: Collection,
  data() {
    return {
      title: 'Requests',
      endpoint: '/http-request/',
      methods: null,
      result: null,
      collections: null,
      parsers: null,
      currentParser: null,

      editorOptions: {
        minimap: { enabled: false },
        // autoIndent: 'full',
        // wrappingIndent: 'none',
        lineNumbers: 'none',
        formatOnPaste: true,
        formatOnType: true,
        // automaticLayout: true,
        quickSuggestions: true,
      },
      fields: [
        {field: 'id', title: 'ID', type: String, link: true},
        {field: 'method', title: 'Method', type: String},
        {field: 'url', title: 'URL', type: String},
        {field: 'params', title: 'Params', type: Array, in_list: false, default: []},
        {field: 'headers', title: 'Headers', type: Array, in_list: false, default: []},
        {field: 'data', title: 'Data', type: String, in_list: false},
        {field: 'position', title: 'Pos', type: Number},
        {field: 'collection_id', name: 'Collection', type: String, in_list: false},
      ]
    }
  },
  computed: {
    statusColor() {
      let cssClass = ''
      const result = this.item.last_response
      if (result['status']) {
        if (result['status'] >= 200) {
          cssClass = 'text-success'
        }
        if (result['status'] >= 300) {
          cssClass = 'text-info'
        }
        if (result['status'] >= 400) {
          cssClass = 'text-warning'
        }
        if (result['status'] >= 500) {
          cssClass = 'text-danger'
        }
      }
      return cssClass
    }
  },
  methods: {
    applyParser() {
      getApiCall('/http-parser/' + this.currentParser + '/parse-response/' + this.item.last_response.id + '/')
      .then(data => {
        console.log(data)
      })
    },
    executeRequest() {
      this.loading(true)
      getApiCall('/http-request/' + this.pk + '/exec/')
          .then(data => this.item['last_response'] = data)
          .then(() => this.loading(false))
    },
    addParam() {
      if (!this.item.params || !this.item.params.length) {
        this.item.params = []
      }
      this.item.params.push({'name': '', 'value': '', 'is_active': true})
    },
    addHeader() {
      if (!this.item.headers || !this.item.headers.length) {
        this.item.headers = []
      }
      this.item.headers.push({'name': '', 'value': '', 'is_active': true})
    }
  },
  mounted() {
    getApiCall('/ws-parser/').then(data => this.parsers = data)
    getApiCall('/ws-methods/').then(data => this.methods = data)
    getApiCall('/ws-collection/').then(data => {
      this.collections = data.map(collection => {
        return {
          'text': collection['name'],
          'value': collection['id'],
        }
      })
    })
  },
}
</script>