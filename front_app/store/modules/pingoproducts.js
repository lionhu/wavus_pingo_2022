import {pingoproductService} from '~/helpers/pingoproduct.service';

const state = () => ({
  list: [],
  meta: {},
  detailed_product: {},
  cart: null,
  current_category_id:0
})
const actions = {
  get_product_IntroQR({commit}, product_id) {
      return pingoproductService.getProductIntroQR(product_id).then(response => {
        return response
      })
  },
  filter_category({commit}, options) {
    pingoproductService.getFilterCategory(options).then(response => {
      commit("setList", response)
    })
  },
  load_product({commit}, options) {
    return new Promise(resolve => {
      pingoproductService.getFilterCategory(options).then(response => {
        resolve(response)
      })
    })
  },
  empty_cart({commit}) {
    commit("clearCart")
  },
  retrieveProductDetail({commit}, product_id) {
      return pingoproductService.getProductDetailByID(product_id).then(response => {
        if (response.id>0) {
          commit("setDetailProduct", response)
          return response
        }
      })
  },
}

const mutations = {
  setCurrentCategoryID(state, payload){
    state.current_category_id=payload
  },
  setList(state, payload) {
    state.list = payload.results;
    state.meta = {
      page:payload.page,
      total:payload.total,
      page_size:payload.page_size,
      links:payload.links
    };
  },
  setCart(state, payload) {
    delete payload.product.item_pingo_sliderimages;
    state.cart = payload;
  },
  setCartQuantity(state, payload) {
    if (state.cart !== null) {
      state.cart.quantity = payload;
    }
  },
  clearCart(state) {
    state.cart = null;
  },
  setDetailProduct(state, payload) {
    state.detailed_product = payload;
  }
};
const getters = {
  getterCurrentCategoryID(state){
    return state.current_category_id
  },
  getterPingoProductList(state) {
    return state.list;
  },
  getterEditProduct(state) {
    return state.product;
  },
  getterProductListMeta(state) {
    return state.meta;
  },
  getterCart(state) {
    return state.cart;
  },
  getterCurrentDetailedProduct: (state) => {
    return state.detailed_product
  },
  // updateProduct(state, _product) {
  //   const index = state.list.results.findIndex(product => product.id === _product.id)
  //   if (index > -1) {
  //     state.list.results.splice(index, 1, _product);
  //   }
  // },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}

