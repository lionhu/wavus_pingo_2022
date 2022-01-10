<script>
import {swalService} from "~/helpers/swal.service"
import {mapGetters} from "vuex";
import {APIServices} from "@/helpers/APIs";

export default {
  name: "edit_product",
  middleware: ['router-auth', 'router-superadmin'],
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
    ProductDetailCard:() => import('../components/ProductDetailCard'),
    CommentList:() => import('../components/ProductCommentList'),
  },
  data() {
    return {
      title: "商品コメント",
      items: [
        {text: "PINGO",},
        {text: "eCommerce",},
        {text: "商品詳細",},
        {text: "コメント", active: true,}
      ],
      product: {}
    };
  },
  mounted() {
    if (this._product_id > 0) {
      this.load_product(this._product_id)
    } else {
      window.location.href = "/backend/superadmin/products"
    }
  },
  computed: {
    ...mapGetters({
      _product_id: "products/getterProductID",
    }),
  },
  methods: {
    async load_product(product_id) {
      let vm = this;
      this.$nuxt.$loading.start();
      await APIServices.get(`store/public/filter_products/by_id/?query=${product_id}`)
        .then(APIServices.handleResponse)
        .then(response => {
          console.log("load_product editor mount", response)
          if (response.length > 0) {
            vm.product = response[0];
          }
        })
      this.$nuxt.$loading.finish();
    },
  }
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-lg-12">
        <ProductDetailCard :product="product" v-if="product.id"/>
        <div class="card">
          <div class="card-body">

            <h4 class="header-title">商品評価</h4>
<!--            <p class="sub-header">下記の基本情報を入力してください。</p>-->
            <CommentList :product="product" v-if="product.id" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
