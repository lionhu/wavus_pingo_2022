<script>
import {mapGetters} from "vuex"
import Swal from "sweetalert2"

export default {
  name: "system_category_setting",
  components: {
    Switches: () => import('vue-switches'),
    "el-tree": () => import('element-ui/lib/tree'),
    "el-button": () => import('element-ui/lib/button')
  },
  data() {
    return {
      mode: "",
      vendor: {},
      menuitem: {
        title: "new node",
        parent: 1,
        active: false,
        isTitle: false,
        isMenuCollapsed: false,
        access: {
          superadmin: true,
          vendor: false,
          client_admin: false
        },
        icon: "ri-dashboard-line",
        badge: {
          text: "menuitems.dashboard.badge",
          variant: "success"
        },
        link: "",
      },
      menuitems: [],
      defaultProps: {
        label: 'title',
        children: 'children'
      },
      clicked_node_data: {},
      clicked_node: {},
    };
  },
  computed: {
    ...mapGetters({
      menuitems_store: "categories/getProductCategories"
    }),
  },
  mounted() {
    this.$store.dispatch("categories/load_superadmin_categorylist")
  },
  methods: {
    updateCategory() {
      let self=this;
      this.$store.dispatch("categories/updateCategory", this.menuitem)
        .then(response => {
          console.log(response)
          Swal.fire({
            title: "Success",
            html: "Category Information Updated",
            icon: "success"
          })
          let newChild = response;
          newChild.label = response.title;
          const parent = this.clicked_node.parent;
          const children = parent.data.children || parent.data;
          const index = children.findIndex(d => d.id === self.clicked_node_data.id);
          children.splice(index, 1, newChild);
        })
    },
    addCategory() {
      let self = this;
      this.$store.dispatch("categories/AddCategory", this.menuitem)
        .then(response => {
          Swal.fire({
            title: "Success",
            html: "Category Information Added",
            icon: "success"
          })
          if (self.clicked_node_data !== null) {
            const newChild = {id: response.id, label: response.title, children: []};
            console.log(newChild)
            if (!self.clicked_node_data.children) {
              self.$set(self.clicked_node_data, 'children', []);
            }
            self.clicked_node_data.children.push(newChild);
          }
        })
    },
    deleteCategory(node, data) {
      if (data.id !== 1) {
        const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
          },
          buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
          title: '再確認',
          html: "本当に削除しますか!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'はい!',
          cancelButtonText: 'いいえ',
          reverseButtons: true
        }).then((result) => {
          if (result.isConfirmed) {
            this.$store.dispatch("categories/deleteCategory", data.id)
              .then(response => {
                Swal.fire({
                  title: "Success",
                  html: "Category Information Deleted",
                  icon: "success"
                })
                const parent = node.parent;
                const children = parent.data.children || parent.data;
                const index = children.findIndex(d => d.id === data.id);
                children.splice(index, 1);
              })
          } else if (result.dismiss === Swal.DismissReason.cancel) {
            console.log("forget it!")
          }
        })

      }
    },
    show_addnew() {
      this.mode = "add";
      this.menuitem = {
        title: "new node",
        parent: this.clicked_node_data !== null && this.clicked_node.level < 2 ? this.clicked_node_data.id : 2,
        active: false,
        isTitle: false,
        children: [],
        isMenuCollapsed: false,
        access: {
          superadmin: true,
          vendor: false,
          client_admin: false
        },
        icon: "ri-dashboard-line",
        badge: {
          text: "menuitems.dashboard.badge",
          variant: "success"
        },
        link: "",
      }
    },
    add_toplevel_category(){
      this.clicked_node=null;
      this.clicked_node_data=null;
      this.show_addnew();
    },
    NodeSelected(data, node, etc) {
      if (data.id !== 1 && data.id !== 2) {
        this.mode = "edit"
        this.menuitem = data;
        this.clicked_node_data = data;
        this.clicked_node = node;
      }
    },
  }
};
</script>
<template>
  <div>

    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h5>カテゴリ編集:</h5>
            <div class="row mb-2">
              <div class="col-sm-6 col-xs-12">
                <a href="javascript:void(0);" class="btn btn-danger mb-2" @click="show_addnew"><i
                  class="mdi mdi-plus-circle mr-1"></i> カテゴリ追加
                </a>
              </div>
              <div class="col-sm-6 col-xs-12">
                <div class="float-sm-right">
                  <button type="button" class="btn btn-success mb-2 mb-sm-0" @click="add_toplevel_category">
                    <i class="fe-settings"></i>Topカテゴリ追加
                  </button>
                </div>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-sm-6">
                <el-tree
                  :data="menuitems_store"
                  :accordion="true"
                  highlight-current
                  :props="defaultProps"
                  node-key="id"
                  default-expand-all
                  @node-click="NodeSelected"
                  :expand-on-click-node="false">
                  <span class="custom-tree-node" slot-scope="{ node, data }">
                  <span>{{ node.label }}({{ data.id }})</span>
                  <span>
                    <el-button
                      type="text"
                      size="mini"
                      @click="() => edit_node(data)" v-if="data.id!==1 && data.id!==2">
                      Edit
                    </el-button>
                    <el-button
                      type="text"
                      size="mini"
                      @click="() => deleteCategory(node,data)" v-if="data.id!==1 && data.id!==2">
                      Delete
                    </el-button>
                  </span>
                </span>
                </el-tree>
              </div>

              <div class="col-sm-6" v-if="mode==='edit' ||mode==='add'">
                <h5 v-if="mode==='edit'">ID: {{ menuitem.id }}</h5>
                <switches v-model="menuitem.is_valid" id="tests" theme="bootstrap" color="warning"
                          class="ml-1 my-auto"></switches>
                <b-form-group id="fieldset-title" label-cols="4" label-cols-lg="2" label-size="sm" label="Text">
                  <b-form-input id="title" v-model="menuitem.title"></b-form-input>
                </b-form-group>
                <b-form-group id="fieldset-parent" label-cols="4" label-cols-lg="2" label-size="sm" label="ParentID"
                              v-if="mode==='add'">
                  <b-form-input id="parent" v-model="menuitem.parent"></b-form-input>
                </b-form-group>
                <b-form-group id="fieldset-link" label-cols="4" label-cols-lg="2" label-size="sm" label="Link">
                  <b-form-input id="link" v-model="menuitem.link"></b-form-input>
                </b-form-group>
                <b-button variant="primary" @click="updateCategory" v-if="mode==='edit'">Updata</b-button>
                <b-button variant="primary" @click="addCategory" v-if="mode==='add'">Save</b-button>
              </div>

              <!-- end col-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
