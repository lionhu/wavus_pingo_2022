<template>
  <div>
    <Breadcrumbs :title="DetailedProduct.item_name" breadcrumb_type="static"/>
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6">
          <div v-swiper:mySwiper="swiperOption" ref="mySwiper">
            <div class="swiper-wrapper">
              <div class="swiper-slide text-center" v-for="(sliderimage,index) in DetailedProduct.item_sliderimages"
                   :key="index">
                <inner-image-zoom class="img-fluid bg-img" :id="sliderimage.id"
                                  :fullscreenOnMobile="true"
                                  zoomType="hover"
                                  :width="480"
                                  :height="540"
                                  :hasSpacer="true"
                                  :src="sliderimage.image_url"
                                  :zoomSrc="sliderimage.image_url"/>
              </div>
            </div>
          </div>

          <div class="row mt-3">
            <div class="col-lg-8 offset-lg-2 col-xs-12 slider-nav-images">
              <div v-swiper:mySwiper1="swiperOption1">
                <div class="swiper-wrapper">
                  <div
                    class="swiper-slide"
                    v-for="(sliderimage,index) in DetailedProduct.item_sliderimages"
                    :key="index"
                  >
                    <img
                      :src="sliderimage.image_url"
                      :id="sliderimage.id"
                      class="img-fluid bg-img"
                      :alt="sliderimage.title"
                      v-on:click="slideTo(index)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="product-right">
            <h2>{{ DetailedProduct.item_name }}</h2>
            <div class="product-buttons border-product" v-if="DetailedProduct.item_variations.length===0">
              <b-button size="lg" class="btn-danger text-white d-block mx-auto">
                売り切れ
              </b-button>
            </div>

            <div class="border-product " v-if="DetailedProduct.item_variations">

              <div class="line-height-3 my-2 d-flex justify-content-around"
                   v-for="variant in DetailedProduct.item_variations"
                   :key="variant.id">
                <div class="">
                  <inner-image-zoom :id="variant.id"
                                    :fullscreenOnMobile="true"
                                    zoomType="hover"
                                    style="max-width:160px;"
                                    :src="variant.image_url"
                                    :zoomSrc="variant.image_url"/>

                  <h6>{{ variant.name }}</h6>
                  <h6>SKU:{{ variant.sku }}</h6>
                </div>
                <div class=" my-auto">
                  <b-button pill block variant="outline-success">
                    {{ variant.price | currency("¥") }}
                  </b-button>
                  <a href="javascript:void(0);" @click="addToCart(variant, DetailedProduct)"
                     class="btn btn-solid d-block my-3"
                     v-if="variant.inventory"><i
                    class="ti-shopping-cart"></i></a>
                  <a href="javascript:void(0);" class="btn btn-outline" v-else>{{ $t("product.sold_out") }}</a>
                  <b-button pill block variant="outline-danger"
                            v-if="variant.point_rule.is_valid && variant.point_rule.policies.user_self>0">
                    <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                    {{ variant.point_rule.policies.user_self | currency("") }}
                  </b-button>
                </div>
              </div>
            </div>
            <div class="border-product">
              <h6 class="product-title">{{ $t('product.about') }}</h6>
              <p v-html='DetailedProduct.description'></p>
            </div>
            <div class="border-product" v-if="isLoggedIn">
              <div class="product-icon">
                <div class="inline-block">
                  <a href="javascript:void(0)" title="Share" class="wishlist-btn text-dark"
                     @click="ShowShareQR" v-b-modal.modal-share-lg
                     variant="primary">
                    <i class="ti-share" aria-hidden="true"></i>
                  </a>
                  <span class="product-title ">share it</span>
                </div>
                <div class="d-inline-block">
                  <a href="javascript:void(0)" class="wishlist-btn text-dark"
                     @click="addToWishlist(DetailedProduct)">
                    <i class="fa fa-heart"></i>
                    <span class="title-font">{{ $t('wishlist.addto') }}</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-12">
          <b-tabs card>
            <b-tab :title="$t('product.details')" active>
              <b-card-text>
                <p v-html="DetailedProduct.description" class="line-height-2"></p>
                <p class="line-height-2">
                  <span class="title">ブランド:</span>{{ DetailedProduct.brand }} <br>
                  <span class="title">シーリズ:</span>{{ DetailedProduct.series }} <br>
                  <span class="title">モデル:</span>{{ DetailedProduct.model }} <br>
                </p>

                <p v-html="DetailedProduct.package"></p>
              </b-card-text>
            </b-tab>
            <b-tab :title="$t('product.video')" v-if="DetailedProduct.video_url!='video_url'">
              <b-card-text>
                <div class="mt-3 text-center">
                  <iframe
                    width="560"
                    height="315"
                    :src="DetailedProduct.video_url"
                    allow="autoplay; encrypted-media"
                    allowfullscreen
                  ></iframe>
                </div>
              </b-card-text>
            </b-tab>
            <b-tab title="コメント">
              <b-card-text>
                <h4 class="mb-3 text-right" v-if="isLoggedIn">
                  <a href="javascript:void(0);" @click="add_comment" class="btn btn-solid d-block mb-3">コメントを書く！</a>
                </h4>
                <section class="section-b-space blog-detail-page review-page">
                  <div class="container">
                    <div class="row">
                      <div class="col-sm-12">
                        <ul class="comment-section">
                          <li v-for="(comment, index) in comments" :key="index" class="d-block"
                              v-bind:class="{'text-center':$device.isMobile}" v-if="comment_visible(comment)">
                            <div class="media">
                              <img :src="comment.user.avatar_thumb_url" alt="item.name"/>
                              <div class="media-body">
                                <h6>
                                  {{ comment.user.username }}
                                  <span>( {{ comment.created_at | short_date }} )</span>
                                </h6>
                                <p v-html="comment.content"></p>
                                <ul class="comnt-sec">
                                  <li>
                                    <a href="javascript:void(0);" @click="change_comment_thumbs(comment,'up')">
                                      <i class="fa fa-thumbs-o-up text-danger" aria-hidden="true"></i>
                                      <span>({{ comment.thumbs_up }})</span>
                                    </a>
                                  </li>
                                  <li>
                                    <a href="javascript:void(0);" @click="change_comment_thumbs(comment,'down')">
                                      <div class="unlike">
                                        <i class="fa fa-thumbs-o-down text-primary" aria-hidden="true"></i>({{
                                          comment.thumbs_down
                                        }})
                                      </div>
                                    </a>
                                  </li>
                                  <li class="text-danger" v-if="isLoggedIn && ME.pk===comment.user.pk">
                                    <a href="javascript:void(0);" @click="delete_comment(comment.id)">
                                      <div class="unlike">
                                        <i class="fa fa-trash" aria-hidden="true"></i>削除
                                      </div>
                                    </a>
                                  </li>
                                </ul>
                              </div>
                            </div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </section>
              </b-card-text>
            </b-tab>
          </b-tabs>
        </div>
      </div>
    </div>
    <shareproductModel :openModal="shareproductModal"
                       @closeModal="closeShareQRModel"/>
  </div>
