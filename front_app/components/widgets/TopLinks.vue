<template>

  <div class="breadcrumb-section pingo_toplink">
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <nav aria-label="breadcrumb" class="theme-breadcrumb">
            <ol class="breadcrumb " style="text-transform:none !important;">
              <li class="breadcrumb-item" v-for="item in items" :key="item.text">
                <a :href="item.link">{{ item.text }}</a>
              </li>
              <li class="breadcrumb-item">
                <a href="/sharebuy">{{ $t("services.share_sales.title") }}</a>
              </li>
              <li class="breadcrumb-item" v-if="gettersGrouponBuyServiceStatus">
                <a href="/tomobuy">{{ $t("services.tomo_sales.title") }}</a>
              </li>
            </ol>
          </nav>
        </div>
      </div>
    </div>
  </div>

</template>
<style>
.pingo_toplink {
  padding: 10px !important;
}
</style>
<script>
import {w3cwebsocket} from 'websocket'
import {swalService} from "~/helpers/swal.service"

const W3CWebSocket = w3cwebsocket
import {mapGetters, mapState} from 'vuex'

export default {
  name: "pingo_top_links",
  data() {
    return {
      websocket_public_url: 'wss://www.pingo.jp/ws/public_notification/',
      ws_public: {},
      websocket_url: 'wss://www.pingo.jp/ws/notification/broadcast/?token=',
      ws: {},
      items: [
        {text: this.$t("pingo.about"), link: "/page/aboutPingo"},
        // {text:  $t("services.tomo_sales.title"), link: "/shop/all"},
        // {text:$t(),link:"/"},
      ]
    }
  },
  computed: {
    ...mapGetters({
      gettersGrouponBuyServiceStatus: "system/gettersGrouponBuyServiceStatus",
      ME: "authfack/ME"
    }),
    ...mapState({
      loggedIn: state => state.auth.loggedIn,
      user: state => state.auth.user,
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
      this.init_websocket()
    },

  },
  mounted() {
    if (this.loggedIn) {
      this.init_websocket()
    }
    this.init_public_websocket()
  },
  methods: {
    init_public_websocket() {
      let self = this;
      self.ws_public = new W3CWebSocket(self.websocket_public_url)
      self.ws_public.onopen = (e) => {
        console.log('WebSocket Client Connected')
      }
      this.ws_public.onmessage = (e) => {
        if (typeof e.data === 'string') {
          const data = JSON.parse(e.data)
          if (data.target === 0) {
            swalService.showToast(data.icon, data.message, data.position, data.timer)
          } else {
            if (this.loggedIn) {
              if (this.ME.pk === data.target) {
                swalService.showToast(data.icon, data.message, data.position, data.timer)
              }
            }
          }
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
          if (typeof e.data === 'string') {
            const data = JSON.parse(e.data)
            console.log(data)
            if (data.message_type === "public_broadcast") {
              swalService.showToast(data.icon, data.message, data.position, data.timer)
            }
          }
        }
      }

    }
    ,
  }
}
</script>
