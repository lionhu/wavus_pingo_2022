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
            <img style="max-width:80%;" id="introcode_image" :src="QR_data.merge_pic">
          </div>
          <ShareButtons class="text-center"
                        :qr_image="QR_data.merge_pic"
                        :link_url="QR_data.share_link"
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

          <ul v-if="productData.item_variations">
            <li v-for="variant in productData.item_variations" :key="variant.id"
                class="row line-height-3 my-2 py-2 border-bottom-grey ">
              <div class="col-12 d-flex justify-content-around align-items-center">
                <div>
                  <h5>{{ variant.name }}</h5>
                  <p>{{ variant.description }}</p>
                </div>

                <b-button pill variant="outline-success">
                  {{ variant.price | currency("¥") }}
                </b-button>
                <div class="text-center">
                  <!--                  <span class="d-block theme-color">{{ variant.price|currency("¥") }}</span>-->
                  <img :src="variant.image_url" style="width: 80px;">
                </div>
              </div>
              <div v-if="variant.point_rule.is_valid" v-show-slide="show_variation_slide_info(variant)" class="col-12">
                <h4 class="mt-2 theme-color">紹介ポイント</h4>
                <div class="row" v-if="isClientSuperAdmin||isSuperAdmin">
                  <div class="col-6">{{ $t("organization.client_superadmin") }}</div>
                  <div class="col-6">
                    <b-button pill block variant="outline-danger">
                      <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                      {{
                        variant.point_rule.policies.client_superadmin | currency("")
                      }}
                    </b-button>
                  </div>
                </div>
                <div class="row" v-if="isClientAdmin||isClientSuperAdmin||isSuperAdmin">
                  <div class="col-6">{{ $t("organization.client_admin") }}</div>
                  <div class="col-6">
                    <b-button pill block variant="outline-danger">
                      <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                      {{
                        variant.point_rule.policies.client_admin | currency("")
                      }}
                    </b-button>
                  </div>
                </div>
                <div class="row" v-if="policies.LEVEL_2">
                  <div class="col-6">{{ $t("organization.level_2") }}</div>
                  <div class="col-6">
                    <b-button pill block variant="outline-danger">
                      <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                      {{
                        variant.point_rule.policies.level_2 | currency("")
                      }}
                    </b-button>
                  </div>
                </div>
                <div class="row" v-if="policies.LEVEL_1">
                  <div class="col-6">{{ $t("organization.level_1") }}</div>
                  <div class="col-6">
                    <b-button pill block variant="outline-danger">
                      <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                      {{
                        variant.point_rule.policies.level_1 | currency("")
                      }}
                    </b-button>
                  </div>
                </div>
              </div>
              <div class="col-12 text-center">
                <a href="javascript:void(0);" class="btn btn-solid" @click="toggleFeatures(variant)">ポイント詳細</a>
              </div>
            </li>
          </ul>
          <b-button size="lg" class="btn-danger text-white d-block mx-auto" v-else>
            売り切れ
          </b-button>
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
import {axios} from '@/plugins/axios.js';
import {swalService} from "@/helpers/swal.service"


export default {
  props: ['openModal',"QR_data"],
  middleware: ["authenticated"],
  data() {
    return {
      qr_image: "",
      product_image: "",
      share_link: "",
      show_intro: false,
      show_slide_flags: []
    }
  },
  components: {
    ShareButtons: () => import("~/components/widgets/sharebuttons")
  },
  computed: {
    ...mapGetters({
      policies: 'authfack/policies',
      isClientAdmin: "authfack/isClientAdmin",
      isClientSuperAdmin: "authfack/isClientSuperAdmin",
      isSuperAdmin: "authfack/isSuperadmin",
      productData: "products/getCurrentDetailedProduct",
    }),
    ...mapState({
      ME: state => state.authfack.user
    })
  },
  watch: {
    openModal: function (newval, oldval) {
      if (newval) {

        let vm = this;
        // this.$store.dispatch("products/get_product_IntroQR", this.productData.id)
        //   .then(res => {
        //     console.log(res)
        //     // if (res.result) {
        //       vm.qr_image = res.merge_pic;
        //       vm.share_link = res.share_link;
        //       let image_element = document.getElementById('introcode_image');
        //       image_element.src = vm.qr_image;
        //     // } else {
        //     //   vm.qr_url = ""
        //     // }
        //   }).catch(err => {
        //   console.log(err)
        //   console.log("get_introduce_QR error:", err);
        // })
        if (this.productData.item_variations.length > 0) {
          vm.show_slide_flags = []
          this.productData.item_variations.forEach(variation => {
            vm.show_slide_flags.push({id: variation.id, show: false})
          })
        }

      }
    },
  },
  mounted() {
    if (this.productData !== undefined && this.productData.id) {
      console.log("good")
    } else {
      this.$emit("closeModal")
    }
  },
  methods: {
    become_promotor(variant_id) {
      var vm = this;
      let url = `/back/store/api/promotions/`;
      axios.$post(url, {variant_id: variant_id})
        .then(res => {
          if (res.result) {
            swalService.showToast("success", `ありがとうございました！クーポンコード ${res.data.promotion.coupon}`)
          } else if (res.error === 'promotion_create_ERROR_03') {

            swalService.showToast("error", "すでに追加されました！")
          }
        })
    },
    closeModal() {
      this.$emit("closeModal")
    },
    show_variation_slide_info(variation) {
      if (this.show_slide_flags.length === 0) return false;

      let index = this.show_slide_flags.findIndex(slide => slide.id === variation.id)
      if (index > -1) {
        return this.show_slide_flags[index].show;
      }
    },
    toggleFeatures(variation) {
      let index = this.show_slide_flags.findIndex(slide => slide.id === variation.id)
      if (index > -1) {
        this.show_slide_flags[index].show = !this.show_slide_flags[index].show;
      }
    },
    copylink() {
      console.log("copylink")
      if (window.clipboardData) {
        window.clipboardData.setData('share_link', this.share_link)
        console.log("window.clipboardData")
        return true
      } else if (navigator.clipboard) {
        console.log("navigator.clipboard")
        return navigator.clipboard.writeText(this.share_link)
      }else {
        console.log("else")
        return false
      }
    }
    //
    // copylink() {
    //   console.log(this.share_link)
    //   document.execCommand("copy");
    //   navigator.clipboard.writeText(this.share_link);
    //   swalService.showToast("success", "リンクをコピーしました。")
    // }
  }
}
</script>

<style>
.line-height-3 {
  line-height: 3rem;
}
</style>
