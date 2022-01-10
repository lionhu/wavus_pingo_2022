<template>
  <div class="box">
    <div class="box-title">
      <h3>{{ $t('dashboard.avatar') }}</h3>
    </div>
    <div class="box-content text-center">
      <el-upload
        class="avatar-uploader"
        action="https://www.pingo.jp/daphne/api/auth/users/avatar/"
        :show-file-list="false"
        :headers="{'Authorization':access_token}"
        :data="{'id':ME.pk}"
        :on-success="handleImageSuccess"
        :before-upload="beforeAvatarUpload">
        <img v-if="ME.avatar_url" :src="ME.avatar_url" class="avatar">
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </div>
  </div>
</template>
<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 100%;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #ff4c3b;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 160px;
  height: 160px;
  line-height: 160px;
  text-align: center;
}

.avatar {
  width: 160px;
  height: 160px;
  display: block;
}
</style>
<script>

import {mapState, mapGetters} from "vuex"
import {swalService} from "@/helpers/swal.service"


export default {
  name: "user_avatar",
  data() {
    return {}
  },
  components: {
    "el-upload": () => import("element-ui/lib/upload"),
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME"
    }),
    access_token() {
      return this.$auth.strategy.token.get()
    },
  },
  methods: {
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt1M = file.size / 1024 / 1024 < 1;
      console.log(isLt1M)
      if (!isLt1M || !isJPG) {
        swalService.showModal("無効な写真", "1M　以下のJPEGフォーマットの写真でしょうか？", "warning")
        return false
      }
      return isJPG && isLt1M;
    },
    handleImageSuccess(res, file) {
      console.log("handleImageSuccess", res)
      if (res.result) {
        this.$store.commit("authfack/updateUserAvatar", res.data)
        window.location.reload()
      }
    },
  }
}
</script>
