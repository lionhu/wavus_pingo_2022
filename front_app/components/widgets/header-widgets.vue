<template>
  <div>
    <div class="icon-nav">
      <ul>
        <li class="onhover-div mobile-search">
          <div>
            <img
              alt
              src='/images/icon/search.png'
              @click="openSearch()"
              class="img-fluid"
            >
            <i class="ti-search" @click="openSearch()"></i>
          </div>
          <div id="search-overlay" class="search-overlay" :class="{ opensearch:search }">
            <div>
              <span class="closebtn" @click="closeSearch()" title="Close Overlay">×</span>
              <div class="overlay-content">
                <div class="container">
                  <div class="row">
                    <div class="col-xl-12">
                      <form>
                        <div class="form-group mb-0">
                          <input
                            type="text"
                            class="form-control"
                            v-model="searchString"
                            @keyup="searchProduct"
                            placeholder="Search a Product"
                          >
                        </div>
                        <button type="submit" class="btn btn-primary">
                          <i class="fa fa-search"></i>
                        </button>
                      </form>
                    </div>
                  </div>
                  <div class="row" v-if="search_products_count">
                    <div class="col-xl-12">

                      <!--              <h4>{{ $t("dashboard_menu.viewproducts") }}</h4>-->
                      <div class="collection-product-wrapper" v-if="$device.isDesktop">
                        <div class="section-t-space portfolio-section portfolio-padding metro-section port-col">
                          <no-ssr>
                            <div v-masonry transition-duration="3s" item-selector=".item"
                                 class="masonry-container isotopeContainer row">
                              <div v-masonry-tile
                                   class="col-xl-2 col-sm-4 col-grid-box isotopeSelector item"
                                   :key="index"
                                   v-for="(product, index) in search_products">
                                <div class="product-box ribbon-box">
                                  <div class="ribbon-two ribbon-two-danger" v-if="!product.is_valid"><span>売切れ</span>
                                  </div>
                                  <div class="img-wrapper" v-if="product.is_valid">
                                    <div class="front">
                                      <a href="javascript:void(0);" @click="redirectToDetailPage(product.id)">
                                        <!--                                      <nuxt-link :to="{ path: '/shop/'+product.id}">-->
                                        <nuxt-img
                                          :src="product.thumbimage_url"
                                          :id="product.id"
                                          class="img-fluid bg-img"
                                          :alt="product.item_name"
                                          :key="index"
                                        />
                                        <!--                                      </nuxt-link>-->
                                      </a>
                                    </div>
                                  </div>
                                  <div class="img-wrapper" v-else>
                                    <div class="front">
                                      <nuxt-img
                                        :src="product.thumbimage_url"
                                        :id="product.id"
                                        class="img-fluid bg-img"
                                        :alt="product.item_name"
                                        :key="index"
                                      />
                                    </div>
                                  </div>
                                  <div class="product-detail">
                                    <a href="javascript:void(0);" @click="redirectToDetailPage(product.id)"
                                       v-if="product.is_valid">
                                      <h6>{{ product.item_name }}</h6>
                                    </a>
                                    <a href="javascript:void(0);" v-else>
                                      <h6>{{ product.item_name }}</h6>
                                    </a>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </no-ssr>
                        </div>
                      </div>

                      <div class="collection-product-wrapper" v-else>
                        <div class="typography-box" :key="index"
                             v-for="(product, index) in search_products">

                          <div class="headings">
                            <a href="javascript:void(0);" @click="redirectToDetailPage(product.id)"
                               v-if="product.is_valid">
                              <h6>{{ product.item_name }}</h6>
                            </a>
                            <a href="javascript:void(0);" v-else>
                              <h6>{{ product.item_name }}</h6>
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="row" v-else>
                    <div class="col-sm-12">
                      <div class="text-center section-t-space section-b-space">
                        <img v-lazy='"/images/empty-search.jpg"' class="img-fluid" alt/>
