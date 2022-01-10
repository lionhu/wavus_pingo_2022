<template>
  <div class="layout-8-bg">

    <div class="title1 section-t-space" v-if="!$device.isMobile">
      <!--      <h2>{{ subtitle }}</h2>-->
      <h3>PinGoは、世界中から選りすぐりの商品だけを、</h3>
      <h3 class="title-inner1">会員のみなさまにリーズナブルな価格でお届けいたします。</h3>
    </div>
    <div class="title1 section-t-space px-3 " v-else>
      <h4 class="title-inner1 line-height-2rem">PinGoは、世界中から選りすぐりの商品だけを、会員のみなさまにリーズナブルな価格でお届けいたします。</h4>
    </div>
    <section class="section-b-space p-t-1 ratio_asos">
      <div class="container">
        <div class="row">
          <div class="col">
            <div class="theme-tab">
              <b-tabs content-class="mt-3" ref="tabs" v-model="activeTabIndex"
                      @activate-tab="changeTab">
                <b-tab
                  :title="category.label"
                  v-for="category in categories"
                  :key="category.value"
                >
                  <div class="no-slider row">
                    <div class="product-box" v-for="(product,index) in products" :key="index">
                      <sigle_ProductBox
                        :product="product"
                        :index="index"
                        @ShowShareQR="ShowShareQR"
                        @showQuickview="showQuickview"
                      />
                    </div>
                  </div>
                </b-tab>
              </b-tabs>
            </div>
          </div>
        </div>
      </div>
    </section>


    <quickviewModel :openModal="show_quickview_model" @closeModal="closeQuickviewModel"/>
    <shareproductModel :openModal="show_shareproduct_modal"
                       @closeModal="closeShareQRModel"/>

  </div>
</template>
<style scoped>
.nav.nav-tabs li.nav-item {
  padding-right: 0 !important;
}

</style>
<script type="text/javascript">
import {mapGetters} from 'vuex'
import {APIServices} from "~/helpers/APIs";

export default {
  components: {
    sigle_ProductBox: () => import('./productbox'),
    quickviewModel: () => import('./quickview'),
    shareproductModel: () => import('./shareproduct'),
  },
  computed: {
    ...mapGetters({
      all_products: "system/getterAllProducts",
      // new_products: "system/getterNewProducts",
      // bestseller_products: "system/getterBestSellerProducts",
      currentProductData: "products/getCurrentDetailedProduct",
    })
  },
  async fetch() {
    this.new_products = await APIServices.get("store/public/filter_products/ofLabel/?query=NW")
      .then(APIServices.handleResponse)
      .then(response => {
        return response
      })
    this.bestseller_products = await APIServices.get("store/public/filter_products/ofLabel/?query=BS")
      .then(APIServices.handleResponse)
      .then(response => {
        return response
      })
  },
  data() {
    return {
      title: 'PinGoは、世界中から選りすぐりの商品だけを、会員のみなさまにリーズナブルな価格でお届けいたします。',
      subtitle: 'exclusive products',
      categories: [{label: this.$t("product.new"), value: 1},
        {label: this.$t("product.best_sales"), value: 2},
        // {label: "ALL", value: 3},
      ],
      products: [],
      activeTabIndex: 0,
      show_quickview_model: false,
      show_shareproduct_modal: false,
      new_products: [],
      bestseller_products: []
    }
  },
  watch: {
    new_products(newVal, oldVal) {
      if (this.activeTabIndex === 0) {
        this.products = this.new_products;
      }
    },
    bestseller_products(newVal, oldVal) {
      if (this.activeTabIndex === 1) {
        this.products = this.bestseller_products;
      }
    },
    all_products(newVal, oldVal) {
      if (this.activeTabIndex === 2) {
        this.products = this.all_products;
      }
    },
    activeTabIndex(newVal, oldVal) {
      if (newVal === 0) {
        this.products = this.new_products;
      } else if (newVal === 1) {
        this.products = this.bestseller_products;
      } else {
        this.products = this.all_products;
      }
    },
  },
  methods: {
    changeTab(e) {
      this.activeTabIndex = e;
    },
    ShowShareQR(product_id) {
      this.$store.commit("products/setCurrentDetailProductID", product_id)
      this.show_shareproduct_modal = true;
    },
    closeShareQRModel() {
      this.show_shareproduct_modal = false;
    },
    showQuickview(product_id) {
      this.$store.commit("products/setCurrentDetailProductID", product_id)
      this.show_quickview_model = true;
    },
    closeQuickviewModel() {
      this.show_quickview_model = false;
    },
  }
}
</script>
