<template>
  <div>
    <particles-bg type="circle"
                  :canvas="{ backgroundColor: '#444' }" num="20" :bg="true"/>
    <div class="template-auth "
         v-bind:class="{'template-register-mobile':$device.isMobile,'template-register':!$device.isMobile}" style="">
      <div class="container">
        <div id="container" class="text-center float-right">
          <div class="row">
            <div class="col-12 bg-white p-5">

              <div class="logo mb-4">
                <nuxt-link :to="{ path: '/'}">
                  <img
                    :src="logoimage"
                    alt="Multikart_fashion"
                    class="img-fluid"
                  />
                </nuxt-link>
              </div>
              <h4 class="mb-3 font-weight-bold">
                {{ title }}
                <font-awesome-icon :icon="['fas', 'compact-disc']"
                                   class="font-awesome-size-solid fa-spin" v-if="isFollower"
                />
              </h4>
              <h5>{{ $t("auth.register") }}<i class="fas fa-user-friends" v-if="isFollower"></i></h5>
              <div class="theme-card text-left">
                <ValidationObserver v-slot="{ invalid }">
                  <form class="theme-form" @submit.prevent="onSubmit">
                    <div class="form-row mb-3">
                      <div class="col-md-12">
                        <!--                                            <label for="email">{{$t('auth.email')}}</label>-->
                        <ValidationProvider rules="required|email" v-slot="{ errors }" name="Email">
                          <p><span
                            v-bind:class="{ 'validate-error': isUsed, 'validate-correct': !isUsed }"
                            id='message' ref='message'></span></p>
                          <input type="email" class="form-control" id="email"
                                 v-model="email" :placeholder="$t('auth.email')" name="email"
                                 @keyup="verifyemail"/>
                          <span class="validate-error" id='emailerr' ref='emailerr'>{{ errors[0] }}</span>
                        </ValidationProvider>
                      </div>
                    </div>
                    <div class="form-row mb-3">
                      <div class="col-md-12">
                        <!--                                            <label for="email">{{$t('auth.username')}}</label>-->
                        <ValidationProvider rules="required|alpha_num" v-slot="{ errors }" name="Name">
                          <input type="text" class="form-control" id="name"
                                 v-model="name" :placeholder="$t('auth.username')" name="name"/>
                          <span class="validate-error" id='nameerr'
                                ref='nameerr'>{{ errors[0] }}</span>
                        </ValidationProvider>
                      </div>
                    </div>
                    <div class="form-row mb-3">
                      <div class="col-md-12">
                        <!--                                            <label for="password">{{$t('auth.password')}}</label>-->
                        <ValidationProvider rules="required" v-slot="{ errors }" name="password">
                          <input type="password" class="form-control" id="password"
                                 v-model="password"
                                 :placeholder="$t('auth.password')" name="password"/>
                          <span class="validate-error">{{ errors[0] }}</span>
                        </ValidationProvider>
                      </div>
                    </div>
                    <div class="form-row mb-3">
                      <div class="col-md-12">
                        <!--                                            <label for="senpassword">{{$t('auth.confirm_password')}}</label>-->
                        <ValidationProvider rules="required" v-slot="{ errors }" name="senpassword">
                          <input type="password" class="form-control" id="senpassword"
                                 v-model="senpassword"
                                 :placeholder="$t('auth.confirm_password')" name="senpassword"/>
                          <span class="validate-error" id='passerr'
                                ref='passerr'>{{ errors[0] }}</span>
                        </ValidationProvider>
                      </div>
                    </div>

                    <input class="form-control" id="introcode" hidden
                           v-model="introcode" name="introcode"/>
                    <p style="line-height:1.2rem;">入会お申込の前に、当社の <a href="/page/ECommerce" target="_blank">利用規約</a>・<a
                      href="/page/Privacy" target="_blank">個人情報保護方針</a>を必ずお読み下さい。</p>
                    <div>
                      <label for="agree_check"></label>
                      <input type="checkbox" id="agree_check" v-model="agreed"> <span
                      class="theme-color ml-2">同意する</span>
                    </div>
                    <div class="form-row">
                      <button type="submit" class="btn btn-solid mt-2 ml-2" :disabled="invalid || !agreed">
                        {{ $t('auth.register') }}
                      </button>
                    </div>
                  </form>
                </ValidationObserver>

                <div style="margin-top: 10px">
                  <a href="/account/login">{{ $t("auth.already_registered") }}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import {ValidationProvider, ValidationObserver} from 'vee-validate/dist/vee-validate.full.esm'
