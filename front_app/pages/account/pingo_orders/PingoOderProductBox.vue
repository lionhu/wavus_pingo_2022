<template>
  <div class="box-border">
    <div class="img-wrapper">
      <div class="lable-block">
        <span class="pingo_label_h1">{{ order.quantity }}</span>
        <b-badge class="pingo_label_v1" :variant="$t(`pingo_order.type.${order.status}.class`)">
          {{$t(`pingo_order.type.${order.status}.text`)}}
        </b-badge>
      </div>
      <div class="front">
        <img
          :src='order.product.thumbimage_url'
          :id="order.product.id"
          class="img-fluid bg-img"
          :alt="order.product.item_name"
          :key="order.product.id"
        />
        <el-rate v-model="order.product.rate" disabled text-color="#ff9900"></el-rate>
      </div>
    </div>
    <div class="product-detail " v-if="isListView">
      <div class="d-flex justify-content-between">
        <div>
          <h6>{{ order.product.item_name }}</h6>
          <h6 class="theme-color">{{ order.price| currency("¥") }} X {{ order.qty}}</h6>
        </div>
        <div>
          <h6><span class="line-title">最終応募数 : </span>{{ order.product.currentNum |currency() }}</h6>
          <h6><span class="line-title">募集目標数 : </span>{{ order.product.targetNum |currency() }}</h6>

          <client-only v-if="order.product.status==='RECRUITING'||order.product.status==='RELEASED'">
            <el-progress :text-inside="true" :format="progress_text"
                         :stroke-width="24" :percentage="percentage(order.product)"
                         :color="colors" class="my-1 "></el-progress>
          </client-only>
          <h6><span>締切日：</span>{{ order.product.until_at | short_date }}</h6>

        </div>
        <div>
          <h6><span>注文日：</span>{{ order.created_at | short_date }}</h6>

        </div>
      </div>
      <b-button variant="outline-primary" v-b-modal:pingo_order_detail_modal size="sm"
                class="inline-block float-left" @click="showOrderDetailModal">注文詳細</b-button>
      <b-button variant="outline-danger" v-b-modal:pingo_order_detail_modal size="sm"
                class="inline-block float-right" @click="$emit('PingoOrderCancel',order.id)">キャンセル</b-button>
    </div>

    <div class="product-detail " v-else>
      <h6>{{ order.product.item_name }}</h6>
      <h6 class="theme-color">
        <span>{{ order.price| currency("¥") }} X {{ order.quantity}}</span>
        <span class="float-right">{{ order.total| currency("¥") }}</span>
      </h6>
      <h6><span>最終応募数 : </span>{{ order.product.currentNum |currency() }}</h6>
      <h6><span>募集目標数 : </span>{{ order.product.targetNum |currency() }}</h6>

      <h6><span>締切日：</span>{{ order.product.until_at | short_date }}</h6>
      <client-only v-if="order.product.status==='RECRUITING'||order.product.status==='RELEASED'">
        <el-progress :text-inside="true" :format="progress_text"
                     :stroke-width="24" :percentage="percentage(order.product)"
                     :color="colors" class="my-1 "></el-progress>
      </client-only>
      <h6><span>注文日：</span>{{ order.created_at | short_date }}</h6>
      <b-button variant="outline-primary" v-b-modal:pingo_order_detail_modal size="sm"
                class="inline-block" @click="showOrderDetailModal">注文詳細</b-button>
      <b-button variant="outline-danger" v-b-modal:pingo_order_detail_modal size="sm"
                class="inline-block float-right" @click="$emit('PingoOrderCancel',order.id)"
                v-if="order.status==='RECRUITING'"
      >キャンセル</b-button>
    </div>
  </div>

</template>

<script>
export default {
  props: ['order', "isListView"],
  components: {
    "el-rate": () => import("element-ui/lib/rate"),
    "el-progress": () => import("element-ui/lib/progress"),
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
      showOrderDetail:false
    }
  },
  methods: {
    showOrderDetailModal(){
      this.$emit("showOrderDetailModal",this.order.id)
    },
    percentage(product) {
      let percent = Math.round(product.currentNum / product.targetNum * 100);
      return percent <= 100 ? percent : 100;
    },
    progress_text: function () {
      return this.order.product.currentNum + "/" + this.order.product.targetNum
    },
  }
}
</script>

<style scoped>
.pingo_label_v1 {
  position: absolute;
  font-size: 14px;
  font-weight: 700;
  color: white;
  text-transform: uppercase;
  -ms-writing-mode: tb-rl;
  writing-mode: vertical-rl;
  transform: rotate(
    0deg
  );
  /*background-color: rgb(17 243 242 /79%);*/
  padding: 5px;
  top: 7px;
  right: 7px;
  letter-spacing: 0.1em;
  z-index: 1;
}

.pingo_label_h1 {
  border-radius: 100%;
  min-height: 48px;
  min-width: 48px;
  background-color: #ff4c3b;
  text-align: center;
  font-size: 14px;
  font-weight: 700;
  position: absolute;
  padding: 12px 6px;
  text-transform: uppercase;
  color: #ffffff;
  top: 7px;
  left: 7px;
  z-index: 1;
}
.box-border {
  border-radius: 5px;
    padding: 5px;
    border: #d0d0d0 solid 1px;
}
</style>
