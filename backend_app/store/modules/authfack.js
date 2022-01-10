import {userService} from '~/helpers/user.service';

const state = {
  entry_role:"",
  user: {},
  websocket_status: false,
}

const actions = {
  // registeruser({dispatch, commit}, user) {
  //   commit('registerRequest', user);
  //   userService.register(user)
  //     .then(
  //       user => {
  //         commit('registerSuccess', user);
  //         dispatch('notification/success', 'Registration successful', {root: true});
  //         this.$router.push({path: "/account/login"});
  //       },
  //       error => {
  //         commit('registerFailure', error);
  //         dispatch('notification/error', error, {root: true});
  //       }
  //     );
  // },
  // validate({commit, state}) {
  //   if (!state.user) return Promise.resolve(null)
  //   if(!state.user){
  //       commit('logout');
  //   }
  //   return userService.validateToken().then(response => {
  //     return response;
  //   });
  //
  // },
};

const getters = {
  ME(state, getters, rootState, rootGetters) {
    return rootState.auth.user
  },
  loggedIn(state, getters, rootState, rootGetters) {
    return rootState.auth.loggedIn
  },
  entryRole(state){
    return state.entry_role;
  },
  isStaff(state) {
    if (state.user === null) return false;
    return state.user.roles.includes("staff")
  },
  isSupplier(state) {
    if (state.user === null) return false;
    return state.user.roles.includes("supplier")
  },
  isMember(state) {
    if (state.user === null) return false;
    return state.user.roles.includes("member")
  },
  isSuperadmin(state) {
    if (state.user === null) return false;
    return state.user.roles.includes("superadmin")
  },
  isClientAdmin(state) {
    return state.user != null ? state.user.roles.includes("client_admin") : false
  },
  isClientSuperAdmin(state, getters, rootState, rootGetters) {
    return state.user != null ? state.user.roles.includes("client_superadmin") : false
  },
};
const mutations = {
  set_user(state, {user,entry_role}) {
    state.user = user
    state.entry_role = entry_role
  },
  set_websocket_status(state, payload) {
    state.websocket_status = payload;
  },
  // update_user_profile(state,profile){
  //   state.user.profile=profile;
  //   console.log("updated profile",state.user.profile)
  // },
  // loginRequest(state, user) {
  //   state.status = {loggingIn: true};
  //   state.user = user;
  // },
  // loginSuccess(state, user) {
  //   state.status = {loggeduser: true};
  //   state.user = user;
  // },
  // loginFailure(state) {
  //   state.status = {};
  //   state.user = null;
  // },
  // logout(state) {
  //   state.status = {};
  //   state.user = null;
  //   // window.location.href = "/account/login"
  // },
  // registerRequest(state) {
  //   state.status = {registering: true};
  // },
  // registerSuccess(state) {
  //   state.status = {};
  // },
  // registerFailure(state) {
  //   state.status = {};
  // },
  // changeVendorContact(state,payload){
  //   state.user.vendor_info.email =payload.email;
  //   state.user.vendor_info.phone =payload.phone;
  // }
};


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
