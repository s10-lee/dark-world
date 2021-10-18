<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h3>Request</h3>
        <request-form></request-form>
      </div>
    </div>
  </div>
</template>

<script>
import RequestForm from 'forms/Request';
export default {
  name: 'Request',
  components: {
    RequestForm
  }
}
</script>