<template>
  <div class="product-box text-center ribbon-box">
    <div class="ribbon-two ribbon-two-danger"><span>{{ discount_percentage }}</span></div>
    <div v-if="!isExpired(product.until_at)" class="box-border">
      <div class="img-wrapper">
        <div class="front">

        <a href="javascript:void(0);" @click="redirectToDetailPage(product.id)">
            <img :src='product.thumbimage_url' :id="product.id" class="img-fluid bg-img"
                 :alt="product.item_name"/>
          </a>
        </div>
        <div class="cart-info cart-wrap" v-if="!isListview">
<!--          <a href="javascript:void(0)" title="Buy" @click="showQuickview(product)" v-b-modal.modal-lg-->
<!--             variant="primary">-->
<!--            <i class="ti-search circle-button" style="color:white!important;"></i>-->
<!--          </a>-->
          <a href="javascript:void(0)" title="Buy" @click="showShareProduct(product)" v-b-modal.modal-share-lg
             variant="primary" v-if="isLoggedIn">
            <i class="ti-share circle-button" style="color:white!important;"></i>
          </a>
        </div>
      </div>
      <div class="product-detail margin-center d-block">

        <a href="javascript:void(0);" @click="redirectToDetailPage(product.id)">
          <el-rate v-model="product.rate" disabled text-color="#ff9900"></el-rate>
          <h6>{{ product.item_name }}</h6>
          <h6><del>{{ product.price| currency("¥") }}</del> <span class="theme-color">{{ discount_percentage }} off</span></h6>
          <h4 class="theme-color">{{ product.discount_price| currency("¥") }}</h4>
          <div v-if="product.point_rule.is_valid" class="my-md-3">

                        <b-button pill block variant="outline-danger">
                          <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                          {{
                            product.point_rule.policies.user_self | currency("")
                          }}
                        </b-button>
          </div>
          <div class="text-center">
            <h6><span class="line-title">EVENT_ID: </span>#{{ product.category }}-{{ product.id }}</h6>
            <h6><span class="line-title">現在応募数: </span>{{ product.currentNum |currency() }}</h6>
            <h6><span class="line-title">募集目標数: </span>{{ product.targetNum |currency() }}</h6>
          </div>

        </a>
      </div>
      <div class="product-detail mt-3 margin-center d-block">
        <client-only>

          <flip-countdown :deadline="countdown_until(product.until_at)"
                          @timeElapsed="timeElapsedHandler(product)"></flip-countdown>
          <el-progress :text-inside="true" :format="progress_text" :stroke-width="24" :percentage="percentage"
                       :color="colors" class="my-1 "></el-progress>
        </client-only>
      </div>
    </div>

    <div class="box-border" v-else>
      <div class="img-wrapper">
        <div class="front">
          <img :src='product.thumbimage_url' :id="product.id" class="img-fluid bg-img"/>
        </div>
      </div>
      <div class="product-detail margin-center d-block">
        <el-rate v-model="product.rate" disabled text-color="#ff9900"></el-rate>
        <h6>{{ product.item_name }}</h6>
          <h6><del>{{ product.price| currency("¥") }}</del> <span>{{ discount_percentage }} off</span></h6>
          <h4 class="theme-color">{{ product.discount_price| currency("¥") }}</h4>
        <div class="text-center">
          <h6><span class="line-title">EVENT_ID : </span>#{{ product.category }}-{{ product.id }}</h6>
          <h6><span class="line-title">最終応募数 : </span>{{ product.currentNum |currency() }}</h6>
          <h6><span class="line-title">募集目標数 : </span>{{ product.targetNum |currency() }}</h6>
        </div>
      </div>
      <div class="product-detail mt-3 margin-center d-block">
        <client-only>
          <el-progress :text-inside="true" :format="progress_text" :stroke-width="24" :percentage="percentage"
                       :color="colors" class="my-1 "></el-progress>
        </client-only>
        <div class="margin-center">
          <b-badge pill :variant="$t(`pingo_product.status.expired.class`)">
            {{$t("pingo_product.status.expired.text")}}
          </b-badge>
          <h6>{{ product.until_at|short_date }}</h6>
        </div>

      </div>
      <div v-if="isListview" class="product-detail d-block margin-center">
        <!--        <div v-for="variant in product.variations">-->
        <!--          <div v-if="variant.variation_type==='PINGO'" class="d-flex justify-content-around mt-3">-->
        <!--            <h6>{{ variant.name }}</h6>-->
        <!--            <h6>{{ variant.price| currency("¥") }}</h6>-->
        <h6>{{ product.price| currency("¥") }}</h6>
        <!--          </div>-->
        <!--        </div>-->
      </div>
    </div>

  </div>

</template>
<script>
import {mapGetters} from 'vuex'
import dayjs from "dayjs";

export default {
  props: ['product', 'index', "isListview"],
  components: {
    "el-rate": ()=>import("element-ui/lib/rate"),
    "el-progress":  ()=>import("element-ui/lib/progress"),
    FlipCountdown:  ()=>import("~/pingo_node_modules/vue2-flip-countdown"),
  },
  head() {
    return {
      title: this.title,
      // script: [
      //   {src: 'https://unpkg.com/element-ui/lib/index.js',},
      // ],
      link: [
        {
          rel: 'stylesheet', type: "text/css",
          href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css',
        },
      ],
    }
  },
  data() {
    return {
      colors: [
        {color: '#03fc40', percentage: 0},
        {color: '#f56c6c', percentage: 20},
        {color: '#e6a23c', percentage: 40},
        {color: '#5cb87a', percentage: 60},
        {color: '#1989fa', percentage: 80},
        {color: '#6f7ad3', percentage: 100}
      ]
    }
  },
  computed: {
    ...mapGetters({
      back_server: 'system/getterBackServer',
      isLoggedIn: "authfack/loggedIn",
    }),
    percentage() {
      let percent = Math.round(this.product.currentNum / this.product.targetNum * 100);
      return percent <= 100 ? percent : 100;
    },
    discount_percentage(){
      let percent = Math.round((this.product.price-this.product.discount_price) / this.product.price * 100);
      return `${percent}%`
    }
  },
  methods: {
    redirectToDetailPage(product_id) {
      let vm=this;
      this.$store.dispatch("pingoproducts/retrieveProductDetail", product_id)
        .then((response) => {
          console.log("redirectToDetailPage",response)
          vm.$router.push("/tomobuy/detail")
      })
    },
    showShareProduct: function () {
      this.$store.commit("pingoproducts/setDetailProduct", this.product)
      this.$emit('ShowShareQR')
    },
    countdown_until: function (until_at) {
      var temp_time = until_at.split('.')[0];
      return temp_time.replace("T", " ");
    },
    isExpired: function (until_at) {
      return dayjs(until_at).isBefore(Date.now());
    },
    progress_text: function () {
      return this.product.currentNum + "/" + this.product.targetNum
    },
    jump_SingleProduct: function (product) {
      this.$store.dispatch('products/set_current_pingo_product', product);
      this.$router.push("/tomobuy/singleproduct")
    }
  }
}
</script>

<style scoped>
.flip-clock .flip-clock__slot {
  font-size: 0.6rem !important;
}

.flip-clock .flip-clock__card {
  font-size: 1rem !important;
}

.margin-center {
  margin: 0 auto;
  text-align: center;
}


.line-title {
  display: inline-block;
  max-width: 100px;
  float: left;
  margin-left: 1rem;
}

.box-border {
  border-radius: 5px;
    padding: 5px;
    border: #d0d0d0 solid 1px;
}
</style>
