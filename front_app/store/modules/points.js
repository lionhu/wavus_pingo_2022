import {pointService} from '~/helpers/point.service'


 const state = () => ({
  pointlist: [],
  pointlist_meta: {},
  pointbank_balance: 0,
  point: {},
  point_summary: []
});
// getters
 const getters = {
  getterPointList: (state) => {
    return state.pointlist
  },
  getterPointListMeta: (state) => {
    return state.pointlist_meta
  },
  getterPointBankBalance: (state) => {
    return state.pointbank_balance || 0
  },
  getterPointSummary: (state) => {
    return state.point_summary
  },
};
// mutations
 const mutations = {
  setPointList: (state, payload) => {
    state.pointlist = payload.results;
    state.pointlist_meta = payload.meta;
  },
  setPointHistorySummary: (state, payload) => {
    state.point_summary = payload.point_summary;
    state.point_balance = payload.point_balance;
  },
};
// actions
 const actions = {
  load_point_list: ({commit}, options) => {
    pointService.getUserPointlist(options).then((response) => {
      commit('setPointList', response)
    })
  },
  load_pointhistory_summary: ({commit}) => {
    pointService.getPointHistorySummary().then((response) => {
      commit('setPointHistorySummary', response)
    })
  },
  retrieve_usable_point: ({commit}) => {
    return new Promise((resolve, reject) => {
      pointService.getUseablePoint().then((response) => {
        if (response.result) {
          resolve(response.point)
        } else {
          resolve(0)
        }
      }).catch((err) => {
        throw error(err)
        resolve(0)
      })
    })
  },

}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
