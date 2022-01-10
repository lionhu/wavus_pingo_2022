<script>
import {mapGetters} from "vuex"
import {swalService} from "~/helpers/swal.service"
import {axios} from '@/plugins/axios.js';

const inputValidOptions = {
  '1': 'Valid',
  '0': 'Invalid'
}
export default {
  name: "marginlist",
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
  },
  data() {
    return {
      title: "Margins",
      items: [
        {
          text: "PINGO"
        },
        {
          text: "eCommerce"
        },
        {
          text: "Margins",
          active: true
        }
      ],
      type_options: [
        {label: "すべて", value: "ALL"},
        {label: "入会賞", value: "INTRODUCE_POINT"},
        {label: "紹介購入賞", value: "DesendentOrderPoint"},
        {label: "商品購入利用", value: "PURCHASE_ORDER"},
        {label: "贈呈", value: "TRANSFER"},
      ],
      margin_filters: {
        created_at__gte: this.week_before(),
        created_at__lte: new Date().toISOString(),
        type: "",
      },
      isLoading: false,
      marginlist: [],
    };
  },
  methods: {

    point_type_class(type) {
      switch (type) {
        case "INTRODUCE_POINT":
          return "success";
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
    load_margins() {
      let vm = this;
      this.isLoading = true;
      axios.$post("/back/store/api/margins/list_clientadmin/", {filters: this.margin_filters})
        .then((response) => {
          if (response.result) {
            vm.marginlist = response.data.margins;
            swalService.showToast("success", "Loaded successfully!")
          }
        })
      this.isLoading = false;
    },
    change_type(margintype) {
      this.margin_filters.type = margintype;
      this.load_margins();
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
  middleware: ['router-auth', 'router-clientadmin'],
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
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-sm-6">
                <b-dropdown variant="primary" v-model="margin_filters.type">
                  <template v-slot:button-content>
                    Status: {{ margin_filters.type }}
                    <i class="mdi mdi-chevron-down"></i>
                  </template>
                  <b-dropdown-item v-for="option in type_options" :key="option.value"
                                   @click="change_type(option.value)">
                    {{ option.label }}
                  </b-dropdown-item>
                </b-dropdown>
              </div>
              <!-- end col-->
            </div>
            <div class="row d-flex justify-content-between">
              <div class="col-md-6">
                <div class="form-group">
                  <label id="fromDate_picker_label">
                    From:
                    <span class="text-danger">*</span>
                  </label>
                  <el-date-picker
                    id="fromDate_picker"
                    v-model="margin_filters.created_at__gte"
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
                    v-model="margin_filters.created_at__lte"
                    align="right"
                    type="date"
                    placeholder="終了日選択">
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

            <!-- Table -->
            <div class="table-responsive mb-0">
              <el-table
                :data="marginlist"
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
                  prop="type" v-if="margin_filters.type==='ALL'">
                  <template slot-scope="scope" align="center">
                    <span :class="'text-'+point_type_class(scope.row.type )">
                      {{ point_type_text(scope.row.type) }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="Amount"
                  sortable
                  align="right"
                  prop="amount">
                  <template slot-scope="scope">{{ scope.row.amount|currency("¥") }}</template>
                </el-table-column>
                <el-table-column
                  label="Info">
                  <template slot-scope="scope" align="center">
                    <div v-if="scope.row.type=='DesendentOrderPoint'" class="text-center">

                      <i class="far fa-user-circle text-success"></i>&nbsp;&nbsp;{{ scope.row.info.username }} <br>
                      <i class="ri-shopping-bag-fill text-warning"></i>&nbsp;&nbsp;#{{ scope.row.info.order_id }}-{{
                        scope.row.info.orderitem_id
                      }}
                    </div>
                    <div v-if="scope.row.type=='INTRODUCE_POINT'" class="text-center">
                      <i class="ri-map-pin-user-fill"></i>&nbsp;&nbsp;{{ scope.row.info.username }}
                    </div>
                    <div v-if="scope.row.type=='PURCHASE_ORDER'" class="text-center">
                      <i class="ri-shopping-bag-fill text-danger"></i>#{{ scope.row.info.order_id }}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  label="Date"
                  sortable
                  prop="created_at">
                  <template slot-scope="scope">
                    {{ scope.row.created_at | short_datetime }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="Valid"
                  sortable
                  width="80"
                  align="center"
                  prop="is_valid">
                  <template slot-scope="scope">
                    <i
                      v-bind:class="{'fe-eye text-success':scope.row.is_valid,'fe-eye-off text-danger':!scope.row.is_valid}"></i>
                  </template>
                </el-table-column>
              </el-table>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
