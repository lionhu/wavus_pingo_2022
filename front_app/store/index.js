import Vue from 'vue'
import Vuex from 'vuex'
import authfack from './modules/authfack'
import cart from './modules/cart'
import layout from './modules/layout'
import menu from './modules/menu'
import products from './modules/products'
import system from './modules/system'
import orders from './modules/orders'
import addressbook from './modules/addressbook'
import points from './modules/points'
import pingoproducts from './modules/pingoproducts'
Vue.use(Vuex)
const createStore = () => {
  return new Vuex.Store({
    modules: {
      authfack,
      menu,
      products,
      pingoproducts,
      cart,
      layout,
      orders,
      addressbook,
      system,
      points
    }
  })
}
export default createStore
