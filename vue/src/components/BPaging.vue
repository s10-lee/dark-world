<template>
  <nav v-if="total" class="pagination-nav">
    <ul class="pagination pagination-dark pt-3">
      <li :class="{'page-item': 1, 'disabled': parseInt(page) - 1 <= 0}">
        <router-link class="page-link" :to="getUrl(-1)">
          <span aria-hidden="true">&laquo;</span>
        </router-link>
      </li>

      <template v-for="p in displayPages">
        <li :class="{'page-item': true, 'active': parseInt(page) === p}">
          <router-link class="page-link" :to="getUrl(p - parseInt(page))">
            {{ p }}
          </router-link>
        </li>
      </template>

      <li :class="{'page-item': 1, 'disabled': parseInt(page) + 1 >= Math.ceil(total / perPage)}">
        <router-link class="page-link" :to="getUrl(1)">
          <span aria-hidden="true">&raquo;</span>
        </router-link>
      </li>
    </ul>
  </nav>
  <div style="min-height:4rem;">&nbsp;</div>
</template>

<script>
export default {
  name: "BPaging",
  props: {
    total: [String, Number],
    page: {
      type: [String, Number],
      default: 1
    },
    frame: {
      type:[String, Number],
      default: 5
    },
    perPage: {
      type: [String, Number],
      default: 20
    },
    url: String,
    fixed: {
      type: Boolean,
      validator(value) {
        return value !== undefined
      }
    },
  },
  data() {
    return {
      prevPage: false,
      nextPage: false,
    }
  },
  computed: {
    displayPages() {
      const page  = parseInt(this.page);
      const total = parseInt(this.total);
      const frame = parseInt(this.frame);
      const perPage = parseInt(this.perPage);

      const allPages = Math.ceil(total / perPage)
      let pages = []
      if (frame >= allPages) {
        for (let i = 1; i <= frame; i++) {
          pages.push(i)
        }
      } else {

        let delta = frame - Math.ceil(frame / 2)
        let start = page - delta
        if (start <= 0) {
          start = 1
        }

        for (let i = start; i < (start + frame); i++) {
          pages.push(i)
        }
      }
      return pages;
    },
  },
  methods: {
    getUrl(delta) {
      let page = this.page ? parseInt(this.page) : 1
      page += delta
      let s = document.location.search.toString()
      let url = document.location.pathname

      if (s.indexOf('page') > -1) {
        if (page > 1) {
          s = s.replace(/(\?|&)page=(\d+)/g, '$1page=' + page)
        } else {
          s = s.replace(/(\?|&)page=(\d+)/g, '')
        }
      } else if (page > 1) {
        if (s.indexOf('?') > -1) {
          s += `&page=${page}`
        } else {
          s += `?page=${page}`
        }
      }
      return url + s
    },
    bindChangePage(e) {
      if (e.shiftKey && e.ctrlKey) {
        if (e.key.toLowerCase() === 'arrowright') {
          let url = this.getUrl(1)
          return this.$router.push(url)
        } else if (e.key.toLowerCase() === 'arrowleft' && parseInt(this.page) > 1) {
          let url = this.getUrl(-1)
          return this.$router.push(url)
        }
      }
    },
  },
  mounted() {
    window.addEventListener('keydown', this.bindChangePage)
  },
  unmounted() {
    window.removeEventListener('keydown', this.bindChangePage)
  }
}
</script>