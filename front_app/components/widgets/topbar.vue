<script src="../../store/authfack.js"></script>
<template>
  <div class="top-header">
    <div class="container">
      <div class="row">
        <div class="col-lg-6">
          <div class="header-contact">
            <ul>
              <li>{{ $t('welcome') }}
                <a href="/account/register" class="theme-color font-weight-bold">新規無料登録</a>
              </li>
              <!--              <li>-->
              <!--                <i class="fa fa-phone" aria-hidden="true"></i>{{ $t('contact.title') }}: {{ company.phone }}-->
              <!--              </li>-->
            </ul>
          </div>
        </div>
        <div class="col-lg-6 text-right">
          <ul class="header-dropdown">
            <li class="mobile-wishlist">
              <nuxt-link :to="{ path: '/account/favorites' }">
                <i class="ti-heart" v-if="isLogin"></i>
              </nuxt-link>
            </li>
            <li class="onhover-dropdown mobile-account">

              <span class="theme-default" v-if="!isLogin">
                <i class="ti-user"></i>
              </span>
              <span class="theme-bgcolor" v-if="isLogin && ME.avatar_url==null">
                <i class="ti-user"></i>
                {{ ME.username }}
              </span>
              <nuxt-img :src="ME.avatar_thumb_url" quality="70" sizes="sm:32px lg:50px" class="nav-avatar"
                        v-if="isLogin && ME.avatar_thumb_url!==null"
              />
              <ul class="onhover-show-div">
                <li>
                  <a v-if="isLogin " @click="logout"> {{ $t("auth.logout") }}</a>
                  <nuxt-link v-if="!isLogin " :to="{ path: '/account/login' }">{{ $t("auth.login") }}
                  </nuxt-link>
                </li>
                <li>
                  <nuxt-link v-if="isLogin " :to="{ path: '/account' }">{{ $t("menu.dashboard") }}
                  </nuxt-link>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState, mapGetters} from 'vuex'
import {swalService} from "~/helpers/swal.service"

export default {
  name:"topbar",
  computed: {
    ...mapState({
      ME: state => state.auth.user,
      isLogin: state => state.auth.loggedIn,
    }),
    ...mapGetters({
      back_server: "system/getterBackServer",
      isClientAdmin: "authfack/isClientAdmin",
      isSuperAdmin: "authfack/isSuperAdmin",
      company: "system/getterCompanyInfo"
    }),
  },
  methods: {
    async logout() {
      await this.$auth.logout();
      swalService.showToast("success", "またお越し下さいませ！");
      this.$router.push({path: '/'})
    },
    jump_to_dashboard: function () {
      if (this.isClientAdmin) {
        this.$router.push({path: '/account/clientadmin/dashboard'})
      } else {
        this.$router.push({path: '/account/dashboard'})
      }
    }
  }
}
</script>
