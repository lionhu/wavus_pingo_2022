<script>
import {swalService} from "~/helpers/swal.service"
import {mapState, mapGetters} from "vuex";
import Swal from "sweetalert2";
import {APIServices} from "@/helpers/APIs";

export default {
  name: "edit_product_variation_table",
  props: ["variations", "product_id"],
  components: {
    Switches: () => import('vue-switches'),
    "el-upload": () => import("element-ui/lib/upload"),
    VariationModal: () => import('./VariationModal'),
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
    csrftoken() {
      return this.$auth.strategy.token.get();
    },
  },
  methods: {
    switchAddVariationMode() {
      this.modeAdd = true;
      this.showVariationModal = true;
    },
    deleteVariation(variation_id) {
      this.$emit("operateTable", {"command": "deleteVariation", "variation": variation_id})
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
        this.$emit("operateTable", {"command": "replaceVariation", "variation": res.data})
      }
    },

    VariationOperate({modeAdd, _variation}) {
      let vm = this;
      console.log("VariationOperate", _variation)
      if (!modeAdd) {
        this.$emit("operateTable", {command: "editVariation", variation: _variation})
        // }
      } else {
        this.$emit("operateTable", {command: "addVariation", variation: _variation})
      }
      vm.showVariationModal = false;
    }
  }
};
</script>
<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="row">
          <div class="col-md-6">登録したバリエーション</div>
          <div class="col-md-6">
            <button class="btn btn-warning mb-2 float-right" v-b-modal.modal_variation_component
                    @click="switchAddVariationMode"><i
              class="mdi mdi-plus-circle mr-1"></i> バリエーションの追加
            </button>
          </div>
        </div>
        <div class="row">
          <div class="table-responsive">
            <table class="table table-bordered table-centered mb-0">
              <thead class="thead-light">
              <tr>
                <th>商品名</th>
                <th>順番</th>
                <th>在庫</th>
                <th>卸価格 </th>
                <th></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="variation in variations">
                <td class="text-center">
                  {{ variation.name }} <br>
                  <el-upload
                    class="avatar-uploader"
                    :action="getUploadVariationimageURL(variation.id)"
                    :show-file-list="false"
                    :headers="{'Authorization':csrftoken}"
                    :on-success="handleVariationImageSuccess"
                    :name="'image'"
                    :before-upload="beforeAvatarUpload">
                    <img v-if="variation.image_url" :src="variation.image_url"
                         class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                </td>
                <td class="text-center">
                  <b-badge variant="danger" pill>{{ variation.sort_by }}</b-badge>
                </td>
                <td class="text-center">
                  <span class="d-block">{{ variation.inventory }}</span>
                </td>
                <td class="text-right">
                  <span class="d-block text-danger">{{ variation.purchase_price|currency("¥") }}</span>
                </td>
                <td class="align-items-center">
                  <a href="javascript:void(0);" @click="editVariation(variation)"
                     v-b-modal.modal_variation_component
                     class="action-icon">
                    <i class="fe-edit"></i></a>
                  <a href="javascript:void(0);" @click="deleteVariation(variation.id)" class="action-icon">
                    <i class="fe-trash"></i></a>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <VariationModal @operateresult="VariationOperate" :showVariationModal="showVariationModal"
                    :modeAdd="modeAdd"
                    :edit_variation="edit_variation" :product_id="product_id"></VariationModal>
  </div>

</template>
