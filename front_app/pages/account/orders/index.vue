<template>
  <div>
    <Header/>
    <!--    <Breadcrumbs :title="$t('menu.dashboard')" breadcrumb_type="static"/>-->
    <section class="section-b-space ratio_asos">
      <div class="collection-wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <DashboardNav active_title="dashboard_menu.orders"/>
            </div>
            <div class="collection-content mt-3 col-lg-9">
              <div class="page-main-content">
                <div class="dashboard-right">
                  <div class="dashboard">
                    <div class="page-title">
                      <h2>{{ $t("services.share_sales.title") }}　{{ $t('menu.orderlist') }}</h2>
                    </div>
                    <div class="box-account box-info">
                      <div>
                        <div class="box">
                          <div class="row mt-2">
                            <el-table ref="filterTable" stripe
                                      :data="orderlist"
                                      style="width: 100%"
                                      v-if="orderlist_meta.total"
                            >
                              <el-table-column type="expand">
                                <template slot-scope="props">
                                  <h4>{{ $t("orderlist.order_detail") }}</h4>
                                  <div class="row">
                                    <div class="col-xs-12 col-lg-6">
                                      <ThumbnailImage :item="item"
                                                      :number="item.quantity"
                                                      v-for="item in props.row.orderitems"
                                                      :key="item.variation.id"></ThumbnailImage>
                                    </div>
                                    <div class="col-xs-12 col-lg-6"
                                         style="border-left: 2px solid grey;line-height:1.4rem;">

                                      <div class="d-flex justify-content-between mb-sm-2">
                                        <span class="inline-title-block">{{ $t('cart_info.taxed_total') }}:</span>
                                        <span class="inline-content-block">{{ props.row.Total|currency('¥') }}</span>
                                      </div>

                                      <div class="d-flex justify-content-between mb-sm-2">
                                        <span class="inline-title-block">{{ $t('cart_info.quantity') }}:</span>
                                        <span class="inline-content-block">{{ props.row.Qty }}</span>
                                      </div>
                                      <div class="d-flex justify-content-between mb-sm-2 text-primary"
                                           v-if="props.row.point_usage.use_point>0">
                                        <span class="inline-title-block">{{ $t('cart_info.use_point') }}:</span>
                                        <span class="inline-content-block">
                                            <font-awesome-icon :icon="['fas','donate']"
                                                               class=" mr-2"></font-awesome-icon>
                                            {{ props.row.point_usage.use_point |currency('') }}
                                        </span>
                                      </div>

                                      <div class="d-flex justify-content-between mb-sm-2r"
                                           v-if="props.row.order_bonus.self_order_bonus_valid">
                                        <span class="inline-title-block">{{ $t('cart_info.get_bonus') }}:</span>
                                        <span class="inline-content-block  text-danger">
                                          <font-awesome-icon :icon="['fas','donate']" class=" mr-2"></font-awesome-icon>
                                          {{ props.row.order_bonus.self_order_bonus_point |currency('') }}
                                        </span>
                                      </div>
                                      <div class="d-flex justify-content-between mb-sm-2">
                                        <span class="inline-title-block">{{ $t('cart_info.chargeAmount') }}:</span>
                                        <span class="inline-content-block  theme-color">{{
                                            props.row.chargeAmount|currency('¥')
                                          }}</span>
                                      </div>
                                      <div v-if="props.row.json_shippingaddress!==undefined" class="mb-md-3">
                                        <h4 class="mt-3">
                                          <i class="fa fa-user mr-3"></i>{{ $t('orderlist.TO') }}:{{
                                            props.row.json_shippingaddress.name
                                          }}
                                        </h4>
                                        <address style="line-height:1.4rem;">
                                          <i class="fa fa-map-marker mr-3"></i>〒{{
                                            props.row.json_shippingaddress.postcode
                                          }}
                                          {{ props.row.json_shippingaddress.state }}{{
                                            props.row.json_shippingaddress.city
                                          }}{{ props.row.json_shippingaddress.town }}
                                          <br>
                                          {{
                                            props.row.json_shippingaddress.address_1
                                          }}{{ props.row.json_shippingaddress.address_2 }} <br>
                                          <abbr title="Phone"><i
                                            class="fa fa-phone mr-3">:</i></abbr>{{
                                            props.row.json_shippingaddress.phone
                                          }}<br>
                                          <abbr title="Email"> <i
                                            class="fa fa-envelope-o mr-3">:</i></abbr>{{
                                            props.row.json_shippingaddress.email
                                          }}
                                        </address>
                                      </div>

                                      <div class="flex-auto">
                                        <a href="javascript:void(0);" class="btn btn-outline"
                                           @click="CANCEL_ORDER(props.row)"
                                           v-if="props.row.status==='NEW'">
                                          {{ $t("orderlist.cancel") }}
                                        </a>
                                        <a target="_blank" class="btn btn-outline"
                                           :href="`https://www.pingo.jp/export_pdf/regular/${props.row.slug}/`"
                                           v-if="props.row.status==='COMPLETED'">
                                          {{ $t("orderlist.invoice") }}
                                        </a>
                                        <a class="btn btn-outline" @click="COMPLETE_ORDER(props.row)"
                                           href="javascript:void(0);"
                                           v-if="props.row.status==='DELIVERING'&&props.row.payment_status==='APPROVED'">
                                          受取完了
                                        </a>
                                      </div>
                                    </div>
                                  </div>
                                </template>
                              </el-table-column>
                              <el-table-column prop="ordered_at" label="日付" sortable>
                                <template slot-scope="scope">
                                  {{ scope.row.ordered_at | short_date }}
                                  <span class="badge rounded-pill bg-warning text-dark"
                                        v-if="scope.row.type==='PINGO'">P</span>
                                  <span class="badge rounded-pill bg-success text-white" v-else>R</span>
                                </template>
                              </el-table-column>
                              <el-table-column prop="status" label="ステータス" sortable>
                                <template slot-scope="scope">
                                  <b-badge pill variant="danger" v-if="scope.row.status==='NEW'">新規</b-badge>
                                  <b-badge pill variant="warning" v-if="scope.row.status==='PROCESSING'">処理中</b-badge>
                                  <b-badge pill variant="primary" v-if="scope.row.status==='DELIVERING'">発送中</b-badge>
                                  <b-badge pill variant="success" v-if="scope.row.status==='COMPLETED'">完了</b-badge>
                                </template>
                              </el-table-column>
                              <el-table-column prop="Total" align="right" :label="$t('cart_info.chargeAmount')">
                                <template slot-scope="scope">
                                  {{ scope.row.chargeAmount | currency("¥") }}
                                </template>
                              </el-table-column>
                              <el-table-column
                                prop="is_paid"
                                :label="$t('orderlist.payment_status')"
                                align="center"
                                :filters="[{ text: '支払済', value: true }, { text: '未払い', value: false }]"
                                :filter-method="filterTag"
                                filter-placement="bottom-end">
                                <template slot-scope="scope">
                                  <div>
                                    <el-tag type="danger" disable-transitions v-if="!scope.row.is_paid">支払い</el-tag>
                                    <el-tag type="success" disable-transitions v-else>支払済</el-tag>
                                  </div>
                                </template>
                              </el-table-column>
                            </el-table>
                            <div class="col" v-else>
                              <EmptyInfo message="注文情報はございません。" buttonText="買い物へ" redirect_url="/"/>
                            </div>
                          </div>

                          <div class="row my-2" v-if="orderlist_meta!==undefined&&orderlist_meta.total">
                            <div class="col">
                              <div class="dataTables_paginate paging_simple_numbers float-right">
                                <ul class="pagination pagination-rounded">
                                  <b-pagination v-model="page"
                                                pills
                                                aria-controls="pingoproduct_table"
                                                :total-rows="orderlist_meta.total"
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
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<script>
import {mapState} from "vuex"
import Swal from "sweetalert2"

