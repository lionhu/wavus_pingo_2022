<script>
import {mapGetters, mapState} from "vuex"
import {swalService} from "~/helpers/swal.service"
import {productService} from "~/helpers/product.service"

export default {
  name: "product_list",
  middleware: ['router-auth', 'router-supplier'],
  head() {
    return {
      title: `${this.title} | PINGO`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    Switches: () => import('vue-switches'),
    "el-tree": () => import('element-ui/lib/tree'),
    "el-date-picker": () => import('element-ui/lib/date-picker'),
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-select": () => import('element-ui/lib/select'),
    "el-rate": () => import('element-ui/lib/rate'),
    "el-dialog": () => import('element-ui/lib/dialog'),
    "el-upload": () => import('element-ui/lib/upload'),
    "el-option": () => import('element-ui/lib/option'),
    "el-cascader": () => import('element-ui/lib/cascader'),
    "el-form": () => import('element-ui/lib/form'),
    Category: () => import('~/components/widgets/CategoryTree'),

  },
  data() {
    return {
      title: "製品一覧",
      items: [
        {text: "PinGo"},
        {text: "eCommerce"},
        {text: "Products List", active: true}
      ],
      submitted: false,
      product_types: [
        {value: "REGULAR", label: "シェア買"},
        {value: "PINGO", label: "トモ買"},
      ],
      product_type: "REGULAR",
      productlist: [],
      productlist_meta: {
        page: 1,
        page_size: 10,
        total: 10,
        links: {}
      },
      current_category: 0
    };
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME",
      mySupplierInfo: "suppliers/getterSupplier",
      isSupplier: "authfack/isSupplier",
      supplierlist: "suppliers/getterSupplierList",
      supplierlistMeta: "suppliers/getterSupplierListMeta",
    }),
    ...mapState({}),
    SupplierName() {
      return this.mySupplierInfo !== null ? this.mySupplierInfo.name : ""
    },
    options() {
      let filterOptions = `?page=${this.productlist_meta.page}&page_size=${this.productlist_meta.page_size}&expand=item_variations,category`
      if (this.mySupplierInfo.id > 0) {
        filterOptions += `&filter{supplier}=${this.mySupplierInfo.id}`
      }
      if (this.current_category > 0) {
        filterOptions += `&filter{category}=${this.current_category}`
      }
      return filterOptions
    }
  },
  methods: {
    tablePageChange(page) {
      this.productlist_meta.page = page;
      this.load_filtered_products()
    },
    load_my_all_products() {
      this.current_category = 0;
      this.load_filtered_products()
    },
    ClickNode({data, node}) {
      this.current_category = data.id;
      this.load_filtered_products()
    },
    async load_filtered_products() {
      let vm = this;
      this.$nuxt.$loading.start();

      if (this.product_type === "REGULAR") {
        await this.$store.dispatch("products/load_category_products", this.options)
          .then(response => {
            vm.productlist = response.results;
            vm.productlist_meta = response.meta;
          })
      } else {
        console.log("loading Pingo products")
      }
      this.$nuxt.$loading.finish();
      if (this.productlist_meta.total) {
        swalService.showToast("success", `${this.productlist_meta.total} 点商品がありました!`)
      }
    },
    edit_product(product) {
      this.$store.commit("products/setProductID", product.id)
      this.$router.push("/supplier/products/edit/")
    },
    add_product(){
      this.$router.push("/supplier/products/create")
    }
  },
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <h5><b-badge variant="danger" pill>サプライヤー：{{ this.SupplierName }}</b-badge></h5>
    <div class="row">
      <div class="col-md-6 col-xs-12">
        <div class="card">
          <div class="card-body">
            <label>シェア買商品カテゴリー：</label>
<!--            <el-select id="supplier_selector" v-model="product_type" placeholder="请选择" class="mb-3">-->
<!--              <el-option-->
<!--                v-for="_type in product_types"-->
<!--                :key="_type.value"-->
<!--                :label="_type.label"-->
<!--                :value="_type.value">-->
<!--              </el-option>-->
<!--            </el-select>-->
            <Category @clickNode="ClickNode"/>
            <div class="d-flex justify-content-between">
              <b-button variant="warning" @click="load_my_all_products">全て商品</b-button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6 col-xs-12">
        <div class="card">
          <div class="card-body">
            <label>商品管理：</label>
            <div class="d-flex justify-content-between">
              <b-button variant="primary" @click="add_product">商品追加</b-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive mb-0">
              <el-table
                :data="productlist"
                style="width: 100%">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <div class="row">
                      <div class="col-lg-12">
                        <div>
                          <div class="table-responsive">
                            <h5 class="font-15 mb-2">Variations</h5>
                            <table class="table table-centered border table-nowrap mb-lg-0">
                              <thead class="bg-light">
                              <tr>
                                <th class="text-center">Product</th>
                                <th>価格</th>
                                <th>在庫</th>
                              </tr>
                              </thead>
                              <tbody>
                              <tr v-for="variation in props.row.item_variations" :key="variation.id">
                                <td>
                                  <div class="media align-items-center">
                                    <div class="mx-3">
                                      <img :src="variation.thumbimage_url" alt="product-img" height="60"/>
                                    </div>
                                    <div class="media-body">
                                      <h6 class="m-0">{{ variation.name }}</h6>
                                      <p>{{ variation.sku }}</p>
                                    </div>
                                  </div>
                                </td>
                                <td>{{ variation.purchase_price|currency("¥") }}</td>
                                <td>{{ variation.inventory |currency() }}</td>
                              </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column width="250" label="Product" sortable prop="id">
                  <template slot-scope="scope">
                    <div v-if="scope.row.image_url">
                      <img :src="scope.row.image_url" alt=""
                           class="rounded mr-3" style="width: 60%;"/>
                    </div>
                    <div v-if="!scope.row.image_url" class="avatar-xs d-inline-block mr-2">
                      <div class="avatar-title bg-soft-primary rounded-circle text-primary">
                        <i class="mdi mdi-account-circle m-0"></i>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  label="製品名"
                  sortable
                  prop="item_name">
                  <template slot-scope="scope">
                    {{ scope.row.item_name }}(#{{ scope.row.id }})
                  </template>
                </el-table-column>
                <el-table-column
                  label="カテゴリ"
                  sortable
                  v-if="current_category===0">
                  <template slot-scope="scope">
                    {{ scope.row.category.title }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="Status"
                  sortable
                  width="80"
                  prop="is_valid">
                  <template slot-scope="scope">
                    <b-badge variant="success" pill v-if="scope.row.is_valid">active</b-badge>
                    <b-badge variant="danger" pill v-else>deactivate</b-badge>
                  </template>
                </el-table-column>

                <el-table-column
                  label="Action">
                  <template slot-scope="scope">
                    <ul class="list-inline table-action m-0">
                      <li class="list-inline-item">
                        <a href="javascript:void(0);" @click="edit_product(scope.row)">
                          <i class="fe-edit"></i>
                        </a>
                      </li>
                    </ul>
                  </template>
                </el-table-column>
              </el-table>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
