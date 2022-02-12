<template>
  <div>
    <b-modal
      id="modal-share-lg"
      size="lg"
      centered
      ok-only
      no-close-on-backdrop
      title="友達とシェアしよう！"
      :hide-footer="true"
      :hide-header="true"
      :hide-header-close="true"
      v-if="openModal">
      <div class="row quickview-modal" v-if="loading">
        <div class="col">
          <div class="quick-view-img text-center mb-2">
            <img style="max-width:80%;" src="/images/icon/loading.gif">
          </div>
        </div>
      </div>
      <div class="row quickview-modal" v-else>
        <div class="col-lg-6 col-xs-12">
          <div class="quick-view-img text-center mb-2">
            <img style="max-width:80%;" id="introcode_image" :src="qr_image">
          </div>
          <ShareButtons class="text-center"
                        :qr_image="qr_image"
                        :link_url="share_link"
                        @copylink="copylink"
          ></ShareButtons>
          <div class="mt-3">
            <a href="javascript:void(0);" class="btn btn-solid black-btn btn-sm"
               @click="show_intro=!show_intro">ポイント説明</a>
            <dl v-show-slide="show_intro">
              <dt class="theme-color">レベル１</dt>
              <dd>- 自分の直接紹介で入会した会員（子供世代）が当該製品を購入する際に、自分が得られるポイントです。</dd>
              <dt class="theme-color">レベル２</dt>
              <dd>- 自分の直接紹介した会員経由で入会した会員（孫世代）が当該製品を購入する際に、自分が得られるポイントです。</dd>
            </dl>
          </div>
        </div>
        <div class="col-lg-6  col-xs-12 rtl-text mt-2">
          <VariationList :item_variations="productData.item_variations"/>
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
import {swalService} from "@/helpers/swal.service"
import {productService} from "~/helpers/product.service";

export default {
  props: ['openModal'],
  middleware: ["authenticated"],
  data() {
    return {
      qr_image: "",
      product_image: "",
      share_link: "",
      show_intro: false,
      QR_data: {
        qr_image: "/images/icon/loading.gif",
        share_link: ""
      },
      loading: false,
      productData: {}
    }
  },
  components: {
    ShareButtons: () => import("~/components/widgets/sharebuttons"),
    VariationList: () => import("./shareproduct_variations")
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME",
      loggedIn: "authfack/loggedIn",
      policies: 'authfack/policies',
      isClientAdmin: "authfack/isClientAdmin",
      isClientSuperAdmin: "authfack/isClientSuperAdmin",
      isSuperAdmin: "authfack/isSuperadmin",
      productDataID: "products/getCurrentDetailedProductID",
      // productData: "products/getCurrentDetailedProduct",
    }),
  },
  watch: {
    QR_data(newval, oldval) {
      if (newval.merge_pic !== "") {
        this.qr_image = newval.merge_pic;
        this.share_link = newval.share_link;
        let image_element = document.getElementById('introcode_image');
        if (image_element !== null) {
          image_element.src = this.qr_image;
        }
      }
    },
    productDataID: function (newval, oldval) {
      // console.log("productDataID", newval)
      if (newval > 0) {
        this.load_product();
      }
    },
  },
  mounted() {
    // console.log("productDataID", this.productDataID)
    if (this.productDataID > 0) {
      this.load_product();
    }
  },
  methods: {
    async load_product() {
      let self = this;
      self.loading = true;
      await productService.getProdoctByID(this.productDataID)
        .then(response => {
          self.productData = response.item
        })

      if (this.loggedIn) {
        await this.$store.dispatch("products/get_product_IntroQR", this.productDataID)
          .then(response => {
            self.QR_data = response;
          })
      }
      self.loading = false;
    },
    closeModal() {
      this.loading = false;
      this.$store.commit("products/setCurrentDetailProductID", 0)
      this.$emit("closeModal")
    },
    copylink() {
      if (window.clipboardData) {
        swalService.showToast("success", "リンクをコピーしました。")
        window.clipboardData.setData('share_link', this.share_link)
        return true
      } else if (navigator.clipboard) {
        swalService.showToast("success", "リンクをコピーしました。")
        return navigator.clipboard.writeText(this.share_link)
      } else {
        return false
      }
    }
  }
}
</script>

<style>
.line-height-3 {
  line-height: 3rem;
}
</style>