<!--                        <h3 class="mt-3">Sorry! Couldn't find the product you were looking For!!!</h3>-->
                        <div class="col-12 mt-3">
                          <nuxt-link :to="{ path: '/'}" class="btn btn-solid">買い物へ</nuxt-link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </li>
        <li class="onhover-div mobile-cart">
          <div>
            <img alt src='/images/icon/cart.png' class="img-fluid max-height-60">
            <i class="ti-shopping-cart"></i>
            <span class="cart_qty_cls">{{ cartQty }}</span>
          </div>
          <ul class="show-div shopping-cart" v-if="!cartQty">
            <li>{{ $t('cart_info.empty_cart') }}</li>
          </ul>
          <ul class="show-div shopping-cart" v-if="cartQty">
            <li v-for="(item,index) in cart" :key="index">
              <div class="media">
                <img alt class="mr-3 max-height-60" :src='item.variant.image_url'>
                <div class="media-body">
                  <nuxt-link :to="{ path: '/shop/'+item.product.id}">
                    <h6>{{ item.product.item_name }}({{ item.variant.name.substring(0, 5) + "..." }})</h6>
                  </nuxt-link>
                  <h6>
                    <span>{{ item.quantity }} x {{ item.variant.price | currency("¥") }}</span>
                  </h6>
                </div>
              </div>
              <div class="close-circle">
                <a href="#" @click='removeCartItem(item)'>
                  <i class="fa fa-times" aria-hidden="true"></i>
                </a>
              </div>
            </li>
            <li>
              <div class="total">
                <h5>
                  {{ $t('cart_info.total') }} :
                  <span>{{ cartTotal  | currency("¥") }}</span>
                </h5>
              </div>
            </li>
            <li>
              <div class="d-flex justify-content-around">
                <nuxt-link :to="{ path: '/account/cart'}" :class="'view-cart'" class="btn btn-solid btn-sm">
                  <i class="ti-shopping-cart text-white"></i>{{ $t('cart_info.short_title') }}
                </nuxt-link>
                <nuxt-link :to="{ path: '/account/checkout'}" :class="'checkout'" class="btn btn-solid btn-sm">
                  {{ $t('cart_info.checkout') }}
                </nuxt-link>
              </div>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
import {mapState, mapGetters} from 'vuex'
import {APIServices} from "~/helpers/APIs";

export default {
  name: "header_widgets",
  data() {
    return {
      currencyChange: {},
      search: false,
      searchString: '',
      search_products: [],
      search_products_count: 0
    }
  },
  computed: {
    ...mapState({
      searchItems: state => state.products.searchProduct
    }),

    ...mapGetters({
      back_server: "system/getterBackServer",
      cart: 'cart/cartItems',
      cartTotal: 'cart/cartTotalAmount',
      cartQty: 'cart/cartQty',
      curr: 'products/changeCurrency',
      CategoryProductIds: "products/getterCategoryProductIds"
    })
  },
  methods: {
    async redirectToDetailPage(product_id) {
      let self = this;
      this.$store.commit("products/setCurrentDetailProductID", product_id)
      this.$nuxt.$loading.start();
      await this.$store.dispatch("products/get_product_byID", product_id)
        .then(response => {
          self.$router.push("/sharebuy/detail")
        })
      this.closeSearch();
      this.$nuxt.$loading.finish();

    },
    openSearch() {
      this.search = true
    },
    closeSearch() {
      this.search = false
      this.search_products = [];
      this.searchString = "";
    },
    searchProduct() {
      let vm = this;
      let url = `store/public/filter_products/by_name_description/?query=${this.searchString}}`
      APIServices.get(url).then(APIServices.handleResponse).then(response => {
        console.log(response)
        if (response.length) {
          vm.search_products = response;
          vm.search_products_count = response.length;
        } else {
          vm.search_products = []
          vm.search_products_count = 0;
        }
      })
    },
    removeCartItem: function (product) {
      this.$store.dispatch('cart/removeCartItem', product)
    },
    updateCurrency: function (currency, currSymbol) {
      this.currencyChange = {curr: currency, symbol: currSymbol}
      this.$store.dispatch('products/changeCurrency', this.currencyChange)
    },
    switchLanguage: function (language) {
      // this.isJa = !this.isJa;
      // const locale = this.isJa ? 'ja' : 'en'
      this.$cookies.set('locale', language, {
        path: '/',
        maxAge: 60 * 60 * 24 * 365
      });  // localeをCookieに保存
      this.$i18n.locale = language;           // 言語を切り替え
    }
  }
}
</script>

<style>
.max-height-60 {
  max-height: 60px;
}
</style>
