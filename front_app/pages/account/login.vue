<template>
  <div>
    <div :class="{'template-auth-mobile':$device.isMobile,'template-auth':!$device.isMobile}">
      <div class="container">
        <div id="container" class="text-center float-right">
          <div class="row">
            <div class="col-12 bg-white p-5 ml-6">

              <div class="logo mb-4">
                <nuxt-link :to="{ path: '/'}">
                  <img
                    :src="logoimage"
                    class="img-fluid"
                  />
                </nuxt-link>
              </div>
              <h4 class="mb-3">{{ title }}</h4>
              <h5>{{ $t("auth.login") }}</h5>
              <div class="theme-card text-left">
                <form class="theme-form" v-on:submit="checkForm" method="post">
                  <div v-if="errors.length">
                    <ul class="validation-error mb-3 text-danger">
                      <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                    </ul>
                  </div>
                  <div class="form-group">
                    <label for="email">{{ $t("auth.email") }}</label>
                    <input
                      class="form-control"
                      id="email"
                      ref="email"
                      v-model="email"
                      @blur="validEmail"
                      :placeholder="$t('auth.email')"
                      name="email"
                      required
                    />
                  </div>
                  <div class="form-group" v-if="showpassword">
                    <label for="password">{{ $t("auth.password") }}</label>
                    <input
                      type="password"
                      class="form-control"
                      id="password"
                      @keyup.enter="login"
                      v-model="password"
                      :placeholder="$t('auth.password')"
                      required
                    />
                  </div>
                  <div class="form-group" v-show="show_resend_activation">
                    <p class="theme-color">
                      メールはまだ有効化になっていないようです。 <br>
                      アクティベーションメールを再送しますか?
                    </p>

                    <a class="btn-solid btn float-right" href="javascript:void(0)" @click="resend_activation_mail">
                      再送 </a>
                  </div>
                  <!--                  <div class="form-group" v-show="showverify">-->
                  <!--                    <label for="verify">{{ $t('auth.email_verify_code') }}</label>-->
                  <!--                    <input-->
                  <!--                      class="form-control border-danger"-->
                  <!--                      id="verify"-->
                  <!--                      v-model="code"-->
                  <!--                      :placeholder="$t('auth.email_verify_code')"-->
                  <!--                      required-->
                  <!--                    />-->
                  <!--                  </div>-->
                  <a class="btn-solid btn  float-right" href="javascript:void(0)" @click="login"
                     v-if="!show_resend_activation">
                    {{ $t("auth.login") }} </a>
                </form>
              </div>
              <div style="margin-top: 10px">
                <a href="/account/forget-password">{{ $t("auth.forget_password") }}</a>
              </div>
              <div style="margin-top: 10px">
                <a href="/account/register">{{ $t("auth.wanto_register") }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import {mapState} from 'vuex'
import {swalService} from "~/helpers/swal.service";
import {userService} from "~/helpers/user.service";

export default {
  name: "front_login",
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs')
  },
  data() {
    return {
      logoimage: '/images/logo/pingo.svg',
      title: this.$t("welcome"),
      copyright: '© 2021, Powered by WAVUS.',
      errors: [],
      code: 'pingo',
      password: '',
      email: "",
      showverify: false,
      show_resend_activation: false,
      showpassword: true
    }
  },
  created() {
    if (this.$route.query.email) {
      this.email = this.$route.query.email;
    }
    if (this.$route.query.verification_code) {
      this.code = this.$route.query.verification_code;
      this.showverify = true;
    }
    const a = "E01";
    this.logout();
  },
  mounted() {
    this.$refs.email.focus();
  },
  computed: {
    ...mapState({
      mastererror: state => state.error.errors,
    }),
  },
  methods: {
    resend_activation_mail() {
      if (this.email !== "") {
        userService.resend_activation({email: this.email})
          .then(response => {
            console.log(response)
            swalService.showToast("success", "アクティベーションメールは再送されました。ご確認ください。")
          })
      }
    },
    checkForm() {
      this.errors = []
      if (!this.email) {
        this.errors.push(this.$root.$t("auth.require_email"))
      } else if (!this.validEmail(this.email)) {
        this.errors.push(this.$root.$t("auth.require_vaild_email"))
      }
      if (!this.password) {
        this.errors.push(this.$root.$t("auth.require_password"))
      }
      if (!this.errors.length) return true
      return false
    },
    validEmail() {
      let vm = this;
      let verified = true;
      if (userService.validEmailFormat(vm.email)) {
        userService.check_activation_status(vm.email)
          .then(response => {
            console.log(response)
            switch (response.error_code) {
              case "LE03":
                vm.show_resend_activation = true;
                break;
              case "LE02":
                vm.showverify = true;
                verified = false;
                break;
              case "LE01":
                console.log("not a registered mail")
                break;
              default:
                vm.showverify = false;
                verified = true;
                console.log("anything wrong?")
            }
          })
      }
      // console.log("verified", verified)
    },
    async login() {
      let self = this;
      let data = {
        "email": this.email,
        "password": this.password
      }
      if (this.showverify && this.code !== "") {
        data.verify_code = this.code
      }
      this.$nuxt.$loading.start();
      try {
        await this.$auth.loginWith('local', {data: data}).then(res => {
          console.log("loginWith ", res.data);
          console.log("result" in res.data);
          if ("result" in res.data && !res.data.result) {
            swalService.showToast("error", "メール、あるいはパスワードは間違いました。")
            return false;
          } else if (res.data.error_code === "wrong_verify_code") {
            swalService.showToast("error", "認証コード間違います。")
            return false;
          } else {
            self.$auth.fetchUser()
            self.$store.commit("authfack/set_user", self.$auth.user)
          }
        })
      } catch (err) {
        console.log("login error", err.response)
        swalService.showToast("error", "ログイン情報は間違いました。")
      }
      this.$nuxt.$loading.finish();
    },
    async logout() {
      await this.$auth.logout();
      console.log("logout finished!")
    },
  }
}
</script>
