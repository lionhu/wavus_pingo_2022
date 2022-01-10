<script>
import CKEditor from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import Swal from "sweetalert2"
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import {mapState, mapGetters} from "vuex";

export default {
  name: "admin_create_product_basicinfo",
  props: ["product"],
  components: {
    Switches: () => import("vue-switches"),
    "el-rate": () => import("element-ui/lib/rate"),
    "el-upload": () => import("element-ui/lib/upload"),
    "el-dialog": () => import("element-ui/lib/dialog"),
    "el-option": () => import("element-ui/lib/option"),
    "el-select": () => import("element-ui/lib/select"),
    "el-cascader": () => import("element-ui/lib/cascader"),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    ckeditor: CKEditor.component,
  },
  data() {
    return {
      editor: ClassicEditor,
      labels: [
        {value: 'NW', label: 'New'},
        {value: 'BS', label: 'Best Seller'}
      ],
      item_status: [
        {value: 'RECRUITING', label: '募集中'},
        {value: 'PROCESSING', label: '処理中'},
        {value: 'ESTABLISHED', label: '募集成立'},
        {value: 'RELEASED', label: '募集失敗'}
      ],
      disabled: false,
      modeAdd: false,
      submitted: false,
      errors: [],
      saved: false
    };
  },
  computed: {
    ...mapGetters({
      back_server: "system/getterBackServer",
      suppliers: "suppliers/getterSupplierList",
      categories: "categories/getProductCategories",
      copy_product: "pingoproducts/getterCopyProduct",
      BasicInfoMode: "pingoproducts/getterBasicInfoMode"
    }),
  },
  methods: {
    handleCategoryChange(val) {
      console.log(val)
      let index = val.length - 1;
      this.product.category = val[index]
    },
    pre_check() {
      this.errors = [];
      let dt = new Date()
      if (parseInt(this.product.supplier) <= 0) {
        this.errors.push("ベンダーを選択してください。")
      }
      if (parseInt(this.product.category) <= 0) {
        this.errors.push("カテゴリを選択してください。")
      }
      if (parseInt(this.product.targetNum) < 0) {
        this.errors.push("目標注文数は0以上が必要")
      }
      if (parseInt(this.product.currentNum) < 0) {
        this.errors.push("現在注文数は0以上が必要")
      }
      if (this.product.until_at < dt) {
        this.errors.push("締切日は今日以降にする必要")
      }
      if (this.errors.length) {
        let message_html = "<ol class='text-left'>"
        this.errors.forEach(error => {
          message_html += `<li>${error}</li>`
        })
        message_html += "</ol>"
        return message_html;
      }
      return ""

    },
    create_product() {
      let check_result = this.pre_check();
      if (check_result !== "") {
        Swal.fire({
          icon: "error",
          html: check_result
        })
      } else {

        this.product.currentNum = parseInt(this.product.currentNum);
        this.product.targetNum = parseInt(this.product.targetNum);
        this.product.price = parseInt(this.product.price);
        this.product.discount_price = parseInt(this.product.discount_price);
        this.product.purchase_price = parseInt(this.product.purchase_price);

        var vm = this;
        console.log("to create new product", this.product)
        this.$store.dispatch("pingoproducts/superadmin_create_product", this.product)
          .then((response) => {
            console.log("created new product", response)
            if (response.id > 0) {
              Swal.fire("Success", "Product was created!", "success")
              vm.saved = true;
              vm.$emit("optResult", {result: true, product_id: response.id})
            }
          })
      }
    },
  },
};
</script>

<template>
  <div class="card">
    <div class="card-body">

      <h4 class="header-title">基本情報</h4>
      <p class="sub-header">下記の基本情報を入力してください。</p>

      <div>
        <div class="row">
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="product-active">有効</label> <br>
              <switches v-model="product.is_valid" id="product-active" type-bold="false"
                        color="warning"
                        class="ml-1 my-auto"></switches>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="product-status">ステータス</label> <br>
              <el-select v-model="product.status" placeholder="请选择" id="product-status">
                <el-option
                  v-for="item in item_status"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </div>
          </div>
          <div class="col-md-4">

            <div class="form-group mb-3">
              <label for="product-sort">
                カテゴリー内の並び順番:
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
              </label>
              <el-rate id="product-rate" v-model="product.rate"></el-rate>
            </div>
          </div>

          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="product-category">
                ラベル
              </label>
              <el-select v-model="product.labels" multiple placeholder="请选择">
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
        <div class="row">
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="targetNum">
                目標注文数
                <span class="text-danger">*</span>
              </label>
              <input type="number" v-model="product.targetNum" id="targetNum" class="form-control"
                     :placeholder="product.targetNum"/>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="targetNum">
                現在注文数
                <span class="text-danger">*</span>
              </label>
              <input type="number" v-model="product.currentNum" id="currentNum"
                     class="form-control"
                     :placeholder="product.currentNum"/>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="until_at">
                締切日
                <span class="text-danger">*</span>
              </label>

              <el-date-picker
                id="until_at"
                v-model="product.until_at"
                align="right"
                type="date"
                placeholder="締切日">
              </el-date-picker>
            </div>
          </div>
        </div>
        <div class="row dotted-border-red">
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="price">
                通常価格
                <span class="text-danger">*</span>
              </label>
              <input type="number" v-model="product.price" id="price" class="form-control"
                     :placeholder="product.price"/>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="discount_price">
                特別価格
                <span class="text-danger">*</span>
              </label>
              <input type="number" v-model="product.discount_price" id="discount_price"
                     class="form-control"
                     :placeholder="product.discount_price"/>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group mb-3">
              <label for="purchase_price">
                仕入価格
                <span class="text-danger">*</span>
              </label>
              <input type="number" v-model="product.purchase_price" id="purchase_price"
                     class="form-control"
                     :placeholder="product.purchase_price"/>
            </div>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-4">

            <label for="product-brand">
              ブランド
            </label>
            <input type="text" v-model="product.brand" id="product-brand" class="form-control"
                   :placeholder="product.brand"/>
          </div>
          <div class="col-md-4">

            <label for="product-Series">
              シリーズ
            </label>
            <input type="text" v-model="product.series" id="product-Series" class="form-control"
                   :placeholder="product.series"/>
          </div>
          <div class="col-md-4">

            <label for="product-model">
              モデル
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
          </label>
          <input type="text" v-model="product.video_url" id="product-video_url" class="form-control"
                 placeholder="e.g : Apple iMac"/>
        </div>
        <div class="form-group mb-3">
          <label for="product-description">
            商品紹介
          </label>
          <ckeditor id="product-description" v-model="product.description"
                    :editor="editor"></ckeditor>
        </div>
        <div class="form-group mb-3">
          <label>商品仕様</label>

          <ckeditor id="product-package" v-model="product.package" :editor="editor"></ckeditor>
        </div>
        <div class="form-group mt-3 float-right">
          <b-button class="btn-rounded" variant="danger" @click="create_product" v-if="!saved">保存</b-button>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.dotted-border-red {
  border: red dotted 1px;
}
</style>
