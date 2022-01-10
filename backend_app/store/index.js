import Vue from 'vue'
import Vuex from 'vuex'
import authfack from './modules/authfack'
import categories from './modules/categories'
import clients from './modules/clients'
import layout from './modules/layout'
import logistics from './modules/logistics'
import margins from './modules/margins'
import notification from './modules/notification'
import orders from './modules/orders'
import pingoproducts from './modules/pingoproducts'
import system from './modules/system'
import products from './modules/products'
import users from './modules/users'
import suppliers from './modules/suppliers'
Vue.use(Vuex)
const createStore = () => {
  return new Vuex.Store({
    modules: {
      authfack,
      categories,
      clients,
      layout,
      logistics,
      margins,
      notification,
      orders,
      pingoproducts,
      products,
      system,
      users,
      suppliers
    }
  })
}
export default createStore
