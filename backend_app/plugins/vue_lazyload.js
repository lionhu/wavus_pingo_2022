import Vue from 'vue'
import VueLazyload from 'vue-lazyload'

const loadimage = require('~/assets/images/plugins/loading.gif')
const errorimage = require('~/assets/images/plugins/clear.png')

Vue.use(VueLazyload, {
  preLoad: 1.3,
  error: errorimage,
  loading: loadimage,
  attempt: 1
})
