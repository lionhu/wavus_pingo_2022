<script>
import {mapGetters} from "vuex"
import Swal from "sweetalert2";
import {axios} from '@/plugins/axios.js';
import {marginService} from "~/helpers/margin.service"


const inputValidOptions = {
  '1': 'Valid',
  '0': 'Invalid'
}
export default {
  name: "toApproved_marginlist",
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-input": () => import('element-ui/lib/input'),
    "el-select": () => import('element-ui/lib/select'),
    "el-option": () => import('element-ui/lib/option'),
    "el-form-item": () => import('element-ui/lib/form-item'),
    "el-form": () => import('element-ui/lib/form'),
  },
  computed: {
    ...mapGetters({}),
    nDays_before() {
      if (this.nDays > 0) {
        var dt = new Date();
        return new Date(dt.setDate(dt.getDate() - this.nDays)).toISOString();
      }
      return ""
    },
  },
  data() {
    return {
      isLoading: false,
      loading: false,
      marginlist_toBeApproved: [],
      marginlist_toBeApproved_meta: {},
      multipleSelection_toBeApproved: [],
      nDays: 5,
      selectUser: null,
      userlist: [],
      filters: {
        is_valid: false,
        is_refound: 1,
        type: "ALL",
        pointbank_saved: false,
        user_id: ""
      },
      page: 1,
      per_page: 10,
    };
  },
  mounted() {
    this.load_margins_toApproved();
  },
  methods: {
    tablePageChange(page) {
      this.page = page;
      this.load_margins_toApproved()
    },
    load_margins_toApproved() {

      let vm = this;
      this.isLoading = true;
      let options = `?per_page=${this.per_page}&page=${this.page}&filter{is_valid}=${false}&include[]=user`
      if (this.nDays_before !== "") {
        let created_at__lte = new Date(this.nDays_before).toISOString()
        console.log(created_at__lte)
        options += `&filter{created_at.lte}=${created_at__lte}`
      }

      if (this.selectUser !== null) {
        options += `&filter{user}=${parseInt(this.selectUser)}`
      }
      console.log(options)
      marginService.load_list(options)
        .then((response) => {
          if (response.result) {
            vm.marginlist_toBeApproved = response.margins;
            vm.marginlist_toBeApproved_meta = response.meta;
          }
        })
      this.isLoading = false;
    },

    handleSelectionChange_toBeApproved(val) {
      var kl = val.map(function (order) {
        return order.id
      });
      this.multipleSelection = kl;
      console.log(this.multipleSelection)
    },
    deleteMargin(margin_id) {
      Swal.fire({
        title: '削除しますか?',
        html: "削除したら、戻せないので、大丈夫でしょうか!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '削除してください'
      }).then((result) => {
        if (result.isConfirmed) {
          let vm = this;
          marginService.remove(margin_id)
            .then((response) => {
              if (response.result) {
                vm.remove_margin(margin_id)
              }
            });
        }
      })
    },

    async updateMarginValid(margin_id) {
      let vm = this;
      const {value: validValue} = await Swal.fire({
        title: 'Select Valid',
        input: 'radio',
        inputOptions: inputValidOptions,
        inputValidator: (value) => {
          if (!value) {
            return 'You need to choose something!'
          }
        }
      })

      if (validValue) {
        marginService.update({
          margin_id: margin_id,
          info: {
            is_valid: !!parseInt(validValue),
            update_fields: ["is_valid"]
          }
        })
          .then(response => {
            console.log("after update", response)
            if (response.result) {
              vm.replace_margin(response.margin.margin)
              Swal.fire({
                icon: "success",
                html: "Updated successfully",
                title: "Success"
              })
            }
          })
      }
    },
    async updateMarginAmount(margin_id) {
      let vm = this;
      const {value: amount} = await Swal.fire({
        icon: "question",
        title: 'Enter amount',
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
          console.log("after update", response)
          if (response.result) {
            vm.replace_margin(response.margin.margin)
            Swal.fire({
              icon: "success",
              html: "Updated successfully",
              title: "Success"
            })
          }
        })
      }
    },


    async batch_updateMarginValid() {
      let vm = this;
      if (this.multipleSelection.length) {
        const {value: validValue} = await Swal.fire({
          title: 'Select Valid',
          input: 'radio',
          inputOptions: inputValidOptions,
          inputValidator: (value) => {
            if (!value) {
              return 'You need to choose something!'
            }
          }
        })

        if (validValue) {
          let info = {
            "margin_ids": this.multipleSelection,
            "update_fields": ["is_valid"],
            "is_valid": !!parseInt(validValue)
          }
          marginService.batch_update(info).then(response => {
            console.log(response)

            if (response.result) {
              response.data.margins.forEach(margin => {
                vm.replace_margin(margin)
              })
            }
          });
        }
      }
    },
    replace_margin(new_margin) {
      console.log(new_margin)
      let vm = this;
      let index = vm.marginlist_toBeApproved.findIndex(margin => margin.id === new_margin.id);
      console.log(index)
      if (index > -1) {
        vm.marginlist_toBeApproved.splice(index, 1, new_margin)
        Swal.fire({
          title: "Success",
          text: "margins has been updated!",
          icon: "success"
        })
      }
    },
    remove_margin(margin_id) {
      let vm = this;
      let index = vm.marginlist_toBeApproved.findIndex(margin => margin.id === margin_id);
      if (index > -1) {
        vm.marginlist_toBeApproved.splice(index, 1)
        Swal.fire("Success", "margins has been removed!", "success")
      }
    },


    batchupdate_margin_common(info) {
      let vm = this;
      this.$store.dispatch("margins/batch_updateMargin_superadmin", info)
        .then(resolve => {
          if (resolve.margins.length) {
            resolve.margins.forEach(margin => {
              vm.replace_margin(margin)
            })
          }
        })
    },
    update_margin_common(info) {
      let vm = this;
      this.$store.dispatch("margins/updateMargin_superadmin", info)
        .then(resolve => {
          var new_margin = resolve.margin;
          vm.replace_margin(new_margin)
        })
    },
    rowSelectable_toBeApproved(row, index) {
      return !!(row.is_refound = 1 && row.pointbank_saved === false)
    },
    querySearchUser(query) {
      let vm = this;
      vm.userlist = [];
      if (query !== "") {
        this.loading = true;
        axios.$post("/apiauth/login/filter_users/", {keystr: query})
          .then((response) => {
            if (response.result && response.data.users.length > 0) {
              this.loading = false;
              vm.userlist = response.data.users
              return true;
            }
          })
      }
      return false;
    },
    ResetUserSearch() {
      this.filters.user_id = "";
      this.selectUser = null;
    },
    handleSelectUser() {
      if (this.filters.user_id !== "") {
        let userIndex = this.userlist.findIndex(user => user.id === this.filters.user_id)
        if (userIndex > -1) {
          this.selectUser = this.userlist[userIndex]
        }
      }
    },

  },
};
</script>

