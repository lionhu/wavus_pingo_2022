<script>
export default {
  name: "regular_order_summary",
  props: ["order","total_margin"],
  data() {
    return {
    };
  },
  computed: {

  },
  methods: {
  }

};
</script>

<template>
  <div>
    <h4>注文概要</h4>
    <div class="table-responsive">
      <table class="table table-centered border mb-0">
        <thead class="bg-light">
        <tr>
          <th colspan="3">サマリー</th>
        </tr>
        </thead>
        <tbody>
        <tr>
          <th scope="row">売上</th>
          <td class="text-right">
            <span class="d-block ">{{ order.total.total_price|currency("¥") }}</span>
            <div v-if="this.order.point_usage.apply_point">
              <p><i class="ri-bank-card-line text-success"></i>:{{ order.chargeAmount |currency("¥") }}<br>
                <i class="ri-refund-2-fill text-danger"></i>:{{ this.order.point_usage.use_point|currency("¥") }}</p>
            </div>
          </td>
        </tr>
        <tr>
          <th scope="row">仕入</th>
          <td class="text-right">
            <span class="d-block ">-{{ order.total.total_purchase_price|currency("¥") }}</span>
          </td>
        </tr>
        <tr>
          <th scope="row">ポイント付与</th>
          <td class="text-right">
            <span class="d-block ">-{{ total_margin|currency("¥") }}</span>
          </td>
        </tr>
        <tr>
          <th scope="row">Profit</th>
          <td class="bg-danger text-white text-center font-16">
            {{ order.total.profit|currency("¥") }}
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
