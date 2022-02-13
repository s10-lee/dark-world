<template>
  <b-wrapper container>
    <b-row align-h="center">
      <b-col cols="auto">
        <form @submit.prevent.stop="handleLogin">
          <div class="mb-4">
            <b-input size="lg" v-model="username" label="LOGIN / @EMAIL" />
          </div>
          <div class="mb-5">
            <b-input size="lg" v-model="password" label="PASSWORD" type="password" />
          </div>
          <div>
            <b-btn type="submit" size="lg">Login</b-btn>
          </div>
        </form>
      </b-col>
    </b-row>
  </b-wrapper>
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
        this.$router.push({path: '/n00b/upload'})
      })
    }
  }

}
</script>