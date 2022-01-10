<script>
import {mapGetters} from "vuex"
import Swal from "sweetalert2"
import {axios} from "~/plugins/axios.js"

export default {
  name: "pingo_order",
  head() {
    return {
      title: `${this.title} | PINGO`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    Switches: () => import('vue-switches'),
    "el-tree": () => import('element-ui/lib/tree'),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-select": () => import('element-ui/lib/select'),
    "el-rate": () => import('element-ui/lib/rate'),
    "el-dialog": () => import('element-ui/lib/dialog'),
    "el-upload": () => import('element-ui/lib/upload'),
    "el-option": () => import('element-ui/lib/option'),
    "el-cascader": () => import('element-ui/lib/cascader'),
    "el-form": () => import('element-ui/lib/form'),
    Category: () => import('../components/CategoryModal'),
    PaymentInfoCard: () => import('../components/PaymentInfoCard'),
    PingoItemInfoCard: () => import('../components/PingoItemInfoCard'),
    DeliveryModal: () => import("~/components/widgets/modal_pingo_delivery"),
    ShippingAddressCard: () => import("~/components/widgets/ShippingAddressCard"),
    DeliveryInfoCard: () => import("~/components/widgets/DeliveryInfoCard"),
  },
  data() {
    return {
      title: "トモ買イベント",
      items: [
        {text: "PinGo"},
        {text: "eCommerce"},
        {text: "トモ買イベント", active: true}
      ],
      multipleSelection: [],
      product: {},
      showmodel_delivery: false,
      orderitem_ids: [],
      edit_orderitem: {},
      orders: [],
      orders_meta: {
        links: {},
        page: 1,
        page_size: 10,
        total: 0
      },
      product_id: 0
    };
  },
  computed: {
    ...mapGetters({
      // product: "pingoproducts/getterCurrentProduct",
      // orders: "pingoproducts/getterCurrentProductOrders",
      // orders_meta: "pingoproducts/getterCurrentProductOrdersMeta",
    }),
    default_options() {
      return `&page=${this.orders_meta.page}&page_size=${this.orders_meta.page_size}&expand=logistic,user`
    }
  },
  methods: {
    async load_product_orders() {
      this.$nuxt.$loading.start();
      let vm = this;
      this.product_id = parseInt(this.$route.params.id);
      if (this.product_id > 0) {
        await this.$store.dispatch("pingoproducts/superadmin_retrieve_product", this.product_id)
          .then(res => {
            console.log("load pingo product", res)
            if (res.id > 0) {
              vm.product = res;
              vm.$store.dispatch("pingoproducts/superadmin_retrieve_product_orders",
                {product_id: vm.product_id, options: vm.default_options})
                .then(response => {
                  vm.orders = response.results;
                  vm.orders_meta = response.meta;
                  this.$nuxt.$loading.finish();
                })
            } else {
              vm.$router.push("/")
            }
          })
      } else {
        this.$router.push("/")
      }
      this.$nuxt.$loading.finish();
    },
    tablePageChange(page) {
      this.orders_meta.page = page;
      let product_id = parseInt(this.$route.params.id);
      this.$store.dispatch("pingoproducts/superadmin_retrieve_product_orders", {
        product_id: product_id, options: this.default_options
      })
    },
    handleSelectionChange(val) {
      let kl = val.map(function (order) {
        return order.id
      });
      this.multipleSelection = kl;
      console.log(this.multipleSelection)
    },
    // rowSelectable(row, index) {
    //   if (row.payment_method === "POINT") {
    //     return true
    //   } else if (row.payment_method === "CARD" && row.payment_status === "APPROVED") {
    //     return true;
    //   }
    //   return false;
    // },
    UpdateOrderItemResult(info) {
      this.ordersReplace(info)
    },
    ordersReplace(info) {
      let orderitem_ids = info.update_info.orderitem_ids
      let update_fields = info.update_info.update_fields
      orderitem_ids.forEach(_id => {
        let itemIndex = this.orders.findIndex(order => order.id === _id);
        if (itemIndex > -1) {
          if (update_fields.includes("delivery")) {
            this.orders[itemIndex].delivered = info.update_info.delivered;
            this.orders[itemIndex].delivered_at = info.update_info.delivered_at;
            this.orders[itemIndex].delivery_info = info.update_info.delivery_info;
          }
        }
      })
      Swal.fire("Updated Successfully!", `items has been updated!`, "success")
    },
    showDeliveryModal(orderitem) {
      if (orderitem.status !== "COMPLETED") {
        this.orderitem_ids = []
        this.edit_orderitem = orderitem;
        this.orderitem_ids.push(orderitem.id)
        this.showmodel_delivery = true
      }
    },
    ReleaseOrders(info) {
      if (info.result_ids.length > 0) {
        this.product.status = "RELEASED"
        Swal.fire('Success', 'Release Orders', 'success')
      }
    },
    EstablishOrders(info) {
      if (info.result_ids.length > 0) {
        this.product.status = "ESTABLISHED"
        Swal.fire('Success', 'Established Orders', 'success')
      }
    },
    DeleteOrders(orderitem_ids) {
      console.log(orderitem_ids)
      orderitem_ids.forEach(_id => {
        let itemIndex = this.orders.findIndex(order => order.id === _id);
        if (itemIndex > -1) {
          this.orders.splice(itemIndex, 1)
        }
      })
      Swal.fire('Success', '', 'success')

    },
    download_orders() {
      axios.$get(`/admin_back/api/pingo_orders/${this.product.id}/download_product_orders/`)
    }
  },
  mounted() {
    this.load_product_orders()
  },
  middleware: ['router-auth', 'router-superadmin'],
}
;
</script>
<style>
.list_title {
  display: inline-block;
  width: 120px;
}
</style>
<template>
  <div>
    <PageHeader :title="title" :items="items"/>

    <div class="row">
      <div class="col-lg-12">
        <PingoItemInfoCard :pingo_product="product"
                           :multipleSelection="multipleSelection"
                           @DeleteOrders="DeleteOrders"
                           @EstablishOrders="EstablishOrders"
                           @ReleaseOrders="ReleaseOrders"
        />
      </div>
    </div>

    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive mb-0">

              <div class="row my-2" v-if="orders_meta.total">
                <div class="col-6">
                  <!--                  <a :href="`/admin_back/download_product_orders/?pk=${product.id}`"-->
                  <!--                     class="btn btn-info waves-effect waves-light">-->
                  <!--                    <span class="btn-label"><i class="ri-download-cloud-2-fill"></i></span>注文リスト-->
                  <!--                  </a>-->
                </div>
                <div class="col-6">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="orders_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="orders_meta.total"
                                    :per-page="orders_meta.page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
              <el-table
                id="pingoorders_table"
                :data="orders"
                @selection-change="handleSelectionChange"
                style="width: 100%">
                <!--                <el-table-column-->
                <!--                  type="selection"-->
                <!--                  :selectable="rowSelectable"-->
                <!--                  width="55"-->
                <!--                  v-if="product.status ==='RECRUITING'"-->
                <!--                >                -->
                <el-table-column
                  type="selection"
                  width="55"
                  v-if="product.status ==='RECRUITING'"
                >
                </el-table-column>
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <div class="row mb-3">
                      <div class="col-lg-4">
                        <ShippingAddressCard :shippingaddress="props.row.json_shippingaddress"/>
                      </div>
                      <div class="col-lg-4">
                        <PaymentInfoCard :payment_info="props.row"/>
                      </div>
                      <div class="col-lg-4">
                        <DeliveryInfoCard :delivery_info="props.row"></DeliveryInfoCard>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  label="会員"
                  sortable
                  prop="user.username">
                </el-table-column>
                <el-table-column
                  label="数量"
                  align="center"
                  sortable
                  width="80"
                  prop="quantity">
                </el-table-column>
                <el-table-column
                  label="合計"
                  sortable
                  prop="total">
                  <template slot-scope="scope">
                    {{ scope.row.total|currency("¥") }}
                  </template>
                </el-table-column>
                <el-table-column
                  sortable
                  align="center"
                  label="支払い">
                  <template slot-scope="scope">
                    <button type="button" class="btn btn-primary btn-sm waves-effect waves-light"
                            v-if="scope.row.payment_method==='POINT'">
                      <span class="btn-label"><i class="ri-coin-fill"></i></span>COMPLETED
                    </button>
                    <button type="button" class="btn  btn-sm waves-effect waves-light"
                            :class="{
                              'btn-warning':scope.row.payment_status==='APPROVED',
                              'btn-success':scope.row.payment_status==='COMPLETED',
                              'btn-secondary':scope.row.payment_status==='RELEASED',}"
                            v-if="scope.row.payment_method==='CARD'">
                      <span class="btn-label"><i class="ri-bank-card-fill "></i></span>
                      {{ scope.row.payment_status }}
                    </button>
                    <button type="button" class="btn btn-danger btn-sm waves-effect waves-light"
                            v-else>
                      <span class="btn-label"><i class="ri-bank-card-fill"></i></span>
                      ERROR...
                    </button>
                  </template>
                </el-table-column>
                <el-table-column
                  sortable
                  text-align="center"
                  label="配送">
                  <template slot-scope="scope">
                    <a href="javascript:void(0);" v-b-modal.modal_pingo_delivery class="card-link text-custom"
                       @click="showDeliveryModal(scope.row)">
                      <b-badge pill variant="success" v-if="scope.row.delivered">
                        <i class=" ri-truck-fill"></i>
                      </b-badge>
                      <b-badge pill variant="secondary" v-else>
                        <i class=" ri-truck-line"></i>
                      </b-badge>
                    </a>
                  </template>
                </el-table-column>
              </el-table>
              <div class="row my-2" v-if="orders_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="orders_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="orders_meta.total"
                                    :per-page="orders_meta.page_size"
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

    <DeliveryModal :openDeliveryModal="showmodel_delivery" :orderitem_ids="orderitem_ids"
                   :orderitem="edit_orderitem" @updateResult="UpdateOrderItemResult"></DeliveryModal>
  </div>
</template>
