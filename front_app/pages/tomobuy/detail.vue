<template>
  <div>
    <Header/>
    <Breadcrumbs :title="getDetail.item_name"/>
    <section>
      <div class="collection-wrapper productdetail">
        <div class="container">
          <div class="row">
            <div class="col-lg-6">
              <div v-swiper:mySwiper="swiperOption" ref="mySwiper">
                <div class="swiper-wrapper">
                  <div class="swiper-slide" v-for="(sliderimage,index) in getDetail.item_pingo_sliderimages"
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
              <div class="row">
                <div class="col-12 slider-nav-images">
                  <div v-swiper:mySwiper1="swiperOption1">
                    <div class="swiper-wrapper">
                      <div class="swiper-slide"
                           v-for="(sliderimage,index) in getDetail.item_pingo_sliderimages"
                           :key="index">
                        <img :src="sliderimage.thumbimage_url"
                             :id="sliderimage.id"
                             class="img-fluid bg-img"
                             :alt="sliderimage.title"
                             v-on:click="slideTo(index)"/>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-6 rtl-text">
              <div class="product-right">
                <h2>{{ getDetail.item_name }}</h2>
                <span class="d-block theme-bg-color">EVENT_ID: #{{ getDetail.category }}-{{ getDetail.id }}</span>
                <el-rate v-model="getDetail.rate" disabled text-color="#ff9900"></el-rate>
                <h6>
                  <del>{{ getDetail.price| currency("¥") }}</del>
                  <span class="theme-color">{{ discount_percentage }} off</span>
                </h6>
                <div class="border-product">
                  <h6 class="product-title">募集要項</h6>
                  <div class="product-icon d-flex justify-content-around">
                    <div class="d-inline-block">
                      <span class="product-title">{{ $t("pingo_product.specification.targetNum.text") }}</span>
                    </div>
                    <div class="d-inline-block">
                      {{ getDetail.targetNum |currency("") }}
                    </div>
                  </div>
                  <div class="product-icon d-flex justify-content-around">
                    <div class="d-inline-block">
                      <span class="product-title">{{ $t("pingo_product.specification.currentNum.text") }}</span>
                    </div>
                    <div class="d-inline-block">
                      {{ getDetail.currentNum |currency("") }}
                    </div>
                  </div>
                </div>

                <div class="d-flex justify-content-around">
                  <div>
                    <h3 class="theme-color">{{ getDetail.discount_price| currency("¥") }}</h3>
                  </div>
                  <div v-if="getDetail.point_rule.is_valid" class="my-md-3">

                    <b-button pill block variant="outline-danger">
                      <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                      {{
                        getDetail.point_rule.policies.user_self | currency("")
                      }}
                    </b-button>
                  </div>
                  <div>
                    <a href="javascript:void(0);" class='btn-solid btn'
                       @click="addCartPingoItem"
                       v-if="!isExpired">
                      <i class="ti-shopping-cart"></i>
                    </a>

                  </div>
                </div>


                <div class="border-product">
                  <h6 class="product-title">{{ $t('product.about') }}</h6>
                  <p v-html="getDetail.description"></p>
                </div>
                <div class="border-product" v-if="getDetail.vendor !==undefined">
                  <h6 class="product-title">{{ $t('vendor.title') }}</h6>
                  <div class="product-icon d-flex justify-content-around">
                    <div class="d-inline-block">
                      <span class="title-font mr-3">{{ $t('vendor.name') }}:</span>{{ getDetail.vendor.name }}
                    </div>
                    <div class="d-inline-block">
                      website
                    </div>
                  </div>
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
                  </div>
                </div>
                <div class="border-product text-center">
                  <h6 class="product-title">{{ $t("pingo_product.specification.remaining_time") }}</h6>
                  <client-only>
                    <flip-countdown :deadline="countdown_until(getDetail.until_at)"></flip-countdown>
                  </client-only>
                  <el-progress :text-inside="true" :format="progress_text" :stroke-width="24" :percentage="percentage"
                               :color="colors" class="my-1 "></el-progress>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="tab-product m-0 ">
      <div class="container">
        <div class="row">
          <div class="col-sm-12 col-lg-12">
            <b-tabs card>
              <b-tab :title="$t('product.details')" active>
                <b-card-text>
                  <p v-html="getDetail.description"></p>
                  <p class="line-height-2 my-2">
                    <span v-if="getDetail.brand!=='ー'"><span class="title">ブランド:</span>{{ getDetail.brand }}</span> <br>
                    <span v-if="getDetail.series!=='ー'"><span class="title">シーリズ:</span>{{ getDetail.series }}</span>
                    <br>
                    <span v-if="getDetail.model!=='ー'"><span class="title">モデル:</span>{{ getDetail.model }}</span>
                  </p>
                  <p v-html="getDetail.package" class="mt-3"></p>
                </b-card-text>
              </b-tab>
              <b-tab :title="$t('product.video')" v-if="getDetail.video_url!==''">
                <b-card-text>
                  <div class="mt-3 text-center">
                    <iframe
                      width="560"
                      height="315"
                      :src="getDetail.video_url"
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
                    <div class="row my-2" v-if="comments_meta.total">
                      <div class="col">
                        <div class="dataTables_paginate paging_simple_numbers float-right">
                          <ul class="pagination pagination-rounded">
                            <b-pagination v-model="page"
                                          pills
                                          aria-controls="pingoproduct_table"
                                          :total-rows="comments_meta.total"
                                          :per-page="page_size"
                                          @change="tablePageChange"
                            >
                            </b-pagination>
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
    </section>
    <shareproductModel :openModal="shareproductModal" :productData="getDetail" @closeModal="shareproductModal=false"/>

    <Footer/>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'
