<script>
import {mapGetters, mapState} from "vuex"
import {swalService} from "~/helpers/swal.service"
import Swal from "sweetalert2";


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
};
export default {
  name: "product_list",
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
      title: "Products List",
      items: [
        {text: "PinGo"},
        {text: "eCommerce"},
        {text: "Products List", active: true}
      ],
      submitted: false,
      product: empty_product,
      searchproduct: {
        item_name: "",
        id: 0
      },
      productlist: [],
      productlist_meta: {
        links: {},
        page: 1,
        total: 0,
        page_size: 100
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
      edit_category: false,
      showQuieckEditProductModal: false,
      search_mode: false,
      current_category: 0
    };
  },
  computed: {
    ...mapGetters({
      categorylist: "categories/getProductCategories"
    }),
    filter_options() {
      let url = `?page=${this.productlist_meta.page}&page_size=${this.productlist_meta.page_size}&expand=supplier`
      return this.current_category ? url + `&filter{category_id}=${this.current_category}` : url;
    }
  },
  methods: {
    ClickNode(data, Node, ev) {
      if (Node.isLeaf) {
        this.current_category = Node.data.id;
        this.load_filtered_products()
      }
    },
    tablePageChange(page) {
      this.productlist_meta.page = page;
      this.load_filtered_products()
    },
    async load_filtered_products() {
      let vm = this;
      this.search_mode = false;

      this.$nuxt.$loading.start();
      await this.$store.dispatch("products/load_category_products", this.filter_options)
        .then(response => {
          vm.productlist = response.results;
          vm.productlist_meta = response.meta;
          if (vm.productlist_meta.total) {
            swalService.showToast("success", `${vm.productlist_meta.total} products loaded!`)
          } else {
            swalService.showToast("warning", `no products found!`)
          }
        })

      this.$nuxt.$loading.finish();
    },


    editProduct(product) {
      console.log(product)
      this.product = product;
      this.showQuieckEditProductModal = true;
    },
    deleteProduct(product_id) {
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
            vm.$store.dispatch("products/remove_product", product_id)
              .then(response => {
                console.log("delete response", response)
                if (response.result) {
                  let index = vm.productlist.findIndex(_product => _product.id == product_id)
                  console.log(index)
                  if (index > -1) {
                    vm.productlist.splice(index, 1)
                    swalService.showToast("success", "product removed successfully!")
                  }
                }
              }).catch(err => {
              console.log(err)
              swalService.showToast("error", "Something wrong when removing product!")
            })
          }
        })
      }
    },
    SearchProducts() {
      let vm = this;
      this.search_mode = true;
      if (this.search_product_key !== "") {
        let filterOptions = {
          "item_name__icontains": this.search_product_key
        };
        this.$store.dispatch("products/search_products", filterOptions).then(response => {
          console.log("search", response.data)

          if (response.result) {
            vm.productlist = response.data.items;
            vm.productlist_meta.total = response.data.items.length;
            if (vm.productlist_meta.total) {
              swalService.showToast("success", `${vm.productlist_meta.total} products loaded!`)
            } else {
              swalService.showToast("warning", `no products found!`)
            }
          }
        })
      }
    },
    copyProduct(product) {
      this.$store.commit("products/setCopyProduct", product);
      this.$router.push("/superadmin/products/create")
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
    EditProduct(product) {
      this.$store.commit("products/setProductID", product.id)
      this.$router.push("/superadmin/products/edit/")
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
        <div class="card" v-if="edit_category">
          <div class="card-body">
            <Category/>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-sm-6">

                <nuxt-link to="/superadmin/products/create" class="btn btn-danger mb-2"><i
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
                          Search
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div><!-- end col-->
            </div>
            <div class="table-responsive mb-0" v-if="productlist_meta.total">

              <div class="row my-2" v-if="!search_mode">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="productlist_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="productlist_meta.total"
                                    :per-page="productlist_meta.page_size"
                                    @change="tablePageChange"
                      >
                      </b-pagination>
                    </ul>
                  </div>
                </div>
              </div>
              <el-table
                :data="productlist"
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
                <el-table-column width="250" label="Product" sortable prop="id">
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
                    <h5 class="m-0 d-inline-block align-middle">
                      {{ scope.row.item_name }}(#{{ scope.row.id }})
                    </h5>
                    <h6>
                      <a href="javascript:void(0);" v-b-modal:modal-quick-editproduct
                         @click="editProduct(scope.row)" class="action-icon">
                        <b-badge variant="primary" pill v-if="scope.row.type==='REGULAR'">REGULAR</b-badge>
                        <b-badge variant="warning" pill v-else>Pingo</b-badge>
                        <i class="mdi mdi-square-edit-outline"></i>
                      </a>
                    </h6>
                  </template>
                </el-table-column>
                <el-table-column
                  label="Order"
                  sortable
                  prop="rate">
                  <template slot-scope="scope">
                    <b-badge variant="danger" pill>{{ scope.row.sort_by }}</b-badge>
                  </template>
                </el-table-column>
                <el-table-column
                  label="サプライヤー"
                  sortable
                  prop="supplier.name">
                </el-table-column>
                <el-table-column
                  label="Status"
                  sortable
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
                      <!--                      <li class="list-inline-item">-->
                      <!--                        <a :href="`https://www.pingo.jp/shop/preview/${scope.row.id}`" target="_blank"-->
                      <!--                           class="action-iconk">-->
                      <!--                          <i class="fe-eye text-danger"></i></a>-->
                      <!--                      </li>-->
                      <li class="list-inline-item">
                        <a href="javascript:void(0);" @click="EditProduct(scope.row)">
                          <i class="fe-edit"></i>
                        </a>
                        <!--                        <nuxt-link :to="'/superadmin/products/edit/' + scope.row.id" class="action-iconk">-->
                        <!--                          <i class="fe-edit"></i></nuxt-link>-->
                      </li>
                      <!--                      <li class="list-inline-item">-->
                      <!--                        <a href='javascript:void(0);' class="action-iconk" @click="copyProduct(scope.row)">-->
                      <!--                          <i class="ri-file-copy-2-fill"></i>-->
                      <!--                        </a>-->
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

              <div class="row my-2" v-if="!search_mode">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="productlist_meta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="productlist_meta.total"
                                    :per-page="productlist_meta.page_size"
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
