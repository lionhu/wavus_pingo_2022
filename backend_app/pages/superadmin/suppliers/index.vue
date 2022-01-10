<script>
import {mapGetters} from "vuex"
import Swal from 'sweetalert2'
import {
  required,
  email,
  minValue,
  url
} from 'vuelidate/lib/validators'

import {axios} from '@/plugins/axios.js';
import {swalService} from "@/helpers/swal.service";

export default {
  name: "supplier_list",
  head() {
    return {
      title: `${this.title} | Admin Dashboard`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    ModalSupplierEdit: () => import("./components/SupplierEditModal")
  },
  data() {
    return {
      title: "サプライヤー",
      items: [
        {text: "PINGO"},
        {text: "eCommerce"},
        {text: "サプライヤー", active: true}
      ],
      auto_searching: false,
      autocomplete_address: false,
      searchkey: "",
      mode: "edit",
      supplier: {
        name: "",
        postcode: "",
        state: "",
        city: "",
        town: "",
        address_1: "",
        address_2: "",
        phone: "",
        email: "",
        website: "",
        admin_id: 0
      },
      supplier_admin_name: "",
      visible_supplierEdit: false,
      edit_supplier_id: 0,
      isLoading: false,
      supplierList: [],
      supplierListMeta: {
        links: {},
        page: 1,
        page_size: 100,
        total: 0,
      }
    };
  },
  computed: {
    options() {
      let _options = `?page_size=${this.supplierListMeta.page_size}&page=${this.supplierListMeta.page}&expand=user`
      if (this.searchkey !== "") {
        _options += "&filter{name__icontains}=${this.searchkey}"
      }
      return _options
    }
  },
  watch: {
    searchkey(newVal, oldVal) {
      if (newVal !== "") {
        this.load_suppliers_list()
      }
    },
  },
  mounted() {
    this.load_suppliers_list()
  },
  methods: {
    async load_suppliers_list() {
      let self=this;
      this.isLoading = true;
      await this.$store.dispatch("suppliers/load_supplier_list", this.options)
      .then(response=>{
        self.supplierList=response.results;
        self.supplierListMeta=response.meta;
      });
      this.isLoading = false;
    },

    tablePageChange(page) {
      this.supplierListMeta.page = page;
      this.load_suppliers_list()

    },
    removesupplierInfo(supplier_id) {
      if (supplier_id) {
        let vm = this;
        Swal.fire({
          title: '再確認?',
          html: "本当に削除しますか？",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'はい、確定!',
          showLoaderOnConfirm: true,
          preConfirm: (confirm) => {
            if (confirm) {
              return vm.$store.dispatch("suppliers/remove_supplier", supplier_id)
                .then((response) => {
                  vm.$bvModal.hide("modelFaq")
                  return {result: true}
                })
            }
          },
          allowOutsideClick: () => false
        }).then((result) => {
          if (result.isConfirmed && result.value.result) {
            swalService.showToast("success", "削除されました!")
          }
        })
      }
    },
    // SearchUsers() {
    //   if (this.searchkey !== "") {
    //     let option = `?page_size=${this.perPage}&expand=user&filter{name.icontains}=${this.searchkey}`
    //     this.load_suppliers_list(option)
    //   }
    // },
    show_supplier_Modal(supplier_id, mode) {
      console.log(supplier_id, mode)
      this.edit_supplier_id = supplier_id;
      this.mode = mode;
      this.visible_supplierEdit = true;
    },
    closesupplierModal(info) {
      console.log(info)
      this.visible_supplierEdit = false;
    }
  },
  middleware: ['router-auth', 'router-superadmin'],
};
</script>
<style>
.line-title-width {
  min-width: 45px !important;
}
</style>
<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row mb-2">
      <div class="col-sm-6 text-left">
        <b-button v-b-modal.modal-edit-supplier
                  variant="danger" @click="show_supplier_Modal(0,'add')">
          サプライヤー追加
        </b-button>
      </div>
      <div class="col-sm-6 text-right">
        <b-spinner variant="danger" v-if="isLoading"></b-spinner>&nbsp;
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <!--            <div class="row mb-2">-->
            <!--              <div class="col-sm-12 col-md-6">-->
            <!--              </div>-->
            <!--              <div class="col-sm-12 col-md-6">-->
            <!--                <div id="tickets-table_filter" class="dataTables_filter text-md-right">-->
            <!--                  <div class="input-group d-inline-flex align-items-center">-->
            <!--                    <input type="text" class="form-control" placeholder="名前の一部"-->
            <!--                           aria-describedby="basic-addon2" v-model="searchkey"/>-->
            <!--                    <div class="input-group-append">-->
            <!--                      <button class="btn btn-dark waves-effect waves-light" type="button" @click="SearchUsers">Search-->
            <!--                      </button>-->
            <!--                    </div>-->
            <!--                  </div>-->
            <!--                </div>-->
            <!--              </div>-->
            <!--            </div>-->
            <!-- Table -->
            <div class="table-responsive mb-0">
              <el-table
                ref="multipleTable"
                :data="supplierList"
                tooltip-effect="dark"
                style="width: 100%">
                <el-table-column prop="id" label="#ID" width="50"></el-table-column>
                <el-table-column
                  prop="name" align="center" label="name">
                  <template slot-scope="scope" class="text-center">
                    <h4>{{ scope.row.name }}</h4>
                    <h6>{{ scope.row.user.username }}</h6>
                  </template>
                </el-table-column>
                <el-table-column
                  label="Address">
                  <template slot-scope="scope">
                    <ul class="list-unstyled">
                      <li><span class="inline-block mr-1">ADD:</span>〒{{ scope.row.postcode }}
                        {{ scope.row.state }}{{ scope.row.city }}
                      </li>
                      <li>{{ scope.row.town }}{{ scope.row.address_1 }}</li>
                      <li>{{ scope.row.address_2 }}</li>
                      <li><span class="inline-block mr-1">TEL:</span>{{ scope.row.phone }}</li>
                      <li><span class="inline-block mr-1">Phone:</span>{{ scope.row.email }}</li>
                    </ul>
                  </template>
                </el-table-column>
                <el-table-column
                  show-overflow-tooltip>
                  <template slot-scope="scope">
                    <ul class="list-inline table-action m-0">
                      <li class="list-inline-item">
                        <a href="javascript:void(0);" class="action-icon">
                          <i class="mdi mdi-eye"></i></a>
                      </li>
                      <li class="list-inline-item">

                        <a href="javascript:void(0);" v-b-modal.modal-edit-supplier variant="danger"
                           @click="show_supplier_Modal(scope.row.id,'edit')">
                          <i class="fe-edit"></i>
                        </a>
                      </li>
                      <li class="list-inline-item">
                        <a href="javascript:void(0);" class="action-icon" @click="removesupplierInfo(scope.row.id)">
                          <i class="fe-trash-2"></i></a>
                      </li>
                    </ul>
                  </template>
                </el-table-column>
              </el-table>

              <div class="row my-2" v-if="supplierListMeta.total">
                <div class="col">
                  <div class="dataTables_paginate paging_simple_numbers float-right">
                    <ul class="pagination pagination-rounded">
                      <b-pagination v-model="supplierListMeta.page"
                                    pills
                                    aria-controls="pingoproduct_table"
                                    :total-rows="supplierListMeta.total"
                                    :per-page="supplierListMeta.page_size"
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
    <ModalSupplierEdit :showModal="visible_supplierEdit" :mode="mode" :supplier_id="edit_supplier_id"
                       @closeMoal="closesupplierModal"/>
  </div>
</template>
