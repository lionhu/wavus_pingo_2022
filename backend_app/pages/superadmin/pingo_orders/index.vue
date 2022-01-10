<script>
import {mapGetters, mapState} from "vuex"
import {pingoproductService} from "~/helpers/pingoproduct.service"

export default {
  name: "pingo_orders_list",
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
  },
  data() {
    return {
      title: "トモ買イベント商品",
      items: [
        {text: "PinGo"},
        {text: "eCommerce"},
        {text: "トモ買イベント商品", active: true}
      ],
      searchproduct: {
        item_name: "",
        id: 0
      },
      search_product_key: "",
      pingo_productlist: [],
      pingo_productlist_meta: {
        links: {},
        page: 1,
        page_size: 5,
        total: 0
      },
      status_options: [
        {label: "すべて", value: "ALL"},
        {label: "RECRUITING", value: "RECRUITING"},
        {label: "PROCESSING", value: "PROCESSING"},
        {label: "ESTABLISHED", value: "ESTABLISHED"},
        {label: "RELEASED", value: "RELEASED"}
      ],
      order_filters: {
        until_at__gte: this.week_before(),
        until_at__lte: new Date().toISOString(),
        status: "RECRUITING",
      },
      isLoading: false
    };
  },
  computed: {
    options() {
      let _options = `?page_size=${this.pingo_productlist_meta.page_size}&page=${this.pingo_productlist_meta.page}`

      if (this.order_filters.until_at__gte !== "") {
        let until_at__gte = new Date(this.order_filters.until_at__gte)
        _options += `&filter{until_at__gte}=${until_at__gte.toISOString()}`
      }

      if (this.order_filters.until_at__lte !== "") {
        let until_at__lte = new Date(this.order_filters.until_at__lte)
        _options += `&filter{until_at__lte}=${until_at__lte.toISOString()}`
      }

      if (this.order_filters.status !== "ALL") {
        _options += `&filter{status}=${this.order_filters.status}`
      }

      return _options;
    }
  },
  methods: {
    change_status(status) {
      this.order_filters.status = status;
    },
    week_before() {
      let dt = new Date();
      return new Date(dt.setDate(dt.getDate() - 7)).toISOString();
    },
    tablePageChange(page) {
      console.log("page changed", page)
      this.pingo_productlist_meta.page = page;
      this.load_pingoproducts()

    },
    async load_pingoproducts() {
      this.$nuxt.$loading.start();
      await pingoproductService.superadmin_getPingoProductList(this.options)
        .then(response => {
          this.pingo_productlist_meta = response.meta;
          this.pingo_productlist = response.results;
        })
      this.$nuxt.$loading.finish();
    },
    expangRow(row, expandedRows) {
      this.$store.dispatch("pingoproducts/superadmin_retrieve_product_orders",
        {product_id: row.id, options: ""})
    },
    product_progress_ratio(currentNum, targetNum) {
      if (currentNum > 0 && targetNum > 0) {
        return parseInt(currentNum / targetNum * 100)
      }
      return 0
    }
  },
  middleware: ['router-auth', 'router-superadmin'],
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>
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
                  <b-dropdown-item v-for="item in status_options" :key="item.value" @click="change_status(item.value)">
                    {{ item.label }}
                  </b-dropdown-item>
                </b-dropdown>
              </div>
              <div class="col-6 text-right">
                <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1"
                          @click="load_pingoproducts">
                  <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;Load Data
                </b-button>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-md-6">
                <div class="form-group">
                  <label id="fromDate_picker_label">
                    From:<span class="text-danger">*</span>
                  </label>
                  <el-date-picker
                    id="fromDate_picker"
                    v-model="order_filters.until_at__gte"
                    align="right"
                    type="date"
                    placeholder="開始日選択">
                  </el-date-picker>
                </div>
              </div>
              <div class="col-md-6 text-right">
                <div class="form-group">
                  <label id="toDate_picker_label">
                    TO:<span class="text-danger">*</span>
                  </label>
                  <el-date-picker
                    id="toDate_picker"
                    v-model="order_filters.until_at__lte"
                    align="right"
                    type="date"
                    placeholder="開始日選択">
                  </el-date-picker>
                </div>
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
              <div class="row my-2" v-if="pingo_productlist_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="pingo_productlist_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="pingo_productlist_meta.total"
                                    :per-page="pingo_productlist_meta.page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
              <el-table
                id="pingoproduct_table"
                :data="pingo_productlist"
                @expand-change="expangRow"
                style="width: 100%">
                <el-table-column width="250" label="商品" sortable prop="id">
                  <template slot-scope="scope">
                    <div v-if="scope.row.thumbimage_url">
                      <img :src="scope.row.thumbimage_url" alt=""
                           class="rounded mr-3" style="width: 60%;"/>
                    </div>
                    <div v-if="!scope.row.thumbimage_url" class="avatar-xs d-inline-block mr-2">
                      <div class="avatar-title bg-soft-primary rounded-circle text-primary">
                        <i class="mdi mdi-account-circle m-0"></i>
                      </div>
                    </div>
                    <span class="m-0 d-inline-block align-middle">
                      {{ scope.row.item_name }}(#{{ scope.row.id }})
                    </span>
                  </template>
                </el-table-column>

                <el-table-column
                  label="有効"
                  sortable
                  prop="is_valid">
                  <template slot-scope="scope">
                    <b-badge variant="success" pill v-if="scope.row.is_valid">active</b-badge>
                    <b-badge variant="danger" pill v-else>deactivate</b-badge>
                  </template>
                </el-table-column>
                <el-table-column
                  label="ステータス"
                  sortable
                  prop="status">
                  <template slot-scope="scope">
                    <b-badge variant="primary" pill v-if="scope.row.status==='RECRUITING'">{{ scope.row.status }}
                    </b-badge>
                    <b-badge variant="warning" pill v-if="scope.row.status==='PROCESSING'">{{ scope.row.status }}
                    </b-badge>
                    <b-badge variant="success" pill v-if="scope.row.status==='ESTABLISHED'">{{ scope.row.status }}
                    </b-badge>
                    <b-badge variant="danger" pill v-if="scope.row.status==='RELEASED'">{{ scope.row.status }}</b-badge>

                  </template>
                </el-table-column>
                <el-table-column
                  label="募集状況">
                  <template slot-scope="scope">
                    <div class="text-center">
                      <span class="d-block">{{ scope.row.currentNum }}/{{ scope.row.targetNum }}</span>
                      <div class="progress progress-sm">
                        <div class="progress-bar bg-success" role="progressbar"
                             :style="`width: ${product_progress_ratio(scope.row.currentNum,scope.row.targetNum)}%`"
                             :aria-valuenow="product_progress_ratio(scope.row.currentNum,scope.row.targetNum)"
                             aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  sortable
                  label="有効期限">
                  <template slot-scope="scope">
                    <span>{{ scope.row.until_at|short_date }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  label="Action">
                  <template slot-scope="scope">
                    <ul class="list-inline table-action m-0">
                      <li class="list-inline-item">
                        <a :href="`/backend/superadmin/pingo_orders/`+scope.row.id"> <i class="fe-eye"></i></a>
                      </li>
                    </ul>
                  </template>
                </el-table-column>
              </el-table>


              <div class="row my-2" v-if="pingo_productlist_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="pingo_productlist_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="pingo_productlist_meta.total"
                                    :per-page="pingo_productlist_meta.page_size"
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
</template>
