<script>
import {mapState} from "vuex"
import {swalService} from "~/helpers/swal.service"

export default {
  name: "clientadmin_user_management",
  middleware: ['router-auth', 'router-clientadmin'],
  head() {
    return {
      title: ` Clients Admin Dashboard - Followers`,
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
    "el-input": () => import('element-ui/lib/input'),
    "el-tree": () => import('element-ui/lib/tree'),
  },
  data() {
    return {
      title: this.$t("menuitems.organizations.follower.title"),
      items: [
        {
          text: "PINGO"
        },
        {
          text: "eCommerce"
        },
        {
          text: this.$t("menuitems.organizations.follower.title"),
          active: true
        }
      ],
      searchkey: "",
      childrenlist: [],
      expands: [],
      expand_userinfo: {
        viewproducts: [],
        orderitems: []
      },
      loading_userinfo: false,
      props: {
        label: 'username',
        children: 'children',
        isLeaf: 'leaf',
        followers: 'get_descendants_count',
        user_id: 0
      },
    };
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user
    }),
  },
  methods: {
    loadNode(node, resolve) {
      let vm = this;
      if (node.level === 0) {
        return resolve([{username: this.ME.username, user_id: this.ME.profile.user_id, follower: 0}]);
      }
      this.$axios.post(`/apiauth/profile/${node.data.user_id}/retrieve_children/`).then((response) => {
        if (response.data.result) {
          var new_children = response.data.data.children.map((node) => {
            node.leaf = node.children.length === 0;
            node.role = node.roles[0];
            return node;
          })
          vm.childrenlist = new_children;
          resolve(new_children)
        }
      });
    },
    ClickNode(data, Node, ev) {
      var list = [];
      if (Node.childNodes.length > 0) {
        list = Node.childNodes.map((node) => {
          return node.data;
        })
      } else {
        list.push(Node.data)
      }
      this.childrenlist = list;
    },
    filterNode(value, data) {
      if (!value) return true;
      return data.username.includes(value);
    },
    getRowKeys: function (row) {
      return row.id
    },
    expandSelect: function (row, expandedRows) {
      var vm = this
      if (expandedRows.length) {
        vm.expands = []
        if (row) {
          vm.expands.push(row.id)
          vm.handleExpandRow(row.user_id);
        }
      } else {
        vm.expands = []
      }
    },
    handleExpandRow(user_id) {
      let vm = this;
      vm.loading_userinfo = true;
      this.$axios.post(`/back/store/api/viewproducts/${user_id}/of_user/`).then((response) => {
        let res = response.data;
        if (res.result) {
          vm.expand_userinfo.viewproducts = res.data.viewproducts;
          vm.expand_userinfo.orderitems = res.data.orderitems;
          swalService.showToast("success", "Loaded successfully!")
        } else {
          swalService.showToast("error", "Failed to loading users info!")
        }
      });
      vm.loading_userinfo = false;
    }
  },
}
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-xs-6 col-lg-8">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h5 class="text-muted font-weight-normal mt-0 text-truncate">{{ $t("menuitems.organizations.follower.tree") }}</h5>
                <el-tree
                  class="filter-tree"
                  :props="props"
                  :load="loadNode"
                  node-key="id"
                  @node-click="ClickNode"
                  lazy
                  :filter-node-method="filterNode"
                  ref="tree">
              <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>
          <i class="fe-users text-warning" v-if="!data.leaf"></i>
          <i class="fe-user text-success" v-else></i>
          {{ node.label }}
        </span>
        </span>
                </el-tree>
              </div>
              <div class="avatar-sm">
                <span class="avatar-title bg-soft-primary rounded">
                <i class="ri-team-fill fa-2x text-warning"></i></span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6 col-lg-4">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h5 title="Campaign Sent" class="text-muted font-weight-normal mt-0 text-truncate">
                  {{ $t("menuitems.organizations.follower.title") }}</h5>
                <h3 class="my-2 py-1">
                  <span data-plugin="counterup">{{ ME.profile.get_descendants_count }}</span></h3>
                <p class="mb-0 text-muted">
                  <span class="text-success mr-2">
                  <span class="mdi mdi-arrow-up-bold"></span>
                        3.27%
                    </span>
                  <span class="text-nowrap">Since last month</span>
                </p>
              </div>
              <div class="avatar-sm">
                <span class="avatar-title bg-soft-primary rounded">
                <i class="ri-parent-fill fa-2x text-success"></i></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-sm-12 col-md-6">
                <button type="button" class="btn btn-success mb-2 mb-sm-0">
                  <i class="fe-settings"></i>
                </button>
              </div>
            </div>
            <!-- Table -->
            <div class="table-responsive mb-0">
              <el-table
                ref="multipleTable"
                :data="childrenlist"
                tooltip-effect="dark"
                :row-key='getRowKeys'
                :expand-row-keys="expands"
                @expand-change="expandSelect"
                style="width: 100%">
                <el-table-column type="expand" width="50">
                  <template slot-scope="props">
                    <div class="row" v-if="loading_userinfo">
                      <div class="col-12 text-center">
                        <b-spinner class="m-2" variant="danger" role="status"></b-spinner>
                      </div>
                    </div>
                    <div class="row" v-else>
                      <div class="col-6">
                        <div class="card">
                          <div class="card-body">
                            <h4 class="header-title">ご覧になった製品</h4>
                            <p class="sub-header">
                              お客様がご覧になった製品一覧
                            </p>
                            <div class="row">
                              <div class="col-sm-2" v-for="vp in expand_userinfo.viewproducts" :key="vp.id">
                                <img :src="vp.product.thumbimage" style="max-width:80px;" alt="">
                              </div>

                            </div> <!-- end row-->

                          </div>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="card">
                          <div class="card-body">
                            <h4 class="header-title">購入製品</h4>
                            <p class="sub-header">
                              お客様が購入された製品一覧.
                            </p>
                            <div class="row">
                              <div class="col-sm-2" v-for="orderitem in expand_userinfo.orderitems" :key="orderitem.id">
                                <img :src="orderitem.item.thumbimage" style="max-width:80px;" alt="">
                              </div>

                            </div> <!-- end row-->

                          </div>
                        </div>
                      </div>
                    </div>

                  </template>
                </el-table-column>
                <el-table-column
                  prop="username"
                  :label="$t('menuitems.organizations.user.text')"
                  width="200">
                  <template slot-scope="scope">
                    {{ scope.row.username }}(#{{ scope.row.user_id }}) <br>
                    <a :href="'mailto:'+scope.row.email ">{{ scope.row.email }}</a>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="user_lastlogin"
                  align="center"
                  label="Last Login"
                  width="100">
                  <template slot-scope="scope">
                    {{ scope.row.user_lastlogin |short_datetime }}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="get_descendants_count"
                  align="center"
                  :label="$t('menuitems.organizations.follower.title')"
                  width="100">
                  <template slot-scope="scope">
                    {{ scope.row.get_descendants_count }}
                  </template>
                </el-table-column>
                <el-table-column
                  :label="$t('menuitems.ecommerce.points.text')"
                  width="160">
                  <template slot-scope="scope">
                    <span class="text-success" v-if="scope.row.validpoint_balance">{{ scope.row.validpoint_balance }} <i class=" ri-coin-fill"></i></span><br>
                    <span class="text-danger" v-if="scope.row.invalidpoint_balance">{{ scope.row.invalidpoint_balance }} <i class="ri-coin-line "></i> </span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="status"
                  width="80"
                >
                  <template slot-scope="scope">
                    <ul class="list-inline table-action m-0">
                      <li class="list-inline-item">
                        <i class="fe-mail"
                           v-bind:class="{'text-danger':!scope.row.is_verified,'text-success':scope.row.is_verified}"></i>
                      </li>
                      <li class="list-inline-item">
                        <i
                          v-bind:class="{'fe-x-circle text-danger':!scope.row.is_active,'fe-check-circle text-success':scope.row.is_active}"></i>
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
