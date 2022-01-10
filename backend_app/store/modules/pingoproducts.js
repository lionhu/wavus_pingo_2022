import {pingoproductService} from '~/helpers/pingoproduct.service';

const state = () => ({
  list: [],
  meta: {},

  product: {},
  product_orders: [],
  product_orders_meta: {},

  copy_product: {},
  basicInfoMode: "create",
})
const actions = {
  superadmin_pingoproduct_list({commit}, options) {
    pingoproductService.superadmin_getPingoProductList(options).then(response => {
      commit("superadmin_setList", response)
    })
  },
  superadmin_filter_category({commit}, options) {
    return pingoproductService.superadmin_getFilterCategory(options).then(response => {
      commit("superadmin_setList", response)
      return response
    })
  },
  superadmin_remove_product({commit}, product_id) {
    pingoproductService.superadmin_remove(product_id).then(response => {
      if (response.result) {
        commit("superadmin_remove_product_from_list", product_id)
      }
    })
  },
  superadmin_retrieve_product({commit}, product_id) {
      return pingoproductService.superadmin_retrieve(product_id)
        .then(response => {
           return response
        })
  },
  superadmin_update_product({commit}, info) {
      return pingoproductService.superadmin_update(info)
        .then(response => {
          return response
        })
  },
  superadmin_create_product({commit}, info) {
    return new Promise((resolve, reject) => {
      pingoproductService.superadmin_create(info)
        .then(response => {
          resolve(response)
        })
    })
  },

  superadmin_retrieve_product_orders({commit}, {product_id, options}) {
    return pingoproductService.superadmin_related_orderlist({product_id, options})
      .then(response => {
        return response
      })
  },
  superadmin_remove_product_orders({commit}, order_ids) {
      return pingoproductService.superadmin_delete_orders(order_ids)
        .then(response => {
          return response
        })
  },
  superadmin_establish_orders({commit}, product_id) {
     return pingoproductService.superadmin_establish(product_id)
        .then(response => {
          return response
        })
  },
  superadmin_release_orders({commit}, product_id) {
      return pingoproductService.superadmin_release(product_id)
        .then(response => {
          return response
        })

  },
  superadmin_batch_update_orders({commit}, updateinfo) {
      return pingoproductService.superadmin_batch_update_orders(updateinfo)
        .then(response => {
          return response
        })
  },


  create_variation({commit}, info) {
    return new Promise((resolve, reject) => {
      pingoproductService.create_variation(info).then(res => {
        if (res.result) {
          resolve(res)
        }
      })
    })
  },
  update_variation({commit}, {variation_id, info}) {
    return new Promise((resolve, reject) => {
      pingoproductService.update_variation({variation_id, info}).then(res => {
        if (res.result) {
          resolve(res)
        }
      })
    })
  },
  delete_variation({commit}, variation_id) {
    return new Promise((resolve, reject) => {
      pingoproductService.delete_variation(variation_id).then(res => {
        if (res.result) {
          resolve(res)
        }
      })
    })
  },


}

const mutations = {
  superadmin_setCopyProduct(state, payload) {
    console.log("superadmin_setCopyProduct", payload)
    state.copy_product = payload.product;
    state.basicInfoMode = payload.mode;
  },
  superadmin_setProductStatus(state, _status) {
    state.product.status = _status;
  },
  superadmin_setProductOrdersStatus(state, {ids, _status}) {
    ids.forEach(id => {
      let index = state.product_orders.findIndex(order => order.id === id);
      if (index > -1) {
        state.product_orders[index].status = _status;
      }
    })
  },
  superadmin_remove_product_orderlist(state, ids) {
    ids.forEach(order_id => {
      let index = state.product_orders.findIndex(order => order.id === order_id)
      if (index > -1) {
        state.product_orders.splice(index, 1)
      }
    })
  },
  superadmin_update_orderlist(state, {updateinfo, data}) {
    updateinfo.orderitem_ids.forEach(_id => {
      let itemIndex = state.product_orders.findIndex(order => order.id === _id);
      if (itemIndex > -1) {
        if (updateinfo.update_fields.includes("delivery")) {
          state.product_orders[itemIndex].delivered = updateinfo.delivered;
          state.product_orders[itemIndex].logistic = data.logistic;
          state.product_orders[itemIndex].delivered_at = updateinfo.delivered_at;
          state.product_orders[itemIndex].delivery_info = updateinfo.delivery_info;
        }
      }
    })
  },
  superadmin_append_product_orders(state, {orders, meta}) {
    state.product_orders = orders
    state.product_orders_meta = meta
  },
  superadmin_setProduct(state, payload) {
    state.product = payload;
  },
  superadmin_setList(state, payload) {
    state.list = payload.results;
    state.meta = payload.meta;
  },
  superadmin_remove_product_from_list(state, payload) {
    let itemIndex = state.list.findIndex(item => item.id === payload)
    if (itemIndex > -1) {
      state.list.splice(itemIndex, 1)
    }
  },
};
const getters = {
  getterSuperadminList(state) {
    return state.list;
  },
  getterCopyProduct(state) {
    return state.copy_product;
  },
  getterBasicInfoMode(state) {
    return state.basicInfoMode;
  },
  getterEditProduct(state) {
    return state.product;
  },
  getterCurrentProduct(state) {
    return state.product;
  },
  getterCurrentProductOrders(state) {
    return state.product_orders;
  },
  getterCurrentProductOrdersMeta(state) {
    return state.product_orders_meta;
  },
  getterProductListMeta(state) {
    return state.meta;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
