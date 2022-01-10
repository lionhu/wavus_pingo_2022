<template>
  <div>
    <Header/>
    <Breadcrumbs :title="$t('wishlist.title')" breadcrumb_type="static"/>
    <section class="wishlist-section section-b-space">
      <div class="container">
        <div class="row d-block d-sm-none">
          <div class="col-sm-12">
            <table class="table cart-table table-responsive-xs" v-if="wishlist.length">
              <thead>
              <tr class="table-head">
                <th scope="col">{{ $t('productname') }}</th>
              </tr>
              </thead>
              <tbody v-for="(favorite,index) in wishlist" :key="index">
              <tr>
                <td>
                  <a href="javascript:void(0);" @click="redirectToDetailPage(favorite.item.id)">
                    <nuxt-img :src='favorite.item.thumbimage_url' alt=""/>
                  </a>
                  <a href="javascript:void(0);">{{ favorite.item.item_name }}</a>
                  <div class="mobile-cart-content row">
                    <div class="col-xs-3">
                      <p>in stock</p>
                    </div>
                  </div>
                  <div class="mobile-cart-content row">
                    <div class="col-xs-3">
                      <h2 class="td-color">
                        <a href="javascript:void(0);" class="icon mr-1" @click="removeWishlistItem(favorite.id)">
                          <i class="ti-close"></i>
                        </a>
                      </h2>
                    </div>
                  </div>
                </td>
                <td>
                </td>
                <td>
                </td>
                <td>
                  <a href="javascript:void(0)" class="icon mr-3" @click="removeWishlistItem(favorite.id)">
                    <i class="ti-close"></i>
                  </a>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="row d-none d-md-block">
          <div class="col-sm-12">
            <table class="table cart-table table-responsive-lg" v-if="wishlist.length">
              <thead>
              <tr class="table-head">
                <th scope="col">{{ $t('image') }}</th>
                <th scope="col">{{ $t('productname') }}</th>
                <th scope="col">{{ $t('availabilities') }}</th>
                <th scope="col"></th>
              </tr>
              </thead>
              <tbody v-for="(favorite,index) in wishlist" :key="index">
              <tr>
                <td>
                  <a href="javascript:void(0);" @click="redirectToDetailPage(favorite.item.id)">
                    <nuxt-img :src='favorite.item.thumbimage_url' alt=""/>
                  </a>
                </td>
                <td>
                  <a href="javascript:void(0);">{{ favorite.item.item_name }}</a>
                  <div class="mobile-cart-content row">
                    <div class="col-xs-3">
                      <p>in stock</p>
                    </div>
                    <div class="col-xs-3">
                    </div>
                  </div>
                  <div class="mobile-cart-content row">
                    <div class="col-xs-3">
                      <h2 class="td-color">
                        <a href="javascript:void(0);" class="icon mr-1" @click="removeWishlistItem(favorite.id)">
                          <i class="ti-close"></i>
                        </a>
                      </h2>
                    </div>
                  </div>
                </td>
                <td>
                  <p v-if="favorite.item.is_valid&&favorite.item.variation_stock_total>0">{{
                      $t("product.in_stock")
                    }}</p>
                  <p class="theme-color" v-else>{{ $t("product.sold_out") }}</p>
                </td>
                <td>
                  <a href="javascript:void(0)" class="icon mr-3" @click="removeWishlistItem(favorite.id)">
                    <i class="ti-close"></i>
                  </a>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="row wishlist-buttons" v-if="wishlist.length">
          <div class="col-12">
            <nuxt-link :to="{ path: '/'}" :class="'btn btn-solid'">{{ $t('continue_shopping') }}</nuxt-link>
          </div>
        </div>
        <div class="col-sm-12 empty-cart-cls text-center" v-if="wishlist.length===0">
          <nuxt-img src='/images/empty-wishlist.png' class="img-fluid" alt="empty cart"/>
          <h3 class="mt-3">
            <strong>{{ $t('empty_wishlist') }}</strong>
          </h3>
          <div class="col-12">
            <nuxt-link :to="{ path: '/'}" class="btn btn-solid">{{ $t('continue_shopping') }}</nuxt-link>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<script>
import {swalService} from "~/helpers/swal.service"
import {mapGetters,} from 'vuex'
import logger from "@fortawesome/vue-fontawesome/src/logger";
import {APIServices} from "~/helpers/APIs";

export default {
  name: "wishlist",
  middleware: 'authenticated',
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
  },
  data() {
    return {
      wishlist: [],
    }
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME"
    }),
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
      this.$nuxt.$loading.finish();
    },
    removeWishlistItem: function (favorite_id) {
      let self = this;
      this.$store.dispatch("products/delete_my_favorites", favorite_id)
        .then((response) => {
          let indexOfWish = self.wishlist.findIndex(item => item.id === favorite_id);
          if (indexOfWish > -1) {
            self.wishlist.splice(indexOfWish, 1)
            swalService.showToast("success", "削除されました！")
          }
        })
    },
  },
  mounted() {
    let self = this;
    let url = `store/public/filter_favorites/me/?query=${this.ME.pk}&omit=user`
    APIServices.get(url)
      .then(APIServices.handleResponse)
      .then(response => {
        console.log(response)
        self.wishlist = response
      })

  }
}
</script>
