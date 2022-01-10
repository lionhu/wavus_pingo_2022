import {marginService} from '~/helpers/margin.service';
import Swal from 'sweetalert2'

const state = () => ({
  list: [],
  list_meta: {},
  margin: {}
})
const actions = {

  load_marginlist({commit}, options) {
    return new Promise((resolve, reject) => {
      marginService.load_list(options).then(res => {
        if (res.result) {
          commit("setList", res)
        }
      })
    })
  },
}

const mutations = {
  setList(state, response) {
    state.list = response.margins;
    state.list_meta = response.meta;
  },
  // setOrder(state, order_id) {
  //   console.log(order_id)
  //   if (state.list.results) {
  //     console.log(state.list.results)
  //     var order = state.list.results.find(order => order.id == order_id);
  //     console.log(order)
  //     console.log(order.payment_info)
  //     // order.payment_info = JSON.parse(order.payment_info);
  //     state.order = order
  //     console.log(state.order)
  //   } else {
  //     state.order = {}
  //   }
  // },
  // updateOrderItem(state, order) {
  //   order.point_usage = JSON.parse(order.point_usage);
  //   // order.payment_info = JSON.parse(order.payment_info);
  //   state.order = order
  // },
  // updateOrder(state, neworder) {
  //   var orderindex = state.list.results.findIndex(order => order.id == neworder.id);
  //   if (orderindex > -1) {
  //     neworder.point_usage = JSON.parse(neworder.point_usage);
  //     // neworder.payment_info = JSON.parse(neworder.payment_info);
  //     state.list.results.splice(orderindex, 1, neworder);
  //   }
  // },
  // removeOrder(state, order_id) {
  //   var orderindex = state.list.results.findIndex(order => order.id == order_id);
  //   if (orderindex > -1) {
  //     state.list.results.splice(orderindex, 1);
  //   }
  // }
};

const getters = {
  // getCategory: (state) => (id) => {
  //   return state.todos.find(todo => todo.id === id)
  // }
  gettersMarginList: (state) => {
    return state.list;
  },
  gettersMarginListMeta: (state) => {
    return state.list_meta;
  }
};
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
