<template>
  <div class="fixed-container">

    <div class="miro-board" @drop="onDrop" @dragenter.prevent @dragover.prevent>

      <div v-for="item in items"
           :key="item.id"
           draggable="true"
           @dragstart="startDrag($event, item)"
           @drag="onDrag($event, item)"
           class="miro-block"
           :style="`left:${item.x}px;top:${item.y}px;`"
      >
        {{ item.text }}
      </div>

    </div>


    <div class="position-absolute shadow rounded" style="right:100px;top:100px;">
      <div class="row no-gutters">
        <div class="col">
          <b-btn variant="green" size="sm" @click.prevent.stop="handleCreate">Create block</b-btn>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Miro',
  data() {
    return {
      deltaX: 0,
      deltaY: 0,
      selected: null,
      items: [
        {id: 'fb7256141d6a4d2a852abcee0319ef94', text: 'First Block', x: 10, y: 50}
      ]
    }
  },
  methods: {
    handleCreate() {

    },
    startDrag(event, item) {

      const {x, y} = event.target.getBoundingClientRect()

      this.deltaX = Math.round(event.x - x)
      this.deltaY = Math.round(event.y - y)

      event.dataTransfer.dropEffect = 'move'
      event.dataTransfer.effectAllowed = 'move'
      // event.dataTransfer.setData('itemId', item.id)
    },
    onDrag(event, item) {
      item.x = event.x - this.deltaX
      item.y = event.y - this.deltaY
    },
    onDrop() {
      this.deltaX = 0
      this.deltaY = 0
    }
  }
}
</script>