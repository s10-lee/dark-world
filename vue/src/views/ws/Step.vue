<template>
  <div class="container">
      <!--
      <form class="row g-3">
        <div class="col-md-2">
          <label class="form-label">Method</label>

          <select class="form-select">
            <option v-for="(name, key) in methods" :key="key" :value="key" :selected="key === modelValue.method">
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
      -->
    <b-row>
      <b-col>

      </b-col>
    </b-row>
  </div>
</template>

<script>
import { HTTP_METHODS } from "services/const";
import { apiCrudMixin } from "mixins";

export default {
  mixins: [ apiCrudMixin ],
  data() {
    return {
      endpoint: '/ws/step',
      fields: {
        url: null,
        method: 'GET',
        headers: '',
        params: {},
        data: {},
      },
      methods: HTTP_METHODS,
    }
  }
}
</script>