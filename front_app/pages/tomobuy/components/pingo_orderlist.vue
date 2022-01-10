<template>
    <b-card-text>
        <div class="dashboard-right">
            <div class="dashboard">

                <div class="my-3">
                    <a href="javascript:void(0);" class=" btn btn-outline" @click="switch_type('PINGO')">PINGO</a>
                    <a href="javascript:void(0);" class=" btn btn-outline pull-right" @click="switch_type('REGULAR')">REGULAR</a>
                </div>
                <div class="page-title">
                    <h2>PINGO {{$t('menu.orderlist')}}</h2>
                </div>
                <div class="welcome-msg">
                    <p>Hello, MARK JECNO !</p>
                    <p>From your Orders you have the ability to view your all orders and status of order.</p>
                </div>
                <div class="box-account box-info">
                    <div class="box-head">
                        <h2>Order Information</h2>
                    </div>
                    <div>
                        <div class="box">
                            <div class="box-title mb-3">
                                <h3>orders list</h3>
                                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem
                                    Ipsum has been the industry's standard dummy text ever since the 1500s,</p>
                            </div>
                            <!--                            <div class="row mt-2" v-for="order in orderlist">-->
                            <!--                                <div class="col-sm-6">-->
                            <!--                                    <h4>Order no: {{order.id}}</h4>-->

                            <!--                                </div>-->
                            <!--                                <div class="col-sm-6">-->
                            <!--                                    <h6>To: {{order.shippingaddress.name}}</h6>-->
                            <!--                                    <h6>Qty: {{order.Qty}} Total: {{order.Total | currency("¥")}}</h6>-->
                            <!--                                </div>-->
                            <!--                                <hr>-->
                            <!--                            </div>-->
                            <div class="row mt-2">
                                <el-table ref="filterTable" stripe
                                          :data="orderlist.slice((currentPage-1)*pagesize,currentPage*pagesize)"
                                          style="width: 100%">
                                    <el-table-column type="expand">
                                        <template slot-scope="props">
                                            <div class="row">
                                                <div class="col-xs-12 col-md-6">
                                                    <ThumbnailImage :image="props.row.product.thumbimage"
                                                                    :number="props.row.qty"></ThumbnailImage>
                                                </div>
                                                <div class="col-xs-12 col-md-6" style="border-left: 2px solid grey;">
                                                    <div class="d-flex justify-content-around">
                                                        <h4>{{$t('cart_info.total')}}: <span class="cont ml-3">{{props.row.TaxedTotal|currency('¥')}}</span>
                                                        </h4>
                                                        <h4>{{$t('cart_info.quantity')}}: <span class="cont ml-3">{{props.row.qty}}</span>
                                                        </h4>
                                                    </div>

                                                    <h4 class="mt-3">TO: {{props.row.shippingaddress.name}}</h4>
                                                    <p>
                                                        〒{{props.row.shippingaddress.postcode}}
                                                        {{props.row.shippingaddress.state}}{{props.row.shippingaddress.city}}{{props.row.shippingaddress.town}}
                                                        <br>
                                                        {{props.row.shippingaddress.address_1}}{{props.row.shippingaddress.address_2}}

                                                    </p>
                                                    <div class="flex-auto" v-if="!props.row.paid_at">
                                                        <nuxt-link
                                                                :to="{name: 'page-account-PaymentForm', params: {order_id: props.row.id, order_slug: props.row.slug}}"
                                                                class="btn btn-outline">
                                                            {{$t('cart_info.pay')}}
                                                        </nuxt-link>
                                                        <a href="javascript:void(0);"
                                                           @click="removeOrder(props.row.id)" class="btn btn-outline">{{$t('delete')}}</a>

                                                    </div>
                                                </div>
                                            </div>
                                        </template>
                                    </el-table-column>

                                    <el-table-column prop="created_at" label="日付" sortable>
                                        <template slot-scope="scope">
                                            {{scope.row.created_at | short_date}}
                                        </template>
                                    </el-table-column>
                                    <el-table-column prop="price" label="Total">
                                        <template slot-scope="scope">
                                            {{scope.row.TaxedTotal | currency("¥")}}
                                        </template>
                                    </el-table-column>
                                    <el-table-column
                                            prop="paid_at"
                                            label="支払状況">
                                        <template slot-scope="scope">
                                            <el-tag :type="scope.row.paid_at ? 'success' : 'danger'"
                                                    disable-transitions>{{scope.row.paid_at?"支払済":"未払い"}}
                                            </el-tag>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                            <div class="row">
                                <div style="text-align: center;margin-top: 30px;">
                                    <el-pagination
                                            background
                                            layout="prev, next"
                                            :total="total"
                                            :page-size="pagesize"
                                            @current-change="current_change">
                                    </el-pagination>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </b-card-text>
</template>

<script>

    import {mapState} from "vuex"
    import {Table, TableColumn} from 'element-ui'
    import Swal from "sweetalert2"
    import ThumbnailImage from "./thumbimage_single"

    export default {
        data() {
            return {
                order: {},
                showCreditModal: false,
                currentPage: 1,
                pagesize: 10,
                total: 0
            }
        },
        components: {
            Table,
            TableColumn,
            ThumbnailImage
        },
        computed: {
            ...mapState({
                orderlist: state => state.orders.pingo_orderlist
            }),
        },
        methods: {
            switch_type: function (type) {
                this.$emit('switch_type', type)
            },
            current_change: function (currentPage) {
                this.currentPage = currentPage;
            },
            load_order_list: function () {
                this.$store.dispatch('orders/getOrderList');
            },
            filterTag(value, row) {
                return row.is_paid === value;
            },
            showCartModal(order) {
                this.showCreditModal = true;
                this.order = order;
                console.log("showCartModal")
                console.log(this.order)
            },
            closeCreditModal() {
                this.showCreditModal = false;
            },
            removeOrder(order_id) {
                Swal.fire({
                    title: "注文削除",
                    text: "注文を削除してもよろしいでしょうか？",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    cancelButtonText: "キャンセル",
                    confirmButtonText: 'はい、削除します!'
                }).then((result) => {
                    if (result.isConfirmed) {
                        this.$store.dispatch('orders/deletePingoOrder', order_id).then((result) => {
                            if (result) {
                                Swal.fire(
                                    '削除済み!',
                                    '注文を削除いたしました.',
                                    'success'
                                )
                            }
                        })

                    }
                })
            }
        },
        mounted() {
            this.$store.dispatch('orders/getPingoOrderList');
            this.total = this.orderlist.length;
            // this.orderlist = this.$store.state.orders.orderlist;
        }
    }
</script>

<style>
    h4 span.cont {
        float: right;
    }
</style>
