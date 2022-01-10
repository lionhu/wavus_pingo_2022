<script>
import { mapState } from 'vuex'

export default {
  components: {},
  props: {
    title: {
      type: String,
      default: ''
    },
    items: {
      type: Array,
      default: () => {
        return []
      }
    }
  },
  computed: mapState([ 'layout' ]),
}
</script>

<template>
  <div class="row">
    <div class="col-12">
      <div class="page-title-box"
        :class="{'page-title-box-alt': layout.layoutType !== 'vertical' && layout.layoutType !== 'two-column'}">
        <h4 class="page-title"> {{ title }} </h4>
        <div class="page-title-right">
          <b-breadcrumb :items="items" class="m-0"/>
        </div>
      </div>
    </div>
  </div>
</template>
