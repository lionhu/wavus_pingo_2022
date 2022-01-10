<script>
import Swal from "sweetalert2";
import {marginService} from "~/helpers/margin.service"
import {swalService} from "@/helpers/swal.service";

const inputValidOptions = {
  '1': '有効',
  '0': '無効'
}
export default {
  name: "marginlist_all",
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    "el-select": () => import('element-ui/lib/select'),
    "el-option": () => import('element-ui/lib/option'),
    "el-form": () => import('element-ui/lib/form'),
    "user_selector": () => import('~/components/widgets/RemoteUserSelect'),
  },
  data() {
    return {
      type_options: [
        {label: "すべて", value: "ALL"},
        {label: "入会賞", value: "INTRODUCE_POINT"},
        {label: '購入取得ボーナス', value: 'OrderBonus'},
        {label: "紹介購入賞", value: "DesendentOrderPoint"},
        {label: "商品購入利用", value: "PURCHASE_ORDER"},
        {label: "贈呈", value: "TRANSFER"},
      ],
      margin_filters: {
        created_at__gte: this.week_before(),
        created_at__lte: new Date().toISOString(),
        type: "ALL",
        user_id: ""
      },
      multipleSelection: [],
      isLoading: false,
      marginlist: [],
      marginlist_meta: {
        page: 1,
        page_size: 10,
        total: 0
      },
      selectUser: {},
      userlist: [],
      loading: false,
    };
  },
  computed: {
    options() {
      let _options = `?page_size=${this.marginlist_meta.page_size}&page=${this.marginlist_meta.page}&expand=user`

      if (this.margin_filters.created_at__gte !== "") {
        let created_at__gte = new Date(this.margin_filters.created_at__gte)
        _options += `&filter{created_at__gte}=${created_at__gte.toISOString()}`
      }

      if (this.margin_filters.created_at__lte !== "") {
        let created_at__lte = new Date(this.margin_filters.created_at__lte)
        _options += `&filter{created_at__lte}=${created_at__lte.toISOString()}`
      }

      if (this.selectUser!==null && this.selectUser.id >0) {
        _options += `&filter{user}=${parseInt(this.selectUser.id)}`
      }

      if (this.margin_filters.type !== "ALL") {
        _options += `&filter{type}=${this.margin_filters.type}`
      }

      return _options;
    }
  },
  methods: {
    tablePageChange(page) {
      this.marginlist_meta.page = page;
      this.load_margins()
    },
    handleSelectUser(selectedUser) {
      this.selectUser = selectedUser
    },
    change_type(margintype) {
      this.margin_filters.type = margintype;
    },
    async load_margins() {
      let self = this;
      self.isLoading = true;

      await marginService.load_list(this.options)
        .then((response) => {
          console.log(response)
          self.isLoading = false;
          self.marginlist = response.results;
          self.marginlist_meta = response.meta;
        })
      this.isLoading = false;
    },


    week_before() {
      let dt = new Date();
      return new Date(dt.setDate(dt.getDate() - 7)).toISOString();
    },

    handleSelectionChange(val) {
      let kl = val.map(function (order) {
        return order.id
      });
      this.multipleSelection = kl;
      console.log(this.multipleSelection)
    },
    deleteMargin(margin_id) {
      let self = this;
      Swal.fire({
        title: '再確認?',
        html: "削除したら、戻せないので、大丈夫でしょうか？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、削除!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            return marginService.remove(margin_id)
              .then(response => {
                self.remove_margin(margin_id)
                return {result: true}
              });
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.result) {
          swalService.showToast("success", "削除されました!")
        }
      })
    },
    async updateMarginAmount(margin_id) {
      let self = this;
      const {value: amount} = await Swal.fire({
        icon: "question",
        title: 'ポイント数',
        input: 'text',
        showCancelButton: true,
        inputValidator: (value) => {
          if (!value) {
            return 'You need to write something!'
          }
        }
      })

      if (parseInt(amount)) {
        marginService.update({
          margin_id: margin_id,
          info: {
            amount: parseInt(amount),
            update_fields: ["amount"]
          }
        }).then(response => {
          self.replace_margin(response)
          Swal.fire({
            icon: "success",
            html: "更新されました！",
            title: "成功"
          })
        })
      }
    },


    async batch_updateMarginValid() {
      let self = this;
      Swal.fire({
        title: '再確認?',
        html: "有効に変更しますか？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、確定!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            let info = {
              "margin_ids": this.multipleSelection,
              "update_fields": ["is_valid"],
              "is_valid": true
            }
            return marginService.batch_update(info).then(response => {
              response.margins.forEach(margin => {
                self.replace_margin(margin)
              })
              return {result: true}
            });
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.result) {
          swalService.showToast("success", "更新されました!")
        }
      })
    },
    replace_margin(new_margin) {
      console.log(new_margin)
      let self = this;
      let index = self.marginlist.findIndex(margin => margin.id === new_margin.id);
      console.log(index)
      if (index > -1) {
        self.marginlist.splice(index, 1, new_margin)
        Swal.fire({
          title: "Success",
          text: "margins has been updated!",
          icon: "success"
        })
      }
    },

    remove_margin(margin_id) {
      let self = this;
      let index = self.marginlist.findIndex(margin => margin.id === margin_id);
      if (index > -1) {
        self.marginlist.splice(index, 1)
        Swal.fire("Success", "margins has been removed!", "success")
      }
    },
    rowSelectable(row, index) {
      return !!(row.is_refound = 1 && row.pointbank_saved === false)
    }
  },
};
</script>

