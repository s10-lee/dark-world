<template>
  <div>
    <h4 class="border-bottom pb-3 mb-3">
      <span v-if="item" class="text-muted">
          <b-link to="/ws/request/">Requests</b-link> &nbsp;
          <small>{{ item.uid }}</small>
      </span>
      <span v-else>Requests</span>
    </h4>

    <div v-if="errors.length">
      {{ errors[0].message }}
      <hr/>
      {{ errors[0].response.status }} - {{ errors[0].response.data }}
    </div>

    <transition name="fade" mode="out-in">
      <div v-if="item">
        <request-form v-model="item" />
      </div>
      <div v-else>
        <div class="row" v-for="item in items" :key="item.uid">
          <div class="col">
            <b-link :to="`/ws/request/${item.uid}/`">{{ item.uid }}</b-link>
          </div>
          <div class="col">{{ item.name }}</div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script>
import { apiCrudMixin } from 'mixins'
import RequestForm from './RequestForm'
export default {
  mixins: [ apiCrudMixin ],
  components: { RequestForm },
  data() {
    return {
      endpoint: '/ws/request/'
    }
  },
}
</script>