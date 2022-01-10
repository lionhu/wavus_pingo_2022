<script>
import { mapGetters, mapState } from 'vuex'
import Swal from "sweetalert2";
// import {w3cwebsocket} from 'websocket'
// const W3CWebSocket = w3cwebsocket

export default {
  data () {
    return {
      // ws: new W3CWebSocket('wss://www.pingo.jp/ws/chat/lionhu/'),
      languages: [
        {
          flag: require('~/assets/images/flags/japan.png'),
          language: 'jp',
          title: 'Japanese',
        },
        {
          flag: require('~/assets/images/flags/us.jpg'),
          language: 'en',
          title: 'English',
        },
        {
          flag: require('~/assets/images/flags/china.png'),
          language: 'zh',
          title: 'Chinese'
        }
      ],
      current_language: this.$i18n.locale,
      text: null,
      flag: null,
      value: null,
    }
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user
    }),
   ...mapGetters({
      back_server:"system/getterBackServer"
    }),
  },
  mounted () {
    // const self = this
    // console.log(self.ws)
    // self.ws.onmessage = (e) => {
    //   if (typeof e.data === 'string') {
    //     const data = JSON.parse(e.data);
    //     if (data.message_type === "chat_message") {
    //       Swal.fire({
    //         icon: data.icon,
    //         title: data.title,
    //         html: data.message,
    //         showConfirmButton: false,
    //         timer: 3000
    //       })
    //     } else if (data.message_type === "sys_opt") {
    //       console.log(data.args.status)
    //       Swal.fire({
    //         icon: "info",
    //         title: data.event,
    //         html: JSON.stringify(data),
    //         showConfirmButton: false,
    //         timer: 3000
    //       })
    //     }
    //   }
    // }
    this.value = this.languages.find((x) => x.language === this.$i18n.locale)
    this.text = this.value.title
    this.flag = this.value.flag
  },
  methods: {
    // sendMessage() {
    //   this.ws.send(JSON.stringify({
    //     message: this.message,
    //     icon: this.icon,
    //     title: this.message_title,
    //     position: this.position
    //   }))
    // },
    // wsUpdateGrouponServiceStatus() {
    //   this.ws.send(JSON.stringify({
    //     message_type: "sys_opt",
    //     eventname: "close_groupon",
    //     args: {status: this.grouponservice}
    //   }))
    // },
    toggleMenu () {
      this.$parent.toggleMenu()
    },
    /**
     * Full screen
     */
    initFullScreen () {
      document.body.classList.toggle('fullscreen-enable')
      if (
        !document.fullscreenElement &&
        /* alternative standard method */
        !document.mozFullScreenElement &&
        !document.webkitFullscreenElement
      ) {
        // current working methods
        if (document.documentElement.requestFullscreen) {
          document.documentElement.requestFullscreen()
        } else if (document.documentElement.mozRequestFullScreen) {
          document.documentElement.mozRequestFullScreen()
        } else if (document.documentElement.webkitRequestFullscreen) {
          document.documentElement.webkitRequestFullscreen(
            Element.ALLOW_KEYBOARD_INPUT
          )
        }
      } else {
        if (document.cancelFullScreen) {
          document.cancelFullScreen()
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen()
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen()
        }
      }
    },
    /**
     * Toggle rightbar
     */
    toggleRightSidebar () {
      this.$parent.toggleRightSidebar()
    },
    /**
     * Set languages
     */
    setLanguage (locale, country, flag) {
      this.$i18n.locale = locale
      this.current_language = locale
      this.text = country
      this.flag = flag
    },
    horizonalmenu () {
      const element = document.getElementById('topnav-menu-content')
      element.classList.toggle('show')
    },
    logoutUser () {
      let self=this;
      this.$auth.logout().then((response) =>{
        self.$router.push({path: '/account/login'})
      })
    },
  },
}
</script>

<template>
  <!-- Topbar Start -->
  <div class="navbar-custom">
    <div class="container-fluid">
      <ul class="list-unstyled topnav-menu float-right mb-0">
        <b-nav-item-dropdown right class="notification-list topbar-dropdown" menu-class="profile-dropdown"
                             toggle-class="p-0"
        >
          <template slot="button-content" class="nav-link dropdown-toggle">
            <div class="nav-user mr-0">
              <img :src="ME.avatar_thumb_url" alt="user-image" class="rounded-circle"/>
              <span class="pro-user-name ml-1">
                            {{ ME ? ME.username : '' }}
                            <i class="mdi mdi-chevron-down"></i>
                        </span>
            </div>
          </template>

          <b-dropdown-header>
            <h6 class="text-overflow m-0 py-2">{{ $t('navbar.dropdown.name.list.greet') }}</h6>
          </b-dropdown-header>

