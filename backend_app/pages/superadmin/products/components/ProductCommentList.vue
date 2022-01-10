<script>
import Swal from "sweetalert2";
import {mapGetters} from "vuex";
import {APIServices} from "~/helpers/APIs"

export default {
  name: "product_comments_table",
  props: ["product"],
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    "el-popover": () => import('element-ui/lib/popover'),
    "el-button": () => import('element-ui/lib/button'),
  },
  data() {
    return {
      comments: [],
      multipleSelection: [],
      update_info: {}
    };
  },
  computed: {
    ...mapGetters({}),
    comments_query_url() {
      return `store/public/filter_comments/of_product/?query=${this.product.id}&omit=item`
    },
    selectionIDs() {
      let ids = [];
      this.multipleSelection.forEach(item => {
        ids.push(item.id)
      })
      return ids;
    }
  },
  mounted() {
    let self = this;
    this.load_product_comments();
  },
  methods: {
    async load_product_comments() {
      await APIServices.get(this.comments_query_url).then(APIServices.handleResponse)
        .then(response => {
          this.comments = response;
          console.log(response)
        })
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    async update(_id) {
      let self = this;
      let url = `store/public/comments/${_id}/`
      Swal.fire({
        icon:"warning",
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
    delete_comments_list() {
      console.log("delete_comments_list", this.selectionIDs)
      this.selectionIDs.forEach(comment_id => {
        let _index = this.comments.findIndex(comment => comment.id === comment_id)
        if (_index > -1) {
          this.comments.splice(_index, 1)
          Swal.fire({icon: "success", html: `${this.selectionIDs.length} comments deleted!}`})
        }
      })
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
  }
};
</script>
<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="row">
          <el-table
            :data="comments"
            @selection-change="handleSelectionChange"
            style="width: 100%">
            <el-table-column type="expand">
              <template slot-scope="props">
                <h6>コメント内容</h6>
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
              label="日期"
              width="200">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span style="margin-left: 10px">{{ scope.row.created_at|short_datetime }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="姓名"
              width="80">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>名前：{{ scope.row.user.username }}</p>
                  <p>メール：{{ scope.row.user.email }}</p>
                  <div slot="reference" class="name-wrapper">
                    <img :src="scope.row.user.avatar_thumb_url" class="mr-3 rounded-circle avatar-sm">
                  </div>
                </el-popover>

              </template>
            </el-table-column>
            <el-table-column
              label="Ups"
              width="80"
              prop="thumbs_up">
            </el-table-column>
            <el-table-column
              label="Downs"
              width="80"
              prop="thumbs_down">
            </el-table-column>
            <el-table-column
              label="承認"
              width="80"
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

</template>
