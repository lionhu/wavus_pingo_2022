import Vue from 'vue'
import ElementUI from "element-ui"
Vue.use(ElementUI)

import {VueMasonryPlugin} from 'vue-masonry'
Vue.use(VueMasonryPlugin);

import VueLazyLoad from 'vue-lazyload'
Vue.use(VueLazyLoad,{
  preLoad: 1.3,
  error: 'https://dummyimage.com/130x120/ccc/999.png&text=Not+Found',
  loading: 'https://dummyimage.com/130x120/dcdcdc/999.png&text=Now loading',
  attempt: 1
});

import VueScrollTo from 'vue-scrollto';
Vue.use(VueScrollTo);

import VueSocialSharing from 'vue-social-sharing'
Vue.use(VueSocialSharing);

import Inview from 'vueinview'
Vue.use(Inview);
// Vue.jsでお手軽にパララックスを実装できる「vue-inview」
// https://www.kabanoki.net/5342/

import VShowSlide from 'v-show-slide'
Vue.use(VShowSlide)

import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'
Vue.use(VueAwesomeSwiper)


// http://vue-prlx.surge.sh/
import VuePrlx from 'vue-prlx'
Vue.use(VuePrlx);


export function disableLogs() {
  console.log = () => {};
  // or you can override any other stuff you want
}

process.env.NODE_ENV === "production" ? disableLogs() : null;
