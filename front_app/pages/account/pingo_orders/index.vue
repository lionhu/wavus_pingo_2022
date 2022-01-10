<template>
  <div>
    <Header/>
    <!--    <Breadcrumbs :title="$t('menu.dashboard')" breadcrumb_type="static"/>-->
    <section class="section-b-space ratio_asos">
      <div class="collection-wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <DashboardNav active_title="dashboard_menu.pingo_orders"/>
            </div>

            <div class="collection-content mt-3 col-lg-9">
              <div class="page-main-content">
                <div class="row my-3">
                  <div class="col text-center">
                    <b-button-group>
                      <b-button :variant="set_button_variant('RECRUITING')" @click="setOrderType('RECRUITING')">
                        {{
                          $t("pingo_order.type.RECRUITING.text")
                        }}
                      </b-button>
                      <b-button :variant="set_button_variant('ESTABLISHED')"
                                @click="setOrderType('ESTABLISHED')">
                        {{ $t("pingo_order.type.ESTABLISHED.text") }}
                      </b-button>
                      <b-button :variant="set_button_variant('RELEASED')" @click="setOrderType('RELEASED')">
                        {{ $t("pingo_order.type.RELEASED.text") }}
                      </b-button>
                      <b-button :variant="set_button_variant('ALL')" @click="setOrderType('ALL')">{{
                          $t("pingo_order.type.ALL.text")
                        }}
                      </b-button>
                    </b-button-group>
                  </div>
                </div>
                <div class="collection-product-wrapper">
                  <div class="row" v-if="orders_meta.total===0">
                    <div class="col-sm-12">
                      <EmptyInfo message="注文情報はございません。" buttonText="買い物へ" redirect_url="/"/>
                    </div>
                  </div>
                  <div class="product-top-filter" v-if="orders_meta.total">
                    <div class="row">
                      <div class="col-12">
                        <div class="product-filter-content">
                          <div class="search-count">
                            <h5>{{ $t(`pingo_order.type.${type_filter}.text`) }} 件数: {{ orders_meta.total }} </h5>
                          </div>
                          <div class="collection-grid-view">
                            <ul>
                              <li>
                                <img
                                  src='/images/icon/2.png'
                                  @click="grid2()"
                                  class="product-2-layout-view"
                                />
                              </li>
                              <li>
                                <img
                                  src='/images/icon/3.png'
                                  @click="grid3()"
                                  class="product-3-layout-view"
                                />
                              </li>
                              <li>
                                <img
                                  src='/images/icon/4.png'
                                  @click="grid4()"
                                  class="product-4-layout-view"
                                />
                              </li>
                              <li>
                                <img
                                  src='/images/icon/6.png'
                                  @click="grid6()"
                                  class="product-6-layout-view"
                                />
                              </li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="product-wrapper-grid" :class="{'list-view':listview == true}">
                    <div class="row my-2" v-if="orders_meta.total">
                      <div class="col">
                        <div class="dataTables_paginate paging_simple_numbers float-right">
                          <ul class="pagination pagination-rounded">
                            <b-pagination v-model="page"
                                          pills
                                          aria-controls="pingoproduct_table"
                                          :total-rows="orders_meta.total"
                                          :per-page="page_size"
                                          @change="tablePageChange"
                            >
                            </b-pagination>
                          </ul>
                        </div>
                      </div>
                    </div>
                    <div class="row">
                      <div class="col-grid-box"
                           :class="{'col-lg-3 col-md-4 col-sm-6':col4 === true, 'col-lg-4 col-sm-6':col3 === true,
                          'col-sm-6':col2 === true, 'col-lg-2 col-md-4 col-sm-6':col6 === true, 'col-lg-12':listview === true}"
                           v-for="order in orders"
                           :key="order.id">
                        <div class="product-box">
                          <PingoOderProductBox :order="order"
                                               @showOrderDetailModal="showOrderDetailModal"
                                               @PingoOrderCancel="PingoOrderCancel"
                                               :isListView="listview"/>
                        </div>
                      </div>
                    </div>
                    <div class="row my-2" v-if="orders_meta.total">
                      <div class="col">
                        <div class="dataTables_paginate paging_simple_numbers float-right">
                          <ul class="pagination pagination-rounded">
                            <b-pagination v-model="page"
                                          pills
                                          aria-controls="pingoproduct_table"
                                          :total-rows="orders_meta.total"
                                          :per-page="page_size"
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
        </div>
      </div>
    </section>
    <Footer/>

    <OrderDetail :openModal="showOrderDetail"
                 @closeModal="showOrderDetail=false"
                 :order_id="show_order_id"/>
  </div>
