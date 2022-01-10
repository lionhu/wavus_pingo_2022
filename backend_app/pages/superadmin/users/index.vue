<script>
import {mapState} from "vuex"
import {swalService} from "~/helpers/swal.service"
import Swal from "sweetalert2"
import {APIServices} from "@/helpers/APIs";
import {userService} from "@/helpers/user.service";

export default {
  name: "superadmin_user_management",
  head() {
    return {
      title: ` Admin Dashboard`,
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
    "UserRoleSelector": () => import('../components/UserRoleSelector'),
    "MessageSender": () => import('../components/MessageSender'),
  },
  data() {
    return {
      title: this.$t("menuitems.organizations.user.text"),
      items: [
        {text: "PINGO"},
        {text: "eCommerce"},
        {text: "Users", active: true}
      ],
      multipleSelection: [],
      searchkey: "",
      mode: "edit",
      user_selected: false,
      user: {
        username: "",
        id: 0
      },
      edit_user: {},
      childrenlist: [],
      props: {
        label: 'user.username',
        children: 'children',
        isLeaf: 'leaf',
        followers: 'get_descendants_count',
        user_id: 0
      },
      targetNodes: [],
      showRoleEditModal: false,
      userlist: [],
      list_type:"logging",
      showMessageSenderModal:false
    };
  },
  computed: {
    ...mapState({
      list: state => state.users.list
    }),
  },
  watch: {
    // perPage: function (val) {
    //   let url = `http://localhost:8000/apiauth/users/?page=1&page_size=${val}`
    //   this.load_users_list(url)
    // },
    // filter: function (val) {
    //   let url = `http://localhost:8000/apiauth/users/?page=1&page_size=${val}`
    //   this.load_users_list(url)
    // },
    filterText(val) {
      this.$refs.tree.filter(val);
    },
    searchkey(val){
      this.SearchUsers()
    }
  },
  methods: {
    async load_loggedIn_users(){
      let self = this;
      this.$nuxt.$loading.start();
      await APIServices.get("auth/search_active_users/get_users/").then(APIServices.handleResponse)
      .then(response=>{
        self.userlist=response
        self.list_type="logging"
      })
      this.$nuxt.$loading.finish();
    },
    async loadNode(node, resolve) {
      console.log("loadNode", node)
      let self = this;
      if (node.level === 0) {
        return resolve([{user:{username: 'PINGO.JP', id: 1}, follower: 0}]);
      }
      this.$nuxt.$loading.start();
      APIServices.get(`auth/search_profiles/retrieve_children/?query=${node.data.user.id}`)
        .then(APIServices.handleResponse)
        .then((response) => {
          console.log(response)
          let new_children = response.map((node) => {
            console.log("node",node)
            node.leaf = node.get_descendants_count===0;
            node.role = node.user.roles[0];
            return node;
          })
          self.childrenlist = new_children;

          self.list_type="descendants"
          resolve(new_children)
        });

      this.$nuxt.$loading.finish();
    },
    closeRoleEditorModal({result, user}) {
      this.showRoleEditModal = false;
      if (result) {
        this.refreshChildrenList(user);
        swalService.showModal('Change Role', 'Role has been changed', 'success')
      }
    },
    changeUserRole(user) {
      console.log("changeUserRole", user)
      this.edit_user = user;
      this.showRoleEditModal = true;
    },
    async setUserTransferPoint(profile) {
      console.log("profile", profile)
      let self = this;
      const selectOptions = {
        'true': '有効',
        "false": "無効"
      };
      const {value: canTransferPoint} = await Swal.fire({
        title: 'ポイント転送機能',
        input: 'radio',
        inputOptions: selectOptions,
        inputValue: `${profile.can_transfer_point}`,
        inputValidator: (value) => {
          console.log("inputValidator", value)
          if (!value) {
            return 'You need to choose something!'
          }
        }
      })
      console.log("canTransferPoint", canTransferPoint)
      if (canTransferPoint !== undefined) {
        this.updateUserProfileInformation(profile.user_id, {"can_transfer_point": canTransferPoint === 'true'})
      }

    },
    updateUserProfileInformation(user_id, info) {
      let self = this;
      APIServices.patch(`auth/profiles/${user_id}/`, {
        "can_transfer_point": info.can_transfer_point
      }).then(APIServices.handleResponse)
        .then((response) => {
          self.refreshChildrenList_canTransferPoint(response.id, info.can_transfer_point)
          swalService.showModal('Change canTransferPoint', 'canTransferPoint has been changed', 'success')
        })
    },
    refreshChildrenList_canTransferPoint(child_id, canTransferPoint) {
      let index = this.childrenlist.findIndex(child => child.user_id === parseInt(child_id))
      if (index > -1) {
        this.childrenlist[index].can_transfer_point = canTransferPoint;
      }
    },
    remove_user(user_id) {
      let self = this;
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
              return APIServices.post(`auth/users/${user_id}/destroy_user/`).then(APIServices.handleResponse)
                .then((response) => {
                  return {result: true}
                })
            }
          },
          allowOutsideClick: () => false
        }
      ).then((result) => {
        if (result.isConfirmed && result.value.result) {
          let index = self.childrenlist.findIndex(profile => profile.user_id === user_id)
          if (index > -1) {
            self.childrenlist.splice(index, 1)
            swalService.showToast("success", "ユーザーは削除されました!")
          }
        }
      })
    },

    resend_activation_mail(user) {
      let self = this;
      if (!user.is_active) {

        Swal.fire({
            title: 'Activationメールの再送?',
            html: "Activationメールを再度ユーザーへ送付しますか？",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'はい、確定!',
            showLoaderOnConfirm: true,
            preConfirm: (confirm) => {
              console.log("confirm", confirm)
              if (confirm) {
                return APIServices.post(`auth/users/resend_activation/`, {
                  email: user.email
                }).then(APIServices.handleResponse)
                  .then((response) => {
                    console.log(response)
                    return {result: true}
                  })
              }
            },
            allowOutsideClick: () => false
          }
        ).then((result) => {
          if (result.isConfirmed && result.value.result) {
            swalService.showToast("success", "Activationメールを再送いたしました!")
          }
        })
      }
    },
    user_moveto(user_id, username) {

      let vm = this;
      Swal.fire({
        title: '移動先のIDを入力してください。',
        input: 'number',
        inputAttributes: {
          autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: '移動先を確認する',
        showLoaderOnConfirm: true,
        preConfirm: (parentID) => {
          console.log("parentID", parentID)
          if (parseInt(parentID) !== 1) {
            let url = `auth/users/validate_transfer_user_ids/`;
            return APIServices.post(url, {"from_id": user_id, "to_id": parentID})
              .then(APIServices.handleResponse)
              .then(response => {
                console.log("response data", response)
                return response
              })
              .catch(error => {
                Swal.showValidationMessage(error.data.message)
              })
          } else {
            Swal.showValidationMessage(
              "Cannot move under Pingo.JP!"
            )
          }

        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        let to_user_id = parseInt(result.value.to_user.id);
        console.log(result.value)
        if (result.isConfirmed && to_user_id > 0) {
          Swal.fire({
            title: '再確認?',
            html: ` ${result.value.from_user.username}(#${result.value.from_user.id})　を${result.value.to_user.username}(#${result.value.to_user.id})の下に移動しますか？`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'はい、確定!',
            showLoaderOnConfirm: true,
            preConfirm: (confirm) => {
              if (result.isConfirmed) {
                let url = `auth/profiles/${user_id}/move_to_client_member/`;

                return APIServices.post(url, {"parent_id": to_user_id})
                  .then(APIServices.handleResponse)
                  .then(response => {
                    return {result: true}
                  }).catch(error => {
                    console.log(error)
                    swalService.showToast("error", "移動できませんでした。")
                  })
              }
            },
            allowOutsideClick: () => false
          }).then((result) => {
            if (result.isConfirmed && result.value.result) {
              swalService.showToast("success", "移動完了しました。画面をリフレッシュしてください。")
            }
          })
        }
      })
    },
    SearchUsers() {
      let self = this;
      if (this.searchkey !== "") {
        userService.query_search_user("email", this.searchkey)
          .then(response => {
            console.log(response)
            self.userlist = response
            self.list_type="search"
          })

      }
    },
    refreshChildrenList(user) {
      let index = this.childrenlist.findIndex(child => child.user.id === user.id)
      console.log(index)
      if (index > -1) {
        this.childrenlist.splice(index, 1, user);
      }
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
    toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
      console.log(this.multipleSelection)
    },

    ClickNode(data, Node, ev) {
      console.log("ClickNode data", data)
      console.log(data.user.username, data.user.id)
      if (data.user.username !== "" && data.user.username !== "PINGO.JP" &&data.user.username !== "wavus" && parseInt(data.user.id)) {
        this.user.username = data.user.username;
        this.user.id = data.user.id;
        this.user_selected = true;
      } else {
        this.user.username = "";
        this.user.id = 0;
        this.user_selected = false;
      }
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
      console.log(data)
      if (!value) return true;
      return data.users.username.includes(value);
    },
    login_location(location){
      return location!==undefined && Object.keys(location).includes("city")?`${location.city}@${location.ip}`:""
    },
    showMessageSender(user){
      this.user = user;
      this.showMessageSenderModal=true;
    }
  },
  middleware: ['router-auth', 'router-superadmin'],
}
;
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
          <i class="ri-alarm-warning-fill text-danger"
             v-if="data.role==='client_superadmin'||data.role==='client_admin'"></i>
          <span v-if="data.role==='client_superadmin'||data.role==='client_admin'">{{ data.client }}--</span>
          {{ data.user.username }}(#{{ data.user.id }})
        </span>
        <span>
          </span>
        </span>
            </el-tree>
          </div>
        </div>
      </div>
      <div class="col-md-6 col-xs-12" v-if="user_selected">
        <div class="card">
          <div class="card-body">
            <h6>{{ $t("menuitems.organizations.user.selected_user") }}:{{ user.username }}</h6>
            <p class="theme-color">* 下記の場合に限り、の移動は可能です。</p>
            <ul class="theme-color">
              <li>一般会員から一般会員の下へ</li>
              <li>一般会員から代理店の下へ</li>
              <li>代理店から一般会員の下へ</li>
            </ul>
            <div class="d-flex justify-content-between">
              <b-button variant="primary" @click="user_moveto(user.id,user.username)">
                {{ $t("menuitems.organizations.user.move_user") }}
              </b-button>
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
                <button type="button" class="btn btn-success mb-2 mb-sm-0" @click="load_loggedIn_users">
                  <i class="fe-users"></i>ログイン中ユーザー
                </button>
              </div>
              <div class="col-sm-12 col-md-6">
                <div id="tickets-table_filter" class="dataTables_filter text-md-right">

                  <div class="input-group d-inline-flex align-items-center">
                    <input type="text" class="form-control" placeholder="username or email"
                           aria-describedby="basic-addon2" v-model="searchkey"/>
                    <div class="input-group-append">
                      <button class="btn btn-dark waves-effect waves-light" type="button" @click="SearchUsers">Search
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Table -->
            <div class="row" v-if="list_type==='descendants'">
              <div class="col">
                <div class="table-responsive mb-0">
                  <el-table
                    ref="multipleTable"
                    :data="childrenlist"
                    tooltip-effect="dark"
                    style="width: 100%"
                    @selection-change="handleSelectionChange">
                    <el-table-column
                      type="selection"
                      width="55">
                    </el-table-column>

<!--                    <el-table-column type="expand">-->
<!--                      <template slot-scope="props">-->
<!--                        <h6>User ID: {{ props.row.user_id }}</h6>-->
<!--                        <h6>Email: {{ props.row.user.email }}</h6>-->
<!--                        <h6>登録回数: {{ props.row.user.login_count }}</h6>-->
<!--                        <h6>Role:</h6>-->
<!--                        <ul>-->
<!--                          <li v-for="role in props.row.user.roles" :key="role">{{ role }}</li>-->
<!--                        </ul>-->
<!--                      </template>-->
<!--                    </el-table-column>-->

                    <el-table-column
                      width="80"
                      label="ID">
                      <template slot-scope="scope">{{ scope.row.user.id }}</template>
                    </el-table-column>
                    <el-table-column
                      width="180"
                      label="username">
                      <template slot-scope="scope">{{ scope.row.user.username }}</template>
                    </el-table-column>
                    <el-table-column
                      width="120"
                      sortable
                      align="center"
                      label="Role">
                      <template slot-scope="scope">
                        <ul>
                          <li v-for="role in scope.row.user.roles">{{ role }}</li>
                        </ul>
                      </template>
                    </el-table-column>
                    <el-table-column
                      prop="can_transfer_point"
                      align="center"
                      width="80"
                      label="ポイント転送">
                      <template slot-scope="scope">
                        <button type="button" class="btn btn-rounded btn-sm ml-1"
                                @click="setUserTransferPoint(scope.row)"
                                v-bind:class="{'btn-success':scope.row.can_transfer_point,'btn-danger':!scope.row.can_transfer_point}">
                          <i class="fe-refresh-cw"></i>
                        </button>
                      </template>
                    </el-table-column>
                    <el-table-column
                      prop="get_descendants_count"
                      align="center"
                      width="80"
                      label="follower">
                      <template slot-scope="scope">
                        {{ scope.row.get_descendants_count }}
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="認証"
                      width="80"
                    >
                      <template slot-scope="scope">
                        <ul class="list-inline table-action m-0" v-if="scope.row.user!==undefined">
                          <!--                      <li class="list-inline-item">-->
                          <!--                        <a href="javascript:void(0)" @click="resend_activation_mail(scope.row.user)">-->
                          <!--                          <i class="fe-mail"-->
                          <!--                             v-bind:class="{'text-danger':!scope.row.user.is_verified,'text-success':scope.row.user.is_verified}"></i>-->
                          <!--                        </a>-->
                          <!--                      </li>-->
                          <li class="list-inline-item">
                            <a href="javascript:void(0)" @click="resend_activation_mail(scope.row.user)">
                              <i
                                v-bind:class="{'fe-x-circle text-danger':!scope.row.user.is_active,'fe-check-circle text-success':scope.row.user.is_active}"></i>
                            </a>
                          </li>
                        </ul>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="最後登録"
                    >
                      <template slot-scope="scope">
                        {{scope.row.user.last_login|short_datetime}} <br>
                        {{login_location(scope.row.user.last_location)}}

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
                            <a href="javascript:void(0);" class="action-icon">
                              <i class="mdi mdi-square-edit-outline"></i></a>
                          </li>
                          <li class="list-inline-item">
                            <a href="javascript:void(0);" class="action-icon"
                               @click="remove_user(scope.row.user_id)"
                               v-if="scope.row.user.username!=='wavus'">
                              <i class="fe-trash-2"></i></a>
                          </li>
                          <li class="list-inline-item">
                            <a href="javascript:void(0);" class="action-icon"
                               @click="changeUserRole(scope.row)" v-b-modal:modal-user-roles-selector>
                              <i class='fe-user'></i></a>
                          </li>

                        </ul>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </div>
            <div class="row" v-if="list_type==='logging'">
              <div class="col">
                <div class="table-responsive mb-0">
                  <el-table
                    ref="loggingList"
                    :data="userlist"
                    tooltip-effect="dark"
                    style="width: 100%">
                    <el-table-column
                      width="80"
                      label="ID">
                      <template slot-scope="scope">{{ scope.row.user.id }}</template>
                    </el-table-column>
                    <el-table-column
                      width="200"
                      label="ユーザー">
                      <template slot-scope="scope">{{ scope.row.user.username }}</template>
                    </el-table-column>
                    <el-table-column
                      label="メール">
                      <template slot-scope="scope">{{ scope.row.user.email }}</template>
                    </el-table-column>
                    <el-table-column
                      label="最後登録"
                      sortable
                      prop="created_at"
                    >
                      <template slot-scope="scope">
                        {{scope.row.created_at|short_datetime}}
                      </template>
                    </el-table-column>
                    <el-table-column
                      label=""
                    >
                      <template slot-scope="scope">
                        <a href="javascript:void(0)" v-b-modal:send_user_message_modal @click="showMessageSender(scope.row.user)">
                          <i class="ri-message-2-line"></i>
                        </a>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </div>
            <div class="row" v-if="list_type==='search'">
              <div class="col">
                <ul>
                  <li v-for="user in userlist">{{user.email}}(#{{user.id}})</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <UserRoleSelector :user="edit_user.user"
                      @closeModal="closeRoleEditorModal"
                      :showModal="showRoleEditModal"
    />
    <MessageSender :user="user" :showModal="showMessageSenderModal"></MessageSender>
  </div>
</template>
