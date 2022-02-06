<template>
  <div class="container">
    <b-row>
      <b-col>
        <h3 class="fw-bold">Profile</h3>
        <div class="mt-3">
          {{ $store.state.user }}
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'Profile',
}
</script>