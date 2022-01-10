<script>
import {swalService} from "~/helpers/swal.service"
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import {mapState, mapGetters} from "vuex";

export default {
  name: "create_pingo_product",
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
    // VariationTable: () => import('./components/VariationTable'),
    BasicProductInfo: () => import('./components/BasicProductInfo_CREATE'),
    ProductImageEditor: () => import('./components/ProductImageEditor'),
    VariationModal: () => import('./components/VariationModal'),
  },
  data() {
    return {
      title: "ADD Product",
      items: [
        {
          text: "PINGO",
        },
        {
          text: "eCommerce",
        },
        {
          text: "Edit Product",
          active: true,
        },
      ],
      showVariationModal: false,
      product: {
        id: 0,
        item_name: "item_name",
        type: "PINGO",
        rate: 4,
        is_valid: false,
        label: "NO",
        brand: "brand",
        series: "series",
        model: "model",
        targetNum: 0,
        currentNum: 0,
        until_at: new Date(),
        image: "",
        sort_by: 0,
        video_url: "video_url",
        description: "description",
        package: "package",
        category: 0,
        supplier: 0,
        price: 0,
        purchase_price: 0,
        discount_price: 0,
        item_pingo_sliderimages: [],
        point_rule: {
          is_valid:false,
          policies: {
            user_self: 0
          }
        }
      }
    };
  },
  computed: {
    ...mapGetters({
      // back_server: "system/getterBackServer",
    })
  },
  methods: {
    switchUpdatePointRule() {
      this.modeAdd = true;
      this.showVariationModal = true;
    },
    updatePointRule(new_point_rule) {
      console.log(new_point_rule)
      this.product.point_rule = new_point_rule;
      this.showVariationModal = false;
      swalService.showModal("Success", "PointRule has been successfully updated!", "success")

    },
    CreateProductResult({result, product_id}) {
      let vm =this;
      console.log("CreateProductResult", result, product_id)
       this.$store.dispatch("pingoproducts/superadmin_retrieve_product", product_id)
        .then(response_product => {
          vm.product = response_product;
          vm.product.supplier = response_product.supplier.id;
        })
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
        <BasicProductInfo :product="product" @optResult="CreateProductResult"/>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-12">
        <ProductImageEditor :product="product"/>
      </div>
    </div>
    <div class="card" >
      <div class="card-body">
        <h4 class="header-title">ポイント付与ルール

          <button class="btn btn-warning mb-2 float-right" v-b-modal.modal_variation_component
                  @click="switchUpdatePointRule"><i
            class="mdi mdi-plus-circle mr-1"></i> 更新
          </button>
        </h4>
        <p class="sub-header">ポイント付与対象</p>

        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center">
            本人
            <span class="badge badge-danger badge-pill">{{ product.point_rule.policies.user_self }}</span>
          </li>
        </ul>
      </div>
    </div>

    <VariationModal :showVariationModal="showVariationModal" :product="product" :point_rule="product.point_rule"
                    @updatePointRule="updatePointRule"></VariationModal>
  </div>
</template>
