<template>
  <div>
    <TopLinks/>
    <section class="section-b-space ratio_asos">
      <div class="collection-wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <sidebar/>
            </div>
            <div class="collection-content col">
              <div class="page-main-content">
                <div class="row">
                  <div class="col-sm-12">
                    <div class="top-banner-wrapper">
                      <img
                        src='/images/banners/sharebuy.jpg'
                        class="img-fluid"
                      />


                      <div class="top-banner-content small-section "
                           v-bind:class='{"px-3":$device.isMobile,"px-5":!$device.isMobile}'>

                        <!--                        <h3 class="theme-color font-weight-bold text-center">{{ $t("services.share_sales.title") }}</h3>-->
                        <p style="line-height: 1.5rem!important;">
                          {{ $t("services.share_sales.title") }}は、PinGoで見つけたお気に入りの商品をSNSへ投稿するだけで、
                          あなたの紹介からその商品を購入した人のポイントがあなたにも戻ってくる仕組みです。
                          <span class="theme-color font-weight-bold">お気に入りをシェアして、どんどんポイントをゲットしましょう！
                        </span></p>
                      </div>
                    </div>
                    <div class="collection-product-wrapper">
                      <div class="product-top-filter">
                        <div class="row">
                          <div class="col-12">
                            <div class="product-filter-content">
                              <div class="search-count">
                                <h5 v-if="productslistMeta.total"> {{ productslistMeta.total }}
                                  点の商品が販売中!</h5>
                              </div>
                              <div class="collection-view">
                                <ul>
                                  <li @click="gridView()">
                                    <i class="fa fa-th grid-layout-view"></i>
                                  </li>
                                  <li @click="listView()">
                                    <i class="fa fa-list-ul list-layout-view"></i>
                                  </li>
                                </ul>
                              </div>
                              <div class="collection-grid-view">
                                <ul>
                                  <li>
                                    <img
                                      src='/images/icon/2.png'
                                      @click="grid2()"
                                      class="product-2-layout-view"
                                    />
                                  </li>
                                  <li>
                                    <img
                                      src='/images/icon/3.png'
                                      @click="grid3()"
                                      class="product-3-layout-view"
                                    />
                                  </li>
                                  <li>
                                    <img
                                      src='/images/icon/4.png'
                                      @click="grid4()"
                                      class="product-4-layout-view"
                                    />
                                  </li>
                                  <li>
                                    <img
                                      src='/images/icon/6.png'
                                      @click="grid6()"
                                      class="product-6-layout-view"
                                    />
                                  </li>
                                </ul>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="row my-2" v-if="productslistMeta.total">
                        <div class="col">
                          <div class="dataTables_paginate paging_simple_numbers float-right">
                            <ul class="pagination pagination-rounded">
                              <b-pagination v-model="page"
                                            pills
                                            aria-controls="pingoproduct_table"
                                            :total-rows="productslistMeta.total"
                                            :per-page="page_size"
                                            @change="tablePageChange"
                              >
                              </b-pagination>
                            </ul>
                          </div>
                        </div>
                      </div>
                      <div class="product-wrapper-grid" :class="{'list-view':listview == true}">
                        <div class="row">
                          <div class="col-sm-12">
                            <div class="text-center section-t-space section-b-space"
                                 v-if="productslistMeta.total === 0">
                              <img v-lazy='"/images/empty-search.jpg"' class="img-fluid" alt/>
                              <h3 class="mt-3">Sorry! Couldn't find the product you were looking For!!!</h3>
                              <div class="col-12 mt-3">
                                <nuxt-link :to="{ path: '/'}" class="btn btn-solid">continue shopping</nuxt-link>
                              </div>
                            </div>
                          </div>
                          <div
                            class="col-grid-box"
                            :class="{'col-lg-3 col-md-4 col-sm-6':col4 == true, 'col-lg-4 col-sm-6':col3 == true, 'col-sm-6':col2 == true, 'col-lg-2 col-md-4 col-sm-6':col6 == true, 'col-lg-12':listview == true}"
                            v-for="(product,index) in productslist"
                            :key="index"
                          >
                            <div class="product-box">
                              <productBox
                                @showQuickview="showQuickview"
                                @ShowShareQR="ShowShareQR"
                                :product="product"
                                :index="index"
                                :isListview="listview"
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="row my-2" v-if="productslistMeta.total">
                        <div class="col">
                          <div class="dataTables_paginate paging_simple_numbers float-right">
                            <ul class="pagination pagination-rounded">
                              <b-pagination v-model="page"
                                            pills
                                            aria-controls="pingoproduct_table"
                                            :total-rows="productslistMeta.total"
                                            :per-page="page_size"
                                            @change="tablePageChange"
                              >
                              </b-pagination>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <quickviewModel :openModal="showquickviewmodel" @closeModal="closeQuickviewModel"/>
    <shareproductModel :openModal="shareproductModal"
                       @closeModal="closeShareQRModel"/>
  </div>