import Swal from "sweetalert2"
import {ParticlesBg} from "particles-bg-vue";
import {APIServices} from "~/helpers/APIs";
import error from "~/layouts/error";

export default {
  name: "front_register",
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    ValidationProvider,
    ValidationObserver,
    ParticlesBg
  },
  data() {
    return {
      logoimage: '/images/logo/pingo.svg',
      title: this.$t("welcome"),
      copyright: '©2021, Powered by WAVUS.',
      name: '',
      email: '',
      password: '',
      senpassword: '',
      introcode: "",
      introducer: "",
      isUsed: 'false',
      isFollower: false,
      register_for_pid: 0,
      register_for_product_type: "",
      agreed: false,
    }
  },
  computed: {
    jump_link() {
      if (this.register_for_pid === 0) {
        return ""
      }
      if (this.register_for_pid && this.register_for_product_type !== "") {
        return `/${this.register_for_product_type}/${this.register_for_pid}`
      }
    }
  },
  mounted() {
    let local_introcode = localStorage.getItem('introcode')
    let query_introcode = this.$route.query.introcode !== undefined ? this.$route.query.introcode : null;
    let introcode = "";
    let introcode_source = "query"
    if (query_introcode) {
      introcode = query_introcode;
    } else if (local_introcode) {
      introcode = local_introcode;
      introcode_source = "localStorage"
    }
    if (introcode) {
      this.verify_introcode(introcode);
    }
    let pid = this.$route.query.pid !== undefined ? this.$route.query.pid : null;
    let product_type = this.$route.query.p_type !== undefined ? this.$route.query.p_type : null;
    if (pid !== null && product_type !== null) {
      this.register_for_pid = pid;
      this.register_for_product_type = product_type;
    }
  },
  methods: {
    onSubmit() {
      let vm = this;
      if (vm.password === vm.senpassword) {
        if (vm.password.length < 6 || vm.password.length > 20) {
          Swal.fire({
            title: "パスワードお見直しください",
            icon: "warning",
            html: "パスワードは６桁〜２０桁内の半角英数字でご設定ください。"
          })
          return false
        }
        const userinfo = {
          "username": vm.name,
          "email": vm.email,
          "password": vm.password,
          "parent_introcode": vm.introcode
        };
        APIServices.post('auth/users/', userinfo)
          .then(response => {
            if (response.id > 0) {
              Swal.fire({
                title: "PinGo.jpへようこそ!",
                icon: "warning",
                html: "登録メールアドレスに認証コードを送信いたしました。認証コードを使って、ログインしてください。"
              })
              if (vm.jump_link !== '') {
                vm.$router.push({path: vm.jump_link, query: {"email": vm.email}})
              } else {
                vm.$router.push({path: '/account/login'})
              }
            }
          })
          .catch(error => {
            delete error.data.result;

            Swal.fire({
              title: "エラー",
              icon: "error",
              html: JSON.stringify(error.data)
            })
          })
      } else {
        this.$refs.passerr.innerText = this.$root.$t("auth.different_password")
      }

    },
    verifyemail() {
      const err = this.$refs.emailerr.innerText
      if (err == '') {
        APIServices.post('auth/users/validate_email/', {"email": this.email})
          .then(resp => {
            this.isUsed = false
            this.$refs.message.innerText = this.$root.$t("auth.valid_email")
          }).catch(error => {
          if (["L01", "L03", "L04"].includes(error.data.error_code)) {
            this.isUsed = true
            this.$refs.message.innerText = this.$root.$t("auth.invalid_email")
          }
        })
      } else {
        this.$refs.message.innerText = ""
      }
    },
    verify_introcode(introcode) {
      var vm = this;
      if (introcode !== undefined) {
        APIServices.post('auth/users/verify_introcode/', {"introcode": introcode})
          .then(function (res) {
            if (res.data.result) {
              vm.introcode = introcode;
              vm.isFollower = true;
              vm.introducer = res.data.data.username;
              // vm.title = `Introduced by ${res.data.data.username}`;
              localStorage.setItem("introcode", introcode);
            }
          })
          .catch(error => {
            vm.introducer = "";
            vm.introcode = "";
            vm.isFollower = false;
          })
      }
    }
  }
}
</script>

<style scoped>

/*.font-awesome-size {*/
/*  font-size: 30px;*/
/*  color: #696969;*/
/*}*/

.font-awesome-size-solid {
  /*font-size: 30px;*/
  color: #f83979;
}
</style>
