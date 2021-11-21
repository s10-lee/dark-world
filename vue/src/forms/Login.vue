<template>
  <div class="container">
    <div class="row mt-6 justify-content-center">
      <div class="col-4">
        <div class="p-5 border bg-white rounded">
          <h1 class="text-100 text-center mb-5">Login</h1>
          <div class="mb-4">
            <b-input label="Username" v-model="username"/>
          </div>
          <div class="mb-5">
            <b-input label="Password" type="password" v-model="password"/>
          </div>
          <div class="mb-3">
            <b-btn block variant="green" @click.prevent.stop="handleLogin">Login</b-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: null,
      password: null
    }
  },
  methods: {
    handleLogin() {
      this.$store.dispatch('obtainToken', {username: this.username, password: this.password}).then(() => {
        this.$router.push({path: '/n00b'})
      })
    }
  }
}
</script>