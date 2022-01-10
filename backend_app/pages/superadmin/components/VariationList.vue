<script>
import {swalService} from "~/helpers/swal.service"
import {mapState, mapGetters} from "vuex";
import Swal from "sweetalert2";
import {APIServices} from "@/helpers/APIs";

export default {
  name: "variation_table",
  props: ["variations"],
  components: {
    Switches: () => import('vue-switches'),
    "el-upload": () => import("element-ui/lib/upload"),
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    VariationModal: () => import('../variations/components/VariationModal'),
  },
  data() {
    return {
      showVariationModal: false,
      modeAdd: false,
      edit_variation: {
        price: 0,
        purchase_price: 0,
        name: "",
        description: "",
        variation_type: "REGULAR",
        inventory: 0,
        sort_by: 0,
        point_rule: {
          is_valid: false,
          type: "amount",
          policies: {
            client_superadmin: 0,
            client_admin: 0,
            level_2: 0,
            level_1: 0,
            user_self: 0
          },
          special_promotion: {
            is_valid: false,
            bonus: 0
          }
        },
      },
    };
  },
  computed: {
    ...mapGetters({}),
    csrftoken() {
      return this.$store.state.auth.user.token;
    },
  },
  methods: {

    VariationOperate({modeAdd, _variation}) {
      this.$emit('ReplaceVariation', _variation)
      this.showVariationModal=false;
    },
    Inventory_Operations(variation, opt) {
      let vm = this;
      let _tilte = opt === "plus" ? "在庫追加" : "在庫削除";
      let data = {
        variation: variation.id,
        type: opt === "plus" ? "BS" : "RS",
        in_out: opt === "plus" ? 1 : -1,
        quantity: 0,
        info: opt === "plus" ? "buy stock from supplier" : "return stock to supplier"
      }
      console.log(data)
      Swal.fire({
        title: _tilte,
        input: 'number',
        inputAttributes: {
          autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: '確定',
        showLoaderOnConfirm: true,
        preConfirm: (stock) => {
          if (stock > 0) {
            data.quantity = stock
            return APIServices.post("store/public/inventory/", data)
              .then(APIServices.handleResponse)
              .then(response => {
                return response
              }).catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          } else {
            return null;
          }

        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        if (result.isConfirmed && result.value !== null) {
          APIServices.get(`store/public/variations/${result.value.variation}/`)
            .then(APIServices.handleResponse)
            .then(response => {
              let index = vm.variations.findIndex(variation => variation.id === result.value.variation)

              console.log("index", index)
              if (index > -1) {
                vm.variations[index].inventory = response.inventory
              }
              swalService.showToast("success", "在庫は更新されました！")
            })
        }
      })
    },
    switchAddVariationMode() {
      this.modeAdd = true;
      this.showVariationModal = true;
    },
    editVariation(variation) {
      this.edit_variation = variation;
      this.modeAdd = false;
      this.showVariationModal = true;
    },
    getUploadVariationimageURL(id) {
      return `https://www.pingo.jp/daphne/api/store/public/variations/${id}/update_image/`
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;
      // return isLt2M;
      if (!isLt2M || !isJPG) {
        swalService.showModal("Invalid picture", "Should be JPEG and below 2M", "warning")
        return false
      }
      return isJPG && isLt2M;
      // return isJPG && isLt2M;
    },
    handleVariationImageSuccess(res, file) {
      if (res.result) {
        this.ReplaceVariation(res.data)
      }
    },

  }
};
</script>
<template>

  <div class="table-responsive">
    <el-table :data="variations"
              style="width: 100%"
              :header-cell-style="{textAlign: 'center'}"
    >
      <el-table-column width="250" sortable prop="id">
        <template slot-scope="scope">
          <el-upload
            class="avatar-uploader"
            :action="getUploadVariationimageURL(scope.row.id)"
            :show-file-list="false"
            :headers="{'Authorization':csrftoken}"
            :on-success="handleVariationImageSuccess"
            :name="'image'"
            :before-upload="beforeAvatarUpload">
            <img v-if="scope.row.thumbimage_url" :src="scope.row.thumbimage_url" style="max-width:160px;"
                 class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </template>
      </el-table-column>
      <el-table-column width="250" label="商品名" sortable prop="id">
        <template slot-scope="scope">
          {{ scope.row.item.item_name }} <br>
          --{{ scope.row.name }} <b-badge variant="primary" pill >#{{ scope.row.id }}</b-badge> <br>
          <b-badge variant="success" pill v-if="scope.row.is_valid">有効</b-badge>
          <b-badge variant="danger" pill v-else>無効</b-badge>
        </template>
      </el-table-column>
      <el-table-column
        label="在庫"
        sortable
        width="100"
        prop="rate">
        <template slot-scope="scope">
          <span class="d-block text-center">{{ scope.row.inventory }}</span>
          <a href="javascript:void(0);" class="btn btn-warning d-block" @click="Inventory_Operations(scope.row,'plus')">+</a>
          <a href="javascript:void(0);" class="btn btn-danger d-block" @click="Inventory_Operations(scope.row,'minus')">-</a>
        </template>
      </el-table-column>
      <el-table-column
        label="価格"
        sortable
        align="right"
        prop="is_valid">
        <template slot-scope="scope">
          <span class="d-block text-right">{{ scope.row.price|currency("¥") }}(販売)</span>
          <span class="d-block text-right text-danger">{{ scope.row.purchase_price|currency("- ¥") }}(仕入)</span>
          <span class="d-block text-right text-danger">{{ scope.row.extra_cost|currency("- ¥") }}(付加)</span>
        </template>
      </el-table-column>
      <el-table-column
        label="ポイントポリシー"
        sortable
        prop="is_valid">
        <template slot-scope="scope">
          <div v-if="scope.row.point_rule.is_valid">
                    <span class="d-inline-block text-right  mr-3">{{
                        $t("menuitems.organizations.user.client_superadmin")
                      }}:</span>{{ scope.row.point_rule.policies.client_superadmin|currency("¥") }} <br>
            <span class="d-inline-block  text-right  mr-3">{{
                $t("menuitems.organizations.user.client_admin")
              }}:</span>{{ scope.row.point_rule.policies.client_admin|currency("¥") }} <br>
            <span class="d-inline-block  text-right mr-3">{{
                $t("menuitems.organizations.user.level_2")
              }}:</span>{{ scope.row.point_rule.policies.level_2|currency("¥") }} <br>
            <span class="d-inline-block  text-right mr-3">{{
                $t("menuitems.organizations.user.level_1")
              }}:</span>{{ scope.row.point_rule.policies.level_1|currency("¥") }} <br>
            <span class="d-inline-block text-right mr-3">{{
                $t("menuitems.organizations.user.user_self")
              }}:</span>{{ scope.row.point_rule.policies.user_self|currency("¥") }}
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="Action">
        <template slot-scope="scope">

          <a href="javascript:void(0);" @click="editVariation( scope.row)"
             v-b-modal.modal_variation_component
             class="action-icon">
            <i class="fe-edit"></i></a>
        </template>
      </el-table-column>
    </el-table>
    <VariationModal @operateresult="VariationOperate" :showVariationModal="showVariationModal"
                    :edit_variation="edit_variation"></VariationModal>
  </div>

</template>
