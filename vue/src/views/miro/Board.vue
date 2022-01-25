<template>
  <div class="fixed-container">
    <div v-if="item && pk" class="mt-5">

      <div class="miro-board" @drop="onDrop" @dragenter.prevent @dragover.prevent>
        <div v-for="block in item.blocks"
             :key="block.uid"
             draggable="true"
             @dragstart="startDrag"
             @drag="onDrag($event, block)"
             :style="`left:${block.x}px;top:${block.y}px;`"
             :class="'miro-block ' + block.css">
          {{ block.name }}
        </div>
      </div>

      <div class="position-absolute shadow rounded" style="right:100px;top:100px;">
        <div class="row no-gutters">
          <div class="col">
            <b-btn variant="green" size="sm" disabled @click.prevent.stop="handleCreate">Create block</b-btn>
          </div>
        </div>
      </div>

    </div>

    <div class="container" v-else>
      <div class="row mt-5">
        <div class="col">
          <b-table endpoint="/m1r0" :columns="columns" :items="items"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {apiCrudMixin} from 'mixins'

export default {
  mixins: [apiCrudMixin],
  name: 'Board',
  data() {
    return {
      columns: [
        {field: 'uid', link: true, name: 'ID'},
        {field: 'name', name: 'Name'},
        {field: 'is_public', name: 'Public'},
      ],
      endpoint: '/miro/board',
      deltaX: 0,
      deltaY: 0,
      selected: null,
    }
  },
  methods: {
    handleCreate() {

    },
    startDrag(event) {
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