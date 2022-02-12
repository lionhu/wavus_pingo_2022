const state = {
  websocket_status: false,
  user: {}
};

const actions = {
  refresh_pointBalance({commit}) {
    this.$axios.get('store/public/pointbanks/me/')
      .then(resp => {
        if (resp.data.result) {
          commit("setPointBalance", resp.data.data)
        } else {
          commit("setPointBalance", 0)
        }
      })
  },
};

const mutations = {
  set_websocket_status(state, payload) {
    state.websocket_status = payload;
  },
  set_user(state, payload) {
    state.user = payload
  },
  setPointBalance(state, payload) {
    state.user.profile.pointbank_balance = payload.pointbank_balance;
  },
  updateUserAvatar(state, payload) {
    state.user.avatar_url = payload.avatar_url;
    state.user.avatar_thumb_url = payload.avatar_thumb_url;
  },
};

const getters = {
  ME(state, getters, rootState, rootGetters) {
    return rootState.auth.user
  },
  loggedIn(state, getters, rootState, rootGetters) {
    return rootState.auth.loggedIn
  },

  profile_info(state) {
    return state.user != null ? state.user.profile : {}
  },
  pointbank_balance(state) {
    return state.user.profile.pointbank_balance||0;
  },
  policies(state, getters, rootState, rootGetters) {
    if (getters.loggedIn){
      return state.user.profile.margin_policy
    }
    return null
  },
  isStaff(state, getters) {
    if (getters.ME === undefined) return false;
    return getters.ME.roles.includes("staff")
  },
  isMember(state, getters) {
    if (getters.ME === undefined) return false;
    return getters.ME.roles.includes("member")
  },
  isSuperadmin(state, getters) {
    if (getters.ME === undefined) return false;
    return getters.ME.roles.includes("superadmin")
  },
  isClientAdmin(state, getters, rootState, rootGetters) {
    if (getters.ME === undefined) return false;
    return getters.ME.roles.includes("client")
  },
  isClientSuperAdmin(state, getters, rootState, rootGetters) {
    if (getters.ME === undefined) return false;
    return getters.ME.roles.includes("client_superadmin")
  },
  getterWebSocketStatus(state) {
    return state.websocket_status;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
