<script>
import {mapGetters} from "vuex"
import {w3cwebsocket} from 'websocket'
import {swalService} from "~/helpers/swal.service"
import {APIServices} from "@/helpers/APIs";
import {userService} from "@/helpers/user.service";

const W3CWebSocket = w3cwebsocket

export default {
  name: "superadmin_system",
  head() {
    return {
      title: `${this.title} | Admin Dashboard`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    Category: () => import('./components/Category'),
    Cache: () => import('./components/Cache'),
    PointPolicy: () => import('./components/PointPolicy'),
    Logistic: () => import('./components/Logistic'),
    "el-select": () => import('element-ui/lib/select'),
    "el-option": () => import('element-ui/lib/option'),
  },
  data() {
    return {
      websocket_url: 'wss://www.pingo.jp/ws/notification/broadcast/?token=',
      ws: {},
      websocket_public_url: 'wss://www.pingo.jp/ws/public_notification/',
      ws_public: {},
      title: "サプライヤー",
      items: [
        {text: "PINGO"},
        {text: "eCommerce"},
        {text: "サプライヤー", active: true}
      ],
      userlist: [],
      loading: false,
      grouponservice: true,
      notification: {
        icon: "success",
        message: "message",
        target: 0,
        position: "top-end",
        message_title: "title",
        timer:true
      },
      icons: ["warning", "error", "success", "info", "question"],
      positions: ['top', 'top-start', 'top-end', 'center', 'center-start', 'center-end', 'bottom', 'bottom-start', 'bottom-end']
    };
  },
  computed: {
    ...mapGetters({
      loggedIn: "authfack/loggedIn"
    }),
    access_token() {
      return this.$auth.strategy.token.get();
    },
    access_token_valid() {
      return this.$auth.strategy.token.status().valid();
    }
  },
  watch: {
    loggedIn(newVal, oldVal) {
      if (!newVal) return;
      console.log("loggedIn")
      this.init_websocket()
      this.init_public_websocket()
    },
  },
  mounted() {
    this.init_websocket()
    this.init_public_websocket()
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
      if (this.order_filters.user_id) {
        let userIndex = this.userlist.findIndex(user => user.id === this.order_filters.user_id)
        if (userIndex > -1) {
          this.selectUser = this.userlist[userIndex]
        }
      }
    },

    init_websocket() {
      let self = this;
      self.$store.commit("authfack/set_websocket_status", false)
      if (this.access_token_valid && this.access_token !== "") {
        const websocket_url = self.websocket_url + this.access_token.split(" ")[1]
        self.ws = new W3CWebSocket(websocket_url)
        self.ws.onopen = (e) => {
          self.$store.commit("authfack/set_websocket_status", true)
          console.log("member client connected")

          function sendHeartBeater() {
            if (self.ws.readyState === self.ws.OPEN) {
              let number = Math.round(Math.random() * 0xFFFFFF)
              let _data = {
                'message_type': 'heartbeat',
                'message': number.toString()
              }
              self.ws.send(JSON.stringify(_data))
              setTimeout(sendHeartBeater, 6000 * 100)
            }
          }

          sendHeartBeater()
        }

        this.ws.onmessage = (e) => {
          console.log(e.data)
          if (typeof e.data === 'string') {
            const data = JSON.parse(e.data)
            console.log("from websocket server: ", data)
            if (data.message_type === "public_broadcast") {
              swalService.showToast(data.icon, data.message, data.position)
            }
          }
        }
      }

    },

    init_public_websocket() {
      let self = this;
      self.ws_public = new W3CWebSocket(self.websocket_public_url)
      self.ws_public.onopen = (e) => {
        console.log('public WebSocket Client Connected')
      }
      this.ws_public.onmessage = (e) => {
        console.log(e.data)
        if (typeof e.data === 'string') {
          const data = JSON.parse(e.data)
          console.log("daphne websocket server: ", data)
          if (data.message_type === "public_broadcast") {
            swalService.showToast(data.icon, data.message, data.position)
          }
        }
      }
    },
    sendMessage() {
      const _data = {
        message_type: 'public_broadcast',
        message: this.notification.message,
        icon: this.notification.icon,
        id: 0,
        read: false,
        title: this.notification.message_title,
        position: this.notification.position,
        hyper_link: "",
        target: this.notification.target,
        timer: this.notification.timer?0:3000
      }
      console.log(_data)
      if (!!this.notification.target) {
        console.log("send member notification")
        this.ws.send(JSON.stringify(_data))
      } else {
        console.log("send public notification")
        this.ws_public.send(JSON.stringify(_data))
      }
    },
    wsUpdateGrouponServiceStatus() {
      this.ws.send(JSON.stringify({
        message_type: "sys_opt",
        eventname: "close_groupon",
        args: {status: this.grouponservice}
      }))
    }
  },
  middleware: ['router-auth', 'router-superadmin']
};
</script>
<style>
.line-title-width {
  min-width: 45px !important;
}
</style>
<template>
  <div>
    <PageHeader :title="title" :items="items"/>
