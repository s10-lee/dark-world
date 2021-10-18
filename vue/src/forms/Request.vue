<template>
  <div>
      <form class="row g-3">
        <div class="col-md-2">
          <label class="form-label">Method</label>
          <select class="form-select">
            <option selected>GET</option>
            <option>POST</option>
            <option>PUT</option>
            <option>PATCH</option>
            <option>DELETE</option>
          </select>
        </div>

        <div class="col-md-10">
          <b-input label="Url" placeholder="https://"/>
        </div>
        <div class="col-md-6">
          <b-label>Params</b-label>
          <div v-for="(value, name) in params">
            <b-input-pair :placeholders="['Key', 'Value']"
                          placeholder-first="Key"
                          placeholder-last="Value"/>

          </div>
        </div>
        <div class="col-md-6">
          <b-text-area rows="10" label="Headers"/>
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
import BInputPair from "blocks/BInputPair";
export default {
  components: {
    BInputPair
  },
  data() {
    return {
      url: null,
      params: {},
      headers: {},
    }
  }

}
</script>