import 'vue-inner-image-zoom/lib/vue-inner-image-zoom.css';
import InnerImageZoom from 'vue-inner-image-zoom';
import dayjs from "dayjs";
import {APIServices} from "~/helpers/APIs";
import Swal from "sweetalert2";
import {swalService} from "~/helpers/swal.service";

export default {
  name: "shop_pingoitem_detail",
  middleware: ["isGrouponServiceValid"],
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    Timer: () => import('~/components/widgets/timer'),
    FlipCountdown: () => import("~/pingo_node_modules/vue2-flip-countdown"),
    shareproductModel: () => import('./components/shareproduct'),
    "el-rate": () => import('element-ui/lib/rate'),
    "el-progress": () => import('element-ui/lib/progress'),
    'inner-image-zoom': InnerImageZoom,
  },
  data() {
    return {
      colors: [
        {color: '#f56c6c', percentage: 20},
        {color: '#e6a23c', percentage: 40},
        {color: '#5cb87a', percentage: 60},
        {color: '#1989fa', percentage: 80},
        {color: '#6f7ad3', percentage: 100}
      ],
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
      comments: [],
      comments_meta: {},
      page: 1,
      page_size: 100,
    }
  },
  computed: {
    ...mapGetters({
      gettersGrouponBuyServiceStatus: "system/gettersGrouponBuyServiceStatus",
      isLoggedIn: "authfack/loggedIn",
      ME: "authfack/ME",
      getDetail: "pingoproducts/getterCurrentDetailedProduct"
    }),
    swiper() {
      return this.$refs.mySwiper.swiper
    },
    percentage() {
      if (this.getDetail !== undefined) {
        return Math.round(this.getDetail.currentNum / this.getDetail.targetNum * 100);
      }
      return 0;
    },
    isExpired: function () {
      return dayjs(this.getDetail.until_at).isBefore(Date.now());
    },
    discount_percentage() {
      let percent = Math.round((this.getDetail.price - this.getDetail.discount_price) / this.getDetail.price * 100);
      return `${percent}%`
    },
  },
  watch: {
    gettersGrouponBuyServiceStatus(newVal, oldVal) {
      if (!newVal) {
        return this.$router.push('/')
      }
    }
  },
  mounted() {
    if (!Object.keys(this.getDetail).length || this.getDetail === null || this.getDetail.status !== 'RECRUITING') {
      this.$router.push("/tomobuy")
    } else {
      this.load_product_comments()
    }
  },
  methods: {
    ShowShareQR() {
      this.shareproductModal = true;
    },
    progress_text: function (percentage) {
      return this.getDetail.currentNum + "/" + this.getDetail.targetNum
    },
    timeElapsedHandler: function () {
      this.can_buy = false;
    },
    countdown_until: function (time) {
      var temp_time = time.split('.')[0];
      return temp_time.replace("T", " ");
    },
    increment() {
      this.counter++
    },
    decrement() {
      if (this.counter > 1) this.counter--
    },

    addCartPingoItem() {
      this.$store.commit("pingoproducts/setCart", {product: this.getDetail, quantity: 1})
      this.$router.push("/tomobuy/checkout")
    },
    slideTo(id) {
      this.swiper.slideTo(id, 1000, false)
    },
    tablePageChange(page) {
      this.page = page;
      this.load_product_comments()
    },

    comment_visible(comment) {
      console.log(`approved: ${comment.approved}, comment.user.id: ${comment.user.pk}, this.ME.id:${this.ME.pk}`)
      if (comment.approved === true || comment.user.pk === this.ME.pk) {
        return true
      }
      return false;
    },
    async load_product_comments() {
      let self = this;
      let url = `store/public/comments/list_pingo/?page=${this.page}&page_size=${this.page_size}&item=${this.getDetail.id}&expand=user`
      APIServices.get(url)
        .then(APIServices.handleResponse)
        .then(res => {
          console.log(res)
          self.comments = res.results;
          self.comments_meta = res.meta;
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
          item: this.getDetail.id,
          content: text
        }
        APIServices.post("store/public/comments/create_pingo/", info)
          .then(APIServices.handleResponse)
          .then(res => {
            console.log(res)
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
          console.log(response)
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
  }
}
</script>
<style scoped>
.flip-card {
  font-size: 1.3rem !important;
}

.margin-center {
  margin: 0 auto;
  text-align: center;
}
</style>