<!--    <div class="card">-->
<!--      <div class="card-body">-->
<!--        <h2>サービス有効化</h2>-->
<!--        <div class="row">-->
<!--          <div class="col-sm-12">-->
<!--            <h6 class="font-13 mt-4">下記のサービスをリアルタイムで有効化/無効化にすることができます。</h6>-->

<!--            <b-form inline>-->
<!--              <b-form-checkbox class="mb-2 mr-sm-2 mb-sm-0" v-model="grouponservice">共同購入サービス</b-form-checkbox>-->
<!--              <b-button variant="primary" @click="wsUpdateGrouponServiceStatus">更新</b-button>-->
<!--            </b-form>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
    <div class="card">
      <div class="card-body">
        <div class="form-group row ">

          <label class="col-sm-2 col-form-label">指定会員</label>
          <div class="col-sm-4">
            <div class="input-group">
              <el-select
                v-model="notification.target"
                filterable
                remote
                reserve-keyword
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
            </div>
          </div>
          <div class="col-sm-6">
            <b-form-checkbox class="mb-2 mr-sm-2 mb-sm-0" v-model="notification.timer">固定メッセージ</b-form-checkbox>
          </div>
        </div>
        <div class="form-group row ">

          <label class="col-sm-2 col-form-label">Title</label>
          <div class="col-sm-10">
            <div class="input-group">
              <input type="text" class="form-control" placeholder="タイトル" v-model="notification.message_title"
                     aria-label="Broadcasting message" aria-describedby="basic-addon2"/>
            </div>
          </div>
        </div>
        <div class="form-group row">
          <label class="col-md-2 col-form-label">Message Icon</label>
          <div class="col-md-10">
            <select class="form-control" v-model="notification.icon">
              <option v-for="_icon in icons">{{ _icon }}</option>
            </select>
          </div>
        </div>
        <div class="form-group row">
          <label class="col-md-2 col-form-label">Position</label>
          <div class="col-md-10">
            <select class="form-control" v-model="notification.position">
              <option v-for="_position in positions">{{ _position }}</option>
            </select>
          </div>
        </div>
        <div class="form-group row mb-0">

          <label class="col-sm-2 col-form-label">PinGo 広告</label>
          <div class="col-sm-10">
            <div class="input-group">
              <input type="text" class="form-control" placeholder="メッセージ" v-model="notification.message"
                     aria-label="Broadcasting message" aria-describedby="basic-addon2"/>
              <div class="input-group-append">
                <button class="btn btn-dark waves-effect waves-light" type="button" @click="sendMessage">送信</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Category/>
    <Cache/>
    <!--    <PointPolicy/>-->
    <!--    <Logistic/>-->
  </div>
</template>
