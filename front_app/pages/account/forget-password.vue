<template>
  <div>
    <Header />
    <Breadcrumbs title="Forget Password" />
    <section class="pwd-page section-b-space">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 offset-lg-3">
            <h2>{{ $t("auth.forget_password_title") }}</h2>
            <small>{{ $t("auth.forget_password_message") }}</small>
            <div class="theme-form">
              <div v-if="errors.length">
                <ul class="validation-error mb-3 text-danger">
                  <li v-for="(error, index) in errors" :key="index">
                    {{ error }}
                  </li>
                </ul>
              </div>
              <div class="form-row">
                <div class="col-md-12">
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="email"
                    placeholder="Enter Your Email"
                    name="email"
                    @blur="verifyEmail"
                    required
                  />
                </div>
                <button
                  class="btn-solid btn"
                  @click="onSubmit"
                  :disabled="invalid"
                >
                  {{ $t("auth.change_password_title") }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <Footer />
  </div>
</template>
<script>
import { userService } from "~/helpers/user.service";
import { swalService } from "~/helpers/swal.service";
import { APIServices } from "~/helpers/APIs";
import Swal from "sweetalert2";

export default {
  name: "request_reset_password",
  components: {
    Header: () => import("~/components/header/header1"),
    Footer: () => import("~/components/footer/footer1"),
    Breadcrumbs: () => import("~/components/widgets/breadcrumbs"),
  },
  data() {
    return {
      errors: [],
      email: null,
      invalid: true,
    };
  },
  methods: {
    checkForm: function () {
      this.errors = [];
      if (!this.email) {
        this.errors.push("Email required.");
        swalService.showToast("error", "Email required.");
      } else if (!this.validEmail(this.email)) {
        swalService.showToast("error", "Valid email required.");
        this.errors.push("Valid email required.");
      }

      if (!this.errors.length) return true;
      return false;
    },

    async verifyEmail() {
      let self = this;
      APIServices.post("auth/users/validate_email/", { email: this.email })
        .then((resp) => {
          self.invalid = true;
        })
        .catch((error) => {
          console.log(error);
          if (error.data.error_code === "L03") {
            Swal.fire({
              icon: "question",
              title: "メール承認済み?",
              html: "アカウントはまだ有効化されていないようです。再度メールにて承認メールを送付いたしますか",
              showCancelButton: true,
              showLoaderOnConfirm: true,
              cancelButtonText: "いいえ",
              confirmButtonText: "はい!",
              preConfirm: (login) => {
                vm.$nuxt.$loading.start();
                return userService
                  .resend_activation({ email: this.email })
                  .then((response) => {
                    vm.$nuxt.$loading.finish();
                    swalService.showToast(
                      "success",
                      "アクティベーションメールは再送されました。ご確認ください。"
                    );
                  });
              },
              allowOutsideClick: () => !Swal.isLoading(),
            });
          }
          if (error.data.error_code === "L04") {
            self.invalid = false;
          }
        });
    },

    validEmail: function (email) {
      return userService.validEmailFormat(email);
    },

    onSubmit() {
      APIServices.post("auth/users/reset_password/", {
        email: this.email,
      }).then((resp) => {
        console.log(resp);
        if (resp === "") {
          swalService.showToast(
            "success",
            "認証メールも送付いたしましたので、ご確認ください。"
          );
          this.$router.push("/");
        } else {
          swalService.showToast(
            "error",
            "システムエラー。管理者（crs@wavus.jp）までご連絡ください。"
          );
        }
      });
    },
  },
};
</script>
