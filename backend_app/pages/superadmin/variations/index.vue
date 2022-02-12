<script>
import {swalService} from "~/helpers/swal.service"
import Swal from "sweetalert2";
import {APIServices} from "@/helpers/APIs";

export default {
  name: "edit_product_variation_table",
  components: {
    Switches: () => import('vue-switches'),
    "el-upload": () => import("element-ui/lib/upload"),
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    VariationModal: () => import('./components/VariationModal'),
  },
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
  data() {
    return {
      title: "商品在庫",
      items: [
        {text: "PINGO",},
        {text: "eCommerce",},
        {text: "商品在庫", active: true,}
      ],
      showVariationModal: false,
      modeAdd: false,
      variations: [],
      variations_meta: {
        links: {},
        page: 1,
        page_size: 10,
        total: 0
      },
      edit_variation: {
        price: 0,
        purchase_price: 0,
        name: "",
        description: "",
        variation_type: "REGULAR",
        inventory: 0,
        sort_by: 0,
        point_rule: {
          is_valid: false,
          type: "amount",
          policies: {
            client_superadmin: 0,
            client_admin: 0,
            level_2: 0,
            level_1: 0,
            user_self: 0
          },
          special_promotion: {
            is_valid: false,
            bonus: 0
          }
        },
      },
    };
  },
  computed: {
    csrftoken() {
      return this.$auth.strategy.token.get();
    },
    list_url() {
      return `store/public/variations/?page=${this.variations_meta.page}&page_size=${this.variations_meta.page_size}&sorted_by=inventory,item`
    }
  },
  mounted() {
    this.load_list();
  },
  methods: {
    tablePageChange(page) {
      this.variations_meta.page = page;
      this.load_list()
    },
    load_list() {
      let self = this;

      this.$nuxt.$loading.start();
      APIServices.get(this.list_url).then(APIServices.handleResponse)
        .then(response => {
          console.log(response)
          self.variations = response.results;
          self.variations_meta = response.meta;
        })

      this.$nuxt.$loading.finish();
    },
    InventoryOpt(variation, opt) {
      let vm = this;
      let _tilte = opt === "plus" ? "在庫追加" : "在庫削除";
      let data = {
        variation: variation.id,
        type: opt === "plus" ? "BS" : "RS",
        in_out: opt === "plus" ? 1 : -1,
        quantity: 0,
        info: opt === "plus" ? "buy stock from supplier" : "return stock to supplier"
      }
      Swal.fire({
        title: _tilte,
        input: 'number',
        inputAttributes: {
          autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: '確定',
        showLoaderOnConfirm: true,
        preConfirm: (stock) => {
          data.quantity = stock
          return APIServices.post("store/public/inventory/", data)
            .then(APIServices.handleResponse)
            .then(response => {
              return response
            }).catch(error => {
              Swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        if (result.isConfirmed) {
          APIServices.get(`store/public/variations/${result.value.variation}/`)
            .then(APIServices.handleResponse)
            .then(response => {
              let index = vm.variations.findIndex(variation => variation.id === result.value.variation)

              console.log("index", index)
              if (index > -1) {
                vm.variations[index].inventory = response.inventory
              }
              swalService.showToast("success", "在庫は更新されました！")
            })
        }
      })
    },
    switchAddVariationMode() {
      this.modeAdd = true;
      this.showVariationModal = true;
    },

    editVariation(variation) {
      this.edit_variation = variation;
      this.modeAdd = false;
      this.showVariationModal = true;
    },

    getUploadVariationimageURL(id) {
      return `https://www.pingo.jp/daphne/api/store/public/variations/${id}/update_image/`
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;
      // return isLt2M;
      if (!isLt2M || !isJPG) {
        swalService.showModal("Invalid picture", "Should be JPEG and below 2M", "warning")
        return false
      }
      return isJPG && isLt2M;
      // return isJPG && isLt2M;
    },
    handleVariationImageSuccess(res, file) {
      if (res.result) {
        this.ReplaceVariation(res.data)
      }
    },

    VariationOperate({modeAdd, _variation}) {
      let vm = this;
      this.ReplaceVariation(_variation)
      vm.showVariationModal = false;
    },
    ReplaceVariation(_variation) {
      let vm = this;
      let index = vm.variations.findIndex(variation => variation.id === _variation.id)
      if (index > -1) {
        vm.variations.splice(index, 1, _variation);
        swalService.showModal("Success", "更新されました!", "success")
      }

    },
  }
};
</script>
<template>
  <div>

    <PageHeader :title="title" :items="items"/>
    <div class="card">
      <div class="card-body">
        <div class="row">
          <div class="table-responsive">
            <div class="row my-2" v-if="variations_meta.total>0">
              <div class="col">
                <div class="dataTables_paginate paging_simple_numbers float-right">
                  <ul class="pagination pagination-rounded">
                    <b-pagination v-model="variations_meta.page"
                                  pills
                                  aria-controls="pingoproduct_table"
                                  :total-rows="variations_meta.total"
                                  :per-page="variations_meta.page_size"
                                  @change="tablePageChange"
                    >
                    </b-pagination>
                  </ul>
                </div>
              </div>
            </div>
            <el-table :data="variations"
                      style="width: 100%"
                      :header-cell-style="{textAlign: 'center'}"
            >
<!--              <el-table-column type="expand">-->
<!--                <template slot-scope="props">-->
<!--                </template>-->
<!--              </el-table-column>-->
              <el-table-column width="250"  sortable prop="id">
                <template slot-scope="scope">
                  <el-upload
                    class="avatar-uploader"
                    :action="getUploadVariationimageURL(scope.row.id)"
                    :show-file-list="false"
                    :headers="{'Authorization':csrftoken}"
                    :on-success="handleVariationImageSuccess"
                    :name="'image'"
                    :before-upload="beforeAvatarUpload">
                    <img v-if="scope.row.image_url" :src="scope.row.image_url" style="max-width:160px;"
                         class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                </template>
              </el-table-column>
              <el-table-column width="250" label="商品名" sortable prop="id">
                <template slot-scope="scope">
                  {{ scope.row.name }} <br>
                  <b-badge variant="success" pill>#{{ scope.row.id }}</b-badge>
                </template>
              </el-table-column>
              <el-table-column
                label="在庫"
                sortable
                width="100"
                prop="rate">
                <template slot-scope="scope">
                  <span class="d-block text-center">{{ scope.row.inventory }}</span>
                  <a href="javascript:void(0);" class="btn btn-warning d-block" @click="InventoryOpt(scope.row,'plus')">+</a>
                  <a href="javascript:void(0);" class="btn btn-danger d-block" @click="InventoryOpt(scope.row,'minus')">-</a>
                </template>
              </el-table-column>
              <el-table-column
                label="価格"
                sortable
                align="right"
                prop="is_valid">
                <template slot-scope="scope">
                  <span class="d-block text-right">{{ scope.row.price|currency("¥") }}(販売)</span>
                  <span class="d-block text-right text-danger">{{ scope.row.purchase_price|currency("- ¥") }}(仕入)</span>
                  <span class="d-block text-right text-danger">{{ scope.row.extra_cost|currency("- ¥") }}(付加)</span>
                </template>
              </el-table-column>
              <el-table-column
                label="ポイントポリシー"
                sortable
                prop="is_valid">
                <template slot-scope="scope">
                  <div v-if="scope.row.point_rule.is_valid">
                    <span class="d-inline-block text-right  mr-3">{{
                        $t("menuitems.organizations.user.client_superadmin")
                      }}:</span>{{ scope.row.point_rule.policies.client_superadmin|currency("¥") }} <br>
                    <span class="d-inline-block  text-right  mr-3">{{
                        $t("menuitems.organizations.user.client_admin")
                      }}:</span>{{ scope.row.point_rule.policies.client_admin|currency("¥") }} <br>
                    <span class="d-inline-block  text-right mr-3">{{
                        $t("menuitems.organizations.user.level_2")
                      }}:</span>{{ scope.row.point_rule.policies.level_2|currency("¥") }} <br>
                    <span class="d-inline-block  text-right mr-3">{{
                        $t("menuitems.organizations.user.level_1")
                      }}:</span>{{ scope.row.point_rule.policies.level_1|currency("¥") }} <br>
                    <span class="d-inline-block text-right mr-3">{{
                        $t("menuitems.organizations.user.user_self")
                      }}:</span>{{ scope.row.point_rule.policies.user_self|currency("¥") }}
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                label="Action">
                <template slot-scope="scope">

                  <a href="javascript:void(0);" @click="editVariation( scope.row)"
                     v-b-modal.modal_variation_component
                     class="action-icon">
                    <i class="fe-edit"></i></a>
                </template>
              </el-table-column>
            </el-table>
            <div class="row my-2" v-if="variations_meta.total>0">
              <div class="col">
                <div class="dataTables_paginate paging_simple_numbers float-right">
                  <ul class="pagination pagination-rounded">
                    <b-pagination v-model="variations_meta.page"
                                  pills
                                  aria-controls="pingoproduct_table"
                                  :total-rows="variations_meta.total"
                                  :per-page="variations_meta.page_size"
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
    <VariationModal @operateresult="VariationOperate" :showVariationModal="showVariationModal"
                    :edit_variation="edit_variation"></VariationModal>
  </div>

</template>
