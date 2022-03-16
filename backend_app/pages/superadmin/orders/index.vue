<script>
import Swal from 'sweetalert2'
import { orderService } from '~/helpers/order.service'
import { Functions } from '~/helpers/functions'
import { swalService } from '~/helpers/swal.service'

export default {
    name: 'order_detail',
    head() {
        return {
            title: `${this.title} | WAVUS, PINGO`,
            script: [{ src: 'https://unpkg.com/element-ui/lib/index.js' }],
            link: [
                {
                    rel: 'stylesheet',
                    href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css',
                },
            ],
        }
    },
    components: {
        'el-table': () => import('element-ui/lib/table'),
        'el-table-column': () => import('element-ui/lib/table-column'),
        'el-date-picker': () => import('element-ui/lib/date-picker'),
        UpdatePaymentModal: () => import('../widgets/modalUpdatePayment'),
        SendOrderMailSelector: () => import('../components/SendOrderMailSelector'),
        user_selector: () => import('~/components/widgets/RemoteUserSelect'),
    },
    data() {
        return {
            title: 'シェア買注文',
            items: [{ text: 'PINGO' }, { text: 'eCommerce' }, { text: 'シェア買注文', active: true }],
            status_options: [
                { label: 'NEW', value: 'NEW' },
                { label: 'PROCESSING', value: 'PROCESSING' },
                { label: 'DELIVERING', value: 'DELIVERING' },
                { label: 'COMPLETED', value: 'COMPLETED' },
            ],
            order_filters: {
                ordered_at__gte: this.week_before(),
                ordered_at__lte: new Date().toISOString(),
                status: 'NEW',
                user_id: 0,
            },
            isLoading: false,
            multipleSelection: [],
            showmodel_payvendor: false,
            showmodal_payment_status: false,
            showmodal_vendor_payment: false,
            showOrderModalSelector: false,
            order_type: '',
            orders: [],
            userlist: [],
            loading: false,
            selectUser: {},
            orders_meta: {
                links: {},
                page: 1,
                page_size: 100,
                total: 0,
            },
            page: 1,
            per_page: 10,
            current_order: {},
        }
    },
    computed: {
        options() {
            let _options = `?page_size=${this.orders_meta.page_size}&page=${this.orders_meta.page}&expand=user`

            if (this.order_filters.ordered_at__gte !== '') {
                let ordered_at__gte = new Date(this.order_filters.ordered_at__gte)
                _options += `&filter{ordered_at__gte}=${ordered_at__gte.toISOString()}`
            }

            if (this.order_filters.ordered_at__lte !== '') {
                let ordered_at__lte = new Date(this.order_filters.ordered_at__lte)
                _options += `&filter{ordered_at__lte}=${ordered_at__lte.toISOString()}`
            }

            if (this.order_filters.user_id > 0) {
                _options += `&filter{user_id}=${parseInt(this.order_filters.user_id)}`
            }
            if (this.order_filters.status !== 'ALL') {
                _options += `&filter{status}=${this.order_filters.status}`
            }

            return _options
        },
    },
    mounted() {},
    methods: {
        get_badge_color(_status) {
            return Functions.get_order_status_badge_color(_status)
        },
        reset_filters() {
            this.selectUser = null
            this.order_filters.user_id = 0
            this.orders_meta = {
                links: {},
                page: 1,
                page_size: 100,
                total: 0,
            }
            this.orders = []
        },
        handleSelectUser(selectedUser) {
            if (selectedUser !== null) {
                this.selectUser = selectedUser
                this.order_filters.user_id = selectedUser.id
            } else {
                this.selectUser = null
                this.order_filters.user_id = 0
            }
        },
        tablePageChange(page) {
            this.orders_meta.page = page
            this.load_orders()
        },
        week_before() {
            let dt = new Date()
            return new Date(dt.setDate(dt.getDate() - 7)).toISOString()
        },
        change_status(status) {
            this.order_filters.status = status
            this.reset_filters()
        },
        async load_orders() {
            let self = this
            self.isLoading = true
            console.log(this.options)
            await orderService.get_list(this.options).then((response) => {
                console.log(response)
                self.orders = response.results
                self.orders_meta = response.meta
            })

            self.isLoading = false
        },
        updateOrder(order_id, info) {
            console.log(info)
        },
        async updateOrderStatus(order_id, batch = false) {
            const self = this
            if (this.multipleSelection.length == 0 && batch) {
                Swal.fire('注意', '何も選択されていないです！', 'warning')
                return null
            }
            const target = batch ? JSON.stringify(this.multipleSelection) : order_id
            Swal.fire({
                title: 'Select Status',
                html: `注文対象 ID：${target}`,
                input: 'select',
                inputOptions: {
                    NEW: 'NEW',
                    PROCESSING: 'PROCESSING',
                    DELIVERING: 'DELIVERING',
                    COMPLETED: 'COMPLETED',
                },
                inputPlaceholder: 'Select a status',
                showCancelButton: true,
                confirmButtonText: 'Submit',
                showLoaderOnConfirm: true,
                preConfirm: (status) => {
                    if (batch) {
                        return orderService
                            .updateOrder_BATCH_superadmin({
                                ids: self.multipleSelection,
                                update_fields: ['status'],
                                update_info: {
                                    status,
                                },
                            })
                            .then((response) => {
                                response.ids.forEach((order_id) => {
                                    self.replaceOrderInfo(order_id, status)
                                })
                            })
                            .catch((error) => {
                                Swal.showValidationMessage(`Request failed: ${error}`)
                            })
                    } else {
                        return orderService
                            .updateOrder_superadmin({
                                id: order_id,
                                update_fields: ['status'],
                                update_info: {
                                    status,
                                },
                            })
                            .then((response) => {
                                if (response.order_id) {
                                    self.replaceOrderInfo(order_id, status)
                                }
                            })
                            .catch((error) => {
                                Swal.showValidationMessage(`Request failed: ${error}`)
                            })
                    }
                },
                allowOutsideClick: () => !Swal.isLoading(),
            })
        },
        RemoveOrder(order) {
            let self = this
            const order_id = order.id

            if (order.status === 'NEW') {
                Swal.fire({
                    title: '注文削除?',
                    html: `注文対象 ID：${order_id}`,
                    showCancelButton: true,
                    confirmButtonText: 'Submit',
                    confirmButtonColor: '#dc3545',
                    showLoaderOnConfirm: true,
                    preConfirm: (status) => {
                        return orderService
                            .removeOrder_superadmin(order_id)
                            .then((response) => {
                                let orderindex = self.orders.findIndex((order) => order.id == order_id)
                                if (orderindex > -1) {
                                    self.orders.splice(orderindex, 1)
                                }
                                swalService.showModal('削除された!', '注文は削除されました.', 'success')
                            })
                            .catch((error) => {
                                Swal.showValidationMessage(`Request failed: ${error}`)
                            })
                    },
                    allowOutsideClick: () => !Swal.isLoading(),
                })
            } else {
                Swal.fire('Warning', 'Onle NEW order can be removed', 'warning')
            }
        },
        handleSelectionChange(val) {
            let kl = val.map(function (order) {
                return order.id
            })
            this.multipleSelection = kl
        },
        isOrderPaid(order) {
            let result = true
            order.orderitems.forEach((item) => {
                console.log('item idx:', item, item.id, item.paid)
                if (!item.paid) {
                    result = false
                }
            })
            return result
        },
        update_order_payment_status(mode, ids) {
            let order_ids = []
            if (mode === 'single') {
                order_ids.push(ids)
                this.multipleSelection = order_ids
            }
            console.log('update_order_payment_status order_ids', this.multipleSelection)
            this.showmodal_payment_status = true
        },
        update_order_payment_status_result(info) {
            console.log('update_order_payment_status_result', info)
            if (info.result) {
                this.replaceOrderPaymentStatus(info.updateinfo.order_ids, info.updateinfo.payment_status)
                this.showmodal_payment_status = false
            } else {
                this.showmodal_payment_status = false
            }
        },
        replaceOrderInfo(order_id, status) {
            let index = this.orders.findIndex((order) => order.id === order_id)
            if (index > -1) {
                this.orders[index].status = status
                this.orders[index].payment_status = status
            }
        },
        replaceOrderPaymentStatus(ids, payment_status) {
            ids.forEach((id) => {
                let index = this.orders.findIndex((order) => order.id === id)
                if (index > -1) {
                    this.orders[index].payment_status = payment_status
                }
            })
        },
        showSendOrderMail(order) {
            this.current_order = order
            this.showOrderModalSelector = true
        },
        closeOrderModalSelector() {
            console.log('index closeOrderModal')
            this.current_order = {}
            this.showOrderModalSelector = false
        },
    },
    middleware: ['router-auth', 'router-superadmin'],
}
</script>
<style>
.font-16 {
    font-size: 1.5rem;
}
</style>
<template>
    <div>
        <PageHeader :title="title" :items="items" />
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <b-dropdown variant="primary" v-model="order_filters.status">
                                    <template v-slot:button-content>
                                        Status: {{ order_filters.status }}
                                        <i class="mdi mdi-chevron-down"></i>
                                    </template>
                                    <b-dropdown-item v-for="item in status_options" :key="item.value" @click="change_status(item.value)">{{ item.label }}</b-dropdown-item>
                                </b-dropdown>
                            </div>
                            <div class="col-sm-6 text-right">
                                <b-dropdown variant="warning" v-model="order_filters.status">
                                    <template v-slot:button-content>
                                        Order Batch Action
                                        <i class="mdi mdi-chevron-down"></i>
                                    </template>
                                    <b-dropdown-item>
                                        <a href="javascript:void(0);" v-b-modal:modal-update-payment @click="update_order_payment_status('multiple', null)">カード決済</a>
                                    </b-dropdown-item>
                                    <b-dropdown-item v-if="multipleSelection.length">
                                        <a href="javascript:void(0);" @click="updateOrderStatus(0, true)">注文ステータス更新</a>
                                    </b-dropdown-item>
                                    <!-- <b-dropdown-item>
                                        <a href="javascript:void(0);" @click="batch_RemoveOrders(null, true)"><i class="fe-trash-2 text-danger"></i> 注文削除</a>
                                    </b-dropdown-item> -->
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
                                    <el-date-picker id="fromDate_picker" v-model="order_filters.ordered_at__gte" align="right" type="date" placeholder="開始日選択"></el-date-picker>
                                </div>
                            </div>
                            <div class="col-md-6 text-right">
                                <div class="form-group">
                                    <label id="toDate_picker_label">
                                        TO:
                                        <span class="text-danger">*</span>
                                    </label>
                                    <el-date-picker id="toDate_picker" v-model="order_filters.ordered_at__lte" align="right" type="date" placeholder="開始日選択"></el-date-picker>
                                </div>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-6 text-left">
                                <user_selector @SelectUser="handleSelectUser" />
                            </div>

                            <div class="col-6 text-right">
                                <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1" @click="load_orders"> <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;Load Data </b-button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <div class="table-responsive mb-0">
                            <div class="row my-2" v-if="orders_meta.total">
                                <div class="col">
                                    <div class="dataTables_paginate paging_simple_numbers float-right">
                                        <ul class="pagination pagination-rounded">
                                            <b-pagination v-model="orders_meta.page" pills aria-controls="pingoproduct_table" :total-rows="orders_meta.total" :per-page="orders_meta.page_size" @change="tablePageChange"></b-pagination>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <el-table :data="orders" style="width: 100%" @selection-change="handleSelectionChange">
                                <el-table-column type="selection" width="30"></el-table-column>
                                <el-table-column type="expand">
                                    <template slot-scope="props">
                                        <div v-if="props.row.message !== ''">
                                            <h4>Message</h4>
                                            <blockquote class="blockquote">
                                                <p class="mb-0">
                                                    {{ props.row.message }}
                                                </p>
                                                <footer class="blockquote-footer">
                                                    From
                                                    <cite title="Source Title">
                                                        {{ props.row.user }}
                                                    </cite>
                                                </footer>
                                            </blockquote>
                                        </div>
                                    </template>
                                </el-table-column>
                                <el-table-column label="注文番号" sortable prop="id">
                                    <template slot-scope="scope">
                                        {{ '#' + scope.row.id }}
                                        <i class="ri-message-2-fill text-danger" v-if="scope.row.message !== ''"></i>
                                    </template>
                                </el-table-column>
                                <el-table-column label="ステータス">
                                    <template slot-scope="scope">
                                        <a href="javascript:void(0);" @click="updateOrderStatus(scope.row.id, false)">
                                            <b-badge :variant="get_badge_color(scope.row.status)" pill>{{ scope.row.status }}</b-badge>
                                        </a>
                                    </template>
                                </el-table-column>
                                <el-table-column label="会員" sortable width="100" prop="user.username"></el-table-column>
                                <el-table-column label="合計" sortable prop="Total">
                                    <template slot-scope="scope">{{ scope.row.Total | currency('¥') }}</template>
                                </el-table-column>
                                <el-table-column label="サプライヤー">
                                    <template slot-scope="scope">
                                        <b-badge variant="danger" class="text-white" pill v-if="!scope.row.supplier_paid">未払い</b-badge>
                                        <b-badge variant="success" class="text-white" pill v-else>支払済み</b-badge>
                                    </template>
                                </el-table-column>
                                <el-table-column label="受注日" sortable width="100" prop="ordered_at">
                                    <template slot-scope="scope">{{ scope.row.ordered_at | short_date }}</template>
                                </el-table-column>
                                <el-table-column label="Action">
                                    <template slot-scope="scope">
                                        <ul class="list-inline table-action m-0">
                                            <li class="list-inline-item">
                                                <nuxt-link :to="'/superadmin/orders/' + scope.row.id" class="action-icon text-success">
                                                    <i class="fe-edit"></i>
                                                </nuxt-link>
                                            </li>
                                            <li class="list-inline-item">
                                                <a href="javascript:void(0)" v-b-modal:modal-send-order-mail-selector @click="showSendOrderMail(scope.row)" class="action-icon text-success">
                                                    <i class="fe-send"></i>
                                                </a>
                                            </li>
                                            <li class="list-inline-item" v-if="scope.row.status === 'NEW'">
                                                <a href="javascript:void(0)" @click="RemoveOrder(scope.row)" class="action-icon text-danger">
                                                    <i class="fe-trash"></i>
                                                </a>
                                            </li>
                                        </ul>
                                    </template>
                                </el-table-column>
                            </el-table>
                            <div class="row my-2" v-if="orders_meta.total">
                                <div class="col">
                                    <div class="dataTables_paginate paging_simple_numbers float-right">
                                        <ul class="pagination pagination-rounded">
                                            <b-pagination v-model="orders_meta.page" pills aria-controls="pingoproduct_table" :total-rows="orders_meta.total" :per-page="orders_meta.page_size" @change="tablePageChange"></b-pagination>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <UpdatePaymentModal :openModal="showmodal_payment_status" :order_ids="multipleSelection" @updateResult="update_order_payment_status_result"></UpdatePaymentModal>
        <SendOrderMailSelector :order="current_order" :showModal="showOrderModalSelector" :closeModal="closeOrderModalSelector" />
    </div>
</template>
