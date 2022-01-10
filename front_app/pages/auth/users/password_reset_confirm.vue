<template>
  <div>
    <Header/>
    <section class="register-page section-b-space">
      <div class="container">
        <div class="row">
          <div class="col-lg-6">
            <h3>{{ $t("auth.change_password_title") }}</h3>
            <div class="theme-card">
              <ValidationObserver v-slot="{ invalid }" ref="Validator">
                <form class="theme-form" @submit.prevent="validateBeforeSubmit">
                  <div class="form-row">
                    <div class="col-md-8">
                      <label for="password">{{ $t("auth.password") }}</label>
                      <ValidationProvider rules="required" v-slot="{ errors }" name="password">
                        <input type="password" class="form-control" id="password" v-model="password"
                               placeholder="Enter your password" name="password"/>
                        <span class="validate-error">{{ errors[0] }}</span>
                      </ValidationProvider>
                    </div>
                  </div>
                  <div class="form-row">
                    <div class="col-md-8">
                      <label for="senpassword">{{ $t("auth.confirm_password") }}</label>
                      <ValidationProvider rules="required|confirmed:password" v-slot="{ errors }" name="senpassword">
                        <input type="password" class="form-control" id="senpassword" v-model="senpassword"
                               placeholder="" name="senpassword"/>
                        <span class="validate-error" id='passerr' ref='passerr'>{{ errors[0] }}</span>
                      </ValidationProvider>
                    </div>
                  </div>
                  <div class="form-row">
                    <button type="submit" class="btn btn-solid mt-2">
                      {{ $t("auth.change_password_title") }}
                    </button>
                  </div>
                </form>
              </ValidationObserver>
            </div>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>

<script>
import {userService} from "~/helpers/user.service";
import {ValidationProvider, ValidationObserver} from 'vee-validate/dist/vee-validate.full.esm'
import {swalService} from "~/helpers/swal.service";


export default {
  name: 'password_reset_confirm',
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    ValidationProvider,
    ValidationObserver,
  },
  data() {
    return {
      error: "",
      uid: "",
      token: "",
      password: '',
      senpassword: '',
    }
  },
  mounted() {
    const query = this.$route.query;
    if (Object.keys(query).length && Object.keys(query).includes("uid") && Object.keys(query).includes("tokens")) {
      this.uid = this.$route.query.uid;
      this.token = this.$route.query.tokens;
    }
  },
  methods: {
    validateBeforeSubmit(values, actions) {
      let self = this;
      console.log(values, actions)
      if (this.uid !== "" && this.token !== "" && this.password !== "") {
        userService.reset_password_confirm({
          uid: this.uid,
          token: this.token,
          new_password: this.password,
          re_new_password: this.senpassword
        }).then(response => {
          if (response.result) {
            swalService.showToast("success","パスワードは変更されました。")
            self.$router.push("/account/login")
          }
        }).catch(error => {
            swalService.showToast("error","パスワード変更用の情報が正しくないです。再確認してください")
          console.log("password_reset error response: ", error)
        })
      }

    }
  }
}
</script>
