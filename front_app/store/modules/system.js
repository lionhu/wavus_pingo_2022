import config from '~/data/config.json'
import {systemService} from "~/helpers/system.service"


 const state = () => ({
  services: {
    groupon_buy: true,
    intro_buy: true
  },

  productlist_regular: [],
  currentCategory: {},
  filteredRegularProducts: [],


  productlist_pingo: [],
  currentPingoCategory: null,
  currentPingoSubcategory: null,
  filteredPingoProducts: [],

  categories: [],
  config: config,
  newspopup: {},
  faqs: {},

  all_products: [],
  new_products: [],
  bestseller_products: []


});
// getters
 const getters = {
  gettersGrouponBuyServiceStatus: (state) => {
    return state.services.groupon_buy
  },
  gettersIntroBuyServiceStatus: (state) => {
    return state.services.intro_buy
  },
  getterCurrentRegularCategory: (state) => {
    return state.currentCategory
  },
  getterNewspopup: (state) => {
    return state.newspopup;
  },
  getterNewProducts: (state) => {
    return state.new_products;
  },
  getterAllProducts: (state) => {
    return state.all_products;
  },
  getterBestSellerProducts: (state) => {
    return state.bestseller_products;
  },
  getterCompanyInfo: (state) => {
    return state.config.company_info
  },
  getterBackServer: (state) => {
    return process.env.DJANGO_SERVER;
  },
  getterFrontServer: (state) => {
    return state.config.system.front_server;
  },
  // getterTopBanner: (state) => {
  //   return banner.top_banner.items
  // },
  // getterBankAccount: (state) => {
  //   return state.config.bank_account
  // },
  // PingoCategories: (state) => {
  //
  //     const category = [...new Set(state.productlist_pingo.map(product => product.category))];
  //
  //     return category
  // },
  filterCategoryProducts_Pingo: (state) => {
    if (state.currentPingoCategory === null) {
      return state.productlist_pingo;
    }
    return state.productlist_pingo.filter(product => product.category.id === state.currentPingoCategory.id);
  },
  filterCategoryProducts_Regular: (state) => {
    if (state.currentSubcategory === {}) {
      return state.productlist_regular;
    }
    return state.productlist_regular.filter(product => product.category.id === state.currentSubcategory.id);
  },
  getterFaqs: (state) => {
    return state.faqs;
  }
}
// mutations
 const mutations = {
  setGrouponBuyServiceStatus(state, payload) {
    state.services.groupon_buy = payload
  },
  setIntroBuyServiceStatus: (state, payload) => {
    state.services.intro_buy = payload
  },
  setNewProducts: (state, payload) => {
    state.new_products = payload;
  },
  setAllProducts: (state, payload) => {
    state.all_products = payload;
  },
  setBestSellerProducts: (state, payload) => {
    state.bestseller_products = payload;
  },
  setNewsPopup: (state, payload) => {
    state.newspopup = payload;
  },
  getCategoryFilter: (state, payload) => {
    state.filteredPingoProducts = []
    // state.tagItems = []
    state.pingoList.filter((product) => {
      if (payload === product.category) {
        state.filteredPingoProducts.push(product)
      }
      if (payload === 'all' || payload === undefined) {
        state.filteredPingoProducts.push(product)
      }
    })
  },
  setCategories(state, payload) {
    state.categories = payload.children
  },
  setPingoList(state, payload) {
    state.productlist_pingo = payload
  },
  setPingoCategory(state, payload) {
    state.currentPingoCategory = payload.category
    state.currentPingoSubcategory = payload.subcategory
  },
  setRegularCategory(state, payload) {
    state.currentCategory = payload
  },
  updatePingoProduct(state, payload) {
    var product = state.productlist_pingo.find(product => product.id === payload.product_id);

    if (product) {
      product.currentNum = payload.currentNum
    }
  },
  setFaqs(state, payload) {
    state.faqs = payload;
  }
}
// actions
const actions = {
  init_shop: ({commit,rootState}) => {
    return new Promise((resolve, reject) => {
      systemService.load_store_system_info().then((res) => {
        if (res.result) {
          commit('setCategories', res.data.categories);
          commit("setNewProducts", res.data.new_products);
          commit("setBestSellerProducts", res.data.bestseller_products);
        }
      })
    })
  },
  load_faqs: ({commit}, options) => {
    // return new Promise((resolve, reject) => {
    systemService.get_faqs(options).then((res) => {
      commit("setFaqs", res)
      // })
    })
  },
  // load_pingo_list: (context) => {
  //   productsAPI.load_pingo_list().then((res) => {
  //     if (res.result) {
  //       context.commit('setPingoList', res.data.pingoitems)
  //     }
  //   })
  // },
  setPingoCategory: (context, payload) => {
    context.commit('setPingoCategory', payload)
  },
  setRegularCategory: (context, payload) => {
    context.commit('setRegularCategory', payload)
  },
  updatePingoProduct: (context, payload) => {
    context.commit('updatePingoProduct', payload)
  }

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
