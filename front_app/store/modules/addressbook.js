import {addressbookService} from '~/helpers/addressbook.service'
import logger from "@fortawesome/vue-fontawesome/src/logger";


export const state = () => ({
  shipping_addresses: [],
  shipping_addresses_meta: {},
  order_address:{}

});
// getters
export const getters = {
  getterOrderAddress: (state) => {
    return state.order_address
  },
  getterAddressList: (state) => {
    return state.shipping_addresses
  },
  getterAddressListMeta: (state) => {
    return state.shipping_addresses_meta
  },
};
// mutations
export const mutations = {
  setAddressList: (state, payload) => {
    console.log(payload)
    state.shipping_addresses = payload.data.results;
    state.shipping_addresses_meta = {
      page: payload.data.page,
      page_size: payload.data.page_size,
      total: payload.data.total,
    };
  },
  setOrderAddress: (state, address) => {
    state.order_address = address
  },
  removeAddress(state, address_id) {
    let addressIndex = state.shipping_addresses.findIndex(address => address.id === address_id)
    if (addressIndex > -1) {
      state.shipping_addresses.splice(addressIndex, 1)
    }
  },
  addAddress(state, address) {
    state.shipping_addresses.push(address)
  }
};
// actions
export const actions = {
  load_address_list: ({commit}) => {
    addressbookService.getUserAddressList().then((response) => {
        commit('setAddressList', response)
    })
  },
  delete_address({commit}, address_id) {
    addressbookService.deleteAddress(address_id).then((response) => {
      console.log("delete_address", response)
      if (response.result) {
        commit('removeAddress', address_id)
      }
    })
  },

  add_address({commit}, shipping_address) {
    return new Promise((resolve, reject) => {
      addressbookService.addAddress(shipping_address).then((response) => {
        console.log("addAddress", response)
        if (response !== undefined && response.id > 0) {
          commit('addAddress', response)
          resolve(response)
        }
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
