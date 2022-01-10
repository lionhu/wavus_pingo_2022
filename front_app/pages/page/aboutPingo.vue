<template>
  <div>
    <Header/>
    <TopLinks/>
    <Collections/>
    <Howitworks/>
    <Footer/>
  </div>
</template>
<script>
import {mapState, mapGetters} from 'vuex'

export default {
  name: "shop_top",
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    TopLinks: () => import('~/components/widgets/TopLinks'),
    // Slider: () => import("./components/slider"),
    // Banner: () => import("./components/banner"),
    // newsletterPopup: () => import('./shop/components/newsletter-popup'),
    Howitworks: () => import("./components/howitworks"),
    Collections: () => import("./components/collection_banner")
  },
  head() {
    return {
      link: [{
        rel: "stylesheet",
        href: "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
        // https://animate.style/
      }]
    }
  },
  data() {
    return {}
  },
  computed: {
    ...mapState({
      isLoggedIn: state => state.auth.loggedIn,
    }),
    ...mapGetters({
      back_server: 'system/getterBackServer',
    })
  },
  mounted() {
    this.load_store_system_info();
  },
  methods: {
    load_store_system_info() {
      this.$store.dispatch("system/init_shop");
    },
  }
}
</script>
