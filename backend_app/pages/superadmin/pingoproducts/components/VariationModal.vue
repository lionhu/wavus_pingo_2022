<script>
import {pingoproductService} from "~/helpers/pingoproduct.service";
import Swal from "sweetalert2"

export default {
  name: "edit_product_variation",
  props: ["showVariationModal", "product","point_rule"],
  components: {
    Switches: () => import('vue-switches'),
  },
  data() {
    return {
      submitted: false,
      errors: []
    };
  },
  methods: {
    pre_check() {
      this.errors = [];
      if (this.point_rule.policies.user_self < 0) {
        this.errors.push("本人のポイントはマイナスになっていますか？")
      }

      return !this.errors.length;

    },
    updateProductPointRule() {
      let vm = this;
      if (this.pre_check()) {
        let info = {
          "id": this.product.id,
          "point_rule": this.point_rule
        }
        pingoproductService.superadmin_update(info).then(res => {
          vm.$emit("updatePointRule", res.point_rule)
        })
      } else {
        Swal.fire({
          title: "Data Errors",
          html: JSON.stringify(this.errors),
          icon: "error"
        })
      }
    },
  },
};
</script>

<template>

  <b-modal id="modal_variation_component"
           scrollable
           centered
           title="Edit Pingo Variation Information"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showVariationModal"
  >
    <div class="row mt-md-2">
      <div class="col-md-6">
        <div class="form-group">
          <label for="field-is_valid" class="control-label">有効
            <span class="text-danger">*</span>
          </label> <br>

          <switches v-model="point_rule.is_valid" id="field-is_valid" type-bold="false"
                    color="warning"
                    class="ml-1 my-auto"></switches>
        </div>
      </div>
    </div>

    <h4>紹介ポイント</h4>
    <div class="row">
      <div class="col-md-4">
        <div class="form-group">
          <label for="field-user_self" class="control-label">{{ $t("menuitems.organizations.user.user_self") }}
            <span class="text-danger">*</span>
          </label>
          <input type="number" id="field-user_self" v-model="point_rule.policies.user_self"
                 class="form-control"
                 :class="{ 'is-invalid': submitted && $v.point_rule.policies.user_self.$error }"
                 :placeholder="point_rule.policies.user_self"/>

          <div v-if="submitted && !$v.point_rule.policies.user_self.required"
               class="invalid-feedback">
            This value is required.
          </div>
        </div>
      </div>
    </div>
    <!--    <div class="row">-->
    <!--      <div class="col-md-4">-->
    <!--        <div class="form-group">-->
    <!--          <label for="field-client_admin"-->
    <!--                 class="control-label">{{ $t("menuitems.organizations.user.client_superadmin") }}-->
    <!--            <span class="text-danger">*</span>-->
    <!--          </label>-->
    <!--          <input type="number" id="field-client_superadmin"-->
    <!--                 v-model="point_rule.policies.client_superadmin"-->
    <!--                 class="form-control"-->
    <!--                 :class="{ 'is-invalid': submitted && $v.point_rule.policies.client_superadmin.$error }"-->
    <!--                 :placeholder="point_rule.policies.client_superadmin"/>-->

    <!--          <div v-if="submitted && !$v.point_rule.policies.client_superadmin.required"-->
    <!--               class="invalid-feedback">This value is required.-->
    <!--          </div>-->
    <!--        </div>-->
    <!--      </div>-->
    <!--      <div class="col-md-4">-->
    <!--        <div class="form-group">-->
    <!--          <label for="field-client_admin"-->
    <!--                 class="control-label">{{ $t("menuitems.organizations.user.client_admin") }}-->
    <!--            <span class="text-danger">*</span>-->
    <!--          </label>-->
    <!--          <input type="number" id="field-client_admin" v-model="point_rule.policies.client_admin"-->
    <!--                 class="form-control"-->
    <!--                 :class="{ 'is-invalid': submitted && $v.point_rule.policies.client_admin.$error }"-->
    <!--                 :placeholder="point_rule.policies.client_admin"/>-->

    <!--          <div v-if="submitted && !$v.point_rule.policies.client_admin.required"-->
    <!--               class="invalid-feedback">This value is required.-->
    <!--          </div>-->
    <!--        </div>-->
    <!--      </div>-->

    <!--      <div class="col-md-4">-->
    <!--        <div class="form-group">-->
    <!--          <label class="control-label">紹介ポイント合計-->
    <!--          </label>-->
    <!--          <b-button class="btn-rounded ml-1" variant="warning">{{ introduction_point_total|currency("¥") }}-->
    <!--          </b-button>-->
    <!--        </div>-->
    <!--      </div>-->
    <!--    </div>-->
    <div class="form-group row">
      <div class="col-8 offset-4">
        <button class="btn btn-primary" @click="updateProductPointRule">Submit</button>
      </div>
    </div>

  </b-modal>

</template>
