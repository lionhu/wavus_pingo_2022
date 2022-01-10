import {orderService} from "~/helpers/order.service"


export const state = () => ({
  orderlist: [],
  orderlist_meta: {},

  pingo_orderlist: [],
  pingo_orderlist_meta: {},
  pingo_order_detail: {},
  order: {}, //new order information
});
// getters
export const getters = {
  new_orderID: (state) => {
    if (state.order) {
      return state.order.id;
    }
    return 0
  },
  getterPingoOrderDetail(state) {
    return state.pingo_order_detail;
  },
  getterPingoOrderList(state) {
    return state.pingo_orderlist;
  },
  getterPingoOrderListMeta(state) {
    return state.pingo_orderlist_meta;
  },

};
// mutations
export const mutations = {
  setOrderList: (state, payload) => {
    state.orderlist = payload.results;
    state.orderlist_meta = {
      "page": payload.page,
      "page_size": payload.page_size,
      "total": payload.total,
      "links": payload.links,
    }
  },
  setPingoOrderList: (state, payload) => {
    state.pingo_orderlist = payload.results;
    state.pingo_orderlist_meta = payload.meta;
  },
  setPingoOrderDetail: (state, payload) => {
    state.pingo_order_detail = payload;
  },
  setOrder: (state, payload) => {
    state.order = payload
  },
  removeOrder: (state, payload) => {
    var order_id = parseInt(payload)
    var orderIndex = state.orderlist.findIndex(order => order.id === order_id);
    if (orderIndex > -1) {
      state.orderlist.splice(orderIndex, 1);
    }
  },
  removePingoOrder: (state, order_id) => {
    var orderIndex = state.pingo_orderlist.findIndex(order => order.id === order_id);
    if (orderIndex > -1) {
      state.pingo_orderlist.splice(orderIndex, 1);
    }
  },
  updateOrderStatus(state, {order_id, _status}) {
    let orderIndex = state.orderlist.findIndex(order => order.id === order_id)

    if (orderIndex > -1) {
      state.orderlist[orderIndex].status = _status
    }
  }
}
// actions
export const actions = {
  getOrderList: ({commit}, options) => {
    orderService.loadOrders(options).then((response) => {
      commit('setOrderList', response.data)
    })
  },
  getPingoOrderDetail: ({commit}, order_id) => {
    return new Promise((resolve, reject) => {
      orderService.loadPingoOrderDetail(order_id).then((response) => {
          commit('setPingoOrderDetail', response)
          resolve(true)
      })
    })

  },
  getPingoOrderList: ({commit}, options) => {
    return orderService.loadPingoOrders_ME(options).then((response) => {
      commit('setPingoOrderList', response)
      return response;
    })
  },
  getOrder: (context, payload) => {
    orderService.loadOrders(payload, "REGULAR").then((response) => {
      if (response.result) {
        context.commit('setOrder', response.order)
      } else {
        context.commit('setOrder', [])
      }
    })
  },
  placeOrder: ({commit}, order_detail) => {
    return new Promise((resolve, reject) => {
      orderService.PlaceOrder(order_detail).then((response) => {
        resolve(response);
      }).catch(err => {
        reject(err)
      });
    })
  },
  placePingoOrder: ({commit}, order_detail) => {
    return orderService.PlacePingoOrder(order_detail).then((response) => {
      return response;
    })
  },
  completeOrder: (context, order_id) => {
    return new Promise((resolve, reject) => {
      orderService.complete_order_user(order_id).then((response) => {
        context.commit("updateOrderStatus", {
          order_id: parseInt(response.order_id),
          _status: "COMPLETED"
        })

        resolve(response);
      }).catch(error => {
        reject(error)
      });
    })
  },
  deleteOrder: (context, order_id) => {
    // return new Promise((resolve, reject) => {
    return orderService.delete_order_user(order_id, "REGULAR").then((response) => {
      if (response.result) {
        context.commit("removeOrder", parseInt(response.data.id));
        return response.data;
      }
    });
    // })
  },
  deletePingoOrder: (context, order_id) => {
    return orderService.delete_pingoorder_user(order_id).then((response) => {
      context.commit("removePingoOrder", parseInt(response.id));
      return response
    });
  }

}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
