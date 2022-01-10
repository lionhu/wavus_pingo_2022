<script>
import CKEditor from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import Swal from "sweetalert2"
import {mapState, mapGetters} from "vuex";
import {pingoproductService} from "~/helpers/pingoproduct.service"

export default {
  name: "edit_pingoproduct",
  head() {
    return {
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
    VariationModal: () => import('../components/VariationModal'),
    ProductImageEditor: () => import('../components/ProductImageEditor'),
    BasicProductInfo: () => import('../components/BasicProductInfo'),
    ckeditor: CKEditor.component,
  },
  data() {
    return {
      title: "トモ買商品詳細",
      items: [
        { text: "PINGO", },
        { text: "eCommerce", },
        { text: "トモ買商品", active: true, },
      ],
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
      image: "",
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      imageUrl: "",
      submitted: false,
      editproduct: {
        is_valid: false,
      },
      showVariationModal: false
    };
  },
  computed: {
    ...mapGetters({
      back_server: "system/getterBackServer",
      categories: "categories/getProductCategories",
      suppliers: "suppliers/getterSupplierList",
    }),
  },
  mounted() {
    let product_id= parseInt(this.$route.params.id)
    if (product_id>0) {
      this.load_product(product_id)
    }else{
      this.$router.push("/superadmin/pingoproducts")
    }
  },
  methods: {
    async load_product(product_id){
      let self = this;
      this.$nuxt.$loading.start();
      await pingoproductService.superadmin_retrieve(product_id)
        .then(response_product => {
          console.log("load pingo product", response_product)
          if (response_product.id>0) {
            self.editproduct = response_product;
            self.editproduct.supplier = response_product.supplier.id;
          }else{
            window.location.href = "/superadmin/pingoproducts"
          }
        })

      this.$nuxt.$loading.finish();
    },
    switchUpdatePointRule() {
      this.showVariationModal = true;
    },
    updatePointRule(new_point_rule) {
      console.log(new_point_rule)
      this.editproduct.point_rule = new_point_rule;
      this.showVariationModal = false;
      Swal.fire({
        title: "Success",
        html: "PointRule has been successfully updated!",
        icon: "success"
      })

    },
    handleCategoryChange(val) {
      let index = val.length - 1;
      this.editproduct.category = val[index]
    },

    pre_check() {
      this.errors = [];
      let dt = new Date()
      if (this.editproduct.supplier === 0) {
        this.errors.push("ベンダーを選択してください。")
      }
      if (this.editproduct.category === 0) {
        this.errors.push("カテゴリを選択してください。")
      }
      if (parseInt(this.editproduct.targetNum) < 0) {
        this.errors.push("目標注文数は0以上が必要")
      }
      if (parseInt(this.editproduct.currentNum) < 0) {
        this.errors.push("現在注文数は0以上が必要")
      }
      if (this.editproduct.until_at < dt) {
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
    update_product() {

      let check_result = this.pre_check();
      if (check_result !== "") {
        Swal.fire({
          icon: "error",
          html: check_result,
          title: "Error"
        })
      } else {

        let vendor_id = 0;
        if (Object.keys(this.editproduct.supplier).includes("id")) {
          vendor_id = this.editproduct.supplier.id;
        } else {
          vendor_id = this.editproduct.supplier
        }

        delete this.editproduct.image;
        delete this.editproduct.thumbimage;
        delete this.editproduct.sliderimages;
        delete this.editproduct.variations;
        delete this.editproduct.supplier;

        this.editproduct.sort_by = parseInt(this.editproduct.sort_by);
        this.editproduct.currentNum = parseInt(this.editproduct.currentNum);
        this.editproduct.targetNum = parseInt(this.editproduct.targetNum);
        this.editproduct.supplier = vendor_id;

        var self = this;
        console.log(this.editproduct)
        this.$store.dispatch("pingoproducts/superadmin_update_product", this.editproduct)
          .then((response) => {
            if (response.pingo_item && response.pingo_item.id) {
              self.editproduct.supplier = response.pingo_item.supplier.id;
              self.editproduct.category = response.pingo_item.category;
              Swal.fire({
                title: "Success",
                html: "Product was updated!",
                icon: "success"
              })
            }
          })
      }
    },
    CreateProductResult(info) {
      if (info.result) {
        this.editproduct = info.product;
      }
    }
  },
  middleware: ['router-auth', 'router-superadmin'],
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-lg-12">
        <BasicProductInfo :product="editproduct"
        @optResult="CreateProductResult"/>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <ProductImageEditor :product="editproduct"/>
      </div>
    </div>
    <div class="card" v-if="editproduct.id">
      <div class="card-body">
        <h4 class="header-title">ポイント付与ルール
          <b-badge variant="success" pill v-if="editproduct.point_rule.is_valid">
            {{editproduct.point_rule.is_valid}}
          </b-badge>
          <b-badge variant="danger" pill v-else>
            {{editproduct.point_rule.is_valid}}
          </b-badge>

          <button class="btn btn-warning mb-2 float-right" v-b-modal.modal_variation_component
                  @click="switchUpdatePointRule"><i
            class="mdi mdi-plus-circle mr-1"></i> 更新
          </button>
        </h4>
        <p class="sub-header">ポイント付与対象</p>

        <ul class="list-group" v-if="editproduct.point_rule.is_valid">
          <li class="list-group-item d-flex justify-content-between align-items-center"
              v-if="editproduct.point_rule.policies.client_superadmin">
            営業代理
            <span class="badge badge-primary badge-pill">{{ editproduct.point_rule.policies.client_superadmin }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center"
              v-if="editproduct.point_rule.policies.client_admin">
            代理店
            <span class="badge badge-success badge-pill">{{ editproduct.point_rule.policies.client_admin }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center"
              v-if="editproduct.point_rule.policies.level_2">
            Level 2
            <span class="badge badge-danger badge-pill">{{ editproduct.point_rule.policies.level_2 }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center"
              v-if="editproduct.point_rule.policies.level_1">
            Level 1
            <span class="badge badge-danger badge-pill">{{ editproduct.point_rule.policies.level_1 }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center"
              v-if="editproduct.point_rule.policies.user_self">
            本人
            <span class="badge badge-danger badge-pill">{{ editproduct.point_rule.policies.user_self }}</span>
          </li>
        </ul>
      </div> <!-- end card-body -->
    </div> <!-- end card-->

    <VariationModal :showVariationModal="showVariationModal" :product="editproduct" :point_rule="editproduct.point_rule"
                    @updatePointRule="updatePointRule"></VariationModal>

  </div>
</template>
