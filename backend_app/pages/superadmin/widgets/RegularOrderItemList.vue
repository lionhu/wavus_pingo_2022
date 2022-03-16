<script>
export default {
  name: "orderitems_list",
  props: ["order"],
  components: {
    "el-table": () => import("element-ui/lib/table"),
    "el-table-column": () => import("element-ui/lib/table-column")
  },
  data() {
    return {};
  },
  methods: {}
};
</script>

<template>
  <div class="mt-2">
    <h4 class="header-title mb-3">注文商品一覧 #{{ order.id }}</h4>
    <div class="row">
      <div class="col-12">
        <div>
          <div class="table-responsive">
            <el-table
              class="table table-centered border table-nowrap mb-lg-0"
              :data="order.order_items"
              style="width: 100%"
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="expand">
                <template slot-scope="props">
                  <div class="row mb-3">
                    <div class="col-lg-6">
                      <h6 class="m-0">商品名：</h6>
                      <div class="card">
                        <div class="card-body">
                          <p class="mb-0">
                            {{ props.row.variation.name }} <br />
                            OrderItem　ID:#{{ props.row.id }} <br />
                            SKU: {{ props.row.variation.sku }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="商品" width="260">
                <template slot-scope="scope">
                  <div class="media align-items-center">
                    <div class="mr-3">
                      <img
                        :src="scope.row.variation.image_url"
                        alt="product-img"
                        height="160"
                      />
                    </div>
                    <div class="media-body">
                      <p class="mb-0">X {{ scope.row.quantity }}</p>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="単価" prop="variation.price">
                <template slot-scope="scope">
                  <span class="d-block ">{{
                    scope.row.variation.price | currency("¥")
                  }}</span>
                  <span class="d-block  text-danger">{{
                    scope.row.variation.purchase_price | currency("¥")
                  }}</span>
                </template>
              </el-table-column>
              <el-table-column label="合計">
                <template slot-scope="scope">
                  <span class="d-block ">{{
                    (scope.row.variation.price * scope.row.quantity)
                      | currency("¥")
                  }}</span>
                  <span class="d-block text-danger">{{
                    (scope.row.variation.purchase_price * scope.row.quantity)
                      | currency("¥")
                  }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
