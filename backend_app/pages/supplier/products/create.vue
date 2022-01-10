<script>
import {swalService} from "~/helpers/swal.service"
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import {mapState, mapGetters} from "vuex";
import {axios} from "@/plugins/axios";

export default {
  middleware: ['router-auth', 'router-supplier'],
  name:"add_product",
  head() {
    return {
      title: `${this.title} | WAVUS PINGO`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    VariationTable: () => import('./components/VariationTable'),
    BasicProductInfo: () => import('./components/BasicProductInfo'),
    ProductImageEditor: () => import('./components/ProductImageEditor'),
  },
  data() {
    return {
      title: "新規紹介製品登録",
      items: [
        { text: "PinGO", },
        { text: "eCommerce", },
        { text: "新規紹介製品登録", active: true, },
      ],
      product: {
        id: 0,
        item_name: "item_name",
        type: "REGULAR",
        rate: 4,
        is_valid: false,
        is_matched: false,
        label: "NO",
        brand: "brand",
        series: "series",
        model: "model",
        image: "",
        sort_by: 0,
        video_url: "video_url",
        description: "description",
        package: "package",
        category: {id: 0},
        supplier: {id: 0, name: ""}
      }
    };
  },
  computed: {
    ...mapGetters({
      mySupplierInfo: "suppliers/getterSupplier",
    }),
  },
  methods: {
    operateVariationTable(result) {
      switch (result.command) {
        case "addVariation":
          this.AddVariation(result.variation);
          break;
        case "editVariation":
          this.ReplaceVariation(result.variation);
          break;
        case "replaceVariation":
          this.ReplaceVariation(result.variation);
          break;
        case "deleteVariation":
          this.deleteVariation(result.variation);
          break;

      }
    },
    AddVariation(_variation) {
      this.product.item_variations.unshift(_variation)
      swalService.showModal("Success", "Variation has been successfully added!", "success")
    },
    ReplaceVariation(_variation) {
      let vm = this;
      if (vm.product.item_variations.length === 0) {
        vm.product.item_variations.push(_variation)
      } else {
        var index = vm.product.item_variations.findIndex(variation => variation.id === _variation.id)
        if (index > -1) {
          vm.product.item_variations.splice(index, 1, _variation);
          swalService.showModal("Success", "Variation has been successfully updated!", "success")
        }
      }
    },
    deleteVariation(variation_id) {
      var vm = this;
      this.$store.dispatch("products/delete_variation", variation_id).then((response) => {

        if (response.result) {
          var index = vm.product.item_variations.findIndex(variation => variation.id === variation_id)
          if (index > -1) {
            vm.product.item_variations.splice(index, 1);
          }
          swalService.showModal("Success", "Variation has been deleted successfully updated!", "success")
          vm.$bvModal.hide("modal_variation")
        }
      })
    },
    CreateProductResult(info) {
      if (info.result) {
        this.product = info.product;
      }
    }
  },
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>

    <div class="row">
      <div class="col-lg-12">
        <BasicProductInfo  @optResult="CreateProductResult"/>
      </div>
    </div>

    <div class="row" v-if="product.id">
      <div class="col-lg-12">
        <ProductImageEditor :product="product"/>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-12">
        <VariationTable :variations="product.item_variations" :product_id="product.id"
                        @operateTable="operateVariationTable" v-if="product.id"></VariationTable>
      </div>
    </div>
  </div>
</template>
