<template>
  <div>
    <b-modal
      id="pingo_order_detail_modal"
      size="lg"
      centered
      title="トモ買注文詳細情報"
      :hide-footer="true"
      v-if="openModal"
    >
      <div class="row quickview-modal">
        <div class="container-fluid">
          <div class="row">
            <div class="col-lg-6 product-right ">
              <img
                :src="order.product.thumbimage_url"
                :id="order.product.id"
                class="img-fluid bg-img mx-auto"
                :alt="order.product.item_name"
              />
              <div class="border-product mt-3 text-left">
                <h6 class="product-title">イベント情報</h6>
                <p>
                  <span class="line-title-block text-right mr-2">ステータス:</span>
                  <b-badge pill :variant="$t(`pingo_order.type.${order.product.status}.class`)">
                    {{ $t(`pingo_order.type.${order.product.status}.text`) }}
                  </b-badge>
                </p>
                <p><span class="line-title-block text-right mr-2">目標募集数:</span>{{
                    order.product.targetNum|currency("")
                  }}</p>
                <p><span class="line-title-block text-right mr-2">募集結果:</span>{{
                    order.product.currentNum|currency("")
                  }}</p>
                <p><span class="line-title-block text-right mr-2">募集締切日:</span>{{ order.product.until_at|short_date }}
                </p>
                <client-only>
                  <el-progress :text-inside="true" :format="progress_text"
                               :stroke-width="24" :percentage="percentage"
                               :color="colors" class="my-1 "></el-progress>
                </client-only>
              </div>
            </div>
            <div class="col-lg-6">
              <div class="product-right">
                <h2>{{ order.product.item_name }} x{{ order.qty }}</h2>
                <h4 class="theme-color">{{ order.total  | currency("¥") }}</h4>

                <div class="border-product">
                  <h6 class="product-title text-left">支払情報</h6>
                  <p style="font-style:normal;text-align:left;">
                    支払方法: {{ $t(`checkout.payment_method.${order.payment_method}`) }} <br>
                    支払金額: {{ order.total|currency("¥") }}
                  </p>
                </div>
                <div class="border-product">
                  <h6 class="product-title text-left">送付先</h6>
                  <address style="font-style:normal;text-align:left;">
                    {{ order.json_shippingaddress.name }} <br>
                    電話：{{ order.json_shippingaddress.phone }} <br>
                    メール：{{ order.json_shippingaddress.email }} <br>
                    住所：〒{{ order.json_shippingaddress.postcode }}{{
                      order.json_shippingaddress.state
                    }}{{ order.json_shippingaddress.city }}{{ order.json_shippingaddress.town }}<br>
                    {{ order.json_shippingaddress.address_1 }} <br>
                    {{ order.json_shippingaddress.address_2 }}
                  </address>
                </div>
                <div class="border-product" v-if="order.delivered">
                  <h6 class="product-title">配達情報</h6>
                  <address style="font-style:normal;">
                    <p><span class='line-title-block text-right mr-2'>配送業者：</span>{{ order.logistic.company }}</p>
                    <p><span class='line-title-block text-right mr-2'>配達番号：</span>
                      <a :href="order.delivery_info.track_link">
                        {{ order.delivery_info.track_no }}</a>
                    </p>
                    <p><span class='line-title-block text-right mr-2'>配達日：</span>{{ order.delivered_at }}</p>
                  </address>
                </div>
                <div class="border-product">
                  <!--                <div class="border-product" v-if="order.delivered && order.status ==='ESTABLISHED'">-->
                  <div class="d-flex justify-content-between">

                    <a target="_blank" class="btn btn-outline"
                       :href="`https://www.pingo.jp/export_pdf/pingo/${order.slug}/`">
                      {{ $t("orderlist.invoice") }}
                    </a>
                    <b-button variant="outline-danger" class="inline-block float-right" @click="$emit('closeModal')"
                    >閉じる
                    </b-button>

                  </div>
                </div>

                <b-button variant="outline-danger" class="inline-block float-right" @click="$emit('closeModal')"
                >閉じる
                </b-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </b-modal>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'

export default {
  props: ['openModal'],
  data() {
    return {
      colors: [
        {color: '#f56c6c', percentage: 20},
        {color: '#e6a23c', percentage: 40},
        {color: '#5cb87a', percentage: 60},
        {color: '#1989fa', percentage: 80},
        {color: '#6f7ad3', percentage: 100}
      ],
    }
  },
  components: {
    "el-progress": () => import("element-ui/lib/progress"),
  },
  computed: {
    ...mapGetters({
      "order": "orders/getterPingoOrderDetail"
    }),
    percentage() {
      let percent = Math.round(this.order.product.currentNum / this.order.product.targetNum * 100);
      return percent <= 100 ? percent : 100;
    },
  },
  methods: {
    progress_text() {
      return this.order.product.currentNum + "/" + this.order.product.targetNum
    },
  }
}
</script>

<style>
.line-title-block {
  display: inline-block;
  min-width: 100px;
}
</style>
