<template>
    <table :class="cssClasses">
      <thead :class="headClass">
      <tr>
        <th scope="col" v-for="f in fields" :key="f.field">
          {{ f.name || f.field }}
        </th>
      </tr>
      </thead>
      <tbody :class="bodyClass">
        <tr v-for="item in getItems" :key="item.uid">
          <td v-for="f in fields" :key="`${f.field}-${item.uid}`">
            <template v-if="f.link">
              <b-link :to="href + '/' + item[pkName]">{{ item[f.field] }}</b-link>
            </template>
            <template v-else>
              {{ item[f.field] }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
</template>

<script>
export default {
  name: 'BTable',
  props: {
    items: Array,
    fields: Array,
    href: String,
    pkName: {
      type: String,
      default: 'uid',
    },
    headClass: [Array, String],
    bodyClass: [Array, String],
    borderless: Boolean,
    bordered: Boolean,
    outlined: Boolean,
    striped: Boolean,
    hover: Boolean,
  },
  computed: {
    getItems() {
      return this.items
    },
    cssClasses() {
      let cls = ['table']

      if (this.borderless) {
        cls.push('table-borderless')
      }
      if (this.bordered) {
        cls.push('table-bordered')
      }
      if (this.outlined) {
        cls.push('border')
      }
      if (this.striped) {
        cls.push('table-striped')
      }
      if (this.hover) {
        cls.push('table-hover')
      }

      return cls
    },
  },
  created() {

  }
}
</script>