import Vue from 'vue'

// import ElementUI from 'element-ui';
//
// Vue.use(ElementUI);
export default () => {
  Vue.component('ElTree', () => import('element-ui/lib/tree'))
  // Vue.component('ElSlider', () => import('element-ui/lib/slider'))
  // Vue.component('ElContainer', () => import('element-ui/lib/container'))
}
