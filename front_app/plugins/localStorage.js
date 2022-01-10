import createPersistedState from 'vuex-persistedstate'

export default ({store}) => {
  createPersistedState({
    key: 'vuex',
    paths: ['cart', "authfack", "products", "pingoproducts",
      "system", "orders", "client", "vendor", "points", "addressbook", "order", "points"]
  })(store)
}
