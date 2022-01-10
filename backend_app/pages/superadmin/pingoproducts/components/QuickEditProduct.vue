<script>
import {mapGetters, mapState} from "vuex"
import {swalService} from "~/helpers/swal.service"

export default {
  name: "quick_edit_product",
  props: ["product", "mode", "showModal"],
  components: {
    Switches: () => import('vue-switches'),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    "el-select": () => import('element-ui/lib/select'),
    "el-rate": () => import('element-ui/lib/rate'),
    "el-dialog": () => import('element-ui/lib/dialog'),
    "el-option": () => import('element-ui/lib/option'),
    "el-cascader": () => import('element-ui/lib/cascader'),
    "el-form": () => import('element-ui/lib/form'),
    Category: () => import('../../components/CategoryModal'),


  },
  data() {
    return {
      submitted: false,
      dropdown_props: {
        label: "title",
        value: "id"
      },
      edit_category: false,
    };
  },
  computed: {
    ...mapGetters({
      categorylist: "categories/getterCategoryList"
    }),
    ...mapState({
      vendorlist: state => state.system.vendorlist,
      backend_server: state => state.system.backend_server
    }),
  },
  watch: {
    product(newval, oldval) {
      console.log("watch edit product", newval.item_name)
    }
  },
  methods: {
    updateProductInformation() {
      let vm = this;

      var product_edititems = {
        id: this.product.id,
        item_name: this.product.item_name,
        sort_by: parseInt(this.product.sort_by),
        rate: this.product.rate,
        is_valid: this.product.is_valid,
        vendor_id: this.product.vendor_id?this.product.vendor_id:this.product.vendor.id,
        category_id: this.product.category_id?this.product.category_id:this.product.category.id,
      }
      console.log(product_edititems)
      this.$store.dispatch("products/update_productinfo", product_edititems)
        .then((res_product) => {
          console.log(res_product)
          swalService.showToast("success", "Updated successfully!")

          vm.$emit("updateResult", {result: true, product: res_product})
        })
      vm.$emit("updateResult", {result: false, product: null})
    },
    handleCategoryChange(values) {
      this.product.category_id = values[values.length - 1];
    },
  },
};
</script>

<template>
  <b-modal id="modal-quick-editproduct" scrollable title="Edit Product Information" title-class="font-18"
           body-class="p-4" hide-footer v-if="showModal">
    <form @submit.prevent="updateProductInformation">
      <div class="row mb-3">
        <div class="col-md-6">
          <label for="field-sort_by" class="control-label">Sort ID:
            <span class="text-danger">*</span>
          </label>
          <input type="number" id="field-sort_by" v-model="product.sort_by" class="form-control"
                 :class="{ 'is-invalid': submitted && $v.product.sort_by.$error }"
                 :placeholder="product.sort_by"/>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <b-form-group id="field-is_valid" label-cols="4" label-cols-lg="4" label-size="sm" label="Active">
            <switches v-model="product.is_valid" id="field-is_valid" type-bold="false" color="warning"
                      class="ml-1 my-auto"></switches>
          </b-form-group>
        </div>
        <div class="col-md-6">
          <b-form-group id="field-rate" label-cols="4" label-cols-lg="4" label-size="sm" label="Rate">
            <el-rate v-model="product.rate"></el-rate>
          </b-form-group>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-item_name" class="control-label">Name
              <span class="text-danger">*</span>
            </label>
            <input type="text" id="field-item_name" v-model="product.item_name" class="form-control"
                   :class="{ 'is-invalid': submitted && $v.product.item_name.$error }"
                   :placeholder="product.item_name"/>

            <div v-if="submitted && !$v.product.item_name.required" class="invalid-feedback">This value is required.
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label class="control-label">Vendor - ({{product.vendor.name}})<span class="text-danger">*</span></label>
            <el-select v-model="product.vendor_id" placeholder="请选择">
              <el-option
                v-for="item in vendorlist"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>


          </div>
        </div>
        <div class="col-md-6">
          <label class="control-label">Category - ({{product.category.title}})<span class="text-danger">*</span></label>
          <el-cascader
            :options="categorylist[0].children"
            :props="dropdown_props"
            @change="handleCategoryChange"></el-cascader>
        </div>
      </div>
      <div class="form-group row">
        <div class="col-8 offset-4">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </div>
    </form>

  </b-modal>
</template>
