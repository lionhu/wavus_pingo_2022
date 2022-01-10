<script>
import Swal from 'sweetalert2'
import {swalService} from "~/helpers/swal.service";

export default {
  name: "orderitems_list",
  props: ["order"],
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
  },
  data() {
    return {
      multipleSelection: []
    };
  },
  computed: {},
  methods: {
    handleSelectionChange(val) {
      let kl = val.map(function (order) {
        return order.id
      });
      this.multipleSelection = kl;
    },
  }

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
              :data="order.orderitems"
              style="width: 100%"
              @selection-change="handleSelectionChange">

<!--              <el-table-column-->
<!--                type="selection"-->
<!--                width="30">-->
<!--              </el-table-column>-->
              <el-table-column type="expand">
                <template slot-scope="props">
                  <div class="row mb-3">
                    <div class="col-lg-6">
                      <h6 class="m-0">商品名：</h6>
                      <div class="card">
                        <div class="card-body">
                          <p class="mb-0">　
                            {{ props.row.variation.name }} <br>
                            OrderItem　ID:#{{ props.row.id }} <br>
                            SKU: {{ props.row.variation.sku }}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div class="col-lg-6">
                      <h6 class="font-15 mb-2">配送情報</h6>
                      <div class="card p-2 mb-lg-0" v-if="props.row.delivered">
                        <div class="text-center">
                          <div class="my-2">
                            <i class="fe-track font-16 text-success"></i>
                          </div>
                          <h5><b>{{ props.row.delivery_info.logistic_name }}</b></h5>
                          <div class="mt-2 pt-1">
                            <p class="mb-1">
                              <span class="font-weight-semibold">追跡番号No: {{props.row.delivery_info.track_no}}</span>
                            </p>
                            <p class="mb-0">
                              <span class="font-weight-semibold">発送日:{{props.row.delivered_at|short_date}}</span>
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-lg-6">
                      <h4 class="font-15 mb-2">支払情報</h4>
                      <div class="card p-2 mb-lg-0" v-if="props.row.paid">
                        <div class="text-center">
                          <h5><b>{{ props.row.paid_at|short_date }}</b></h5>
                          <div class="mt-2 pt-1">
                            <p class="mb-1">
                              <span class="font-weight-semibold">支払方法: {{ props.row.paid_info.method }}</span>
                            </p>
                            <p class="mb-0">
                              <span class="font-weight-semibold">メモ :{{ props.row.paid_info.memo }}</span>
                            </p>
                          </div>
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
                      <img :src="scope.row.variation.image_url" alt="product-img" height="160"/>
                    </div>
                    <div class="media-body">
                      <p class="mb-0">X {{ scope.row.quantity }}</p>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                label="単価"
                width="120"
                prop="variation.price">
                <template slot-scope="scope">
                  <span class="d-block ">{{ scope.row.variation.price|currency("¥") }}</span>
                  <span class="d-block  text-danger">{{
                      scope.row.variation.purchase_price|currency("¥")
                    }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="合計"
                width="120">
                <template slot-scope="scope">
                            <span
                              class="d-block ">{{ scope.row.variation.price * scope.row.quantity|currency("¥") }}</span>
                  <span
                    class="d-block text-danger">{{
                      scope.row.variation.purchase_price * scope.row.quantity|currency("¥")
                    }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="ステータス"
                align="center"
              >
                <template slot-scope="scope">
<!--                  <a href="javascript:void(0);" @click="$emit('updateOrderItemStatus',scope.row.id)">-->
                    <span class="badge" :class="{'badge-soft-danger': scope.row.status === 'PROCESSING',
                                    'badge-soft-success': scope.row.status === 'COMPLETED'}">
                      {{ scope.row.status }}
                    </span>
                    <b-spinner small label="Small Spinner" variant="danger" class="mt-3"
                               v-if="scope.row.status === 'PROCESSING'">
                    </b-spinner>
<!--                  </a>-->
                </template>
              </el-table-column>
              <el-table-column
                label="配送">
                <template slot-scope="scope">
                  <a href="javascript:void(0);" v-b-modal:modal-delivery
                     @click="$emit('showDeliveryModal',{'mode':'single','orderitem':scope.row})">
                              <span class="badge"
                                    :class="{'text-danger': !scope.row.delivered ,
                                    'text-success': scope.row.delivered }">
                                <i class="fe-truck font-16"></i>
                              </span>
                  </a>
                </template>
              </el-table-column>
              <el-table-column
                label="支払">
                <template slot-scope="scope">
                  <a href="javascript:void(0);" v-b-modal:modal-update-supplier-payment
                     @click="$emit('showPaySupplierModal',{'mode':'single','orderitem':scope.row})">
                    <b-badge variant="success" class="text-white" pill v-if="scope.row.paid">Paid</b-badge>
                    <b-badge variant="danger" class="text-white" pill v-else>Unpaid</b-badge>
                  </a>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
