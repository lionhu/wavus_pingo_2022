<script>
import CKEditor from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import Swal from "sweetalert2"
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import {mapState, mapGetters} from "vuex";

export default {
  name: "admin_create_product_basicinfo",
  props: ["mode", "existed_product"],
  created() {
    console.log("created copy_product", this.copy_product)
    if (this.copy_product !== undefined && this.copy_product.id) {
      this.product.item_name = this.copy_product.item_name;
      this.product.description = this.copy_product.description;
      this.product.package = this.copy_product.package;
      this.product.supplier = this.copy_product.supplier.id;
      this.product.is_valid = this.copy_product.is_valid;
      this.product.sort_by = this.copy_product.sort_by;
      this.product.category = this.copy_product.category;
      this.product.video_url = this.copy_product.video_url;
      this.product.rate = this.copy_product.rate;
      this.product.brand = this.copy_product.brand;
      this.product.label = this.copy_product.label;
      this.product.model = this.copy_product.model;
      this.product.series = this.copy_product.series;
    }
  },
  components: {
    Switches: () => import("vue-switches"),
    "el-rate": () => import("element-ui/lib/rate"),
    "el-upload": () => import("element-ui/lib/upload"),
    "el-dialog": () => import("element-ui/lib/dialog"),
    "el-option": () => import("element-ui/lib/option"),
    "el-select": () => import("element-ui/lib/select"),
    "el-cascader": () => import("element-ui/lib/cascader"),
    ckeditor: CKEditor.component,
  },
  data() {
    return {
      editor: ClassicEditor,
      labels: [
        {value: 'NW', label: 'New'},
        {value: 'BS', label: 'Best Seller'}
      ],
      disabled: false,
      modeAdd: false,
      submitted: false,
      product: {
        id: 0,
        item_name: "item_name",
        type: "REGULAR",
        rate: 4,
        is_valid: false,
        is_matched: false,
        labels: [],
        brand: "brand",
        series: "series",
        model: "model",
        image: "",
        sort_by: 0,
        video_url: "video_url",
        description: "description",
        package: "package",
        category: 0,
        supplier: 0
      },
      errors: []
    };
  },
  computed: {
    ...mapGetters({
      copy_product: "products/getterCopyProduct",
      suppliers: "suppliers/getterSupplierList",
      categories: "categories/getProductCategories",
    }),
    // vendorlist() {
    //   return this.$store.state.system.vendorlist;
    // },
    csrftoken() {
      return this.$store.state.auth ? this.$store.state.auth.user.token : "";
    },
  },
  methods: {
    handleCategoryChange(val) {
      let index = val.length - 1;
      this.product.category = val[index]
    },
    pre_check() {
      this.errors = [];
      if (this.product.supplier === 0) {
        this.errors.push("supplier is empty")
      }
      if (this.product.category === 0) {
        this.errors.push("Category is empty")
      }
      return this.errors.length

    },
    update_product() {
      let product_id = this.product.id;
      delete this.product.id;
      delete this.product.image;
      delete this.product.sliderimages;
      delete this.product.variations;
      delete this.product.created_at;
      var vm = this;
      console.log("edit product", this.product)
      this.$store.dispatch("products/update_product", {product_id: product_id, info: this.product})
        .then((item) => {
          vm.product = item;
          vm.product.supplier = item.supplier.id;
          Swal.fire("Success", "Product was updated!", "success")
        })
    },
    async create_product() {
      let vm = this;
      this.$nuxt.$loading.start();
      if (this.pre_check()) {
        Swal.fire("error", JSON.stringify(this.errors))
      } else {
        delete this.product.id;
        delete this.product.image;
        console.log("create product", this.product)

        await this.$store.dispatch("products/create_product", this.product).then((response) => {
          vm.product = response;
          vm.product.supplier = response.supplier;
          Swal.fire("Success", "Product was created!", "success")
          vm.$emit("optResult", {result: true, product: response})
        })
      }

        this.$nuxt.$loading.finish();
    },
  },
};
</script>

<template>
  <div class="card">
    <div class="card-body">

      <h4 class="header-title">基本情報(商品ID #{{ product.id }})</h4>
      <p class="sub-header">下記の基本情報を入力してください。</p>

      <div>
        <div class="row">

          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="product-active">有効<span class="text-danger">*</span></label> <br>
              <switches v-model="product.is_valid" id="product-active" type-bold="false"
                        color="warning"
                        class="ml-1 my-auto"></switches>
            </div>
          </div>
          <div class="col-md-2">

            <div class="form-group mb-3">
              <label for="product-sort">
                カテゴリー内の並び順番:
                <span class="text-danger">*</span>
              </label>
              <input type="number" v-model="product.sort_by" id="product-sort" class="form-control"
                     :placeholder="product.sort_by"/>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="product-rate">
                評価
                <span class="text-danger">*</span>
              </label>
              <el-rate id="product-rate" v-model="product.rate"></el-rate>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="product-label">ラベル<span class="text-danger">*</span></label> <br>
              <el-select v-model="product.labels" multiple placeholder="请选择" id="product-label">
                <el-option
                  v-for="item in labels"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </div>
          </div>
        </div>
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
                size="medium"
                :props="{ expandTrigger: 'hover',multiple:false,label:'title',value:'id'}"
                @change="handleCategoryChange"></el-cascader>
            </div>
          </div>
          <div class="col-md-6">

            <div class="form-group">
              <label class="control-label">サプライヤー<span class="text-danger">*</span></label>
              <el-select v-model="product.supplier" placeholder="请选择">
                <el-option
                  v-for="item in suppliers"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>


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


          <b-button class="btn-rounded" variant="danger" @click="update_product" v-if="product.id>0">更新</b-button>
          <b-button class="btn-rounded" variant="danger" @click="create_product" v-else>保存</b-button>

        </div>
      </div>
    </div>
  </div>
</template>
