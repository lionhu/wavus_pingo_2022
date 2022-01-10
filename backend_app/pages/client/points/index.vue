<script>
import {mapGetters} from "vuex"
import {swalService} from "~/helpers/swal.service"
import {pointbankService} from "~/helpers/pointbank.service"

const inputValidOptions = {
  '1': 'Valid',
  '0': 'Invalid'
}
export default {
  name: "client_points",
  middleware: ['router-auth', 'router-clientadmin'],
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
    "countTo": () => import('vue-count-to'),
  },
  data() {
    return {
      title: "ポイント",
      items: [
        {text: "PINGO"},
        {text: "eCommerce"},
        {text: "ポイント", active: true}
      ],
      type_options: [
        {label: "すべて", value: "ALL"},
        {label: "入会賞", value: "INTRODUCE_POINT"},
        {label: "購入ボーナスポイント", value: "OrderBonus"},
        {label: "紹介購入賞", value: "DesendentOrderPoint"},
        {label: "商品購入利用", value: "PURCHASE_ORDER"},
        {label: "贈呈", value: "TRANSFER"},
      ],
      pointbank_filters: {
        created_at__gte: this.week_before(),
        created_at__lte: new Date().toISOString(),
        margin__order_type: "ALL",
      },
      isLoading: false,
      pointbank_list: [],
      pointbank_list_meta: {
        total: 0,
        page: 1,
        page_size: 10000,
        links: {}
      },
    };
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME"
    }),
    pointbank_balance() {
      if (this.ME.profile.pointbank_balance === null) return 0;
      return this.ME.profile.pointbank_balance
    },
    options() {
      let options = `?page_size=${this.pointbank_list_meta.page_size}&page=${this.pointbank_list_meta.page}&expand=margin`
      if (this.pointbank_filters.margin__order_type !== "ALL") {
        options += `&filter{margin__order_type}=${this.pointbank_filters.margin__order_type}`
      }
      if (this.pointbank_filters.created_at__lte !== "") {
        let created_at__lte = new Date(this.pointbank_filters.created_at__lte).toISOString()
        console.log(created_at__lte)
        options += `&filter{created_at__lte}=${created_at__lte}`
      }
      if (this.pointbank_filters.created_at__gte !== "") {
        let created_at__gte = new Date(this.pointbank_filters.created_at__gte).toISOString()
        options += `&filter{created_at__gte}=${created_at__gte}`
      }
      options += `&filter{user}=${this.ME.pk}`
      return options
    }
  },
  mounted() {
  },
  methods: {
    tablePageChange(page) {
      this.pointbank_list_meta.page = page;
      this.load_pointbanks()
    },
    point_type_class(type) {
      switch (type) {
        case "INTRODUCE_POINT":
          return "success";
        case "OrderBonus":
          return "danger";
        case "PURCHASE_ORDER":
          return "danger";
        case "DesendentOrderPoint":
          return "primary";
        case "REFOUND_FROM_DELETED_ORDER":
          return "warning";

      }
    },
    point_type_text(type) {
      switch (type) {
        case "INTRODUCE_POINT":
          return "入会紹介";
        case "TRANSFER_OUT":
          return "ポイント贈呈";
        case "TRANSFER_IN":
          return "ポイント受取";
        case "OrderBonus":
          return "購入ボーナスポイント";
        case "PURCHASE_ORDER":
          return "購入利用";
        case "DesendentOrderPoint":
          return "製品紹介購入";
        case "REFOUND_FROM_DELETED_ORDER":
          return "使用ポイント取消";

      }
    },
    week_before() {
      var dt = new Date();
      return new Date(dt.setDate(dt.getDate() - 7)).toISOString();
    },
    async load_pointbanks() {
      let self = this;
      this.isLoading = true;
      console.log("options",this.options)
      await pointbankService.load_list(this.options)
        .then((response) => {
          console.log(response)
          self.isLoading = false;
          self.pointbank_list = response.results;
          self.pointbank_list_meta = response.meta;
        })

      this.isLoading = false;
    },
    change_type(pointbanktype) {
      this.pointbank_filters.margin__order_type = pointbanktype;
      this.load_pointbanks();
    },
    tableRowClassName({row, rowIndex}) {
      console.log(row.type)
      switch (row.type) {
        case "DesendentOrderPoint":
          return "success-row";
        case "PURCHASE_ORDER":
          return "warning-row"
      }
    }
  },
};
</script>
<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>
<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-md-6">
        <div class="widget-rounded-circle card">
          <div class="card-body">
            <div class="row">
              <div class="col-6">
                <div class="avatar-lg rounded-circle bg-icon-success">
                  <i class="ri-auction-fill font-24 avatar-title text-white"></i>
                </div>
              </div>
              <div class="col-6">
                <div class="text-right">
                  <h3 class="text-dark mt-1">
                    <span> <countTo :end-val="pointbank_balance" :duration="1500"></countTo> </span>
                  </h3>
                  <p class="text-muted mb-1 text-truncate">有効ポイント</p>
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
            <div class="row d-flex justify-content-between">
              <div class="col-md-6">
                <div class="form-group">
                  <label id="fromDate_picker_label">
                    From:
                    <span class="text-danger">*</span>
                  </label>
                  <el-date-picker
                    id="fromDate_picker"
                    v-model="pointbank_filters.created_at__gte"
                    align="right"
                    type="date"
                    placeholder="開始日選択">
                  </el-date-picker>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label id="toDate_picker_label">
                    TO:
                    <span class="text-danger">*</span>
                  </label>
                  <el-date-picker
                    id="toDate_picker"
                    v-model="pointbank_filters.created_at__lte"
                    align="right"
                    type="date"
                    placeholder="終了日選択">
                  </el-date-picker>
                </div>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col ">
                <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1 float-right"
                          @click="load_pointbanks">
                  <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;Load Data
                </b-button>
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

            <!-- Table -->
            <div class="table-responsive mb-0">
              <div class="row my-2" v-if="pointbank_list_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="pointbank_list_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="pointbank_list_meta.total"
                                    :per-page="pointbank_list_meta.page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
              <el-table
                :data="pointbank_list"
                style="width: 100%"
                :row-class-name="tableRowClassName">
                <el-table-column label="ID" sortable prop="id" width="80">
                  <template slot-scope="scope">
                    {{ '#' + scope.row.id }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="Type"
                  sortable
                  prop="type" v-if="pointbank_filters.type==='ALL'">
                  <template slot-scope="scope" align="center">
                    <span :class="'text-'+point_type_class(scope.row.type )">
                      {{ point_type_text(scope.row.type) }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="ポイント"
                  sortable
                  align="right"
                  prop="point">
                  <template slot-scope="scope">{{ scope.row.point|currency("¥") }}</template>
                </el-table-column>
                <el-table-column
                  label="発生者"
                  sortable
                  prop="margin.fromuser">
                </el-table-column>
                <el-table-column
                  label="種類"
                  sortable
                  prop="margin.type">
                  <template slot-scope="scope">
                    {{ point_type_text(scope.row.margin.type) }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="発生日"
                  sortable
                  prop="created_at">
                  <template slot-scope="scope">
                    {{ scope.row.created_at | short_datetime }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="有効期限"
                  sortable
                  prop="until_at">
                  <template slot-scope="scope">
                    {{ scope.row.until_at | short_datetime }}
                  </template>
                </el-table-column>
              </el-table>

              <div class="row my-2" v-if="pointbank_list_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="pointbank_list_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="pointbank_list_meta.total"
                                    :per-page="pointbank_list_meta.page_size"
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
