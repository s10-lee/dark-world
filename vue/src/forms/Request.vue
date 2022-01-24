<template>
  <div>
      <form class="row g-3">
        <div class="col-md-2">
          <label class="form-label">Method</label>
          <select class="form-select">
            <option v-for="(name, key) in methods" :value="key" :selected="key === modelValue.method">
              {{ name }}
            </option>
          </select>
        </div>

        <div class="col-md-10">
          <b-input label="Url" placeholder="https://" v-model="modelValue.url" />
        </div>
        <div class="col-md-5">
          {{ modelValue.headers }}
          <br/>

          <div v-if="modelValue.params">
            <b-label>Params</b-label>
            <div v-for="(value, name) in modelValue.params" class="mb-3">
              <b-input-pair size="sm"
                            placeholder-first="Key"
                            placeholder-last="Value"/>

            </div>
          </div>
        </div>
        <div class="col-md-2">
        </div>
        <div class="col-md-5">
          <b-label>Headers</b-label>
          <div v-if="modelValue.headers">
            <div v-for="(value, name, index) in modelValue.headers" class="mb-3">

              <b-input-pair size="sm"
                            :value-first="name"
                            :value-second="value"
                            placeholder-first="Key"
                            placeholder-last="Value"/>
              <small class="text-muted">
                {{ value }} = {{ name }} = {{ index }}
              </small>

            </div>
          </div>
          <div>
            <b-input-pair size="sm"
                          placeholder-first="Key"
                          placeholder-last="Value"/>
          </div>

        </div>
        <div class="col-12">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="gridCheck">
            <label class="form-check-label" for="gridCheck">
              Check me out
            </label>
          </div>
        </div>
        <div class="col-12">
          <b-btn variant="green">Save Changes</b-btn>
        </div>
      </form>
  </div>
</template>

<script>
import BInputPair from 'blocks/BInputPair';
export default {
  props: {
    modelValue: {
      type: Object,
      default: {
        url: null,
        method: 'GET',
        headers: {},
        params: {},
        data: {}
      },
      required: true
    },
  },
  components: {
    BInputPair
  },
  data() {
    return {
      methods: {
        'GET': 'GET',
        'POST': 'POST',
        'PUT': 'PUT',
        'PATCH': 'PATCH',
        'DELETE': 'DELETE',
      }
    }
  }

}
</script>