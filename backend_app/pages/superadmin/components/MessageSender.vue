<script>
import {swalService} from "@/helpers/swal.service";
import {w3cwebsocket} from "websocket";

const W3CWebSocket = w3cwebsocket
export default {
  name: "message_sender",
  props: ["showModal", "user"],
  components: {},
  data() {
    return {
      title:`送信`,
      websocket_url: 'wss://www.pingo.jp/ws/notification/broadcast/?token=',
      ws: {},
      websocket_public_url: 'wss://www.pingo.jp/ws/public_notification/',
      ws_public: {},
      submitted: false,
      icons: ["warning", "error", "success", "info", "question"],
      positions: ['top', 'top-start', 'top-end', 'center', 'center-start', 'center-end', 'bottom', 'bottom-start', 'bottom-end'],
      notification: {
        icon: "success",
        message: "message",
        target: this.user.id,
        position: "top-end",
        message_title: "title",
        timer: true
      },
    };
  },
  mounted() {
    this.init_websocket()
    this.init_public_websocket()
  },
  methods: {
    init_websocket() {
      console.log("init_websocket")
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
      console.log("init_public_websocket")
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
        target: this.user.id,
        timer: this.notification.timer ? 0 : 3000
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
  },
};
</script>

<template>

  <b-modal id="send_user_message_modal"
           scrollable
           centered
           :title="title"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showModal"
  >
    <form @submit.prevent="sendMessage">


      <div class="card">
        <div class="card-body">
          <h4>{{user.username}}へ送信</h4>
          <div class="form-group row ">
            <div class="col-sm-6">
              <b-form-checkbox class="mb-2 mr-sm-2 mb-sm-0" v-model="notification.timer">固定メッセージ</b-form-checkbox>
            </div>
          </div>
          <div class="form-group row ">
            <div class="col-sm-12">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="タイトル" v-model="notification.message_title"
                       aria-label="Broadcasting message" aria-describedby="basic-addon2"/>
              </div>
            </div>
          </div>
          <div class="form-group row">
            <div class="col-md-6">
              <select class="form-control" v-model="notification.icon">
                <option v-for="_icon in icons">{{ _icon }}</option>
              </select>
            </div>
            <div class="col-md-6">
              <select class="form-control" v-model="notification.position">
                <option v-for="_position in positions">{{ _position }}</option>
              </select>
            </div>
          </div>
          <div class="form-group row mb-0">
            <div class="col-sm-12">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="メッセージ" v-model="notification.message"
                       aria-label="Broadcasting message" aria-describedby="basic-addon2"/>
                <div class="input-group-append">
                  <button class="btn btn-dark waves-effect waves-light" type="button" @click="sendMessage">送信
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!--      <div class="form-group row">-->
      <!--        <div class="col-8 offset-4">-->
      <!--          <button type="submit" class="btn btn-primary">登録</button>-->
      <!--        </div>-->
      <!--      </div>-->
    </form>

  </b-modal>

</template>
