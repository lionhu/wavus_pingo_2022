<template>
  <div>
    <b-modal
      id="modal-lg"
      size="lg"
      centered
      no-close-on-backdrop
      :title="$t('quickview.title')"
      :hide-footer="true"
      v-if="openModal"
    >

      <div class="row quickview-modal" v-if="!loading">
        <div class="col-lg-6 col-xs-12">
          <div class="quick-view-img text-center">
            <a href="javascript:void(0);" @click="view_product_detail"
               :to="{ path: '/shop/'+productData.id, params:{id:productData.id,product: productData, product_type:'REGULAR'}}">
              <img
                :src="productData.image_url"
                class="img-fluid bg-img"
                style="max-width:240px;"
              />
            </a>
          </div>
        </div>
        <div class="col-lg-6 rtl-text">
          <div class="product-right">
            <h2>{{ productData.item_name }}</h2>
            <h3 v-if="productData.sale">
              <del>{{ productData.price | currency("¥") }}</del>
            </h3>
            <h3 v-else>{{ productData.price  | currency("¥") }}</h3>
            <div class="border-product">
              <h6 class="product-title">{{ $t('quickview.detail') }}</h6>
              <p v-html='short_description'></p>
            </div>
            <div class="product-buttons" v-if="productData.item_variations">
              <div v-for="variant in productData.item_variations" :key="variant.id" class="row line-height-3 mt-3">
                <div class="col-12 d-flex justify-content-between" v-if="variant.variation_type==='REGULAR'">
                  <div class="text-center">
                    <img :src="variant.image_url" style="width: 80px;"> <br>
                    <span class="my-auto">{{ variant.sku }}</span> <br>
                    <span class="my-auto">{{ variant.name }}</span>
                  </div>
                  <!--                  <div class=" my-auto" v-if="policies && policies.USER_SELF && !$device.isMobile">-->
                  <!--                    <b-button pill block variant="outline-danger"-->
                  <!--                              v-if="variant.point_rule.is_valid && variant.point_rule.policies.user_self>0">-->
                  <!--                      <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>-->
                  <!--                      {{ variant.point_rule.policies.user_self | currency("") }}-->
                  <!--                    </b-button>-->
                  <!--                  </div>-->

                  <div>
                    <b-button pill block variant="outline-success">
                      {{ variant.price | currency("¥") }}
                    </b-button>
                    <span class="my-auto">
                      <a href="javascript:void(0);" @click="addToCart(variant, productData)"
                         class="btn btn-solid d-block my-3"
                         v-if="variant.inventory"><i
                        class="ti-shopping-cart"></i></a>
                      <a href="javascript:void(0);" class="btn btn-outline" v-else>{{ $t("product.sold_out") }}</a>
                    </span>

                    <div class=" my-auto" v-if="policies!==null && policies.USER_SELF ">
                      <b-button pill block variant="outline-danger"
                                v-if="variant.point_rule.is_valid && variant.point_rule.policies.user_self>0">
                        <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                        {{ variant.point_rule.policies.user_self | currency("") }}
                      </b-button>
                    </div>
                  </div>

                </div>
              </div>
            </div>

            <b-button size="lg" class="btn-danger text-white d-block mx-auto" v-else>
              売り切れ
            </b-button>
          </div>
        </div>
      </div>

      <div class="row quickview-modal" v-else>
        <div class="col">
          <div class="quick-view-img text-center mb-2">
            <img style="max-width:80%;" src="/images/icon/loading.gif">
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-6 offset-6 text-right">
          <b-button size="sm" variant="outline-danger" @click="closeModal">
            Close
          </b-button>
        </div>
      </div>
    </b-modal>
  </div>
</template>
<script>
import {mapGetters, mapState} from 'vuex'
import {productService} from "~/helpers/product.service";

export default {
  props: ['openModal'],
  data() {
    return {
      swiperOption: {
        slidesPerView: 1,
        spaceBetween: 20,
        freeMode: true
      },
      loading: false,
      productData: {}
    }
  },
  computed: {
    ...mapGetters({
      policies: 'authfack/policies',
      productDataID: "products/getCurrentDetailedProductID"
    }),
    short_description() {
      return this.productData.description ? this.productData.description.substring(0, 50) + "..." : ""
    }
  },
  watch: {
    productDataID: function (newval, oldval) {
      if (newval > 0) {
        this.load_product_byID();
      }
    },
    openModal(newval, oldval) {
      if (newval ) {
        this.load_product_byID();
      }
    }
  },
  methods: {
    async load_product_byID() {
      let self = this;
      self.productData={}
      this.loading = true;
      await productService.getProductByID(this.productDataID)
        .then(response => {
          self.productData = response.item
        })
          this.loading = false;
    },
    closeModal() {
      this.loading = false;
      this.$store.commit("products/setResetCurrentDetailProductinfo")
      this.$emit("closeModal")
    },
    view_product_detail(product) {
      this.$router.push("/sharebuy/detail")
    },
    addToCart: function (variant, product) {
      this.$store.dispatch('cart/addToCart', {product: product, variant: variant})
    },
  }
}
</script>

<style>
.line-height-3 {
  line-height: 3rem;
}
</style>
