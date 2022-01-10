<script>
import {swalService} from "~/helpers/swal.service"
import {pointbankService} from "@/helpers/pointbank.service"

export default {
  name: "admin_pointbanks_management",
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
    "countTo": () => import('vue-count-to'),
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    "el-autocomplete": () => import('element-ui/lib/autocomplete'),
    "el-select": () => import('element-ui/lib/select'),
    "el-option": () => import('element-ui/lib/option'),
    "user_selector": () => import('~/components/widgets/RemoteUserSelect'),
  },
  computed: {
    total() {
      if (this.pointbanks_meta.total === 0) return 0;
      return this.pointbanks.reduce((accumulator, val) => {
        accumulator += parseInt(val.point)
        return accumulator
      }, 0)
    },
    options() {
      let _options = `?page_size=${this.pointbanks_meta.page_size}&page=${this.pointbanks_meta.page}&expand=user`

      if (this.filters.until_at__gte !== "") {
        let until_at__gte = new Date(this.filters.until_at__gte)
        _options += `&filter{until_at__gte}=${until_at__gte.toISOString()}`
      }

      if (this.filters.until_at__lte !== "") {
        let until_at__lte = new Date(this.filters.until_at__lte)
        _options += `&filter{until_at__lte}=${until_at__lte.toISOString()}`
      }

      if (this.filters.user_id > 0) {
        _options += `&filter{user_id}=${parseInt(this.filters.user_id)}`
      }

      return _options;
    }
  },
  data() {
    return {
      title: "有効ポイント",
      items: [
        {text: "PINGO"},
        {text: "eCommerce"},
        {text: "有効ポイント", active: true}
      ],
      filters: {
        until_at__gte: this.yesterday(),
        until_at__lte: this.year_after(),
        user_id: 0,
      },
      page_sizes: [
        {label: "50", value: "50"},
        {label: "100", value: "100"},
        {label: '500', value: '500'},
      ],
      selectUser: null,
      multipleExpiredPointSelection: [],
      isLoading: false,
      pointbanks: [],
      pointbanks_meta: {
        links: {},
        page: 1,
        page_size: 100,
        total: 0
      },
      loading: false,
      value: "",
      active_tab: "失効ポイント"
    };
  },
  mounted() {
    this.load_pointbanks(this.options);
  },
  methods: {
    change_type_size(page_size) {
      this.pointbanks_meta.page_size = parseInt(page_size)
    },
    tablePageChange(page) {
      this.pointbanks_meta.page = page;
      this.load_pointbanks()
    },
    year_after() {
      let dt = new Date();
      return new Date(dt.setDate(dt.getDate() + 365)).toISOString();
    },
    yesterday() {
      let dt = new Date();
      return new Date(dt.setDate(dt.getDate() - 1)).toISOString();
    },
    async load_pointbanks() {
      let vm = this;
      this.isLoading = true;
      console.log(this.options)
      await pointbankService.load_list(this.options)
        .then((response) => {
          vm.pointbanks = response.results;
          vm.pointbanks_meta = response.meta;
        })
      this.isLoading = false;
    },

    handleExpiredSelectionChange(val) {
      let kl = val.map(pointbank => pointbank.id);
      this.multipleExpiredPointSelection = kl;
    },
    deleteExpiredPointbanks() {
      let vm = this;
      vm.isLoading = true;

      let info = {
        "ids": this.multipleExpiredPointSelection,
      }

      pointbankService.destroy_list(info)
        .then((response) => {
          if (response.result) {
            swalService.showToast("success", `${response.data.count} records deleted!`)
            vm.load_pointbanks();
          }
        })
      this.isLoading = false;

    },
    handleSelectUser(selectedUser) {
      if (selectedUser !== null) {
        this.selectUser = selectedUser
        this.filters.user_id = selectedUser.id;
      } else {
        this.selectUser = null
        this.filters.user_id = 0;
      }
    },
  },
  middleware: ['router-auth', 'router-superadmin'],
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>

    <div class="card">
      <div class="card-body">
        <div class="row">
          <div class="col">
            <div class="widget-rounded-circle card">
              <div class="card-body">
                <div class="row">
                  <div class="col-6">
                    <div class="avatar-lg rounded-circle bg-icon-primary">
                      <i class="ri-coin-fill font-24 avatar-title text-white"></i>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="text-right">
                      <h5 class="text-dark mt-1">
                        <span> <countTo :end-val="total" :duration="1500"></countTo> </span>
                      </h5>
                      <p class="text-muted mb-1 text-truncate">Total Points</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col">
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
                      <h5 class="text-dark mt-1">
                        <span><countTo :end-val="pointbanks_meta.total" :duration="1500"></countTo></span>
                      </h5>
                      <p class="text-muted mb-1 text-truncate">{{ pointbanks_meta.total }} records</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col" v-if="selectUser!==null">
            <div class="widget-rounded-circle card">
              <div class="card-body">
                <div class="row align-items-center">
                  <div class="col-6">
                    <div class="avatar-lg">
                      <div class="avatar-lg rounded-circle bg-icon-warning">
                        <img :src="selectUser.avatar"
                             style="max-width: 60px;border-radius:100%;"
                             v-if="selectUser.avatar!==null">
                        <i class="ri-map-pin-user-fill font-24 avatar-title text-white" v-else></i>
                      </div>
                    </div>
                  </div>
                  <div class="col-6">
                    <h5 class="mt-0">{{ selectUser.value }}</h5>
                    <p class="text-muted mb-1 font-13">{{ selectUser.email }}</p>
                    <!--                            <small class="text-muted">-->
                    <!--                                <b>user.type</b>-->
                    <!--                            </small>-->
                  </div>
                </div>
              </div>
              <!-- end row-->
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <div class="card">
              <div class="card-body">
                <div class="row mb-2">
                  <div class="col-sm-6">
                  </div>
                  <div class="col-sm-6 text-right">

                  </div>
                  <!-- end col-->
                </div>
                <div class="row">
                  <div class="col-md-4">
                    有効期限
                  </div>
                  <div class="col-md-4">
                    <div class="form-group">
                      <label id="UntilFromDate_picker_label">
                        From:
                        <span class="text-danger">*</span>
                      </label>
                      <el-date-picker
                        id="UntilFromDate_picker"
                        v-model="filters.until_at__gte"
                        align="right"
                        type="date"
                        placeholder="開始日選択">
                      </el-date-picker>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="form-group">
                      <label id="UntiletoDate_picker_label">
                        TO:
                        <span class="text-danger">*</span>
                      </label>
                      <el-date-picker
                        id="UntiletoDate_picker"
                        v-model="filters.until_at__lte"
                        align="right"
                        type="date"
                        placeholder="終了日選択">
                      </el-date-picker>
                    </div>
                  </div>
                </div>
                <div class="row mb-3">
                  <div class="col-md-4">
                    ユーザー
                  </div>
                  <div class="col-md-8">
                    <user_selector @SelectUser="handleSelectUser"/>
                  </div>
                </div>
                <div class="row">
                  <div class="col-12 text-right">

                    <b-dropdown variant="primary" v-model="pointbanks_meta.page_size">
                      <template v-slot:button-content>
                        Page size:
                        <i class="mdi mdi-chevron-down"></i>
                      </template>
                      <b-dropdown-item v-for="option in page_sizes" :key="option.value"
                                       @click="change_type_size(option.value)">
                        {{ option.label }}
                      </b-dropdown-item>
                    </b-dropdown>
                    <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1"
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

                  <div class="row my-2" v-if="pointbanks_meta.total">
                    <div class="col">
                      <div class="dataTables_paginate paging_simple_numbers float-right">
                        <ul class="pagination pagination-rounded">
                          <b-pagination v-model="pointbanks_meta.page"
                                        pills
                                        aria-controls="pingoproduct_table"
                                        :total-rows="pointbanks_meta.total"
                                        :per-page="pointbanks_meta.page_size"
                                        @change="tablePageChange"
                          >
                          </b-pagination>
                        </ul>
                      </div>
                    </div>
                  </div>
                  <el-table
                    :data="pointbanks"
                    style="width: 100%"
                  >
                    <el-table-column type="expand">
                      <template slot-scope="props">
                        {{ props.row.info }}
                      </template>
                    </el-table-column>
                    <el-table-column label="ID" sortable prop="id">
                      <template slot-scope="scope">
                        {{ '#' + scope.row.id }}
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="会員"
                      sortable
                      prop="user.username">
                    </el-table-column>
                    <el-table-column
                      label="ポイント"
                      sortable
                      prop="point">
                      <template slot-scope="scope">{{ scope.row.point|currency("¥") }}</template>
                    </el-table-column>
                    <el-table-column
                      label="取得日"
                      sortable
                      width="160"
                      prop="created_at">
                      <template slot-scope="scope">
                        <span>{{ scope.row.created_at | short_date }}</span>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="有効期限"
                      sortable
                      width="160"
                      prop="created_at">
                      <template slot-scope="scope">
                        <span class="text-danger">{{ scope.row.until_at | short_date }}</span>
                      </template>
                    </el-table-column>
                  </el-table>

                  <div class="row my-2" v-if="pointbanks_meta.total">
                    <div class="col">
                      <div class="dataTables_paginate paging_simple_numbers float-right">
                        <ul class="pagination pagination-rounded">
                          <b-pagination v-model="pointbanks_meta.page"
                                        pills
                                        aria-controls="pingoproduct_table"
                                        :total-rows="pointbanks_meta.total"
                                        :per-page="pointbanks_meta.page_size"
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
</template>
