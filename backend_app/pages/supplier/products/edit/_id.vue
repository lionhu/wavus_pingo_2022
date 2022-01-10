<script>
import CKEditor from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import {swalService} from "~/helpers/swal.service"
import {mapState, mapGetters} from "vuex";
import {axios} from "@/plugins/axios";
import {APIServices} from "@/helpers/APIs";

export default {
  name: "edit_product",
  middleware: ['router-auth', 'router-supplier'],
  head() {
    return {
      title: `${this.title} | Pingo Admin`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    "el-select": () => import("element-ui/lib/select"),
    "el-rate": () => import("element-ui/lib/rate"),
    "el-dialog": () => import("element-ui/lib/dialog"),
    "el-upload": () => import("element-ui/lib/upload"),
    "el-option": () => import("element-ui/lib/option"),
    "el-cascader": () => import("element-ui/lib/cascader"),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    Switches: () => import('vue-switches'),
    VariationTable: () => import('../components/VariationTable'),
    ProductImageEditor: () => import('../components/ProductImageEditor'),
    ckeditor: CKEditor.component,
  },
  data() {
    return {
      title: "商品情報",
      items: [
        {text: "PINGO",},
        {text: "eCommerce",},
        {text: "商品情報", active: true,}
      ],
      editor: ClassicEditor,
      // editorData: "<p>Content of the editor.</p>",
      labels: [
        {value: 'NW', label: 'New'},
        {value: 'BS', label: 'Best Seller'}
      ],
      image: "",
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      imageUrl: "",
      submitted: false,
      product: {}
    };
  },
  mounted() {
    if (this._product_id > 0) {
      this.load_product(this._product_id)
    } else {
      this.$router.push("/supplier/products/")
    }
  },
  computed: {
    ...mapGetters({
      mySupplierInfo: "suppliers/getterSupplier",
      categories: "categories/getProductCategories",
      _product_id: "products/getterProductID",
    }),
  },
  methods: {
    load_product(product_id) {
      let vm = this;
      this.$store.dispatch("products/load_product", product_id)
        .then(response => {
          vm.product = response.item;
          vm.product.category = response.item.category.id;
        })
    },
    handleCategoryChange(val) {
      let index = val.length - 1;
      this.product.category = val[index]
    },
    async update_product() {
      let product_id = this.product.id;
      this.product.supplier = this.mySupplierInfo.id;
      this.product.is_valid = false;
      delete this.product.id;
      delete this.product.image;
      delete this.product.item_sliderimages;
      delete this.product.item_variations;
      delete this.product.created_at;
      delete this.product.labels;

      let vm = this;

      vm.$nuxt.$loading.start();
      await this.$store.dispatch("products/update_product", {
        product_id: product_id,
        info: this.product
      }).then(item => {
        vm.load_product(product_id)
        swalService.showModal("Success", "Product was updated!", "success")
      })

      vm.$nuxt.$loading.finish();
    },


    operateVariationTable(result,) {
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
      let url = `store/public/variations/${variation_id}/`
      var vm = this;
      APIServices.destroy(url)
        .then(APIServices.handleResponse)
        .then((response) => {
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
        <div class="card">
          <div class="card-body">
            <h4 class="header-title">
              基本情報(商品ID #{{ product.id }})
              <b-badge variant="success" pill v-if="product.is_valid">有効</b-badge>
              <b-badge variant="warning" pill v-else>審査中</b-badge>
            </h4>
            <p class="sub-header">下記の基本情報を入力してください。</p>
            <p class="theme-color">データー修正された場合、一旦「審査中」な状態になり、審査後「有効」になります。ご了承ください。</p>
            <div>
              <div class="row">
                <div class="col-md-6">

                  <div class="form-group mb-3">
                    <label for="product-category">
                      カテゴリー
                      <span class="text-danger">*</span>
                    </label>
                    <el-cascader
                      id="product-category"
                      v-model="product.category"
                      :options="categories"
                      size="large"
                      :show-all-levels="false"
                      :props="{ expandTrigger: 'hover',multiple:false,label:'title',value:'id'}"
                      @change="handleCategoryChange"></el-cascader>
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-4">

                  <label for="product-brand">
                    ブランド
                    <span class="text-danger">*</span>
                  </label>
                  <input type="text" v-model="product.brand" id="product-brand" class="form-control"
                         :placeholder="product.brand"/>
                </div>
                <div class="col-md-4">

                  <label for="product-Series">
                    シリーズ
                    <span class="text-danger">*</span>
                  </label>
                  <input type="text" v-model="product.series" id="product-Series" class="form-control"
                         :placeholder="product.series"/>
                </div>
                <div class="col-md-4">

                  <label for="product-model">
                    モデル
                    <span class="text-danger">*</span>
                  </label>
                  <input type="text" v-model="product.model" id="product-model" class="form-control"
                         :placeholder="product.model"/>
                </div>
              </div>

              <div class="form-group mb-3">
                <label for="product-name">
                  商品名
                  <span class="text-danger">*</span>
                </label>
                <input type="text" v-model="product.item_name" id="product-name" class="form-control"
                       placeholder="e.g : Apple iMac"/>
              </div>
              <div class="form-group mb-3">
                <label for="product-video_url">
                  ビデオURL
                  <span class="text-danger">*</span>
                </label>
                <input type="text" v-model="product.video_url" id="product-video_url" class="form-control"
                       placeholder="e.g : Apple iMac"/>
              </div>
              <div class="form-group mb-3">
                <label for="product-description">
                  商品紹介
                  <span class="text-danger">*</span>
                </label>
                <ckeditor id="product-description" v-model="product.description" :editor="editor"></ckeditor>
              </div>


              <div class="form-group mb-3">
                <label>商品仕様</label>

                <ckeditor id="product-package" v-model="product.package" :editor="editor"></ckeditor>
              </div>
              <div class="form-group mt-3 float-right">

                <b-button class="btn-rounded" variant="danger" @click="update_product">更新</b-button>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <ProductImageEditor :product="product"/>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <VariationTable :variations="product.item_variations" :product_id="product.id"
                        @operateTable="operateVariationTable"></VariationTable>
      </div>
    </div>
  </div>
</template>