export default {
  name: "pingo_orders",
  middleware: ['authenticated'],
  data() {
    return {
      page: 1,
      page_size: 10,
    };
  },
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    EmptyInfo: () => import('~/components/widgets/EmptyInfo'),
    DashboardNav: () => import('~/components/widgets/dashboardnav'),
    ThumbnailImage: () => import( "~/components/widgets/thumbimage_number"),

  },
  computed: {
    ...mapState({
      orderlist: state => state.orders.orderlist,
      orderlist_meta: state => state.orders.orderlist_meta,
      ME: state => state.authfack.ME
    }),
    options(){
      // return `me/?page=${this.page}&page_size=${this.page_size}`;
      return `me/?page=${this.page}&page_size=${this.page_size}&expand=orderitems`;
    }
  },
  watch: {
    orderlist_meta(newVal, oldVal) {
      if (newVal !== undefined) {
        this.page = newVal.page;
        this.page_size = newVal.page_size;
        this.total = newVal.total;
      }
    }
  },
  mounted() {
    this.$store.dispatch('orders/getOrderList', this.options);
  },
  methods: {
    tablePageChange(currentPage) {
      this.page = currentPage;
      this.$store.dispatch('orders/getOrderList', this.options);

    },
    CANCEL_ORDER(order) {
      let self = this;
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
            return this.$store.dispatch("orders/deleteOrder", order.id).then((res) => {
              return {result: true, order_id: res.id, pointbank_balance: res.pointbank_balance};
            }).catch(error => {
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


      // Swal.fire({
      //   title: 'ポイント確定?',
      //   html: "商品が無事に届きましたか?",
      //   icon: 'warning',
      //   showCancelButton: true,
      //   confirmButtonColor: '#3085d6',
      //   cancelButtonColor: '#d33',
      //   confirmButtonText: 'はい、確定!'
      // }).then((result) => {
      //   if (result.isConfirmed) {
      //     this.$store.dispatch("orders/completeOrder", order.id).then((res) => {
      //       let order_id = parseInt(res.order_id)
      //       if (order_id) {
      //         Swal.fire(
      //           '成功!',
      //           'ポイントを確定させていただきました！',
      //           'success')
      //       }
      //     })
      //   }
      // })
    },
    COMPLETE_ORDER(order) {
      let self = this;
      Swal.fire({
        title: 'ポイント確定?',
        html: "商品が無事に届きましたか?<br>　確定したら、返品やキャンセルができなくなりますので、ご了承ください。",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、確定!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            return this.$store.dispatch("orders/completeOrder", order.id).then((res) => {
              return {result: true, order_id: res.order_id, point_balance: res.pointbank_balance};
            }).catch(error => {
              throw new Error("管理者にご連絡ください。")
            })
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.order_id) {
          self.$store.commit("authfack/update_pointbank_balance", result.value.point_balance)
          Swal.fire(
            '成功!',
            'ポイントを確定させていただきました！',
            'success')
        }
      })


      // Swal.fire({
      //   title: 'ポイント確定?',
      //   html: "商品が無事に届きましたか?",
      //   icon: 'warning',
      //   showCancelButton: true,
      //   confirmButtonColor: '#3085d6',
      //   cancelButtonColor: '#d33',
      //   confirmButtonText: 'はい、確定!'
      // }).then((result) => {
      //   if (result.isConfirmed) {
      //     this.$store.dispatch("orders/completeOrder", order.id).then((res) => {
      //       let order_id = parseInt(res.order_id)
      //       if (order_id) {
      //         Swal.fire(
      //           '成功!',
      //           'ポイントを確定させていただきました！',
      //           'success')
      //       }
      //     })
      //   }
      // })
    },
    switch_type: function (type) {
      this.$emit('switch_type', type)
    },
    filterTag(value, row) {
      return row.is_paid === value;
    },
    // isOrderDelivered(order) {
    //   var result = true;
    //   if (order.orderitems && order.orderitems.length) {
    //     for (let item of order.orderitems) {
    //       if (!item.delivered) {
    //         result = false;
    //         break;
    //       }
    //     }
    //   }
    //   return result;
    // },
    // showCartModal(order) {
    //   this.showCreditModal = true;
    //   this.order = order;
    // },
    // closeCreditModal() {
    //   this.showCreditModal = false;
    // },
    // ShowModalPayment(order) {
    //   this.showPaymentModal = true;
    //   this.order = order;
    // },
    // closeModalPayment() {
    //   this.showPaymentModal = false;
    //   this.order = {};
    // },
    // removeOrder(order_id) {
    //   Swal.fire({
    //     title: "注文削除",
    //     text: "注文を削除してもよろしいでしょうか？",
    //     icon: 'warning',
    //     showCancelButton: true,
    //     confirmButtonColor: '#3085d6',
    //     cancelButtonColor: '#d33',
    //     cancelButtonText: "キャンセル",
    //     confirmButtonText: 'はい、削除します!'
    //   }).then((result) => {
    //     if (result.isConfirmed) {
    //       this.$store.dispatch('orders/deleteOrder', order_id).then((result) => {
    //         if (result) {
    //           Swal.fire(
    //             '削除済み!',
    //             '注文を削除いたしました.',
    //             'success'
    //           )
    //         }
    //       })
    //
    //     }
    //   })
    // }
  }

}
</script>