</template>
<script>
import {mapGetters, mapState} from 'vuex'

export default {
  name: "shop_top",
  layout:"sharebuy",
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    productBox: () => import('./components/productbox'),
    sidebar: () => import('./components/sidebar'),
    quickviewModel: () => import('./components/quickview'),
    shareproductModel: () => import('./components/shareproduct'),
    TopLinks: () => import('~/components/widgets/TopLinks'),
  },
  data() {
    return {
      bannerimagepath: '/images/side-banner.png',
      col2: false,
      col3: true,
      col4: false,
      col6: false,
      listview: false,
      page_size: 12,
      page: 1,
      showquickviewmodel: false,
      shareproductModal: false
    }
  },
  computed: {
    ...mapGetters({
      productslist: "products/getterCategoryProducts",
      productslistMeta: "products/getterCurrentCategoryProductsMeta",
      isLoggedIn: "authfack/loggedIn",
      currentCategory: "products/getterCurrentCategory",
      CurrentSubategory: "products/getterCurrentSubategory",
    }),
    filter_options() {
      return `store/public/filter_products/${this.CurrentSubategory.id}/ofCategory/`
    }
  },
  watch: {
    CurrentSubategory(newVal, oldVal) {
      this.load_products()
    }
  },
  mounted() {
    this.load_products()
  },
  methods: {
    async load_products() {
      console.log(this.filter_options)
      this.$store.dispatch("products/load_category_products", this.filter_options)
    },
    tablePageChange(page) {
      this.page = page;
      this.load_products()
    },
    onChangeSort(event) {
      this.$store.dispatch('filter/sortProducts', event.target.value)
    },
    gridView() {
      this.col4 = true
      this.col2 = false
      this.col3 = false
      this.col6 = false
      this.listview = false
    },
    listView() {
      this.listview = true
      this.col4 = false
      this.col2 = false
      this.col3 = false
      this.col6 = false
    },
    grid2() {
      this.col2 = true
      this.col3 = false
      this.col4 = false
      this.col6 = false
      this.listview = false
    },
    grid3() {
      this.col3 = true
      this.col2 = false
      this.col4 = false
      this.col6 = false
      this.listview = false
    },
    grid4() {
      this.col4 = true
      this.col2 = false
      this.col3 = false
      this.col6 = false
      this.listview = false
    },
    grid6() {
      this.col6 = true
      this.col2 = false
      this.col3 = false
      this.col4 = false
      this.listview = false
    },
    ShowShareQR(product_id) {
      this.$store.commit("products/setCurrentDetailProductID", product_id)
      this.shareproductModal = true;

    },
    closeShareQRModel() {
      this.shareproductModal = false;
    },
    showQuickview(product_id) {
      this.$store.commit("products/setCurrentDetailProductID", product_id)
      this.showquickviewmodel = true;

    },

    closeQuickviewModel() {
      this.showquickviewmodel = false;
    },

  }
}
</script>
