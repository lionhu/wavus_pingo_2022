<script>
export default {
  name: "edit_product_variation",
  props: ["showVariationModal", "modeAdd", "edit_variation", "product_id"],
  components: {
    Switches: () => import('vue-switches'),
  },
  data() {
    return {
      submitted: false
    };
  },
  computed: {
  },
  methods: {
    updateProductVariationInformation() {
      var vm = this;
      this.edit_variation.item = this.product_id;
      this.edit_variation.purchase_price = parseInt(this.edit_variation.purchase_price);
      this.edit_variation.sort_by = parseInt(this.edit_variation.sort_by);

      if (!this.modeAdd) {
        let variation_id=this.edit_variation.id;
        delete this.edit_variation.image;
        console.log(variation_id,this.edit_variation)
        this.$store.dispatch("products/update_variation",
          {variation_id:variation_id,info:this.edit_variation})
          .then((response) => {
            console.log(response)
              vm.$emit("operateresult", {"modeAdd": false, "_variation": response, variation_id:variation_id})
          })
      } else {
        this.$store.dispatch("products/create_variation", this.edit_variation)
          .then((response) => {
            console.log("create_variation",response)
              // var variation_server = response.variation;
              vm.$emit("operateresult", {"modeAdd": true, "_variation": response})
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
           title="Edit Variation Information"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showVariationModal"
  >
    <form @submit.prevent="updateProductVariationInformation">
      <div class="row mt-md-2">
        <div class="col-md-6">
          <div class="form-group">
            <label for="product-sku" class="control-label">SKU
              <span class="text-danger">*</span>
            </label>
            <input type="text" v-model="edit_variation.sku" id="product-sku" class="form-control"
                   :placeholder="edit_variation.sku"/>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="product-sort">
              並び順番:
              <span class="text-danger">*</span>
            </label>
            <input type="number" v-model="edit_variation.sort_by" id="product-sort" class="form-control"
                   :placeholder="edit_variation.sort_by"/>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-item_name" class="control-label">バリュエーション名
              <span class="text-danger">*</span>
            </label>
            <input type="text" id="field-item_name" v-model="edit_variation.name" class="form-control"
                   :class="{ 'is-invalid': submitted && $v.edit_variation.name.$error }"
                   :placeholder="edit_variation.name"/>

            <div v-if="submitted && !$v.edit_variation.name.required" class="invalid-feedback">This value is required.
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-description" class="control-label">概要<span class="text-danger">*</span></label>
            <textarea id="field-description" v-model="edit_variation.description" class="form-control"
                      :placeholder="edit_variation.description"
                      :class="{ 'is-invalid': submitted && $v.edit_variation.description.$error }"/>

            <div v-if="submitted && !$v.edit_variation.description.required" class="invalid-feedback">This value is
              required.
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-4">
          <div class="form-group">
            <label for="field-purchase_price" class="control-label">卸価格
              <span class="text-danger">*</span>
            </label>
            <input type="number" id="field-purchase_price" v-model="edit_variation.purchase_price"
                   class="form-control"
                   :class="{ 'is-invalid': submitted && $v.edit_variation.purchase_price.$error }"
                   :placeholder="edit_variation.purchase_price"/>
            <div v-if="submitted && !$v.edit_variation.purchase_price.required" class="invalid-feedback">This value is
              required.
            </div>
          </div>
        </div>
        <div class="col-8">
          <button type="submit" class="btn btn-primary float-right">登録</button>
        </div>
      </div>
    </form>

  </b-modal>

</template>
