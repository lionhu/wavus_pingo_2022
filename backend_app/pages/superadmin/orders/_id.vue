<script>
import Swal from 'sweetalert2'
import {swalService} from "~/helpers/swal.service";
import {orderService} from "~/helpers/order.service"
import {marginService} from "@/helpers/margin.service";

export default {
  name: "order_detail",
  head() {
    return {
      title: `${this.title} | Pingo - Order`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'},
      ]
    };
  },
  components: {
    DeliveryModal: () => import("~/components/widgets/modal_delivery"),
    modalUpdateSupplierPayment: () => import("../components/modalUpdateSupplierPayment"),
    MarginBoard: () => import("../widgets/MarginBoard"),
    RegularOrderSummary: () => import("../widgets/RegularOrderSummary"),
    RegularOrderItemList: () => import("../widgets/RegularOrderItemList"),
    ShippingAddress: () => import("../widgets/ShippingAddress"),
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
  },
  async asyncData({params}) {
    let order_id = parseInt(params.id);

    if (order_id) {
      let options = `${order_id}/?expand=orderitems,user`
      let orderDetail = await orderService.get_list(options).then((response) => {
        return response
      }).catch((error) => {
        console.log(error)
      })
      let margins = await marginService.load_list(`?expand=user&filter{from_orderID}=${order_id}`)
        .then((response) => {
          return response.results
        })
      return {order: orderDetail, margins: margins}
    }
    window.location.href = "/superadmin/ecommerce/orders"
  },
  data() {
    return {
      title: "Order Detail",
      items: [
        {text: "WAVUS"},
        {text: "eCommerce"},
        {text: "Order Detail", active: true}
      ],
      showmodel_delivery: false,
      showmodel_paysupplier: false,
      edit_orderitem: {},
      multipleSelection: []
    };
  },
  middleware: ['router-auth', 'router-superadmin'],
  computed: {
    backend_server() {
      return this.$store.state.system.backend_server
    },
    card_payment() {
      return JSON.parse(this.order.payment_info)
    },
    total_margin() {
      return this.margins.reduce((prev, current) => prev + current.amount, 0)
    },
  },
  methods: {
    marginRemoved(margin_id) {
      let self = this;
      let index = self.margins.findIndex(margin => margin.id === margin_id);
      if (index > -1) {
        self.margins.splice(index, 1)
        swalService.showToast("success", `#${margin_id}削除されました！`)
      }
    },
    marginUpdated(new_margin) {
      let self = this;
      let marginIndex = self.margins.findIndex(margin => margin.id === new_margin.id)
      if (marginIndex > -1) {
        self.margins.splice(marginIndex, 1, new_margin)
        swalService.showToast("success", "更新されました！")
      }
    },
    async updateOrderItemStatus(orderitem_id) {
      let self = this;
      const {value: status} = await Swal.fire({
        title: 'Select Status',
        input: 'select',
        inputOptions: {
          'NEW': 'NEW',
          'COMPLETED': 'COMPLETED'
        },
        inputPlaceholder: 'Select a status',
        showCancelButton: true,
      })

      if (status) {
        orderService.updateOrderItemStatus({orderitem_id: orderitem_id, status: status}).then((res) => {
          console.log("update item status", res)
          if (parseInt(res.orderitem_id)) {
            let orderitemIndex = self.order.orderitems.findIndex(item => item.id === orderitem_id)
            if (orderitemIndex > -1) {
              self.order.orderitems[orderitemIndex].status = res.status
            }
            swalService.showModal(`Item Status Update! `, `orderitem #${orderitem_id}  status: ${status} updated!`, "success")
          }
        })
      }
    },
    showDeliveryModal({mode, orderitem}) {
      console.log(mode, orderitem)
      if (mode === "single") {
        this.multipleSelection = [];
        this.edit_orderitem = orderitem;
        this.multipleSelection.push(orderitem.id)
      } else {
        this.edit_orderitem = null
      }
      this.showmodel_delivery = true
    },
    UpdateOrderItem(response) {
      console.log("UpdateOrderItem", response)

      if (response.result) {
        let newItem = response.orderitems[0];
        let itemIndex = this.order.orderitems.findIndex(item => item.id == newItem.id)
        if (itemIndex > -1) {
          this.order.orderitems.splice(itemIndex, 1, newItem)
          swalService.showToast("success", `Item #${newItem.id} delivery info has beedn updated!`)
        }
      }
      // this.order=result.order
    },
    showPaySupplierModal({mode, orderitem}) {
      console.log(mode, orderitem)
      if (mode === "single") {
        this.multipleSelection = [];
        this.edit_orderitem = orderitem;
        this.multipleSelection.push(orderitem.id)
      } else {
        this.edit_orderitem = null;
      }
      this.showmodel_paysupplier = true
    },
    UpdateOrderItemResult(info) {
      let self = this;
      console.log("info", info)
      let new_orderitems = info.updated_orderitems;
      if (info.result) {
        new_orderitems.forEach(newitem => {
          let itemIndex = self.order.orderitems.findIndex(item => item.id === newitem.id)
          if (itemIndex > -1) {
            self.order.orderitems[itemIndex].delivered = newitem.delivered;
            self.order.orderitems[itemIndex].delivered_at = newitem.delivered_at;
            self.order.orderitems[itemIndex].delivery_info = newitem.delivery_info;

            self.order.orderitems[itemIndex].paid = newitem.paid;
            self.order.orderitems[itemIndex].paid_at = newitem.paid_at;
            self.order.orderitems[itemIndex].paid_info = newitem.paid_info;
          }
        })
        swalService.showModal("Updated Successfully!", "Refresh to view", "success")
      }
    }
  }

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
      <div class="col-lg-12">
        <div class="card">
          <div class="card-header border-bottom bg-transparent">
            <h5 class="header-title mb-0">Order #{{ order.id }}
              <span class="ml-md-3 badge"
                    :class="{'badge-soft-danger': order.status === 'NEW',
                          'badge-soft-success': order.status === 'COMPLETED'}">
                      {{ order.status }}
            </span>
            </h5>
          </div>
          <div class="card-body">
            <div>
              <h5 v-if="order.message!==''">Message from Customer: </h5>
              <b-alert show dismissible class="bg-danger text-white border-0 mb-2" v-if="order.message!==''">
                {{ order.message }}
              </b-alert>
              <div class="row">
                <div class="col-lg-3 col-sm-6">
                  <div class="media mb-2">
                    <div class="mr-2 align-self-center">
                      <i class="ri-hashtag h2 m-0 text-muted"></i>
                    </div>
                    <div class="media-body">
                      <p class="mb-1">注文番号No.</p>
                      <h5 class="mt-0">
                        #{{ order.id }}
                      </h5>
                    </div>
                  </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                  <div class="media mb-2">
                    <div class="mr-2 align-self-center">
                      <i class="ri-user-2-line h2 m-0 text-muted"></i>
                    </div>
                    <div class="media-body">
                      <p class="mb-1">ユーザー</p>
                      <h5 class="mt-0">
                        {{ order.user.username }}
                      </h5>
                    </div>
                  </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                  <div class="media mb-2">
                    <div class="mr-2 align-self-center">
                      <i class="ri-calendar-event-line h2 m-0 text-muted"></i>
                    </div>
                    <div class="media-body">
                      <p class="mb-1">日付</p>
                      <h5 class="mt-0">
                        {{ order.ordered_at |short_date }} <small
                        class="text-muted">{{ order.ordered_at|short_time }}</small>
                      </h5>
                    </div>
                  </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                  <div class="media mb-2">
                    <div class="mr-2 align-self-center">
                      <i class="fe-git-merge h2 m-0 text-muted"></i>
                    </div>
                    <div class="media-body">
                      <p class="mb-1">ポイント付与</p>
                      <h5 class="mt-0">
                        {{ total_margin|currency("¥") }}
                      </h5>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <RegularOrderItemList :order="order"
                                  @updateOrderItemStatus="updateOrderItemStatus"
                                  @showDeliveryModal="showDeliveryModal"
                                  @showPaySupplierModal="showPaySupplierModal"
            />

          </div>
        </div>
        <div class="row mb-3">

          <div class="col-lg-8">
            <MarginBoard :margins="margins"
                         @marginRemoved="marginRemoved"
                         @marginUpdated="marginUpdated"
            />
          </div>
          <div class="col-lg-4">
            <RegularOrderSummary :order="order" :total_margin="total_margin"/>
          </div>

        </div>
        <div class="row mb-3">
          <div class="col-6">
            <ShippingAddress :shippingaddress="order.json_shippingaddress"/>
          </div>
          <div class="col-6">
            <div>
              <h4 class="font-15 mb-2">クレジットカード決済情報</h4>

              <div class="card p-2 mb-lg-0">
                {{ order.payment_info }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <DeliveryModal :openDeliveryModal="showmodel_delivery" :orderitem_ids="multipleSelection"
                   :orderitem="edit_orderitem" @updateResult="UpdateOrderItemResult"></DeliveryModal>

    <modalUpdateSupplierPayment :showModal="showmodel_paysupplier" :orderitem_ids="multipleSelection"
                                :orderitem="edit_orderitem"
                                @updateResult="UpdateOrderItemResult"></modalUpdateSupplierPayment>
  </div>
</template>
