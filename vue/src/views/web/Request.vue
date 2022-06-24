<template>
  <b-wrapper scroll container>

    <b-row>
      <b-col>
        <h3>{{ title }}</h3>
      </b-col>
    </b-row>

    <b-row v-if="item">
      <b-col>
        <b-label size="lg"><b-link :to="'/n00b/collection/' + item['collection_id']">Collection</b-link></b-label>

        <form @submit.prevent.stop="saveFormItem">
          <b-row class="mb-5" v-if="collections">
            <b-col>
              <b-select size="lg" :options="collections" v-model="item['collection_id']"/>
            </b-col>
          </b-row>
          <b-row align-h="start" align-v="end" class="mb-5">
            <b-col cols="2">
              <b-select size="lg" label="Method" :options="methods" v-model="item.method "/>
            </b-col>
            <b-col>
              <b-input size="lg" label="URL" v-model="item.url" spellcheck="false" />
            </b-col>
            <b-col cols="1">
              <b-input size="lg" label="Position" v-model="item['position']" type="number"/>
            </b-col>
          </b-row>

          <b-row class="mb-5">
            <b-col>
              <b-label size="lg">Params</b-label>
              <b-row v-for="(p, index) in item.params" class="mb-3" align-v="start">
                <b-col cols="4" class="d-flex">
                  <b-check size="lg" v-model="item.params[index].is_active" class="mr-2"/>
                  <b-input v-model="item.params[index].name" />
                </b-col>
                <b-col cols="4">
                  <b-input v-model="item.params[index].value" />
                </b-col>
                <b-col cols="auto">
                  <b-btn @click.stop.prevent="item.params.splice(index, 1);">&minus;</b-btn>
                </b-col>
              </b-row>
              <b-row class="mt-5">
                <b-col>
                  <b-btn variant="out-success" @click.stop.prevent="addParam">&plus;</b-btn>
                </b-col>
              </b-row>
            </b-col>
          </b-row>

          <b-row class="mb-5">
            <b-col>
              <b-label size="lg">Headers</b-label>

              <b-row v-for="(h, index) in item.headers" class="mb-3" align-v="center">
                <b-col cols="4" class="d-flex">
                  <b-check size="lg" v-model="item.headers[index].is_active" class="mr-2"/>
                  <b-input v-model="item.headers[index].name" />
                </b-col>
                <b-col cols="4">
                  <b-input v-model="item.headers[index].value" />
                </b-col>
                <b-col cols="auto">
                  <b-btn @click.stop.prevent="item.headers.splice(index, 1);">&minus;</b-btn>
                </b-col>
              </b-row>

              <b-row class="mt-5">
                <b-col>
                  <b-btn variant="out-success" @click.stop.prevent="addHeader">&plus;</b-btn>
                </b-col>
              </b-row>

            </b-col>
          </b-row>

          <b-row class="mb-5">
            <b-col>
              <b-label size="lg">Data</b-label>
              <b-text-area rows="20" class="mono" v-model="item.data" spellcheck="false" />
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

        <b-row v-if="result">
          <b-col>
            <h2 class="text-500 mb-3">{{ result['method'] }} &nbsp; <span :class="statusColor">{{ result['status'] }}</span></h2>
            <h4 class="text-300 mono fw-normal mb-5">{{ result['url']}}</h4>

            <div class="p-3 rounded-3 bg-gray-600 mb-3">
              <div v-for="(value, key) in result['headers']">
                <b>{{ key }}:</b>  &nbsp; {{ value }}
              </div>
            </div>

            <div class="p-3 rounded-3 bg-secondary">
              <pre><code>{{ result.body ? result.body : 'EMPTY' }}</code></pre>
            </div>
          </b-col>
        </b-row>

      </b-col>
    </b-row>

    <b-row v-else>
      <b-col>
        <div class="text-end mb-5">
          <b-btn size="lg"
                 variant="out-primary"
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
import Collection from 'views/web/Collection';
import { getApiCall } from 'services/http'
import MonacoEditor from 'monaco-editor-vue3'

export default {
  name: 'Request',
  components: { MonacoEditor },
  extends: Collection,
  data() {
    return {
      title: 'Requests',
      endpoint: '/http-request/',
      methods: {},
      headerNames: [],
      result: null,
      collections: null,

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
      if (this.result['status']) {
        if (this.result['status'] >= 200) {
          cssClass = 'text-success'
        }
        if (this.result['status'] >= 300) {
          cssClass = 'text-info'
        }
        if (this.result['status'] >= 400) {
          cssClass = 'text-warning'
        }
        if (this.result['status'] >= 500) {
          cssClass = 'text-danger'
        }
      }
      return cssClass
    }
  },
  methods: {
    executeRequest() {
      this.loading(true)
      getApiCall('/http-request/' + this.pk + '/exec/')
          .then(data => this.result = data)
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
    getApiCall('/http-methods/').then(data => this.methods = data)
    getApiCall('/http-collection/').then(data => {
      this.collections = data.map(collection => {
        return {
          'text': collection['name'],
          'value': collection['id'],
        }
      })
    })
  }
}
</script>