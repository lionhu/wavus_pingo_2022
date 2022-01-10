<script>
import {mapGetters, mapState} from "vuex"
import Swal from "sweetalert2";
import {swalService} from "@/helpers/swal.service";

const empty_product = {
  id: 0,
  item_name: "",
  is_valid: false,
  rate: 0,
  vendor: {
    id: 0,
    name: ""
  },
  category: {
    id: 0,
    title: ""
  },
  type: "",
  currentNum: 0,
  targetNum: 10,
  until_at: ""
};
export default {
  name: "pingoproduct_list",
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
    Category: () => import('../components/CategoryModal'),
    QuickEditProduct: () => import('./components/QuickEditProduct'),

  },
  data() {
    return {
      title: "トモ買い商品",
      items: [
        {text: "PinGo"},
        {text: "eCommerce"},
        {text: "トモ買い商品", active: true}
      ],
      product: empty_product,
      searchproduct: {
        item_name: "",
        id: 0
      },
      search_product_key: "",
      props: {
        label: 'title',
        children: 'children',
        isLeaf: 'leaf',
        user_id: 0
      },
      dropdown_props: {
        label: "title",
        value: "id"
      },
      category_id: 0,
      showQuieckEditProductModal: false,
      page: 1,
      total: 0,
      page_size: 10
    };
  },
  computed: {
    ...mapGetters({
      categorylist: "categories/getProductCategories",
      pingoproductlist: "pingoproducts/getterSuperadminList",
      ProductListMeta: "pingoproducts/getterProductListMeta",
      back_server: "system/getterBackServer"
    }),
    ...mapState({
      vendorlist: state => state.system.vendorlist
    }),
    filter_options() {
      if (this.category_id === 0) {
        return `?page=${this.page}&page_size=${this.page_size}&expand=supplier`
      } else {
        return `?page=${this.page}&page_size=${this.page_size}&expand=supplier&filter{category_id}=${this.category_id}`
      }
    }
  },
  methods: {
    async load_category_products() {
      this.$nuxt.$loading.start();
      await this.$store.dispatch("pingoproducts/superadmin_filter_category", this.filter_options)
        .then((response) => {
          console.log(response.meta.total)
          swalService.showToast("success", `${response.meta.total} 点商品が見つかりました。`)
        })
      this.$nuxt.$loading.finish();
    },
    tablePageChange(page) {
      this.page = page;
      this.load_category_products()

    },
    copyProduct(product) {
      this.$store.commit("pingoproducts/superadmin_setCopyProduct", {product: product, mode: "copy"});
      this.$router.push("/superadmin/pingoproducts/create")
    },
    editProduct(product) {
      this.$store.commit("pingoproducts/superadmin_setCopyProduct", {product: product, mode: "edit"});
      this.$router.push(`/superadmin/pingoproducts/edit/${product.id}`)
    },
    deleteProduct(product_id) {
      console.log(product_id)
      let vm = this;
      if (product_id) {
        Swal.fire({
          title: 'Are you sure?',
          text: "You won't be able to revert delete product!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
          if (result.isConfirmed) {
            vm.$store.dispatch("pingoproducts/superadmin_remove_product", product_id)
          }
        })
      }
    },
    ClickNode(data, Node, ev) {
      if (Node.isLeaf) {
        this.category_id = Node.data.id;
        this.load_category_products()
      }
    },
    SearchProducts() {
      if (this.search_product_key !== "") {
        var filterOptions = {
          "item_name__icontains": this.search_product_key
        };
        this.load_filtered_products(filterOptions)
      }
    },
    load_filtered_products(options) {
      let vm = this;
      this.$store.dispatch("products/load_category_products", options)
    },
    QuickEditProductResult(info) {
      console.log("QuickEditProductResult", info)
      if (info.result) {
        let index = this.productlist.findIndex(product => product.id === info.product.id);
        if (index > -1) {
          if (info.product.category.id === this.productlist[0].category.id) {
            this.productlist.splice(index, 1, info.product);
          } else {
            this.productlist.splice(index, 1)
          }
        }
      }
      this.showQuieckEditProductModal = false;
    },

    product_progress_ratio(currentNum, targetNum) {
      return parseInt(currentNum / targetNum * 100)
    },

    status_badge(product) {
      switch (product.status) {
        case  'ESTABLISHED':
          return "success"
        case  'RECRUITING':
          return "warning"
        case  'PROCESSING':
          return "info"
        case  'RELEASED':
          return "danger"
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
      <div class="col-md-6 col-xs-12">
        <div class="card">
          <div class="card-body">
            <el-tree
              class="filter-tree"
              :props="props"
              :data="categorylist"
              node-key="id"
              draggable
              @node-click="ClickNode"
              ref="tree">
            </el-tree>
          </div>
        </div>
      </div>
      <div class="col-md-6 col-xs-12">
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-sm-6">

                <nuxt-link to="/superadmin/pingoproducts/create" class="btn btn-danger mb-2"><i
                  class="mdi mdi-plus-circle mr-1"></i> 商品追加
                </nuxt-link>
              </div>
              <div class="col-sm-6">
                <div class="form-group row mb-0">
                  <div class="col-sm-12">
                    <div class="input-group">
                      <input type="text" class="form-control" placeholder="product name" v-model="search_product_key"
                             aria-describedby="basic-addon2"/>
                      <div class="input-group-append">
                        <button class="btn btn-dark waves-effect waves-light" type="button" @click="SearchProducts">
                          検索
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div><!-- end col-->
            </div>
            <div class="table-responsive mb-0">

              <div class="row my-2" v-if="ProductListMeta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="ProductListMeta.total"
                                    :per-page="page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
              <el-table
                id="pingoproduct_table"
                :data="pingoproductlist"
                :per-page="page_size"
                :current-page="page"
                style="width: 100%">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <div class="row">
                        <div class="col-12">
                          <ul>
                            <li v-for="variant in props.row.variations_admin">
                              <ul class="list-inline">
                                <li class="list-inline-item">{{ variant.name }}</li>
                                <li class="list-inline-item">{{ variant.purchase_price |currency("¥") }}</li>
                                <li class="list-inline-item">{{ variant.price |currency("¥") }}</li>
                              </ul>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column width="250" label="商品" sortable prop="id">
                  <template slot-scope="scope">
                    <div v-if="scope.row.thumbimage_url">
                      <img :src="scope.row.thumbimage_url" alt=""
                           class="rounded mr-3" style="width: 60%;"/>
                    </div>
                    <div v-if="!scope.row.thumbimage_url" class="avatar-xs d-inline-block mr-2">
                      <div class="avatar-title bg-soft-primary rounded-circle text-primary">
                        <i class="mdi mdi-account-circle m-0"></i>
                      </div>
                    </div>
                    <p class="m-0 d-inline-block align-middle">{{ scope.row.item_name }}(#{{ scope.row.id }})</p>
                    <h6>
                      <b-badge variant="success" pill v-if="scope.row.is_valid">active</b-badge>
                      <b-badge variant="danger" pill v-else>deactivate</b-badge>
                    </h6>
                  </template>
                </el-table-column>
                <el-table-column
                  label="イベント情報">
                  <template slot-scope="scope">
                    <!--                    <b-badge variant="primary" class="d-block">{{scope.row.currentNum}}</b-badge>-->
                    <!--                    <b-badge variant="warning" class="d-block">{{scope.row.targetNum}}</b-badge>-->
                    <div class="text-center">
                      <span class="d-block">{{ scope.row.currentNum }}/{{ scope.row.targetNum }}</span>
                      <div class="progress progress-sm">
                        <div class="progress-bar bg-success" role="progressbar"
                             :style="`width: ${product_progress_ratio(scope.row.currentNum,scope.row.targetNum)}%`"
                             :aria-valuenow="product_progress_ratio(scope.row.currentNum,scope.row.targetNum)"
                             aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                    <div class="text-center">
                      <b-badge :variant="status_badge(scope.row)" pill>{{ scope.row.status }}</b-badge>
                    </div>
                    <div class="text-center">
                      <span>締切日：{{ scope.row.until_at|short_date }}</span>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  label="サプライヤー"
                  sortable
                  prop="supplier.name">
                </el-table-column>
                <el-table-column
                  label="順番"
                  sortable
                  prop="sort_by">
                  <template slot-scope="scope">
                      <b-badge variant="danger" pill>{{ scope.row.sort_by }}</b-badge>
                  </template>
                </el-table-column>
                <el-table-column
                  label="Action">
                  <template slot-scope="scope">
                    <ul class="list-inline table-action m-0">
                      <!--                      <li class="list-inline-item">-->
                      <!--                        <a :href="`https://www.pingo.jp/shop/preview/${scope.row.id}`" target="_blank"-->
                      <!--                           class="action-iconk">-->
                      <!--                          <i class="fe-eye text-danger"></i></a>-->
                      <!--                      </li>-->
                      <li class="list-inline-item">
                        <a href="javascript:void(0);" @click="editProduct(scope.row)"> <i class="fe-edit"></i></a>
                      </li>
                      <!--                      <li class="list-inline-item">-->
                      <!--                        <a href='javascript:void(0);' class="action-iconk" @click="copyProduct(scope.row)">-->
                      <!--                          <i class="ri-file-copy-2-fill"></i></a>-->
                      <!--                      </li>-->
                      <!--                      <li class="list-inline-item">-->
                      <!--                        <a href="javascript:void(0);" class="action-iconk" @click="deleteProduct(scope.row.id)">-->
                      <!--                          <i class="fe-trash-2"></i>-->
                      <!--                        </a>-->
                      <!--                      </li>-->
                    </ul>
                  </template>
                </el-table-column>
              </el-table>


              <div class="row my-2" v-if="ProductListMeta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="ProductListMeta.total"
                                    :per-page="page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <QuickEditProduct :product="product" mode="edit" :showModal="showQuieckEditProductModal"
                      @updateResult="QuickEditProductResult"/>
  </div>
</template>