</template>
<script>
import {mapGetters} from "vuex"
import Swal from "sweetalert2";

export default {
  name: "pingo_orders",
  middleware: ['authenticated'],
  data() {
    return {
      col2: false,
      col3: false,
      col4: true,
      col6: false,
      listview: false,
      page: 1,
      page_size: 60,
      type_filter: "ALL",
      showOrderDetail: false,
      show_order_id: 0
    };
  },
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    EmptyInfo: () => import('~/components/widgets/EmptyInfo'),
    PingoOderProductBox: () => import('./PingoOderProductBox'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    DashboardNav: () => import('~/components/widgets/dashboardnav'),
    "el-pagination": () => import('element-ui/lib/pagination'),
    OrderDetail: () => import("./OrderDetail")
  },
  computed: {
    ...mapGetters({
      orders: "orders/getterPingoOrderList",
      orders_meta: "orders/getterPingoOrderListMeta",
    }),
    list_page_info() {
      let info = `page=${this.page}&page_size=${this.page_size}&expand=product`
      if (this.type_filter !== "ALL") {
        info = `page=${this.page}&page_size=${this.page_size}&expand=product&filter{status}=${this.type_filter}`
      }
      return info
    }
  },
  watch: {
    orders(newVal, oldVal) {
      this.type_filter = "ALL"
    }
  },
  mounted() {
    this.load_me_orders();
    this.type_filter = "ESTABLISHED";
  },
  methods: {
    async load_me_orders() {
      await this.$store.dispatch("orders/getPingoOrderList", {page_info: this.list_page_info})
    },
    tablePageChange(currentPage) {
      this.page = currentPage;
      this.load_me_orders();

    },
    PingoOrderCancel(order_id) {
      let self = this;
      console.log("PingoOrderCancel", order_id)
      Swal.fire({
        title: '注文キャンセル?',
        html: "本当に注文をキャンセルしますか？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、確定!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            console.log("confirm cancel order", confirm)
            return this.$store.dispatch("orders/deletePingoOrder", order_id).then(response => {
              console.log("cancel order", response)
              return {result: true, order_id: response.id, pointbank_balance: response.pointbank_balance};
            }).catch(error => {
              console.log("throw error", error)
              throw new Error("管理者にご連絡ください。")
            })
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.order_id) {
          self.$store.commit("authfack/setPointBalance", result.value.pointbank_balance)
          Swal.fire(
            '成功!',
            '注文をキャンセルしました！',
            'success')
        }
      })
    },
    showOrderDetailModal(order_id) {
      console.log("index showOrderDetailModal", order_id)
      this.$store.dispatch("orders/getPingoOrderDetail", order_id).then(response => {
          this.showOrderDetail = true;
      })
    },
    setOrderType(val) {
      this.type_filter = val;
      this.load_me_orders();
    },
    set_button_variant(button_title) {
      if (this.type_filter === button_title) {
        return "warning"
      }
      return "secondary"
    },
    pageChanged(currentPage) {
      this.page = currentPage;
      this.load_me_orders();
    },
    gridView() {
      this.col4 = true
      this.col2 = false
      this.col3 = false
      this.col6 = false
      this.listview = false
    },
    listView() {
      this.listview = true
      this.col4 = false
      this.col2 = false
      this.col3 = false
      this.col6 = false
    },
    grid2() {
      this.col2 = true
      this.col3 = false
      this.col4 = false
      this.col6 = false
      this.listview = false
    },
    grid3() {
      this.col3 = true
      this.col2 = false
      this.col4 = false
      this.col6 = false
      this.listview = false
    },
    grid4() {
      this.col4 = true
      this.col2 = false
      this.col3 = false
      this.col6 = false
      this.listview = false
    },
    grid6() {
      this.col6 = true
      this.col2 = false
      this.col3 = false
      this.col4 = false
      this.listview = false
    },
  }

}
</script>

