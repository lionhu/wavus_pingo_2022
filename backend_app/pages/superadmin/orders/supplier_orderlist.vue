<script>
import {mapGetters} from "vuex"
import {swalService} from "~/helpers/swal.service";
import {orderService} from "~/helpers/order.service";

export default {
  name: "supplier_orderlist",
  head() {
    return {
      title: `${this.title} | WAVUS, PINGO`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    "el-select": () => import('element-ui/lib/select'),
    "el-option": () => import('element-ui/lib/option'),
    DeliveryModal: () => import("~/components/widgets/modal_delivery"),
    PaySupplierModal: () => import("../components/modalUpdateSupplierPayment"),
  },
  data() {
    return {
      title: "サプライヤー注文",
      items: [
        {text: "PINGO"},
        {text: "eCommerce"},
        {text: "サプライヤー注文", active: true}
      ],
      status_options: [
        {label: "すべて", value: "ALL"},
        {label: "NEW", value: "NEW"},
        {label: "PROCESSING", value: "PROCESSING"},
        {label: "DELIVERING", value: "DELIVERING"},
        {label: "COMPLETED", value: "COMPLETED"}
      ],
      order_filter: {
        order__ordered_at__gte: this.week_before(),
        order__ordered_at__lte: new Date().toISOString(),
        status: "NEW",
        item__supplier_id: 0
      },
      isLoading: false,
      multipleSelection: [],
      orderitems: [],
      orderitems_meta: {
        // links:{},
        // page:1,
        // page_size:10,
        total: 0
      },
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
      SupplierList: "suppliers/getterSupplierList",
    }),
    supplier_options() {
      if (this.SupplierList.length) {
        let supplier_select_options = this.SupplierList.map(supplier => {
          return {label: supplier.name, value: supplier.id}
        })
        return supplier_select_options;
      }
      return []
    }
  },
  methods: {
    tablePageChange(page) {
      this.orderitems_meta.page = page;
      this.load_orders()
    },
    week_before() {
      let dt = new Date();
      return new Date(dt.setDate(dt.getDate() - 7)).toISOString();
    },
    change_status(status) {
      this.order_filter.status = status;
    },
    async load_orders() {
      let self = this;
      this.isLoading = true;
      console.log(this.isLoading )
      let options = `?page_size=${this.orderitems_meta.page_size}&page=${this.orderitems_meta.page}&expand=variation,order,item,user,logistic`
      if (this.order_filter.status === "ALL") {
        delete this.order_filter.status
      }
      if (this.order_filter.item__supplier_id === 0) {
        delete this.order_filter.item__supplier_id
      }
      await orderService.getSuperadminFilteredOrderitemList({
        options: options,
        data: this.order_filter
      }).then(response => {
          console.log(response)
          self.orderitems = response.results;
          self.orderitems_meta.total = response.results.length;
        })

      this.isLoading = false;
      console.log(this.isLoading )
    },
    showDeliveryModal(orderitem) {
      this.orderitem_ids = []
      this.edit_orderitem = null;
      this.showmodel_delivery = false;
      if (orderitem.status !== "COMPLETED") {
        this.orderitem_ids = []
        this.edit_orderitem = orderitem;
        this.orderitem_ids.push(orderitem.id)
        this.showmodel_delivery = !this.showmodel_delivery
      }
    },
    showPaySupplierModal(orderitem) {
      this.orderitem_ids = []
      this.edit_orderitem = orderitem;
      this.orderitem_ids.push(orderitem.id)
      this.showmodel_paysupplier = true
    },
    batch_updatePaySupplierInfo() {
      this.orderitem_ids = this.multipleSelection
      this.edit_orderitem = null;
      this.showmodel_paysupplier = !this.showmodel_paysupplier
    },
    batch_updateDeliveryInfo() {
      let self = this;
      this.orderitem_ids = [];
      this.multipleSelection.forEach(order_id => {
        let itemIndex = self.orderitems.findIndex(item => item.id === order_id)
        if (itemIndex > -1) {
          if (self.orderitems[itemIndex].status !== "COMPLETED") {
            self.orderitem_ids.push(order_id)
          }
        }
      })
      // this.orderitem_ids = this.multipleSelection
      console.log(this.orderitem_ids)
      this.edit_orderitem = null;
      this.showmodel_delivery = true
    },
    UpdateOrderItemResult(info) {
      console.log("result", info)
      if (info.result) {
        info.updated_orderitems.forEach(neworderItem => {
          let itemIndex = this.orderitems.findIndex(item => item.id === neworderItem.id);
          if (itemIndex > -1) {

            if (info.update_fields.includes("delivery_info")) {
              this.orderitems[itemIndex].delivered = neworderItem.delivered;
              this.orderitems[itemIndex].logistic = neworderItem.logistic;
              this.orderitems[itemIndex].delivered_at = neworderItem.delivered_at;
              this.orderitems[itemIndex].delivery_info = neworderItem.delivery_info;
            }

            if (info.update_fields.includes("payment_supplier")) {
              this.orderitems[itemIndex].paid = neworderItem.paid;
              this.orderitems[itemIndex].paid_at = neworderItem.paid_at;
              this.orderitems[itemIndex].paid_info = neworderItem.paid_info;
            }
            this.orderitems[itemIndex].status = neworderItem.status;
          }
          swalService.showModal("Updated Successfully!", `items has been updated!`, "success")
        })
      }
    },
    UpdateOrderItems(res) {
      let itemIndex = -1;
      res.orderitems.forEach(_orderitem => {
        itemIndex = this.orderitems.findIndex(item => item.id === _orderitem.id)
        if (itemIndex > -1) {
          console.log(`orderitem ${_orderitem.id}, index: ${itemIndex}`)
          this.orderitems.splice(itemIndex, 1, _orderitem)
        }
      })
    },
    handleSelectionChange(val) {
      let kl = val.map(function (orderitem) {
        return orderitem.id
      });
      this.multipleSelection = kl;
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
  middleware: ['router-auth', 'router-superadmin'],
};
</script>
<style>
.font-16 {
  font-size: 1.5rem;
}
</style>
<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-sm-6">
                <b-dropdown variant="primary" v-model="order_filter.status">
                  <template v-slot:button-content>
                    Status: {{ order_filter.status }}
                    <i class="mdi mdi-chevron-down"></i>
                  </template>
                  <b-dropdown-item v-for="item in status_options" :key="item.value" @click="change_status(item.value)">
                    {{
                      item.label
                    }}
                  </b-dropdown-item>
                </b-dropdown>
              </div>
              <div class="col-sm-6 text-right">
                <b-dropdown variant="warning">
                  <template v-slot:button-content>
                    一括処理
                  </template>
                  <b-dropdown-item>
                    <a href="javascript:void(0)" v-b-modal.modal-delivery @click="batch_updateDeliveryInfo">配送処理</a>
                  </b-dropdown-item>
                  <b-dropdown-item>
                    <a href="javascript:void(0)" v-b-modal.modal-update-supplier-payment
                       @click="batch_updatePaySupplierInfo">支払処理</a>
                  </b-dropdown-item>
                </b-dropdown>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-md-6">
                <div class="form-group">
                  <label id="fromDate_picker_label">
                    From:
                    <span class="text-danger">*</span>
                  </label>
                  <el-date-picker
                    id="fromDate_picker"
                    v-model="order_filter.order__ordered_at__gte"
                    align="right"
                    type="date"
                    placeholder="開始日選択">
                  </el-date-picker>
                </div>
              </div>
              <div class="col-md-6 text-right">
                <div class="form-group">
                  <label id="toDate_picker_label">
                    TO:
                    <span class="text-danger">*</span>
                  </label>
                  <el-date-picker
                    id="toDate_picker"
                    v-model="order_filter.order__ordered_at__lte"
                    align="right"
                    type="date"
                    placeholder="開始日選択">
                  </el-date-picker>
                </div>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-sm-6">
                <label>サプライヤー選択：</label>
                <el-select id="supplier_selector" v-model="order_filter.item__supplier_id" placeholder="请选择">
                  <el-option
                    v-for="supplier in supplier_options"
                    :key="supplier.value"
                    :label="supplier.label"
                    :value="supplier.value">
                  </el-option>
                </el-select>
              </div>
              <div class="col-6 text-right">

                  <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1"
                            @click="load_orders">
                    <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;Load Data
                  </b-button>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
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
                            <h5 class="font-15 mb-2">注文詳細</h5>
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
                        <div>
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

                <el-table-column
                  label="supplier"
                  sortable
                  prop="item.supplier.name" v-if="order_filter.item__supplier_id===undefined">
                  <template slot-scope="scope">
                    {{ scope.row.item.supplier.name }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="ユーザー"
                  sortable
                  prop="user.username">
                  <template slot-scope="scope">
                    {{ scope.row.user.username }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="Date"
                  sortable>
                  <template slot-scope="scope">
                    {{ scope.row.order.ordered_at|short_date }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="Total"
                  align="right"
                  sortable>
                  <template slot-scope="scope">
                    {{ scope.row.quantity * scope.row.variation.purchase_price | currency("¥") }}
                  </template>
                </el-table-column>

                <el-table-column
                  label="Paid"
                  width="65"
                >
                  <template slot-scope="scope">
                    <a href="javascript:void(0);" v-b-modal:modal-update-supplier-payment
                       @click="showPaySupplierModal(scope.row)">
                      <span class="badge " :class="{'badge-soft-danger text-danger':!scope.row.paid,
                            'badge-soft-success text-success':scope.row.paid}">
                        <i class="fe-home font-16"></i>
                      </span>
                    </a>
                  </template>
                </el-table-column>
                <el-table-column label="Deli" width="65">
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
                <el-table-column label="Status" sortable prop="status">
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
          </div>
        </div>
      </div>
    </div>
    <DeliveryModal :openDeliveryModal="showmodel_delivery" :orderitem_ids="orderitem_ids"
                   :orderitem="edit_orderitem" @updateResult="UpdateOrderItemResult"></DeliveryModal>
    <PaySupplierModal :showModal="showmodel_paysupplier" :orderitem_ids="orderitem_ids"
                      :orderitem="edit_orderitem" @updateResult="UpdateOrderItemResult"></PaySupplierModal>
  </div>
</template>
