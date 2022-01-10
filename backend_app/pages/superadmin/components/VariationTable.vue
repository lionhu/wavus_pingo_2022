<script>
import {swalService} from "~/helpers/swal.service"
import {mapState, mapGetters} from "vuex";

export default {
  name: "edit_product_variation_table",
  props: ["variations"],
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
    ...mapGetters({
    }),
    csrftoken() {
      return this.$store.state.auth.user.token;
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
      return `${process.env.DJANGO_SERVER}/admin_back/api/variations/${id}/variationimage/`
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
      console.log(res)
      if (res.result) {
        let new_variation = res.variation.variation;
        this.$emit("operateTable", {"command": "replaceVariation", "variation": new_variation})
      }
    },

    VariationOperate({modeAdd, _variation}) {
      let vm = this;
      console.log("VariationOperate",_variation)
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
          <div class="col-md-6">Available Variations</div>
          <div class="col-md-6">
            <button class="btn btn-warning mb-2 float-right" v-b-modal.modal_variation_component
                    @click="switchAddVariationMode"><i
              class="mdi mdi-plus-circle mr-1"></i> Add Variation
            </button>
          </div>
        </div>
        <div class="row">
          <div class="table-responsive">
            <table class="table table-bordered table-centered mb-0">
              <thead class="thead-light">
              <tr>
                <th>name</th>
                <th>Order</th>
                <th>Inventory</th>
                <th>price</th>
                <th>point_rule</th>
                <th></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="variation in variations">
                <td class="text-center">
                  {{ variation.name }} <br>
                  <b-badge variant="primary" pill v-if="variation.variation_type==='REGULAR'">REGULAR
                  </b-badge>
                  <b-badge variant="warning" pill v-else>Pingo</b-badge>
                  <b-badge variant="success" pill class="d-block" >#{{ variation.id }}</b-badge>

                  <el-upload
                    class="avatar-uploader"
                    :action="getUploadVariationimageURL(variation.id)"
                    :show-file-list="false"
                    :headers="{'Authorization':csrftoken}"
                    :on-success="handleVariationImageSuccess"
                    :before-upload="beforeAvatarUpload">
                    <img v-if="variation.image_url" :src="variation.image_url"
                         class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                </td>
                <td class="text-center">
                  <b-badge variant="danger" pill>{{ variation.sort_by }}</b-badge>
                </td>
                <td class="text-center">{{ variation.inventory }}</td>
                <td class="text-right">
                  <span class="d-block">{{ variation.price|currency("¥") }}</span>
                  <span class="d-block">{{ variation.purchase_price|currency("¥") }}</span>
                </td>
                <td class="text-right">
                  <h5>
                    <span class="d-inline-block float-left">Introduction Point</span>
                    <b-badge variant="success float-right" pill v-if="variation.point_rule.is_valid">on
                    </b-badge>
                    <b-badge variant="danger float-right" pill v-else>off</b-badge>
                  </h5>
                  <div class="clearfix"></div>
                  <ul style="list-style-type: none;" v-if="variation.point_rule.is_valid">
                    <li>
                          <span
                            class="inline-block text-right mr-3">{{
                              $t("menuitems.organizations.user.client_superadmin")
                            }}:</span>
                      {{ variation.point_rule.policies.client_superadmin|currency("¥") }}
                    </li>
                    <li>
                          <span
                            class="inline-block text-right mr-3">{{
                              $t("menuitems.organizations.user.client_admin")
                            }}:</span>
                      {{ variation.point_rule.policies.client_admin|currency("¥") }}
                    </li>
                    <li>
                          <span
                            class="inline-block text-right mr-3">{{
                              $t("menuitems.organizations.user.level_2")
                            }}:</span>{{
                        variation.point_rule.policies.level_2|currency("¥")
                      }}
                    </li>
                    <li>
                          <span
                            class="inline-block text-right mr-3">{{
                              $t("menuitems.organizations.user.level_1")
                            }}:</span>{{
                        variation.point_rule.policies.level_1|currency("¥")
                      }}
                    </li>
                    <li>
                          <span
                            class="inline-block text-right mr-3">{{
                              $t("menuitems.organizations.user.user_self")
                            }}:</span>{{
                        variation.point_rule.policies.user_self|currency("¥")
                      }}
                    </li>
                  </ul>

                  <h5>
                    <span class="d-inline-block float-left">Spcial Promotion Bonus</span>
                    <b-badge variant="success float-right" pill
                             v-if="variation.point_rule.special_promotion.is_valid">on
                    </b-badge>
                    <b-badge variant="danger float-right" pill v-else>off</b-badge>
                  </h5>
                  <div class="clearfix"></div>
                  <ul style="list-style-type: none;" v-if="variation.point_rule.special_promotion.is_valid">
                    <li>
                          <span
                            class="inline-block text-right mr-3">{{
                              $t("menuitems.organizations.user.client_superadmin")
                            }}:</span>
                      {{ variation.point_rule.special_promotion.bonus|currency("¥") }}
                    </li>
                  </ul>
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
