<template>
  <b-navbar/>
  <div class="fixed-container-scroll">
    <div class="container">
      <div class="row mt-6">
        <div class="col">
          <h3 class="fw-bold">Profile</h3>
          <div class="mt-3">
            {{ $store.state.user }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
}
</script>