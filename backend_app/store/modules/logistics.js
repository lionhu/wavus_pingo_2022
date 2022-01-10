import {logisticService} from '~/helpers/logistic.service';
import {swalService} from "~/helpers/swal.service"

export const state = () => ({
  list: []
})
export const actions = {
  load_Logistic_list({commit}) {
    logisticService.list_logistic()
      .then(response => {
        commit("set_logistic_list", response)
      });
  },
  // before renewal


  updateLogistic({commit}, {logistic_id, info}) {
    // return new Promise(resolve => {
    console.log({logistic_id: logistic_id, info: info})
    logisticService.update_logistic({logistic_id: logistic_id, info: info})
      .then(response => {
          if (response.result) {
            commit("updateLogistic", response.logistic)
            // resolve(response)
          }
        }
      );
    // })
  },
  createLogistic({commit}, info) {
    // return new Promise(resolve => {
    logisticService.create_logistic(info)
      .then(response => {
        if (response.result) {
          commit("addLogistic", response.logistic)
          // resolve(response)
        }
      });
    // })
  },
  removeLogistic({commit}, logistic_id) {
    // return new Promise(resolve => {
    logisticService.remove_logistic(logistic_id)
      .then(response => {
        if (response.result) {
          commit("removeLogistic", logistic_id)
        }
        // resolve(response)
      });
    // })
  },
};

export const mutations = {
  set_logistic_list(state, payload) {
    state.list = payload;
  },

  // before renewal


  updateLogistic(state, _logistic) {
    console.log("mutation updated logistic", _logistic)
    var index = state.list.findIndex(logistic => logistic.id === _logistic.id)
    console.log(index)
    if (index > -1) {
      state.list.splice(index, 1, _logistic)
      swalService.showToast("success", "Updated successfully!")
    }
  },
  removeLogistic(state, _logistic_id) {
    console.log("mutation remove logistic", _logistic_id)
    var index = state.list.findIndex(logistic => logistic.id === _logistic_id)
    if (index > -1) {
      state.list.splice(index, 1)
      swalService.showToast("success", "Removed successfully!")
    }
  },
  addLogistic(state, _logistic) {
    console.log("mutation addLogistic logistic", _logistic)
    state.lists.push(_logistic)
    swalService.showToast("success", "Added successfully!")
  }
};

export const getters = {
  getterLogistics: (state) => {
    return state.list
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
