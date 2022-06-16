<template>
  <b-wrapper scroll container>
    <b-row>
      <b-col>
        <h3>{{ title }}</h3>
      </b-col>
    </b-row>

    <b-row v-if="item">
      <b-col>
        <form @submit.prevent.stop="saveFormItem">
          <b-row align-h="start" align-v="end">
            <b-col cols="4">
              <b-input size="lg" label="Name" v-model="item['name']"/>
            </b-col>
            <b-col cols="1">
              <b-input size="lg" label="Position" v-model="item['position']" type="number"/>
            </b-col>
            <b-col>
              <b-btn size="lg" type="submit">Save</b-btn>
            </b-col>
            <b-col>
              <b-btn v-if="'add' === pk" size="lg" variant="out-secondary" @click.prevent.stop="$router.push(routePath)">
                Cancel
              </b-btn>
              <b-btn v-else size="lg" variant="out-danger"  @click.prevent.stop="destroyItem(pk)">
                Delete
              </b-btn>
            </b-col>
          </b-row>

        </form>
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
import { apiCrudMixin } from 'mixins'
export default {
  name: 'Collection',
  mixins: [ apiCrudMixin ],
  data() {
    return {
      title: 'Collections',
      endpoint: '/http-collection/',
      fields: [
        {field: 'id', name: 'ID', type: String},
        {field: 'name', name: 'Name', link: true, type: String},
        {field: 'position', name: 'Pos', type: Number},
      ]
    }
  }
}
</script>