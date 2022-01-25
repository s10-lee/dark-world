<template>
  <div>
    <table class="table">
      <thead>
      <tr>
        <th scope="col" v-for="col in columns" :key="col.field">
          {{ col.name || col.field }}
        </th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="item in getItems" :key="item.uid">
          <td v-for="col in columns" :key="`${col.field}-${item.uid}`">
            <template v-if="col.link">
              <b-link :to="endpoint + '/' + item[pkName]">{{ item[col.field] }}</b-link>
            </template>
            <template v-else>
              {{ item[col.field] }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'BTable',
  props: {
    items: Array,
    columns: Array,
    endpoint: String,
    pkName: {
      type: String,
      default: 'uid',
    }
  },
  computed: {
    getItems() {
      return this.items
    }
  }
}
</script>