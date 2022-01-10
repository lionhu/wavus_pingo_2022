<script>
import {mapGetters} from "vuex"
import {swalService} from "~/helpers/swal.service"
import {APIServices} from "@/helpers/APIs";

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
        {text: "PINGO"},
        {text: "eCommerce"},
        {text: this.$t("menuitems.organizations.follower.title"), active: true}
      ],
      searchkey: "",
      list_type: "children",
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
      isLoading: false,
      expand_user: 0
    };
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME"
    }),
  },
  methods: {
    loadNode(node, resolve) {
      console.log("loadNode", node, resolve)
      this.list_type = "children";
      let self = this;
      if (node.level === 0) {
        return resolve([{username: this.ME.username, user_id: this.ME.pk, follower: 0}]);
      }
      APIServices.post(`auth/profiles/${node.data.user_id}/retrieve_children/?page_size=10000&expand=user`)
        .then(APIServices.handleResponse)
        .then((response) => {
          let new_children = response.children.map((node) => {
            node.leaf = node.children.length === 0;
            node.role = node.roles[0];
            return node;
          })
          self.childrenlist = new_children;
          resolve(new_children)
        });
    },
    async load_all_descendants() {
      this.list_type = "all";
      let self = this;
      self.isLoading = true;
      await APIServices.post(`auth/profiles/${this.ME.profile.client}/retrieve_descendants/?page_size=10000&expand=user`)
        .then(APIServices.handleResponse)
        .then((response) => {
          self.childrenlist = response.children
          response.children.forEach(user => {
            delete user.children;
          });
        });

      self.isLoading = false;
    },
    ClickNode(data, Node, ev) {
      console.log("clickNode", data, Node)
      let list = [];
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
      return row.pk
    },
    expandSelect: function (row, expandedRows) {
      let self = this
      console.log("row", row)
      if (expandedRows.length) {
        self.expands = []
        if (row) {
          self.expands.push(row.id)
          self.handleExpandRow(row);
        }
      } else {
        self.expands = []
      }
    },
    async handleExpandRow(row) {
      let self = this;
      self.expand_user = row;
      let url = `store/public/viewproducthistory/${row.user_id}/user_list/?page_size=10000&expand=item`
      await APIServices.get(url).then(APIServices.handleResponse).then((response) => {
        console.log(response)
        self.expand_userinfo.viewproducts = response;
        swalService.showToast("success", "Loaded successfully!")
      });
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
                <h5 class="text-muted font-weight-normal mt-0 text-truncate">
                  {{ $t("menuitems.organizations.follower.tree") }}

                  <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1"
                            @click="load_all_descendants">
                    <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;すべて
                  </b-button>

                </h5>
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
                <i class="ri-team-fill fa-2x text-warning"></i>
                </span>
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
                <!--                <p class="mb-0 text-muted">-->
                <!--                  <span class="text-success mr-2">-->
                <!--                  <span class="mdi mdi-arrow-up-bold"></span>-->
                <!--                        3.27%-->
                <!--                    </span>-->
                <!--                  <span class="text-nowrap">Since last month</span>-->
                <!--                </p>-->
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
      <div class="col-8">
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
            <div class="row">
              <div class="col">
                <div class="table-responsive mb-0">
                  <el-table
                    ref="multipleTable"
                    :data="childrenlist"
                    tooltip-effect="dark"
                    :row-key='getRowKeys'
                    :expand-row-keys="expands"
                    @expand-change="expandSelect"
                    style="width: 100%"
                  >
                    <el-table-column type="expand">
                      <template slot-scope="props">
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
                      label="Last Login">
                      <template slot-scope="scope">
                        {{ scope.row.last_login |short_datetime }}
                      </template>
                    </el-table-column>
                    <el-table-column
                      prop="get_descendants_count"
                      align="center"
                      :label="$t('menuitems.organizations.follower.title')"
                      width="100">
                      <template slot-scope="scope">
                        {{ scope.row.get_descendants_count }}<i class=" ri-user-fill text-success"></i>
                      </template>
                    </el-table-column>
                    <el-table-column
                      :label="$t('menuitems.ecommerce.points.text')"
                      width="160">
                      <template slot-scope="scope">
                      <span>
                        {{ scope.row.pointbank_balance !== null ? scope.row.pointbank_balance : 0 }}
                        <i class=" ri-coin-fill text-success"></i>
                      </span>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="status"
                    >
                      <template slot-scope="scope">
                        <ul class="list-inline table-action m-0">
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
      <div class="col-4" v-if="expand_user!==null && expand_user.user_id>0">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col">
                <div class="table-responsive mb-0">
                  <div class="card">
                    <div class="card-body">
                      <h4 class="header-title">{{ expand_user.username }}</h4>
                      <h5>({{ expand_user.user.email }})</h5>
                      <div v-if="expand_user.id>0 && expand_userinfo.viewproducts.length>0">
                        <h4 class="header-title">ご覧になった製品</h4>
                        <p class="sub-header">お客様がご覧になった製品一覧</p>
                        <div>
                          <img :src="vp.item.thumbimage_url" style="max-width:120px;"
                               v-for="vp in expand_userinfo.viewproducts" :key="vp.id">
                        </div>
                      </div>
                      <div v-else>
                        <h4 class="header-title">ご覧になった製品</h4>
                        <p class="sub-header">まだご覧になっていないようです。</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
