<script>
import {mapGetters} from "vuex"
import {swalService} from "~/helpers/swal.service";
import {orderService} from "~/helpers/order.service";

export default {
  name: "supplier_orderlist",
  middleware: ['router-auth', 'router-supplier'],
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
    OrderItems:()=>import("./orderlist")
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
        links:{},
        page:1,
        page_size:100,
        total: 0
      },
      loading: false,
      orderitem_ids: [],
      edit_orderitem: {},
      order_id: 0,
      showmodel_delivery: false,
    };
  },
  computed: {
    ...mapGetters({
      mySupplierInfo: "suppliers/getterSupplier",
    }),
    SupplierName() {
      return this.mySupplierInfo !== null ? this.mySupplierInfo.name : ""
    },
  },
  mounted() {
    if (this.mySupplierInfo.id>0){
      this.order_filter.item__supplier_id=this.mySupplierInfo.id
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
      console.log(this.order_filter)
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
    handleSelectionChange(ids) {
      this.multipleSelection = ids;
    },
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
    <PageHeader :title="title" :items="items"/>
    <h5><b-badge variant="danger" pill>サプライヤー：{{ this.SupplierName }}</b-badge></h5>
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
              <div class="col text-right">

                  <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1"
                            @click="load_orders">
                    <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;Load Data
                  </b-button>
              </div>
            </div>
          </div>
        </div>
        <OrderItems :orderitems="orderitems" :orderitems_meta="orderitems_meta"
                    @tablePageChange="tablePageChange"
                    @showDeliveryModal="showDeliveryModal"
                    @handleSelectionChange="handleSelectionChange"
        />
      </div>
    </div>
    <DeliveryModal :openDeliveryModal="showmodel_delivery" :orderitem_ids="orderitem_ids"
                   :orderitem="edit_orderitem" @updateResult="UpdateOrderItemResult"></DeliveryModal>
  </div>
</template>
