<template>
  <div class="text-center mt-4">
    <h2 class="mt-4">Activating</h2>
    <img src="images/logo/pingo_dark.svg" style="max-width:200px;" class="mt-4">
    <p v-if="error!==''">{{error}}</p>
  </div>
</template>

<script>
import {swalService} from "~/helpers/swal.service";

export default {
  name: 'activate',
  data() {
    return {
      error:""
    }
  },
  mounted() {
    const query = this.$route.query;
    if (Object.keys(query).length && Object.keys(query).includes("uid") && Object.keys(query).includes("tokens")) {
      let uid = this.$route.query.uid;
      let tokens = this.$route.query.tokens;
      this.activate(uid, tokens)
    }
  },
  methods: {
     activate(uid, token) {
       let self =this;
         this.$axios.post('auth/users/activation/', {
          uid: uid,
          token: token
        }).then(response =>{
          if (parseInt(response.status)===204){
            swalService.showToast("success","アカウントは有効化されました。ログインしてください。")
            self.$router.push("/account/login")
          }
        }).catch(error=>{
          swalService.showToast("error","無効なリンクです。再確認ください。")
         })
    }
  }
}
</script>
