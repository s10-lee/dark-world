<template>
  <div class="fixed-container-scroll">

    <div class="moon">

      <header>
        <img class="logo" src="../assets/img/moon.png"/>
        <h1>MOON IN ME</h1>
      </header>


      <section class="title-gold">
        Your future <br/>
        has always been written <br/>
        in the stars
      </section>

      <section class="photo-01 vh-80"></section>

      <section class="title-gold mb-7">
        Behold the magic <br/>
        meaning of the cards! <br/>
<!--        <br/>-->
<!--        These are my tarot <br/>-->
<!--        readings for you!-->
      </section>

      <kinesis-container event="scroll" style="position: absolute; top: 100%; right:0; height: 100%;">
        <kinesis-element :strength="100"
                         axis="y"
                         originY="-120">
          <div class="branch-right"></div>
        </kinesis-element>
      </kinesis-container>



      <section class="dark">
        <!--
        <div style="width:100%;max-width:920px;">
        <div class="row h-100">
          <div class="col">
            <div class="price-box">
              <h3>Audio Reading</h3>
              <p>
                At welementum a ac mi quis penatibus tellus donec amet mattis vel ultrices scelerisque sit iaculis gravida
                imperdiet semper feugiat morbi velit laoreet faucibus.
              </p>
            </div>
          </div>
          <div class="col">
            <div class="price-box">
              <h3>Video Reading</h3>
              <p>
                Quis metus adipiscing tincidunt diam orci ipsum, urna volutpat sagittis tristique maecenas vestibulum eget
                ornare maecenas eget tellus dignissim velit lorem tellus sit gravida sed pulvinar neque, ultrices.
              </p>
            </div>
          </div>
          <div class="col">
            <div class="price-box">
              <h3>Three Third</h3>
              <p>
                Tristique massa nunc, cursus semper tincidunt et et sed accumsan, in habitasse integer diam arcu rhoncus
                ullamcorper quisque viverra morbi.
              </p>
            </div>
          </div>
        </div>
        </div>
        -->
      </section>

      <kinesis-container event="scroll" style="position: absolute; top: 100%; left:0; height: 100%;">
        <kinesis-element :strength="300"
                         axis="y"
                         originY="0"
                         transformOrigin="50% 300%">
          <div class="branch-left"></div>
        </kinesis-element>
      </kinesis-container>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Landing'
}
</script>

<style lang="scss">
  @import "src/scss/moon";
</style>