<!--          <b-dropdown-item href="#">-->
<!--            <i class="remixicon-account-circle-line"></i>-->
<!--            <span>{{ $t('navbar.dropdown.name.list.account') }}</span>-->
<!--          </b-dropdown-item>-->

<!--          <b-dropdown-item href="#">-->
<!--            <i class="remixicon-settings-3-line"></i>-->
<!--            <span>{{ $t('navbar.dropdown.name.list.settings') }}</span>-->
<!--          </b-dropdown-item>-->

<!--          <b-dropdown-item href="#">-->
<!--            <i class="remixicon-wallet-line"></i>-->
<!--            <span>-->
<!--                        {{ $t('navbar.dropdown.name.list.mywallet') }}-->
<!--                        <span class="badge badge-success float-right">3</span>-->
<!--                    </span>-->
<!--          </b-dropdown-item>-->

<!--          <b-dropdown-item href="#">-->
<!--            <i class="remixicon-lock-line"></i>-->
<!--            <span>{{ $t('navbar.dropdown.name.list.lockscreen') }}</span>-->
<!--          </b-dropdown-item>-->

          <b-dropdown-divider></b-dropdown-divider>
          <a class="dropdown-item" @click="logoutUser" href="javascript: void(0);">
            <i class="fe-log-out mr-1"></i>
            <span>{{ $t('navbar.dropdown.name.list.logout') }}</span>
          </a>
        </b-nav-item-dropdown>

        <li class="dropdown notification-list" v-if="ME.role==='superadmin'">
          <a href="javascript:void(0);" @click="toggleRightSidebar" class="nav-link right-bar-toggle toggle-right">
            <i class="fe-settings noti-icon toggle-right"></i>
          </a>
        </li>
      </ul>

      <!-- LOGO -->
      <div class="logo-box">
        <nuxt-link to="/" class="logo logo-dark text-center">
                <span class="logo-sm">
                    <img src="~/assets/images/logo-sm-dark.png" alt height="24"/>
                  <!-- <span class="logo-lg-text-light">Minton</span> -->
                </span>
          <span class="logo-lg">
                    <img src="~/assets/images/logo-dark.png" alt height="20"/>
            <!-- <span class="logo-lg-text-light">M</span> -->
                </span>
        </nuxt-link>

        <nuxt-link to="/" class="logo logo-light text-center">
                <span class="logo-sm">
                    <img src="~/assets/images/logo-sm.png" alt height="24"/>
                </span>
          <span class="logo-lg">
                    <img src="~/assets/images/logo-light.png" alt height="20"/>
                </span>
        </nuxt-link>
      </div>

      <ul class="list-unstyled topnav-menu topnav-menu-left m-0">
        <li>
          <button class="button-menu-mobile waves-effect waves-light" @click="toggleMenu">
            <i class="fe-menu"></i>
          </button>
        </li>

        <li>
          <a class="navbar-toggle nav-link" data-toggle="collapse" @click="horizonalmenu()"
             data-target="#topnav-menu-content"
          >
            <div class="lines">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </a>
        </li>
<!--        <b-nav-item-dropdown class="d-none d-lg-block">-->
<!--          <template slot="button-content">-->
<!--            {{ $t('navbar.dropdown.createnew.text') }}-->
<!--            <i class="mdi mdi-chevron-down"></i>-->
<!--          </template>-->
<!--          <b-dropdown-item href="#">-->
<!--            <i class="fe-briefcase mr-1"></i>-->
<!--            <span>{{ $t('navbar.dropdown.createnew.list.projects') }}</span>-->
<!--          </b-dropdown-item>-->
<!--          <b-dropdown-item href="#">-->
<!--            <i class="fe-user mr-1"></i>-->
<!--            <span>{{ $t('navbar.dropdown.createnew.list.users') }}</span>-->
<!--          </b-dropdown-item>-->
<!--          <b-dropdown-item href="#">-->
<!--            <i class="fe-bar-chart-line- mr-1"></i>-->
<!--            <span>{{ $t('navbar.dropdown.createnew.list.revenue') }}</span>-->
<!--          </b-dropdown-item>-->
<!--          <b-dropdown-item href="#">-->
<!--            <i class="fe-settings mr-1"></i>-->
<!--            <span>{{ $t('navbar.dropdown.createnew.list.settings') }}</span>-->
<!--          </b-dropdown-item>-->
<!--          <b-dropdown-item href="#">-->
<!--            <i class="fe-headphones mr-1"></i>-->
<!--            <span>{{ $t('navbar.dropdown.createnew.list.help') }}</span>-->
<!--          </b-dropdown-item>-->
<!--        </b-nav-item-dropdown>-->
      </ul>
      <div class="clearfix"></div>
    </div>
  </div>
  <!-- end Topbar -->
</template>
