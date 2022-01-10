import {userService} from '~/helpers/user.service';
import Swal from 'sweetalert2'

const user = JSON.parse(localStorage.getItem('user'));

 const state = () => ({
  list: []
})
 const actions = {
  // Logs in the user.
  // eslint-disable-next-line no-unused-vars
  load_superadmin_users({dispatch, commit}, url) {
    // commit("setUserList", [])

    return new Promise((resolve, reject) => {
      userService.getAll(url).then(res => {
        if (res.result) {
          resolve(res.data.users.results)
        }
      })
    })
  },
  set_User_Role({commit}, {user_id, roles}) {
    return new Promise((resolve, reject) => {
      userService.setUserRole({user_id, roles}).then(res => {
        resolve(res.user)
      })
    })
  },
  update_user_information({commit}, {user_id, info}) {
    return new Promise((resolve, reject) => {
      userService.updateUserInfo({user_id, info}).then(res => {
        resolve(res.id)
      })
    })
  },
  update_user_profile_information({commit}, {user_id, info}) {
    return new Promise((resolve, reject) => {
      userService.updateUserProfileInfo({user_id, info}).then(res => {
        resolve(res.id)
      })
    })
  }
};

 const mutations = {
  setUserList(state, res) {
    console.log(res)
    if (res.results) {
      res.results.forEach(function (user) {
        if (user.roles) {
          user.role = user.roles[0]
        } else {
          user.role = ""
        }
        return user;
      })
    }


    state.list = res;
  },
  setUserRole(state, res) {
    const index = state.list.results.findIndex(user => user.id === res.id);
    if (index > -1) {
      if (res.roles) {
        res.role = res.roles[0]
      } else {
        res.role = ""
      }
      state.list.results.splice(index, 1, res);
    }
  }
};

 const getters={}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
