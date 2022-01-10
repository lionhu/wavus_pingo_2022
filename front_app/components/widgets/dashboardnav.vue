<template>
  <div>
    <b-list-group>
      <b-list-group-item :href="item.path"
                         v-bind:key="item.title"
                         v-bind:class="{'active':isActive(item.title)}"
                         v-for="item in menulist">{{ $t(`${item.title}`) }}</b-list-group-item>
    </b-list-group>
  </div>
</template>
<script>
import {mapState} from 'vuex'

export default {
  name:"dashboard_nav",
  props: ['active_title'],
  data() {
    return {
    }
  },
  computed: {
    ...mapState({
      menulist: state => state.menu.dashboardnav
    })
  },
  methods: {
    isActive: function (menuItem) {
      return menuItem === this.active_title
    },
  }
}
</script>
<style scoped="scoped">
.list-group-item.active {
  background-color: #ff4c3b !important;
  border-color: #ff4c3b !important;
}
</style>
