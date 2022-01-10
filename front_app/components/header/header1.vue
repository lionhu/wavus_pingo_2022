<template>
  <div>
    <header>
      <div class="mobile-fix-option"></div>
      <TopBar/>
      <div class="container">
        <div class="row">
          <div class="col-sm-12">
            <div class="main-menu">
              <div class="menu-left">
                <div class="navbar">
                  <a @click="left_sidebar">
                    <div class="bar-style">
                      <i class="fa fa-bars sidebar-bar" aria-hidden="true"></i>
                    </div>
                  </a>
                  <LeftSidebar :leftSidebarVal="leftSidebarVal" @closeVal="closeBarValFromChild"/>
                </div>
                <div class="brand-logo">
                  <nuxt-link :to="{ path: '/'}" >
                    <img :src='logoimage' class="img-fluid animate__animated animate__slideInDown" />
                  </nuxt-link>
                </div>
              </div>
              <div class="menu-right pull-right">
                <Nav/>
                <HeaderWidgets/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>
<script>
import {mapState,mapGetters} from 'vuex'
export default {
  name:"pingo_header",
  data() {
    return {
      leftSidebarVal: false,
      logoimage:"/images/logo/pingo_dark.svg"
    }
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
  components: {
    TopBar: () => import('../widgets/topbar'),
    LeftSidebar: () => import('../widgets/left-sidebar'),
    Nav: () => import('../widgets/navbar'),
    HeaderWidgets: () => import('../widgets/header-widgets')
  },
  methods: {
    left_sidebar() {
      this.leftSidebarVal = true
    },
    closeBarValFromChild(val) {
      this.leftSidebarVal = val
    }
  },
  computed: {
    ...mapGetters({
      layout:"layout/getterLayout"
    })
  },
  watch :{
    layout(newVal,oldVal){
      if (newVal==="dark"){
        this.logoimage="/images/logo/pingo_light.svg"
      }else {
        this.logoimage="/images/logo/pingo_dark.svg"

      }
    }
  }
}
</script>

<style>
.brand-logo img {
  max-height: 60px;
  width: 100%;
}
</style>
