<template>
  <div class="fixed-container-scroll">

    <div class="moon">
      <kinesis-container event="scroll">
        <header>
            <img class="logo" src="../assets/img/moon.png"/>
          <kinesis-element :strength="30" axis="y" originY="0">
            <h1>MOON IN ME</h1>
          </kinesis-element>
        </header>
      </kinesis-container>


      <section class="justify-content-center text-gold p-5 w-100">
        <div class="w-25 text-center">
          Behold the magic meaning of the cards! These are my tarot readings for you!
        </div>
      </section>

      <section class="photo-01 vh-80"></section>

      <div class="branch-right"></div>

      <section class="dark"></section>

      <kinesis-container event="scroll" style="position: absolute; top: 75%; left:0; height: 100%;">
        <kinesis-element :strength="300"
                         axis="y"
                         originY="80"
                         transformOrigin="50% 300%">
          <div class="branch-left"></div>
        </kinesis-element>
      </kinesis-container>
    </div>

  </div>
</template>

<script>
// import { KinesisContainer, KinesisElement} from 'vue-kinesis'
export default {
  name: 'Landing'
}
</script>

<style lang="scss">
  @import "src/scss/moon";
</style>
