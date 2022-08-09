<template>
  <div>

  <nav class="nav nav-pills">
    <button class="nav-link active" type="button">Home</button>
    <button class="nav-link" type="button">Profile</button>
    <button class="nav-link" type="button">Contact</button>
    <button class="nav-link" type="button" disabled>Disabled</button>
  </nav>

  <div class="tab-content">
    <div class="tab-pane fade show active" tabindex="0">
      <p>This is some placeholder content the <strong>Home tab's</strong> associated content. Clicking another tab will toggle the visibility of this one for the next. The tab JavaScript swaps classes to control the content visibility and styling. You can use it with tabs, pills, and any other <code>.nav</code>-powered navigation.</p>
    </div>
    <div class="tab-pane fade" tabindex="0">
      <p>To help fit your needs, this works with <code>&lt;ul&gt;</code>-based markup, as shown above, or with any arbitrary “roll your own” markup. Note that if you’re using <code>&lt;nav&gt;</code>, you shouldn’t add <code>role="tablist"</code> directly to it, as this would override the element’s native role as a navigation landmark. Instead, switch to an alternative element (in the example below, a simple <code>&lt;div&gt;</code>) and wrap the <code>&lt;nav&gt;</code> around it.</p>
    </div>
    <div class="tab-pane fade" tabindex="0">
      Selects the given tab and shows its associated pane. Any other tab that was previously selected becomes unselected and its associated pane is hidden. Returns to the caller before the tab pane has actually been shown (i.e. before the shown.bs.tab event occurs).
    </div>
    <div class="tab-pane fade" tabindex="0">
      <p>Use the tab JavaScript plugin—include it individually or through the compiled <code>bootstrap.js</code> file—to extend our navigational tabs and pills to create tabbable panes of local content.</p>
    </div>
  </div>


  </div>


</template>

<script>
export default {
  name: 'BTabs',
  data() {
    return {

    }
  }
}
</script>
