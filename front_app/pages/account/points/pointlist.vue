<template>
  <b-card-text>
    <div class="dashboard-right">
      <div class="dashboard">
        <div class="box-account box-info row">
          <div class="box-head col-lg-6 col-xs-12" v-if="canTransferPoint">
            <h3>{{ $t('point_menu.title') }}</h3>
            <p>{{ $t('piontlist_menu.found_records', [pointlist_meta.total]) }}</p>
            <p>{{ $t('pointlist.walletID') }}: <br>
              <span class="theme-color">{{ ME.profile.introcode }}</span>
            </p>

            <b-button variant="warning" size="sm" @click="transfer_margin_preconfirm">{{
                $t("pointlist.point_transfer")
              }}
            </b-button>
            <!--            <p>{{ $t('cart_info.total') }} {{ TotalPoint | currency("¥") }}</p>-->
          </div>
        </div>

        <div class="box-account box-info">
          <div>
            <div class="box">
              <div class="row">
                <div class="col-sm-6">
                  <div class="box">
                    <div class="box-title">
                      <h3>{{ $t("pointlist.valid_point") }}</h3>
                      <a href="#">{{ ME.profile.pointbank_balance | currency('') }}</a>
                    </div>
                    <div class="box-content">
                      <p v-html="$t('pointlist.valid_point_info')"></p>
                    </div>
                    <!--                    <div class="box-title">-->
                    <!--                      <h3>{{ $t("pointlist.invalid_point") }}</h3>-->
                    <!--                      <a href="javascript:void(0);">{{ InvalidPoint != null ? InvalidPoint : 0 | currency('') }}</a>-->
                    <!--                    </div>-->
                    <!--                    <div class="box-content">-->
                    <!--                      <p v-html="$t('pointlist.invalid_point_info')"></p>-->
                    <!--                    </div>-->
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="box">

                    <div class="box-title">
                      <h3>期限切れポイント</h3>
                      <!--                      <a href="#">{{ ValidPoint|currency('') }}</a>-->
                    </div>
                    <div class="box-content" v-if="PointSummary && PointSummary.length">
                      <el-table ref="filterTable" stripe
                                :show-header="false"
                                :data="PointSummary"
                                style="width: 100%">
                        <el-table-column prop="due_date" :label="$t('date')" sortable>
                          <template slot-scope="scope">
                            {{ scope.row.due_date | short_date }}
                          </template>
                        </el-table-column>
                        <el-table-column prop="sum" :label="$t('pointlist.point')">
                          <template slot-scope="scope">
                            {{ scope.row.sum | currency("¥") }}
                          </template>
                        </el-table-column>
                      </el-table>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row mt-2 " v-if="pointlist_meta.total">
                <el-table ref="filterTable"
                          :row-class-name="tableRowClassName"
                          :data="pointlist"
                          style="width: 100%">
                  <el-table-column prop="created_at" :label="$t('date')" sortable>
                    <template slot-scope="scope">
                      {{ scope.row.created_at | short_date }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="amount" :label="$t('pointlist.point')">
                    <template slot-scope="scope">
                      <span :class="'text-'+point_type_class(scope.row.type )">
                        {{ $t(`pointlist.point_type.${scope.row.type}.amount_prefix`) }} {{scope.row.amount | currency("¥")}}
                      </span>
                      <font-awesome-icon :icon="['fas','check-circle']"
                                         :class="{'text-warning':scope.row.pointbank_saved,'text-default':!scope.row.pointbank_saved}">
                      </font-awesome-icon>
                    </template>
                  </el-table-column>
                  <!--                  <el-table-column prop="is_valid" :label="$t('pointlist.valid')">-->
                  <!--                    <template slot-scope="scope">-->
                  <!--                      <i :class="{'ti-check text-success':scope.row.is_valid,-->
                  <!--                                'ti-close text-danger':!scope.row.is_valid}"></i>-->
                  <!--                    </template>-->
                  <!--                  </el-table-column>-->
                  <el-table-column prop="info.username" :label="$t('followers.text')">
                  </el-table-column>
                  <el-table-column
                    prop="type"
                    :label="$t('type')"
                    :filters="margin_filters"
                    :filter-method="filterTag"
                    filter-placement="bottom-end">
                    <template slot-scope="scope">
                      <el-tag :type="$t(`pointlist.point_type.${scope.row.type}.type_class`)"
                              disable-transitions>{{ $t(`pointlist.point_type.${scope.row.type}.title`) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                </el-table>
              </div>

              <div class="row my-2" v-if="pointlist_meta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="pointlist_meta.total"
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
  </b-card-text>
</template>

<script>

import {mapState, mapGetters} from "vuex"
import {APIServices} from "~/helpers/APIs";

export default {
  data() {
    return {
      order: {},
      showCreditModal: false,
      page: 1,
      page_size: 100,
      total: 0,
      margin_filters: [
        {text: '会員加入', value: 'JOINBONUS_POINT'},
        {text: 'ポイント注文取消', value: 'ORDER_CANCELED'},
        {text: 'メンバー入会紹介', value: 'INTRODUCE_POINT'},
        {text: '購入利用', value: 'PURCHASE_ORDER'},
        {text: '購入取得ボーナス', value: 'OrderBonus'},
        {text: '製品紹介購入', value: 'DesendentOrderPoint'},
        {text: 'ポイント譲渡', value: 'TRANSFER_OUT'},
        {text: 'ポイント受取', value: 'TRANSFER_IN'},
      ],
      transferPointInfo: {
        toUserSlug: "",
        points: 0
      },
      monthlyhistory: [],
    }
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME",
      pointlist: "points/getterPointList",
      pointlist_meta: "points/getterPointListMeta",
      PointSummary: "points/getterPointSummary",
    }),
    canTransferPoint() {
      return this.ME.profile.pointbank_balance && this.ME.profile.can_transfer_point;
    }
  },
  watch: {
    pointlist_meta(newVal, oldVal) {
      this.page = newVal.page;
      this.page_size = newVal.page_size;
      this.total = newVal.total;
    }
  },
  mounted() {
    this.load_margins("me/");
  },
  methods: {
    load_margins(options) {
      this.$store.dispatch("points/load_point_list", options);
      this.$store.dispatch("points/load_pointhistory_summary")
    },
    transfer_margin(toUserSlug, toUserName, maxPoints) {
      // 86ab92ec-1b91-40b8-ab20-921396e193b8-33
      let vm = this;
      this.$swal.fire({
        title: `${toUserName}　へ贈呈ポイント数`,
        input: 'range',
        inputLabel: `お持ちポイント数: ${maxPoints}`,
        inputAttributes: {
          min: 0,
          max: maxPoints,
          step: 100
        },
        inputValue: 100,
        showCancelButton: true,
        showLoaderOnConfirm: true,
        allowOutsideClick: () => false,
        preConfirm: (transferPoints) => {
          if (transferPoints && maxPoints >= transferPoints) {

            return vm.$axios.post("/back/store/api/margins/transfer/", {
              "toUserSlug": toUserSlug,
              "point": transferPoints
            }).then((res) => {
              if (res.data.result) {
                return {result: true, transferPoints: transferPoints, toUserName: toUserName};
              } else {
                throw new Error(`贈呈はできませんでした。管理者にご連絡ください。`)
              }
            }).catch(error => {
              vm.$swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
          }
        },
      }).then((result) => {
        if (result.isConfirmed) {
          let options = `?page=${this.page}&page_size=${this.page_size}`
          vm.load_margins(options);
          vm.$swal.fire(
            '成功!',
            `${result.value.transferPoints} ポイントは${result.value.toUserName}に贈呈いたしました。`,
            'success')
        }
      })

    },
    async transfer_margin_preconfirm() {
      let vm = this;
      this.$swal.fire({
        title: vm.$t('pointlist.receiver_walletID'),
        input: 'text',
        inputAttributes: {
          autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: vm.$t('checkout.confirm'),
        cancelButtonText: vm.$t('checkout.cancel'),
        showLoaderOnConfirm: true,
        preConfirm: (toUserSlug) => {
          return vm.$axios.post(`/back/store/api/margins/pre_confirm/`,
            {"toUserSlug": toUserSlug})
            .then(response => {
              if (!response.data.result) {
                throw new Error(response.data.message)
              }
              return response.data.data
            })
            .catch(error => {
              vm.$swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        if (result.isConfirmed) {
          vm.transfer_margin(result.value.data_toUserSlug, result.value.info.to_username, result.value.validpoint);
        }
      })
    },
    tablePageChange(currentPage) {
      this.page = currentPage;
      let options = `?page=${this.page}&page_size=${this.page_size}`;
      this.load_margins(options);
    },

    filterTag(value, row) {
      return row.type === value;
    },
    amount_prefix(type) {

      let amount_prefix = `pointlist.point_type.${type}.amount_prefix`

      return this.$t(amount_prefix)
    },
    point_type_class(type) {
      let type_class = `pointlist.point_type.${type}.type_class`
      return this.$t(type_class)
    },
    point_type_text(type) {
      let title = `pointlist.point_type.${type}.title`
      return this.$t(title)
    },
    tableRowClassName({row, rowIndex}) {
      if (row.is_refound === -1) {
        return 'warning-row';
      }
      return '';
    }

  },

}
</script>

<style scoped>
h4 span.cont {
  float: right;
}

.swal2-title {
  font-size: 1rem !important;
}

.swal2-file, .swal2-input, .swal2-textarea {
  font-size: 0.5rem !important;
}

.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}

.el-table__empty-block {
  display: none !important;
}
</style>