<template>
  <div>
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
              <div class="col-sm-6 text-right">
                <user_selector @SelectUser="handleSelectUser"/>
              </div>
              <!-- end col-->
            </div>
            <div class="row">
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
              <div class="col-md-6 text-right">
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
            <div class="row">
              <div class="col-sm-6 text-left">
                <b-dropdown variant="warning">
                  <template v-slot:button-content>
                    Margin Batch Action
                  </template>
                  <b-dropdown-item>
                    <a href="javascript:void(0);" @click="batch_updateMarginValid">Update
                      Valid</a>
                  </b-dropdown-item>
                </b-dropdown>
              </div>
              <div class="col-md-6 text-right">
                <b-button variant="success" v-bind:disabled="isLoading" class="btn-rounded ml-1"
                          @click="load_margins">
                  <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;Load Data
                  <span v-if="selectUser!==null">(User: {{ selectUser.value }})</span>

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
              <div class="row my-2" v-if="marginlist_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="marginlist_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="marginlist_meta.total"
                                    :per-page="marginlist_meta.page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
              <el-table
                :data="marginlist"
                style="width: 100%"
                @selection-change="handleSelectionChange"
              >

                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <div class="row">
                        <div class="col-12">
                          <h4>ポイント付加情報</h4>
                          <p v-html="props.row.info"></p>
                          <!--                          <div v-if="props.row.type==='DesendentOrderPoint'">-->

                          <!--                            <i class="far fa-user-circle text-success"></i>&nbsp;&nbsp;{{ props.row.info.username }}-->
                          <!--                            <br>-->
                          <!--                            <nuxt-link :to="'/superadmin/orders/' + props.row.info.order_id" class="action-icon">-->
                          <!--                              <i class="fas fa-shopping-cart"></i>&nbsp;&nbsp;#{{ props.row.info.order_id }}-{{ props.row.info.orderitem_id }}-->
                          <!--                            </nuxt-link>-->
                          <!--                          </div>-->


                          <!--                          <div v-if="props.row.type==='OrderBonus'">-->

                          <!--                          {{props.row.info}}-->
                          <!--                            <nuxt-link :to="'/superadmin/orders/' + props.row.info.order_id" class="action-icon">-->
                          <!--                              <i class="fas fa-shopping-cart"></i>&nbsp;&nbsp;#{{ props.row.info.order_id }}-{{ props.row.info.orderitem_id }}-->
                          <!--                            </nuxt-link>-->
                          <!--                          </div>-->

                          <!--                          <div v-if="props.row.type==='PURCHASE_ORDER'">-->
                          <!--                            <nuxt-link :to="'/superadmin/orders/' + props.row.info.order_id" class="action-icon">-->
                          <!--                              <i class="ri-shopping-basket-2-fill"></i>&nbsp;&nbsp;#{{ props.row.info.order_id }}-->
                          <!--                            </nuxt-link>-->
                          <!--                          </div>-->


                          <!--                          <div v-if="props.row.type==='INTRODUCE_POINT'">-->
                          <!--                            <i class="fas fa-street-view"></i>&nbsp;&nbsp;{{ props.row.info.username }}-->
                          <!--                          </div>-->

                          <!--                          <div v-if="props.row.type==='TRANSFER_IN'">-->
                          <!--                            <i class="ri-gift-fill text-warning"></i>&nbsp;&nbsp;{{ props.row.info.username }}-->
                          <!--                          </div>-->
                          <!--                          <div v-if="props.row.type==='TRANSFER_OUT'">-->
                          <!--                            <i class="ri-hand-heart-fill text-success"></i>&nbsp;&nbsp;{{ props.row.info.username }}-->
                          <!--                          </div>-->
                        </div>
                      </div>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column
                  type="selection"
                  :selectable="rowSelectable"
                  width="55">
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
                  label="注文種類"
                  sortable
                  prop="order_type">
                  <template slot-scope="scope">
                    <b-badge pill variant="warning" v-if="scope.row.order_type==='PINGO'">PINGO</b-badge>
                    <b-badge pill variant="primary" v-else>REGULAR</b-badge>
                  </template>
                </el-table-column>
                <el-table-column
                  label="レベル"
                  sortable
                  prop="type" v-if="margin_filters.type==='ALL'">
                  <template slot-scope="scope">
                    {{ scope.row.type }}
                    <i :class="{'ri-user-voice-fill text-danger':scope.row.info.level==='SUPERADMIN',
                                  'ri-team-fill  text-warning':scope.row.info.level==='CLIENTADMIN',
                                  'ri-user-heart-line  text-primary':scope.row.info.level==='LEVEL_1',
                                  'ri-parent-fill  text-success':scope.row.info.level==='LEVEL_2',
                                  'ri-coin-fill  text-success':scope.row.info.level==='USER_SELF',}"></i>
                  </template>
                </el-table-column>
                <el-table-column
                  label="ポイント"
                  sortable
                  prop="amount">
                  <template slot-scope="scope">
                    <span class="text-danger" v-if="scope.row.type=='PURCHASE_ORDER'">-{{
                        scope.row.amount|currency("¥")
                      }}</span>
                    <span class="text-success" v-else>{{ scope.row.amount|currency("¥") }}</span>

                  </template>
                </el-table-column>
                <el-table-column
                  label="発生日"
                  sortable
                  width="100"
                  prop="created_at">
                  <template slot-scope="scope">
                    {{ scope.row.created_at | short_datetime }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="有効"
                  sortable
                  width="80"
                  align="center"
                  prop="is_valid">
                  <template slot-scope="scope">

                    <a href="javascript:void(0);" v-if="!scope.row.is_valid">
                      <i class="fe-eye-off text-danger"></i>
                    </a>
                    <a href="javascript:void(0);" v-else>
                      <i class="fe-eye text-success"></i>
                    </a>
                  </template>
                </el-table-column>

                <el-table-column
                  label="Action">
                  <template slot-scope="scope">
                    <ul class="list-inline table-action m-0">
                      <li class="list-inline-item" v-if="!scope.row.is_valid">
                        <a href="javascript:void(0);" @click="updateMarginAmount(scope.row.id)">
                          <i class="fe-edit-2"></i>
                        </a>
                      </li>
                      <li class="list-inline-item" v-if="!scope.row.is_valid">
                        <a href="javascript:void(0);" @click="deleteMargin(scope.row.id)">
                          <i class="fe-trash"></i>
                        </a>
                      </li>
                    </ul>
                  </template>
                </el-table-column>
              </el-table>

              <div class="row my-2" v-if="marginlist_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="marginlist_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="marginlist_meta.total"
                                    :per-page="marginlist_meta.page_size"
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
