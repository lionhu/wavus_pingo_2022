<script>
import {mapGetters} from "vuex"
import Swal from 'sweetalert2'

export default {
  name:"ModalCategory",
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
        active: true,
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
      test_switch: false,
      // menuitems_store:[]
    };
  },
  computed: {
    ...mapGetters({
      menuitems_store: "categories/getterCategoryList"
    }),
  },
  mounted() {
    this.$store.dispatch("categories/load_superadmin_categorylist")
    // this.load_menuitems();
  },
  methods: {
    // load_menuitems(){
    //   let vm=this;
    //   this.menuitems_store=[];
    //   this.$axios.$get(`/back/store/api/categories/`).then(response => {
    //     console.log("loading menuitems",response)
    //     if (response.result) {
    //       vm.menuitems_store = response.data.categories.children;
    //     }
    //   })
    // },
    async show_swalModal(_menuitem, mode) {

      const {value: formValues} = await Swal.fire({
        title: mode ==='add'?'New Category':`Edit Category Id:${_menuitem.id}`,
        showCancelButton: true,
        html:
          `<input id="swal-input1" class="swal2-input" value="${_menuitem.title}" placeholder="title">` +
          `<input id="swal-input2" class="swal2-input"  value="${_menuitem.parent}" placeholder="parentID">` +
          `<input id="swal-input3" class="swal2-input"  value="${_menuitem.link}" placeholder="link">`,
        focusConfirm: false,
        preConfirm: () => {
          return [
            document.getElementById('swal-input1').value,
            document.getElementById('swal-input2').value,
            document.getElementById('swal-input3').value,
          ]
        }
      })

      console.log(formValues)
      if (formValues !== undefined && formValues.length) {
        let _title = formValues[0];
        let _parentID = formValues[1];
        let _link = formValues[2];
        if (_title !== '' && parseInt(_parentID) > 0) {
          var menuitem = {
            title: _title,
            parent: parseInt( _parentID),
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
            link: _link,
          }

          if (mode === "add") {
            this.$store.dispatch("categories/AddCategory", menuitem)
          } else {
            menuitem.id = _menuitem.id;
            this.$store.dispatch("categories/updateCategory", menuitem);
          }
        }
      }


    },
    async show_addnew() {
      var menuitem = {
        title: "title",
        parent: 1,
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
        link: "_link",
      }
      this.show_swalModal(menuitem,"add");
    },
    edit_node(data) {
      console.log(data.id)
      var vm = this;
      this.mode = "edit"
      this.menuitem = data;
      this.$axios.$get(`/back/store/api/categories/${data.id}/`).then(response => {
        if (response.result) {
          vm.menuitem = response.category;
          vm.show_swalModal(response.category, "edit");
        }
      })

    },
    NodeSelected(data, node, etc) {
      this.edit_node(data)
    },
    deleteCategory(category) {
      if (category.id !== 1) {
        this.$store.dispatch("categories/deleteCategory", category.id);
      }
    },
  }
};
</script>
<style>
.line-title-width {
  min-width: 45px !important;
}
</style>
<template>
  <div>
    <div class="row mb-2">
      <div class="col-12">
        <div class="float-sm-right">
          <button type="button" class="btn btn-success mb-2 mb-sm-0" @click="show_addnew">
            <i class="fe-plus"></i>
          </button>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
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
                  <span>{{ node.label }}</span>
                  <span>
                    <el-button
                      type="text"
                      size="mini"
                      @click="() => edit_node(data)"  v-if="data.id!==1 && data.id!==2">
                      Edit
                    </el-button>
                    <el-button
                      type="text"
                      size="mini"
                      @click="() => deleteCategory(data)"  v-if="data.id!==1 && data.id!==2">
                      Delete
                    </el-button>
                  </span>
                </span>
                </el-tree>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
