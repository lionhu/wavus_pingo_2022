<script>
import {mapGetters} from "vuex"
import {swalService} from "~/helpers/swal.service";
import {orderService} from "~/helpers/order.service";

export default {
  name: "orderlist",
  props:["orderitems","orderitems_meta"],
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
  },
  data() {
    return {
      loading: false,
      orderitem_ids: [],
      edit_orderitem: {},
      order_id: 0,
      showmodel_delivery: false,
      showmodel_paysupplier: false,
    };
  },
  computed: {
    ...mapGetters({
      mySupplierInfo: "suppliers/getterSupplier",
    }),
  },
  methods: {
    tablePageChange(page) {
      this.$emit("tablePageChange",page)
    },
    showDeliveryModal(orderitem) {
      this.$emit("showDeliveryModal",orderitem)
    },
    handleSelectionChange(val) {
      let kl = val.map(function (orderitem) {
        return orderitem.id
      });
      this.multipleSelection = kl;
      this.$emit("handleSelectionChange",this.multipleSelection)
    },
    expandRowChange(row, expandedRows) {
      let self = this;
      if (row.status === "NEW") {
        let info = {orderitem_id: row.id, status: "PROCESSING"}
        orderService.updateOrderItemStatus(info).then((res) => {
          console.log("status changed result", res)
          let itemIndex = self.orderitems.findIndex(item => item.id === parseInt(res.orderitem_id))
          if (itemIndex > -1) {
            self.orderitems[itemIndex].status = res.status;
          }
        })
      }
    }
  },
};
</script>
<style>
.font-16 {
  font-size: 1.5rem;
}
</style>
<template>
  <div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
              <div class="row my-2" v-if="orderitems_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="orderitems_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="orderitems_meta.total"
                                    :per-page="orderitems_meta.page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
            <div class="table-responsive mb-0">
              <el-table
                :data="orderitems"
                style="width: 100%"
                @selection-change="handleSelectionChange"
                @expand-change="expandRowChange"
              >
                <el-table-column
                  type="selection"
                  width="55">
                </el-table-column>

                <el-table-column type="expand">
                  <template slot-scope="props">
                    <div class="row">
                      <div class="col-lg-12">
                        <div>
                          <div class="table-responsive">
                            <h5 class="font-15 mb-2">注文詳細
                            <span class="float-right">購入者：{{props.row.user.username}}</span>
                            </h5>
                            <table class="table table-centered border table-nowrap mb-lg-0">
                              <thead class="bg-light">
                              <tr>
                                <th class="text-center">商品</th>
                                <th>単価</th>
                                <th>小計</th>
                              </tr>
                              </thead>
                              <tbody>
                              <tr>
                                <td>
                                  <div class="media align-items-center">
                                    <div class="mx-3">
                                      <img :src="props.row.variation.image_url" alt="product-img" height="60"/>
                                    </div>
                                    <div class="media-body">
                                      <h6 class="m-0">{{ props.row.variation.item.item_name }}</h6>
                                      <p class="mb-0">
                                        {{ props.row.variation.name }} X {{ props.row.quantity }}<br>
                                        (SKU: {{ props.row.variation.sku }})
                                      </p>
                                    </div>
                                  </div>
                                </td>
                                <td>{{ props.row.variation.purchase_price |currency("¥") }}</td>
                                <td>{{ props.row.total_purchase_price  |currency("¥") }}</td>
                              </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="row mb-3">
                      <div class="col-lg-4">
                          <h5 class="font-15 mb-2">送付先</h5>
                          <div class="card p-2 mb-lg-0">
                            <table class="table table-borderless table-sm mb-0">
                              <tbody>
                              <tr>
                                <th colspan="2">
                                  <h5 class="font-15 m-0">{{ props.row.order.json_shippingaddress.name }}</h5>
                                </th>
                              </tr>
                              <tr>
                                <th scope="row">Address:</th>
                                <td>〒{{
                                    props.row.order.json_shippingaddress.postcode
                                  }}{{ props.row.order.json_shippingaddress.state }}
                                  {{ props.row.order.json_shippingaddress.city }}
                                </td>
                              </tr>
                              <tr>
                                <th scope="row"></th>
                                <td>〒{{
                                    props.row.order.json_shippingaddress.town
                                  }}{{ props.row.order.json_shippingaddress.address_1 }}
                                  {{ props.row.order.json_shippingaddress.address_2 }}
                                </td>
                              </tr>
                              <tr>
                                <th scope="row">Phone :</th>
                                <td>{{ props.row.order.json_shippingaddress.phone }}</td>
                              </tr>
                              <tr>
                                <th scope="row">Email :</th>
                                <td>{{ props.row.order.json_shippingaddress.email }}</td>
                              </tr>
                              </tbody>
                            </table>
                          </div>
                      </div>
                      <div class="col-lg-4">
                        <div>
                          <h5 class="font-15 mb-2">配送情報</h5>

                          <div class="card p-2 mb-lg-0" v-if="props.row.delivered">
                            <div class="text-center">
                              <div class="my-2">
                                <i class="mdi mdi-truck-fast h1 text-muted"></i>
                              </div>
                              <h5><b>{{ props.row.logistic ? props.row.logistic.company : "" }}</b></h5>
                              <div class="mt-2 pt-1">
                                <p class="mb-1">
                                  <span class="font-weight-semibold">Track ID :</span>
                                  <a :href="props.row.delivery_info.track_link">{{
                                      props.row.delivery_info.track_no
                                    }}</a>
                                </p>
                              </div>
                            </div>
                          </div>
                          <div class="card p-2 mb-lg-0" v-else>
                            <h5>未発送</h5>
                          </div>
                        </div>
                      </div>
                      <div class="col-lg-4">
                        <h5 class="font-15 mb-2">支払情報</h5>
                        <div class="card p-2 mb-lg-0">
                          <table class="table table-borderless table-sm mb-0">
                            <tbody>
                            <tr>
                              <th scope="row">支払状態:</th>
                              <td>
                                <i
                                  :class="{'ri-checkbox-circle-fill text-success':props.row.paid,'ri-close-circle-fill text-danger':!props.row.paid}"></i>
                              </td>
                            </tr>
                            <tr v-if="props.row.paid">
                              <th scope="row">支払日 :</th>
                              <td>{{ props.row.paid_at }}</td>
                            </tr>
                            <tr v-if="props.row.paid">
                              <th scope="row">詳細:</th>
                              <td>{{ props.row.paid_info }}</td>
                            </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </template>
                </el-table-column>

                <el-table-column label="ID" sortable prop="id">
                  <template slot-scope="scope">
                    #_{{ scope.row.id }} <br>
                    <b-badge variant="primary" class="text-white" pill>{{ scope.row.order.id }}</b-badge>
                  </template>
                </el-table-column>