<template>
  <b-tab>
    <template #title>
      <b-spinner type="grow" small class="mr-3 text-warning" v-if="marginlist_toBeApproved.length"></b-spinner>
      <strong>承認待ちポイント</strong>
    </template>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row mb-2">
              <el-form ref="form" :inline="true">
                <el-form-item label="n 日前まで">
                  <el-input v-model="nDays" type="number" id="input_nDays_before"
                            placeholder="n Days Before"></el-input>
                </el-form-item>
                <el-form-item label="ユーザー：">
                  <el-select
                    v-model="selectUser"
                    filterable
                    remote
                    reserve-keyword
                    @change="handleSelectUser"
                    placeholder="ユーザー名"
                    :remote-method="querySearchUser"
                    :loading="loading">
                    <el-option
                      v-for="item in userlist"
                      :key="item.id"
                      :label="item.username"
                      :value="item.id">
                    </el-option>
                  </el-select>
                  <b-button variant="primary" @click="ResetUserSearch">Reset</b-button>
                </el-form-item>
                <el-form-item>
                  <b-button variant="success" v-bind:disabled="isLoading" class="btn-rounded ml-1"
                            @click="load_margins_toApproved">
                    <b-spinner small v-if="isLoading"></b-spinner>
                    Load Data
                    <span v-if="selectUser!==null">(for User)</span>
                  </b-button>
                </el-form-item>
                <el-form-item>
                  <b-dropdown variant="warning">
                    <template v-slot:button-content>
                      Margin Batch Action
                    </template>
                    <b-dropdown-item>
                      <a href="javascript:void(0);" @click="batch_updateMarginValid">Update
                        Valid</a>
                    </b-dropdown-item>
                  </b-dropdown>
                </el-form-item>
              </el-form>
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
              <div class="row my-2" v-if="marginlist_toBeApproved_meta.total_results">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="marginlist_toBeApproved_meta.total_results"
                                    :per-page="per_page"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
              <el-table
                :data="marginlist_toBeApproved"
                style="width: 100%"
                @selection-change="handleSelectionChange_toBeApproved"
              >
                <el-table-column
                  type="selection"
                  :selectable="rowSelectable_toBeApproved"
                  width="55">
                </el-table-column>
                <el-table-column label="ID" sortable prop="id">
                  <template slot-scope="scope">
                    {{ '#' + scope.row.id }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="User"
                  sortable
                  prop="user.username">
                </el-table-column>
                <el-table-column
                  label="Type"
                  sortable
                  prop="type">
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
                  label="Amount"
                  sortable
                  prop="amount">
                  <template slot-scope="scope">{{ scope.row.amount|currency("¥") }}</template>
                </el-table-column>
                <el-table-column
                  label="Info">
                  <template slot-scope="scope">
                    <div v-if="scope.row.type=='DesendentOrderPoint'">

                      <i class="far fa-user-circle text-success"></i>&nbsp;&nbsp;{{ scope.row.info.username }} <br>
                      <nuxt-link :to="'/superadmin/orders/' + scope.row.info.order_id" class="action-iconk">
                        <i
                          class="fas fa-shopping-cart"></i>&nbsp;&nbsp;#{{
                          scope.row.info.order_id
                        }}-{{ scope.row.info.orderitem_id }}
                      </nuxt-link>
                    </div>


                    <div v-if="scope.row.type=='OrderBonus'">
                      <nuxt-link :to="'/superadmin/orders/' + scope.row.info.order_id" class="action-iconk">
                        <i
                          class="fas fa-shopping-cart"></i>&nbsp;&nbsp;#{{
                          scope.row.info.order_id
                        }}-{{ scope.row.info.orderitem_id }}
                      </nuxt-link>
                    </div>

                    <div v-if="scope.row.type=='PURCHASE_ORDER'">
                      <nuxt-link :to="'/superadmin/orders/' + scope.row.info.order_id" class="action-iconk">
                        <i class="ri-shopping-basket-2-fill"></i>&nbsp;&nbsp;#{{ scope.row.info.order_id }}
                      </nuxt-link>
                    </div>


                    <div v-if="scope.row.type=='INTRODUCE_POINT'">
                      <i class="fas fa-street-view"></i>&nbsp;&nbsp;{{ scope.row.info.username }}
                    </div>

                    <div v-if="scope.row.type=='TRANSFER_IN'">
                      <i class="ri-gift-fill text-warning"></i>&nbsp;&nbsp;{{ scope.row.info.username }}
                    </div>
                    <div v-if="scope.row.type=='TRANSFER_OUT'">
                      <i class="ri-hand-heart-fill text-success"></i>&nbsp;&nbsp;{{ scope.row.info.username }}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  label="Date"
                  sortable
                  width="100"
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

                    <a href="javascript:void(0);" @click="updateMarginValid(scope.row.id)"
                       v-if="!scope.row.is_valid">
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

              <div class="row my-2" v-if="marginlist_toBeApproved_meta.total_results">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="marginlist_toBeApproved_meta.total_results"
                                    :per-page="per_page"
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
  </b-tab>
</template>