</template>
<script>
import {mapState, mapGetters} from 'vuex'
import Swal from "sweetalert2"
import {swalService} from "~/helpers/swal.service";
import 'vue-inner-image-zoom/lib/vue-inner-image-zoom.css';
import InnerImageZoom from 'vue-inner-image-zoom';
import {APIServices} from "~/helpers/APIs";

export default {
  name: "shop_item_detail",
  layout:"sharebuy",
  components: {

    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    shareproductModel: () => import('./components/shareproduct'),
    'inner-image-zoom': InnerImageZoom
  },
  data() {
    return {
      swiperOption: {
        slidesPerView: 1,
        spaceBetween: 20,
        freeMode: true
      },
      swiperOption1: {
        slidesPerView: 3,
        spaceBetween: 30,
        freeMode: true,
        centeredSlides: false
      },
      shareproductModal: false,
      page: 1,
      page_size: 100,
      comments: [],
      comments_meta: {},
      'zoomerOptions': {
        zoomFactor: 3, // scale for zoomer
        pane: 'pane', // three type of pane ['pane', 'container-round', 'container']
        hoverDelay: 300, // how long after the zoomer take effect
        namespace: 'zoomer', // add a namespace for zoomer component, useful when on page have mutiple zoomer
        move_by_click: false,// move image by click thumb image or by mouseover
        scroll_items: this.zoom_images.length, // thumbs for scroll
        choosed_thumb_border_color: "#bbdefb", // choosed thumb border color
        scroller_button_style: "line",
        scroller_position: "left",
        zoomer_pane_position: "right"
      }
    }
  },
  computed: {
    ...mapGetters({
      policies: 'authfack/policies',
      cart: 'cart/cartItems',
      isLoggedIn: "authfack/loggedIn",
      ME: "authfack/ME",
      DetailedProduct: "products/getCurrentDetailedProduct",
      DetailedProductID: "products/getCurrentDetailedProductID",
    }),
    swiper() {
      return this.$refs.mySwiper.swiper
    },
  },
  mounted() {
    if (this.DetailedProductID > 0) {
      this.load_product_comments()
    } else {
      this.$router.push("/sharebuy")
    }
  },
  methods: {
    comment_visible(comment) {
      return comment.approved === true || comment.user.id === this.ME.pk;
    },
    tablePageChange(page) {
      this.page = page;
      this.load_product_comments()
    },
    async load_product_comments() {
      let self = this;let url = `store/public/filter_comments/of_product/?query=${this.DetailedProductID}&omit=item`
      await APIServices.get(url)
        .then(APIServices.handleResponse)
        .then(res => {
          self.comments = res;
          self.comments_meta.total = res.length;
        })
    },
    async add_comment() {
      let self = this;
      const {value: text} = await Swal.fire({
        input: 'textarea',
        inputLabel: 'コメント',
        inputPlaceholder: 'コメント...',
        inputAttributes: {
          'aria-label': 'コメントを入力してください。'
        },
        showCancelButton: true
      })

      if (text) {
        let info = {
          user: this.ME.profile.user_id,
          item: this.DetailedProduct.id,
          content: text
        }
        APIServices.post("store/public/comments/", info)
          .then(APIServices.handleResponse)
          .then(res => {
            self.comments.unshift(res.comment);
            swalService.showToast("success", "ありがとうございました！");

          })
      }
    },
    replace_comment_thumbs(comment_id, thumb_type) {
      let index = this.comments.findIndex(item => item.id === comment_id)
      if (index > -1) {
        if (thumb_type === "up") {
          this.comments[index].thumbs_up += 1
        } else {
          this.comments[index].thumbs_down += 1
        }

        swalService.showToast("success", "ありがとうございました！");
      }
    },
    delete_comment(comment_id) {
      let self = this;
      APIServices.destroy(`store/public/comments/${comment_id}/`)
        .then(response => {
          if (response) {
            let index = this.comments.findIndex(item => item.id === comment_id)
            if (index > -1) {
              self.comments.splice(index, 1)
            }
          }
        })
    },
    change_comment_thumbs(comment, thumb_type) {
      if (!this.isLoggedIn) {
        swalService.showToast("error", "会員に加入する必要があります。");
        return false;
      }
      let self = this;
      APIServices.post("store/public/thumbs/", {"comment": comment.id, "thumb_type": thumb_type})
        .then(APIServices.handleResponse)
        .then(res => {
          if (res.id > 0) {
            self.replace_comment_thumbs(comment.id, thumb_type)
          }
        }).catch(errors => {
        swalService.showToast("error", "評価は一回のみです。");
      })
    },
    zoom_images(DetailedProduct) {
      if (DetailedProduct.item_sliderimages && DetailedProduct.item_sliderimages.length) {
        let result = {};
        let thumbs = [];
        let normal_size = [];
        DetailedProduct.sliderimages.forEach(image => {
          thumbs.push({"id": image.id, "url": image.thumbimage_url});
          normal_size.push({"id": image.id, "url": image.image_url});
        })
        result.thumbs = thumbs;
        result.normal_size = normal_size;
        return result;
      }
    },
    ShowShareQR() {
      console.log("products/setCurrentDetailProductID", this.DetailedProductID)
      this.$store.commit("products/setCurrentDetailProductID", this.DetailedProductID)
      this.shareproductModal = true;
    },
    closeShareQRModel() {
      this.shareproductModal = false;
    },
    addToWishlist: function (product) {
      var vm = this;
      this.dismissCountDown = this.dismissSecs;
      let info = {
        item: product.id
      }
      this.$store.dispatch("products/add_my_favorites", info)
        .then((res) => {
          if (res.id > 0) {
            swalService.showToast("success", vm.$root.$t("wishlist.added"));
          }
        }).catch(err => {
        switch (err.data.message) {
          case "wishlist.existed":
            swalService.showToast("warning", vm.$root.$t(err.data.message));
            break;
          default:
            break
        }
      })
    },
    addToCart: function (variant, product) {
      this.$store.dispatch('cart/addToCart', {product: product, variant: variant})

    },
    slideTo(id) {
      this.swiper.slideTo(id, 1000, false)
    },
  }
}
</script>

<style scoped>
.line-height-2 {
  line-height: 1.2rem;
}

.title {
  display: inline-block;
  min-width: 120px !important;
  text-align: center !important;
}

a .nav-link {
  color: #3f3f40 !important;
}
</style>
<!--#FF4C3C-->
