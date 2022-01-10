<script>
import Swal from 'sweetalert2'
import {swalService} from "~/helpers/swal.service";
import {marginService} from "~/helpers/margin.service"

export default {
  name: "order_detail_marginboard",
  props: ["margins"],
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
  },
  computed: {
    total_margin() {
      return this.margins.reduce((prev, current) => prev + current.amount, 0)
    },
  },
  methods: {
    async deleteMargin(margin_id) {
      let self = this;
      await Swal.fire({
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
                return {result: true}
              });
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.result) {
          self.$emit("marginRemoved", margin_id)
        }
      })
    },
    async updateMargin(margin) {
      if (margin.pointbank_saved) return false;

      let self = this;
      const margin_id = margin.id;

      const {value: amount} = await Swal.fire({
        icon: "question",
        title: 'ポイント変更',
        input: 'number',
        showCancelButton: true,
        inputValidator: (value) => {
          if (!value) {
            return 'You need to write something!'
          }
        }
      })

      if (parseInt(amount) > 0) {
        let margin_ids = []
        margin_ids.push(margin_id)
        let info = {
          margin_ids: margin_ids,
          update_fields: ["amount"],
          amount: parseInt(amount)
        }
        marginService.batch_update(info)
          .then(response => {
            self.$emit("marginUpdated", response.margins[0])
          })
      }
    },
    async updateMargin_valid(margin_id, valid_flag) {
      let self = this;
      let margin_ids = []
      margin_ids.push(margin_id)
      let info = {
        margin_ids: margin_ids,
        update_fields: ["is_valid"],
        is_valid: valid_flag
      }

      await Swal.fire({
        title: '再確認?',
        html: "有効にしたら、戻せないので、大丈夫でしょうか？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、有効に!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            return marginService.batch_update(info)
              .then(response => {
                return {result: true, update_margin: response.margins[0]}
              })
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.result) {
          self.$emit("marginUpdated", result.value.update_margin)
        }
      })
    },
  }

};
</script>

<template>
  <div>
    <h4 class="font-15 mb-2">ポイント付与一覧
      <span class="badge badge-outline-danger badge-warning float-right">
                          {{ total_margin|currency("¥") }}</span>
    </h4>
    <div class="card p-2 mb-lg-0">
      <el-table
        class="table table-centered border table-nowrap mb-lg-0"
        :data="margins"
        :default-sort="{prop: 'user', order: 'descending'}"
        style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <div class="row mb-3">
              <div class="col-lg-6">
                <h6 class="m-0">ポイント詳細情報：</h6>
                <p>{{props.row.info}}</p>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="会員" sortable prop="user">
          <template slot-scope="scope">
            {{ scope.row.user.username }}
            <i :class="{'ri-user-voice-fill text-danger':scope.row.info.level==='SUPERADMIN',
                                          'ri-team-fill  text-warning':scope.row.info.level==='CLIENTADMIN',
                                          'ri-user-heart-line  text-primary':scope.row.info.level==='LEVEL_1',
                                          'ri-map-pin-user-fill  text-default':scope.row.info.level==='USER_SELF',
                                          'ri-parent-fill  text-success':scope.row.info.level==='LEVEL_2',}"></i>
            <br>
            (#{{ scope.row.id }})
          </template>
        </el-table-column>
        <el-table-column
          label="Level"
          align="right"
          prop="info.level">
        </el-table-column>
        <el-table-column
          label="ポイント数"
          align="right"
          prop="amount">
          <template slot-scope="scope">
            <a href="javascript:void(0);" @click="updateMargin(scope.row)">
              {{ scope.row.amount|currency("¥") }}
            </a>
          </template>
        </el-table-column>
        <el-table-column
          label="OrderItem"
          align="right"
          sortable
          prop="info.orderitem_id">
          <template slot-scope="scope">
            #{{ scope.row.info.orderitem_id }}
            <a href="javascript:void(0);" @click="deleteMargin(scope.row.id)" v-if="!scope.row.pointbank_saved">
              <i class="fe-trash text-danger"></i>
            </a>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          prop="pointbank_saved">
          <template slot-scope="scope">
            <a href="javascript:void(0);" @click="updateMargin_valid(scope.row.id, false)"
               v-if="scope.row.pointbank_saved">
              <i class="ri-checkbox-circle-fill text-success"></i>
            </a>
            <a href="javascript:void(0);" @click="updateMargin_valid(scope.row.id, true)" v-else>
              <i class="ri-close-circle-fill text-danger"></i>
            </a>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
