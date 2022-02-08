<template>
  <div class="container">
    <b-row class="my-3 pb-3">
      <b-col>
        <h3>Chain</h3>
      </b-col>
      <b-col cols="auto">
        <transition name="fade" mode="out-in" v-if="loaded">
          <b-btn v-if="item" @click="closeForm">Close</b-btn>
          <b-btn v-else @click="createEmptyItem">Add item</b-btn>
        </transition>
      </b-col>
    </b-row>

    <b-row>

      <transition name="fade" mode="out-in" v-if="loaded" appear>
        <b-col v-if="item" key="form">

          <b-row class="mb-5">
            <b-col cols="6">
              <form @submit.stop.prevent="handleSave">
                <b-row>
                  <b-col>
                    <b-input placeholder="Name" v-model="item.name"/>
                  </b-col>
                  <b-col cols="auto">
                    <b-btn type="submit" :disabled="!loaded">Save</b-btn>
                  </b-col>
                  <b-col cols="auto">
                    <b-btn variant="out-danger" @click="handleDelete" :disabled="!loaded">Remove</b-btn>
                  </b-col>
                </b-row>
              </form>
            </b-col>
          </b-row>

          <b-row>
            <b-col cols="auto">
              <h3>Steps</h3>
            </b-col>
            <b-col>
              <b-btn size="sm">Create</b-btn>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div v-for="s in item.steps" :key="s.uid" class="mb-3 py-3 border-bottom">
                {{ s.name }}
              </div>
            </b-col>
          </b-row>
        </b-col>

        <b-col v-else key="list">
          <b-table :fields="listFields"
                   :items="items"
                   :href="routePath"
                   head-class="table-dark"
                   borderless
                   hover/>
        </b-col>
      </transition>
    </b-row>
  </div>
</template>

<script>
import { apiCrudMixin } from 'mixins'

const BASE_URL = '/ws/chain'

export default {
  mixins: [ apiCrudMixin ],
  data() {
    return {
      endpoint: BASE_URL,
      routePath: BASE_URL,
      fields: {
        name: ''
      },
      listFields: [
        {field: 'uid', name: 'ID', link: true},
        {field: 'name', name: 'Name', link: true},
      ]
    }
  },
  methods: {
    closeForm() {
      return this.pk ? this.$router.push(this.routePath) : this.item = null
    },
    handleSave() {
      this.saveItem(this.makePayload(), this.pk).then(() => this.listItems())
    },
    handleDelete() {
      if (this.pk) {
        if (window.confirm('Delete ?')) {
          this.destroyItem(this.pk).then(() => this.closeForm())
        }
      }
    }
  }
}
</script>