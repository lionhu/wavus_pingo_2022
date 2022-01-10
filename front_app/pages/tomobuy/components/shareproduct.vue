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
      <div class="row quickview-modal">
        <div class="col-lg-6 col-xs-12">
          <div class="quick-view-img text-center mb-2">
            <img style="max-width:80%;" id="introcode_image" alt="">
          </div>
          <ShareButtons class="text-center"
                        :qr_image="qr_image"
                        :link_url="share_link"
                        @copylink="copylink"
          ></ShareButtons>

        </div>
        <div class="col-lg-6  col-xs-12 rtl-text mt-2">
          <div class="product-right"><h2>{{ productData.item_name }}</h2>
            <h4>
              <del>{{ productData.price |currency("¥") }}</del>
              <span class="theme-color">{{ discount_percentage }} off</span></h4>
            <h3 class="theme-color">{{ productData.discount_price |currency("¥") }}</h3>
            <div v-if="productData.point_rule.is_valid" class="my-md-3">

              <b-button pill block variant="outline-danger">
                <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                {{
                  productData.point_rule.policies.user_self | currency("")
                }}
              </b-button>
            </div>
            <div class="pro_inventory">
              <p class="active"> Come on! Join us! </p>
              <el-progress :text-inside="true" :format="progress_text" :stroke-width="24" :percentage="percentage"
                           :color="colors" class="my-1 "></el-progress>
            </div>
            <div class="product-description border-product">
              <h6 class="product-title size-text">
                {{ $t("pingo_product.specification.targetNum.text") }}<span>{{
                  productData.targetNum |currency("")
                }}</span>
              </h6>
              <h6 class="product-title size-text">
                {{ $t("pingo_product.specification.currentNum.text") }}<span>{{
                  productData.currentNum |currency("")
                }}</span>
              </h6>
              <h6 class="product-title size-text">
                {{ $t("pingo_product.specification.until_at.text") }}<span>{{ productData.until_at |short_date }}</span>
              </h6>
            </div>
            <div class="border-product">
              <h6 class="product-title">{{ $t("pingo_product.specification.remaining_time") }}</h6>
              <client-only>
                <flip-countdown :deadline="countdown_until(productData.until_at)"></flip-countdown>
              </client-only>
            </div>
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
import {swalService} from "@/helpers/swal.service"

export default {
  props: ['openModal'],
  middleware: ["authenticated"],
  data() {
    return {
      qr_image: "",
      product_image: "",
      share_link: "",
      QR_data: {},
      colors: [
        {color: '#f56c6c', percentage: 20},
        {color: '#e6a23c', percentage: 40},
        {color: '#5cb87a', percentage: 60},
        {color: '#1989fa', percentage: 80},
        {color: '#6f7ad3', percentage: 100}
      ],
      loading: false,
    }
  },
  components: {
    ShareButtons: () => import("@/components/widgets/sharebuttons"),
    "el-progress": () => import('element-ui/lib/progress'),
    FlipCountdown: () => import('vue2-flip-countdown')
  },
  computed: {
    ...mapGetters({
      policies: 'authfack/policies',
      productData: 'pingoproducts/getterCurrentDetailedProduct',
      isClientAdmin: "authfack/isClientAdmin",
      isClientSuperAdmin: "authfack/isClientSuperAdmin",
      isSuperAdmin: "authfack/isSuperAdmin",
      // ME: "authfack/ME",
    }),
    discount_percentage() {
      let percent = Math.round((this.productData.price - this.productData.discount_price) / this.productData.price * 100);
      return `${percent}%`
    },
    percentage() {
      if (this.productData !== undefined) {
        return Math.round(this.productData.currentNum / this.productData.targetNum * 100);
      }
      return 0;
    },
  },
  watch: {
    QR_data(newval, oldval) {
      // console.log("QR_data", newval)
      if (newval.merge_pic !== "") {
        this.qr_image = newval.qr_image;
        this.share_link = newval.share_link;
        let image_element = document.getElementById('introcode_image');
        image_element.src = this.qr_image;
      }
    },
    openModal: function (newval, oldval) {
      if (newval) {
        let vm = this;
        this.$store.dispatch("pingoproducts/get_product_IntroQR", this.productData.id)
          .then(res => {
            console.log(res)
            vm.QR_data = {
              qr_image: res.merge_pic,
              share_link: res.share_link
            }
          }).catch(err => {
          console.log("get_introduce_QR error:", err);
        })
      }
    },
  },
  methods: {
    countdown_until: function (time) {
      var temp_time = time.split('.')[0];
      return temp_time.replace("T", " ");
    },
    progress_text: function (percentage) {
      return this.productData.currentNum + "/" + this.productData.targetNum
    },
    closeModal() {
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

<style scoped>
.line-height-3 {
  line-height: 3rem;
}

.flip-card {
  font-size: 1.5rem !important;
}

.flip-clock .flip-clock__slot {
  font-size: 0.8rem !important;
}

.flip-clock .flip-clock__card {
  font-size: 1rem !important;
}
</style>
