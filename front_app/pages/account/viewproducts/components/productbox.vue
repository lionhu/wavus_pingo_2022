<template>
  <div>
    <div class="img-wrapper">
      <div class="lable-block">
        <span class="lable3" v-if="product.item.is_valid && product.item.variation_stock_total">在庫あり</span>
        <span class="lable4 theme-bgcolor pingo_label" style="transform: rotate(0)"
              v-if="product.item.is_valid && product.item.variation_stock_total">販売中</span>
      </div>
      <div class="front">
        <a href="javascript:void(0);" @click="redirectToDetailPage(product.item.id)">
          <nuxt-img :src='product.item.thumbimage_url' :id="product.id" class="img-fluid bg-img"/>
        </a>
      </div>
      <div class="cart-info cart-wrap">
        <a href="javascript:void(0)" @click="showQuickview(product.item)"
           v-b-modal.modal-lg variant="primary"
           v-if="isLoggedIn && product.item.is_valid && product.item.variation_stock_total">
          <i class="ti-shopping-cart theme-bgcolor"></i>
        </a>
        <a
          href="javascript:void(0)"
          @click="ShowShareQR(product.item)"
          v-b-modal.modal-share-lg
          variant="primary"
          v-if="isLoggedIn && product.item.is_valid && product.item.variation_stock_total">
          <i class="ti-share theme-bgcolor" aria-hidden="true"></i>
        </a>
      </div>
    </div>
    <div class="product-detail">
      <el-rate v-model="product.rate" disabled text-color="#ff9900"></el-rate>
      <a href="javascript:void(0);" @click="redirectToDetailPage(product.item.id)"
         class="d-flex justify-content-around text-white">
        <h6>{{ product_name(product.item) }}</h6>
      </a>
        <h6 style="line-height:1.4rem;">{{ product.created_at | short_date }}</h6>
    </div>


  </div>

</template>

<script>
import {mapGetters} from 'vuex'
import {swalService} from "~/helpers/swal.service";

export default {
  props: ['product', 'index'],
  components: {
    "el-rate": () => import("element-ui/lib/rate"),
  },
  data() {
    return {}
  },
  computed: {
    ...mapGetters({
      isLoggedIn: "authfack/loggedIn",
    })
  },
  methods: {
    product_name(item) {
      return item.item_name.substring(0, 16) + "..."
    },
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

    addToWishlist: function (product) {
      let self = this;
      this.dismissCountDown = this.dismissSecs;
      let info = {
        item: product.id
      }
      this.$store.dispatch("products/add_my_favorites", info)
        .then((res) => {
          if (res.id > 0) {
            swalService.showToast("success", self.$root.$t("wishlist.added"));
          }
        }).catch(err => {
        switch (err.data.message) {
          case "wishlist.existed":
            swalService.showToast("warning", self.$root.$t(err.data.message));
            break;
          default:
            break
        }
      })
    },
    load_product() {
      return this.$store.dispatch("products/get_product_byID", this.product.id)
        .then(response => {
          return response
        })
    },
    ShowShareQR() {
      this.$emit("ShowShareQR", this.product.item.id)
    },
    showQuickview() {
      this.$emit("showQuickview", this.product.item.id)
    },
  }
}
</script>

<style>
.circle-button {
  background-color: #ff4c3b;
  border-radius: 100%;
  width: 40px;
  padding: 5px;
  color: white;
}

.line-height-2 {
  line-height: 2rem;
}

</style>
