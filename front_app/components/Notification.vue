<!-- Please remove this file from your project -->
<template>
  <div>
    <h2 style="display:none">Hello</h2>
  </div>
</template>
<script>
import {w3cwebsocket} from 'websocket'
import {mapState, mapGetters} from 'vuex'

const W3CWebSocket = w3cwebsocket

export default {
  name: 'notification',
  data() {
    return {
      websocket_url: 'wss://www.pingo.jp/ws/notification/broadcast/?token=',
      ws: {}
    }
  },
  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn,
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
    },

  },
  mounted() {
    this.init_websocket()
  },
  methods: {
    init_websocket() {
      let self = this;

      self.$store.commit("authfack/set_websocket_status", false)
      if (this.access_token_valid && this.access_token !== "") {
        const websocket_url = self.websocket_url + this.access_token.split(" ")[1]
        self.ws = new W3CWebSocket(websocket_url)
        self.ws.onopen = (e) => {
          console.log('WebSocket Client Connected')
          self.$store.commit("authfack/set_websocket_status", true)

          function sendHeartBeater() {
            if (self.ws.readyState === self.ws.OPEN) {
              let number = Math.round(Math.random() * 0xFFFFFF)
              let _data = {
                'message_type': 'heartbeat',
                'message': number.toString()
              }
              self.ws.send(JSON.stringify(_data))
              console.log(`send _data:`, _data)
              setTimeout(sendHeartBeater, 600 * 100)
            }
          }

          sendHeartBeater()
        }

        this.ws.onmessage = (e) => {
          if (typeof e.data === 'string') {
            const data = JSON.parse(e.data)
            console.log("from websocket server: ", data)
          }
        }
      }

    }
  }
}
</script>
