<template>
  <div>
    <Header/>
    <nuxt id="body-content"/>
    <Footer/>

    <layoutSetting/>

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
  name: "default_layout",
  head() {
    return {
      title: 'PinGo Mall'
    }
  },
  components: {
    layoutSetting,
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
  },
  mounted() {
    this.$nextTick(() => {
      this.$nuxt.$loading.start()
      setTimeout(() => this.$nuxt.$loading.finish(), 1000)
    })
  }
}
</script>
