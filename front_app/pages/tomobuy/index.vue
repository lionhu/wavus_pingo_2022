<template>
  <div>
    <Header/>
    <TopLinks/>
    <section class="section-b-space ratio_asos">
      <div class="collection-wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <sidebar @allFilters="allfilter" @SelectCategory="getCategoryFilteredPingoProducts"/>
            </div>
            <div class="collection-content col">
              <div class="page-main-content">
                <div class="row">
                  <div class="col-sm-12">
                    <div class="top-banner-wrapper">
                      <!--                      <a href="javascript:void(0);">-->
                      <img :src='require("@/assets/images/banners/tomo_buy.jpg")' class="img-fluid"/>
                      <!--                      </a>-->
                      <div class="top-banner-content small-section "
                           v-bind:class='{"px-3":$device.isMobile,"px-5":!$device.isMobile}'>
                        <!--                        <h3 class="theme-color font-weight-bold text-center">{{ $t("services.tomo_sales.title") }}</h3>-->
                        <!--                        <h5 class="theme-color text-center">（{{ $t("services.tomo_sales.alias") }}）</h5>-->
                        <p style="line-height: 1.5rem!important;">
                          {{
                            $t("services.tomo_sales.title")
                          }}は、友達や仲間たちが集まって、みんなで同じ商品を買うことで、安価に購入できる仕組みです。例えば、「ある商品」を「一定の期間」に「設定された人数(最小購入数以上)」で買うと、通常の価格より、とても安く買える。それが{{
                            $t("services.tomo_sales.title")
                          }}(共同購入)です。
                          みなさんが「いいなぁ」と思った商品の情報をSNSで拡散して、友達や仲間たちと一緒に商品を購入することで、
                          {{ $t("pingo.mall") }}の商品をお得に手に入れることができる、楽しいお買い物方法です。<span
                          class="theme-color font-weight-bold">「トモダチや仲間と一緒に買うから{{
                            $t("services.tomo_sales.title")
                          }}と覚えてください。」</span>
                        </p>
                      </div>
                    </div>
                    <div class="collection-product-wrapper">
                      <div class="product-top-filter">
                        <div class="row">
                          <div class="col-12">
                            <div class="product-filter-content">
                              <div class="search-count">
                                <h5> {{ ProductListMeta.total }} avaliable!</h5>
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
                      <div class="row my-2" v-if="ProductListMeta.total">
                        <div class="col">
                          <div class="dataTables_paginate paging_simple_numbers float-right">
                            <ul class="pagination pagination-rounded">
                              <b-pagination v-model="page"
                                            pills
                                            aria-controls="pingoproduct_table"
                                            :total-rows="ProductListMeta.total"
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
                          <div class="col-sm-12" v-if="ProductListMeta.total == 0">
                            <div class="text-center section-t-space section-b-space">
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
                            v-for="(product,index) in PingoProductList"
                            :key="index">
                            <productBox
                              @opencartmodel="showCart"
                              @showCompareModal="showCompare"
                              @openquickview="showQuickview"
                              @ShowShareQR="ShowShareQR"
                              @showalert="alert"
                              @alertseconds="alert"
                              :product="product"
                              :index="index"
                              :isListview="listview"
                            />
                          </div>
                        </div>
                      </div>
                      <div class="row my-2" v-if="ProductListMeta.total">
                        <div class="col">
                          <div class="dataTables_paginate paging_simple_numbers float-right">
                            <ul class="pagination pagination-rounded">
                              <b-pagination v-model="page"
                                            pills
                                            aria-controls="pingoproduct_table"
                                            :total-rows="ProductListMeta.total"
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
    <shareproductModel :openModal="shareproductModal" @closeModal="shareproductModal=false"/>
    <Footer/>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'

export default {
  name: "pingo_top",
  middleware: ["isGrouponServiceValid"],
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    productBox: () => import('./components/product-box'),
    sidebar: () => import('./components/sidebar'),
    shareproductModel: () => import('./components/shareproduct'),
    TopLinks: () => import('~/components/widgets/TopLinks'),
  },
  data() {
    return {
      bannerimagepath: '/images/side-banner.png',
      col2: true,
      col3: false,
      col4: false,
      col6: false,
      listview: false,
      category_id: 0,
      priceArray: [],
      allfilter: [],
      items: [],
      page_size: 12,
      page: 1,
      showquickviewmodel: false,
      quickviewproduct: {},
      shareproduct: {},
      shareproductModal: false
    }
  },
  computed: {
    ...mapGetters({
      CurrentCategoryID: 'pingoproducts/getterCurrentCategoryID',
      CurrentDetailedProduct: 'pingoproducts/getterCurrentDetailedProduct',
      PingoProductList: 'pingoproducts/getterPingoProductList',
      ProductListMeta: "pingoproducts/getterProductListMeta",
      gettersGrouponBuyServiceStatus: "system/gettersGrouponBuyServiceStatus",
    }),
    list_page_info(){
      return `page=${this.page}&page_size=${this.page_size}`
    }
  },
  watch: {
    gettersGrouponBuyServiceStatus(newVal, oldVal) {
      if (!newVal) {
        return this.$router.push('/')
      }
    },
    CurrentCategoryID(newVal, oldVal) {
      if (newVal > 0) {
        this.load_pingo_products(newVal)
      }
    }
  },
  mounted() {
      this.load_pingo_products(this.CurrentCategoryID)
  },
  methods: {
    ShowShareQR() {
      if (this.CurrentDetailedProduct.id > 0) {
        this.shareproductModal = true;
      }
    },
    tablePageChange(page) {
      this.page = page;
      this.load_pingo_products(this.CurrentCategoryID)
    },
    load_pingo_products(category_id) {
      this.$store.dispatch("pingoproducts/filter_category", {page_info:this.list_page_info, category_id:category_id})
    },
    onChangeSort(event) {
      this.$store.dispatch('filter/sortProducts', event.target.value)
    },
    getCategoryFilteredPingoProducts(category_id) {
      this.category_id = category_id;
      this.load_pingo_products(this.filter_options)
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
    alert(item) {
      this.dismissCountDown = item
    },
    showQuickview(productData) {
      this.showquickviewmodel = true;
      this.quickviewproduct = productData
    },
    showShareProduct(productData) {
      this.shareproduct = productData
      this.shareproductModal = true
    },
    showCompare(item, productData) {
      this.showcomparemodal = item
      this.comapreproduct = productData
    },
    closeCompareModal(item) {
      this.showcomparemodal = item
    },
    showCart(item, productData) {
      this.showcartmodal = item
      this.cartproduct = productData
    },
    closeCartModal(item) {
      this.showcartmodal = item
    },
    addCartPingoItem(info) {
      this.$store.commit("pingoproducts/setCart", info)
      this.$router.push("/pingo/checkout")
    }

  }
}
</script>
