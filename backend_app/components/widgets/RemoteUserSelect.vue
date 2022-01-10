<script>
import {userService} from "@/helpers/user.service";

export default {
  name: "remote_user_selector",
  components: {
    "el-select": () => import('element-ui/lib/select'),
    "el-option": () => import('element-ui/lib/option'),
  },
  data() {
    return {
      isLoading: false,
      selectUser: {},
      user_id:0,
      userlist: [],
      loading: false,
    };
  },
  methods: {
    querySearchUser(query) {
      let self = this;
      if (query.length) {
        self.loading = true;
        userService.query_search_user("email", query)
          .then(response => {
            self.userlist = response
            self.loading = false;
          })
      }
    },
    handleSelectUser() {
        let userIndex = this.userlist.findIndex(user => user.id === this.user_id)
        if (userIndex > -1) {
          this.selectUser = this.userlist[userIndex]
      this.$emit("SelectUser",this.selectUser)
        }
    },
    ResetUserSearch() {
      this.selectUser = null;
      this.user_id=0;
      this.$emit("SelectUser",null)
    },
  },
};
</script>

<template>
  <div>
    <el-select
      v-model="user_id"
      filterable
      remote
      reserve-keyword
      @change="handleSelectUser"
      placeholder="ユーザー名"
      :remote-method="querySearchUser"
      :loading="loading">
      <el-option
        v-for="item in userlist"
        :key="item.id"
        :label="item.email"
        :value="item.id">
      </el-option>
    </el-select>
    <b-button variant="primary" @click="ResetUserSearch" >Reset</b-button>
  </div>
</template>
