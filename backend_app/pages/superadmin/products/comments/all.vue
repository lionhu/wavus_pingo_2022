<script>
import {swalService} from "~/helpers/swal.service"
import {mapGetters} from "vuex";
import {APIServices} from "@/helpers/APIs";
import Swal from "sweetalert2";

export default {
  name: "product_comments",
  middleware: ['router-auth', 'router-superadmin'],
  head() {
    return {
      title: `${this.title} | Pingo Admin`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    "el-select": () => import("element-ui/lib/select"),
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-popover": () => import('element-ui/lib/popover'),
    "el-button": () => import('element-ui/lib/button'),
    Switches: () => import('vue-switches'),
    ProductDetailCard: () => import('../components/ProductDetailCard'),
    CommentList: () => import('../components/ProductCommentList'),
  },
  data() {
    return {
      title: "商品コメント",
      items: [
        {text: "PINGO",},
        {text: "eCommerce",},
        {text: "商品詳細",},
        {text: "コメント", active: true,}
      ],
      comments: [],
      multipleSelection: [],
      update_info: {},
      approved: true,
      checked: true
    };
  },
  mounted() {
  },
  computed: {
    ...mapGetters({}),
    selectionIDs() {
      let ids = [];
      this.multipleSelection.forEach(item => {
        ids.push(item.id)
      })
      return ids;
    },
    comments_query_url() {
      return `store/public/filter_comments/all/?approved=${this.approved}&checked=${this.checked}`
    },
  },
  watch: {
    approved() {
      this.load_comments();
    },
    checked() {
      this.load_comments();
    },
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    async load_comments() {
      this.$nuxt.$loading.start();
      await APIServices.get(this.comments_query_url).then(APIServices.handleResponse)
        .then(response => {
          this.comments = response;
          console.log(response)
        })

      this.$nuxt.$loading.finish();
    },
    async update(_id) {
      let self = this;
      let url = `store/public/comments/${_id}/`
      Swal.fire({
        icon: "warning",
        title: '更新しますか？',
        showCancelButton: true,
        confirmButtonText: '更新',
        showLoaderOnConfirm: true,
        preConfirm: (login) => {
          return APIServices.patch(url, this.update_info).then(APIServices.handleResponse)
            .then(response => {
              return response;
            }).catch(error => {
              Swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        console.log(result)
        if (result.isConfirmed) {
          self.update_comments_list(result.value)
        }
      })
    },
    async approve_comment(_id) {
      this.multipleSelection = []
      this.multipleSelection.push(_id)

      const inputOptions = new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            '0': '未承認にする',
            '1': '承認にする'
          })
        }, 10)
      })

      const {value: isApproved} = await Swal.fire({
        title: '承認にしますか',
        input: 'radio',
        inputOptions: inputOptions,
        inputValidator: (value) => {
          if (!value) {
            return 'You need to choose something!'
          }
        }
      })

      if (isApproved) {
        this.update_info = {
          approved: isApproved
        }
        await this.update(_id);
      }
    },
    async check_comment(_id) {

      this.multipleSelection = []
      this.multipleSelection.push(_id)
      const inputOptions = new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            '0': '未確認にする',
            '1': '確認にする'
          })
        }, 10)
      })

      const {value: isChecked} = await Swal.fire({
        title: '確認にしますか',
        input: 'radio',
        inputOptions: inputOptions,
        inputValidator: (value) => {
          if (!value) {
            return 'You need to choose something!'
          }
        }
      })

      if (isChecked) {
        this.update_info = {
          checked: isChecked
        }
        await this.update(_id);
      }
    },
    update_comments_list(_comment) {
      let _index = this.comments.findIndex(comment => comment.id === _comment.id)
      if (_index > -1) {
        if (Object.keys(this.update_info).includes("checked")) {
          this.comments[_index].checked = _comment.checked
        }
        if (Object.keys(this.update_info).includes("approved")) {
          this.comments[_index].approved = _comment.approved
        }
        Swal.fire({icon: "success", html: `${this.selectionIDs.length} comments updated!}`})
      }
    }
  },
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body">

            <h3 class="header-title">条件</h3>
            <div class="row">
              <div class="col-6">
                <div class="form-group mb-3">
                  <label for="filter_approved">承認済み<span class="text-danger">*</span></label> <br>
                  <switches v-model="approved" id="filter_approved" type-bold="false"
                            color="warning"
                            class="ml-1 my-auto">

                  </switches>
                </div>
              </div>
              <div class="col-6">

                <div class="form-group mb-3">
                  <label for="filter_checked">確認済み<span class="text-danger">*</span></label> <br>
                  <switches v-model="checked" id="filter_checked" type-bold="false"
                            color="warning"
                            class="ml-1 my-auto">
                  </switches>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body">

            <h4 class="header-title">商品評価</h4>
            <div class="card">
              <div class="card-body">
                <div class="row">
                  <el-table
                    :data="comments"
                    @selection-change="handleSelectionChange"
                    style="width: 100%">
                    <el-table-column type="expand">
                      <template slot-scope="props">
                        <div class="d-flex justify-content-between">
                          <span class="d-inline-bloc font-weight-bold">コメント内容</span>
                          <span class="d-inline-block font-weight-bold">{{ props.row.created_at|short_datetime }}</span>
                        </div>
                        <hr>
                        <p v-html="props.row.content"></p>
                      </template>
                    </el-table-column>

                    <el-table-column
                      label="ID"
                      prop="id"
                      width="60">
                    </el-table-column>
                    <el-table-column
                      label="商品"
                      prop="item.id"
                      sortable
                      width="200">
                      <template slot-scope="scope">
                        <el-popover trigger="hover" placement="top">
                          <p>商品名：{{ scope.row.item.item_name }}</p>
                          <div slot="reference" class="name-wrapper">
                            <img :src="scope.row.item.thumbimage_url" class="mr-3 rounded-circle avatar-xl">
                          </div>
                        </el-popover>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="ユーザー"
                      prop="user.username"
                      sortable
                      width="80">
                      <template slot-scope="scope">
                        <el-popover trigger="hover" placement="top">
                          <p>名前：{{ scope.row.user.username }}</p>
                          <p>メール：{{ scope.row.user.email }}</p>
                          <div slot="reference" class="name-wrapper">
                            <img :src="scope.row.user.avatar_thumb_url" class="mr-3 rounded-circle avatar-md">
                          </div>
                        </el-popover>

                      </template>
                    </el-table-column>
                    <el-table-column
                      label="Ups"
                      width="80"
                      sortable
                      prop="thumbs_up">
                    </el-table-column>
                    <el-table-column
                      label="Downs"
                      width="80"
                      sortable
                      prop="thumbs_down">
                    </el-table-column>
                    <el-table-column
                      label="承認"
                      width="80"
                      sortable
                      prop="approved">
                      <template slot-scope="scope">
                        <a href="javascript:void(0);" @click="approve_comment(scope.row.id)">
                          <i class="ri-checkbox-circle-line text-success" v-if="scope.row.approved"></i>
                          <i class="ri-close-circle-fill text-danger" v-else></i>
                        </a>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="確認済み"
                      width="80"
                      sortable
                      prop="checked">
                      <template slot-scope="scope">
                        <a href="javascript:void(0);" @click="check_comment(scope.row.id)">
                          <i class="ri-checkbox-circle-line text-success" v-if="scope.row.checked"></i>
                          <i class="ri-close-circle-fill text-danger" v-else></i>
                        </a>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="内容">
                      <template slot-scope="scope">
                        {{ scope.row.content.substring(0, 40) }}...
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
