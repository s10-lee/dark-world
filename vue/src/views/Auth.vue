<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col" style="max-width: 18rem;">
        <form @submit.prevent.stop="handleLogin">
          <div class="mb-6 text-center">
            <img src="~assets/error.png"
                 alt="Image Not Found"
                 style="opacity:0.1;max-width:100%;height:auto;"/>
          </div>
          <div class="mb-5">
            <b-input size="lg" v-model="username" label="Login / @email" />
          </div>
          <div class="mb-7">
            <b-input size="lg" v-model="password" label="Password" type="password" />
          </div>
          <div>
            <b-btn block
                   type="submit"
                   variant="secondary"
                   size="lg">
              <b>Sign In</b>
            </b-btn>
          </div>
        </form>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: 'Auth',
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