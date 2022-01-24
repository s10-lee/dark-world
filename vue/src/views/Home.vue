<template>
  <div class="fixed-container">
    <div class="container">
      <div class="row mt-6 mb-3">
        <div class="col">
          <div class="mb-2">
            <b-input label="Label" v-model="inputValue" placeholder="Text..."/>
            <i>value: {{ inputValue }}</i>
          </div>
          <div>
            <b-check v-model="checkValue">Checkbox</b-check>
            <br/>
            <i>value: {{ checkValue }}</i>
          </div>
        </div>
        <div class="col">
          <b-text-area label="Label" v-model="textAreaValue"/>
          <i>value: {{ textAreaValue }}</i>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <b-select v-model="selectValue" :options="selectOptions"></b-select>
          <i>value: {{ selectValue }}</i>
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
      selectValue: null,
      selectOptions: [
        {value: 1, text: 'One'},
        {value: 2, text: 'Second'},
        {value: 3, text: '33333'}
      ]
    }
  }
}
</script>
