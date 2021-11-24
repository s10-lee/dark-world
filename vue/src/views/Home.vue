<template>
  <div class="fixed-container">
    <div class="container">
      <div class="row mt-6 mb-3">
        <div class="col">
          <div class="mb-2">
            <b-input label="Label" v-model="inputValue" placeholder="Text..."/>
            value: {{ inputValue }}
          </div>
          <div>
            <b-check v-model="checkValue">Custom checkbox</b-check>
            <br/>
            value: {{ checkValue }}
          </div>
        </div>
        <div class="col">
          <b-text-area label="Label" v-model="textAreaValue"/>
          value: {{ textAreaValue }}
        </div>
      </div>
      <div class="row">
        <div class="col">
        </div>
        <div class="col">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      inputValue: null,
      textAreaValue: null,
      checkValue: null,
    }
  }
}
</script>