<!--                <el-table-column-->
<!--                  label="ユーザー"-->
<!--                  sortable-->
<!--                  prop="user.username">-->
<!--                  <template slot-scope="scope">-->
<!--                    {{ scope.row.user.username }}-->
<!--                  </template>-->
<!--                </el-table-column>-->
                <el-table-column
                  label="受注日"
                  sortable>
                  <template slot-scope="scope">
                    {{ scope.row.order.ordered_at|short_date }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="合計"
                  align="right"
                  sortable>
                  <template slot-scope="scope">
                    {{ scope.row.quantity * scope.row.variation.purchase_price | currency("¥") }}
                  </template>
                </el-table-column>

                <el-table-column
                  label="代金支払"
                  width="100"
                >
                  <template slot-scope="scope">
                      <span class="badge " :class="{'badge-soft-danger text-danger':!scope.row.paid,
                            'badge-soft-success text-success':scope.row.paid}">
                        <i class="fe-home font-16"></i>
                      </span>
                  </template>
                </el-table-column>
                <el-table-column label="配送" width="65">
                  <template slot-scope="scope">
                    <a href="javascript:void(0);" v-b-modal.modal-delivery class="card-link text-custom"
                       @click="showDeliveryModal(scope.row)">
                      <span class="badge "
                            :class="{'badge-soft-danger text-danger':!scope.row.delivered,
                            'badge-soft-success text-success':scope.row.delivered}">
                        <i class="fe-truck font-16"></i>
                      </span>
                    </a>
                  </template>
                </el-table-column>
                <el-table-column label="ステータス" sortable prop="status">
                  <template slot-scope="scope">
                    <b-badge variant="danger" class="text-white" pill v-if="scope.row.status==='NEW'">
                      NEW
                    </b-badge>
                    <b-badge variant="warning" class="text-white" pill v-if="scope.row.status==='PROCESSING'">
                      PROCESSING
                    </b-badge>
                    <b-badge variant="primary" class="text-white" pill v-if="scope.row.status==='DELIVERING'">
                      DELIVERING
                    </b-badge>
                    <b-badge variant="success" class="text-white" pill v-if="scope.row.status==='COMPLETED'">
                      COMPLETED
                    </b-badge>
                  </template>
                </el-table-column>
              </el-table>
            </div>
              <div class="row my-2" v-if="orderitems_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="orderitems_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="orderitems_meta.total"
                                    :per-page="orderitems_meta.page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
