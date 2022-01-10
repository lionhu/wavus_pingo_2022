<template>
  <div>
    <Header/>
    <Breadcrumbs title="全ての商品" breadcrumb_type="static"/>
    <div class="container-fluid layout-8" style="padding:0;">

      <section class="section-b-space p-t-0 ratio_asos mt-3">
        <div class="container">
          <div class="row">
            <div class="col">
              <div class="theme-tab">
                <div class="no-slider row">
                  <div class="product-box" v-for="(product,index) in products" :key="index">
                    <sigle_ProductBox :product="product" :index="index"/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
    <Footer/>
  </div>
</template>
<script>

import {mapGetters} from 'vuex'


export default {
  name: "shop_index",
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('@/components/widgets/breadcrumbs'),
    sigle_ProductBox: () => import('./components/productbox'),
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
    ...mapGetters({
      products: "system/getterAllProducts",
      back_server: 'system/getterBackServer',
      currentCategory: "products/getCurrentCategory",
      currentSubcategory: "products/getCurrentSubategory",
    }),
  },
}
</script>
