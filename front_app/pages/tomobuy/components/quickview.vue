<template>
  <div>
    <b-modal
      id="modal-lg"
      size="lg"
      centered
      title="商品購入"
      :hide-footer="true"
      v-if="openModal"
    >
      <div class="row quickview-modal">
        <div class="col-lg-6 col-xs-12">
          <div class="quick-view-img text-center mb-2">
            <img :src="productData.thumbimage_url" class="img-fluid bg-img"/>

          </div>
        </div>
        <div class="col-lg-6 rtl-text">
          <div class="product-right">
            <h2>{{ productData.item_name }}</h2>
            <h6>
              <del>{{ productData.price| currency("¥") }}</del>
              <span class="theme-color">{{ discount_percentage }} off</span></h6>
            <h3 class="theme-color">{{ productData.discount_price| currency("¥") }}</h3>
            <client-only>
              <el-progress :text-inside="true" :format="progress_text" :stroke-width="24" :percentage="percentage"
                           :color="colors" class="my-1 "></el-progress>
            </client-only>
            <div class="border-product">
              <h6 class="product-title">{{ $t('quickview.detail') }}</h6>
              <p v-html="productData.description"></p>
            </div>
          </div>
        </div>
      </div>
    </b-modal>
  </div>
</template>
<script>
import {mapGetters, mapState} from 'vuex'

export default {
  props: ['openModal', 'product_id'],
  components: {
    "el-rate": () => import("element-ui/lib/rate"),
    "el-progress": () => import("element-ui/lib/progress"),
    FlipCountdown: () => import("vue2-flip-countdown"),
  },
  data() {
    return {
      productData: {},

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
      back_server: "system/getterBackServer"
    }),
    discount_percentage() {
      let percent = Math.round((this.productData.price - this.productData.discount_price) / this.productData.price * 100);
      return `${percent}%`
    },
    percentage() {
      let percent = Math.round(this.productData.currentNum / this.productData.targetNum * 100);
      return percent <= 100 ? percent : 100;
    },
  },
  watch: {
    product_id(newVal, oldVal) {
      console.log("watcher newval", newVal)
      this.load_product_details(newVal)
    }
  },
  methods: {
    load_product_details(product_id) {
      let vm = this;
      let options = `${product_id}/?include[]=sliderimages`

      this.$store.dispatch("pingoproducts/load_product", options).then(response => {
        console.log(response)
        vm.productData = response.pingo_item
      })
    },
    countdown_until(until_at) {
      console.log("countdown_until", until_at)
      // var temp_time = until_at.split('.')[0];
      return until_at.replace("T", " ");
    },
    progress_text: function () {
      return this.productData.currentNum + "/" + this.productData.targetNum
    },
    addToCart() {
      this.$store.commit("pingoproducts/setCart", {product: this.productData, quantity: 1})
      this.$router.push("/tomobuy/checkout")
    },
  }
}
</script>

<style>
.line-height-3 {
  line-height: 3rem;
}
</style>
