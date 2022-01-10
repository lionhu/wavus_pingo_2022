<template>
  <div>
    <nuxt id="body-content"/>
    <layoutSetting/>
    <div class="tap-top top-cls" v-scroll-to="'#body-content'">
      <div>
          <i class="fa fa-angle-double-up"></i>
      </div>
    </div>
  </div>
</template>
<!--<script src="https://cdn.jsdelivr.net/npm/vue-scrollto"></script>-->

<script>
import layoutSetting from '../components/widgets/layout-setting'
export default {
  head() {
    return {
      title: 'PinGo Mall'
    }
  },
  components: {
    layoutSetting
  },
  mounted() {
    this.$nextTick(() => {
      this.$nuxt.$loading.start()
      setTimeout(() => this.$nuxt.$loading.finish(), 1000)
    })
  }
}
</script>
