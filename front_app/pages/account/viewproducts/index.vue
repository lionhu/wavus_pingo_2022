<template>
  <div>
    <Header/>
    <Breadcrumbs :title="$t('menu.dashboard')" breadcrumb_type="static"/>

    <section class="section-b-space ratio_asos">
      <div class="collection-wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <DashboardNav active_title="dashboard_menu.viewproducts"/>
            </div>
            <div class="mt-3 col-lg-9">
              <h4>{{ $t("dashboard_menu.viewproducts") }}</h4>
              <div class="collection-product-wrapper" v-if="view_product_histories.length">

                <div class="no-slider row">
                  <div class="product-box" v-for="(history,index) in view_product_histories" :key="index">
                    <sigle_ProductBox
                      :product="history"
                      :index="index"
                      @ShowShareQR="ShowShareQR"
                      @showQuickview="showQuickview"
                    />
                  </div>
                </div>
                <!--                <div class="section-t-space portfolio-section portfolio-padding metro-section port-col">-->
                <!--                  <no-ssr>-->
                <!--                    <div-->
                <!--                      v-masonry-->
                <!--                      transition-duration="3s"-->
                <!--                      item-selector=".item"-->
                <!--                      class="masonry-container isotopeContainer row"-->
                <!--                    >-->
                <!--                      <div-->
                <!--                        v-masonry-tile-->
                <!--                        class="col-xl-4 col-xs-6 col-grid-box isotopeSelector item"-->
                <!--                        :key="index"-->
                <!--                        v-for="(history, index) in view_product_histories"-->
                <!--                      >-->
                <!--                        <div class="product-box ribbon-box">-->
                <!--                          <div class="ribbon-two ribbon-two-danger" v-if="!history.item.is_valid"><span>売切れ</span></div>-->
                <!--                          <div class="img-wrapper" v-if="history.item.is_valid">-->
                <!--                            <div class="front">-->
                <!--                              <a href="javascript:void(0);" @click="redirectToDetailPage(history.item.id)">-->
                <!--                                <nuxt-img-->
                <!--                                  :src="history.item.thumbimage_url"-->
                <!--                                  :id="history.item.id"-->
                <!--                                  class="img-fluid bg-img"-->
                <!--                                  :alt="history.item.item_name"-->
                <!--                                  :key="index"-->
                <!--                                />-->
                <!--                              </a>-->
                <!--                            </div>-->
                <!--                          </div>-->
                <!--                          <div class="img-wrapper" v-else>-->
                <!--                            <div class="front">-->
                <!--                              <nuxt-img-->
                <!--                                :src="history.item.thumbimage_url"-->
                <!--                                :id="history.item.id"-->
                <!--                                class="img-fluid bg-img"-->
                <!--                                :alt="history.item.item_name"-->
                <!--                                :key="index"-->
                <!--                              />-->
                <!--                            </div>-->
                <!--                          </div>-->
                <!--                          <div class="product-detail">-->
                <!--                            <a href="javascript:void(0);" @click="redirectToDetailPage(history.item.id)"-->
                <!--                               v-if="history.item.is_valid">-->
                <!--                              <h6>{{ history.item.item_name }}</h6>-->
                <!--                            </a>-->
                <!--                            <a href="javascript:void(0);" v-else>-->
                <!--                              <h6>{{ history.item.item_name }}</h6>-->
                <!--                            </a>-->
                <!--                          </div>-->
                <!--                        </div>-->
                <!--                      </div>-->
                <!--                    </div>-->
                <!--                  </no-ssr>-->
                <!--                </div>-->
              </div>

              <EmptyInfo messages="閲覧履歴はございません。" buttonText="買い物へ" redirect_url="/" v-else/>

            </div>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
    <quickviewModel :openModal="show_quickview_model" @closeModal="closeQuickviewModel"/>
    <shareproductModel :openModal="show_shareproduct_modal"
                       @closeModal="closeShareQRModel"/>
  </div>
</template>
<script>
import {mapState, mapGetters} from "vuex"
// import {axios} from "~/plugins/axios"
import {APIServices} from "~/helpers/APIs";

export default {
  name: "dashboard",
  middleware: ['authenticated'],
  data() {
    return {
      view_product_histories: [],
      show_shareproduct_modal: false,
      show_quickview_model: false
    };
  },
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    EmptyInfo: () => import('~/components/widgets/EmptyInfo'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    DashboardNav: () => import('~/components/widgets/dashboardnav'),
    sigle_ProductBox: () => import('./components/productbox'),
    quickviewModel: () => import('./components/quickview'),
    shareproductModel: () => import('./components/shareproduct'),
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user,
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

    ShowShareQR(product_id) {
      this.$store.commit("products/setCurrentDetailProductID", product_id)
      this.show_shareproduct_modal = true;
    },
    closeShareQRModel() {
      this.show_shareproduct_modal = false;
    },
    showQuickview(product_id) {
      this.$store.commit("products/setCurrentDetailProductID", product_id)
      this.show_quickview_model = true;
    },
    closeQuickviewModel() {
      this.show_quickview_model = false;
    },
  },
  created() {
    let vm = this;
    let url = `store/public/filter_viewproducts/me/?query=${this.ME.pk}&omit=user`
    console.log(url)
    APIServices.get(url)
      .then(APIServices.handleResponse)
      .then(response => {
        console.log(response)
        vm.view_product_histories = response;
      })
  }
}
</script>
