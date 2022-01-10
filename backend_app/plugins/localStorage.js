import createPersistedState from 'vuex-persistedstate'

export default ({ store }) => {
  createPersistedState({
    key: 'vuex',
    paths: ['auth','authfack',"suppliers", 'layout',"system","categories","orders","logistics","products"]
  })(store)
}
