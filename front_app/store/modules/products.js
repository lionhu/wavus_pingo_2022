import {productService} from "~/helpers/product.service"

const state = {
  currentCategory: {id:0},
  currentSubcategory: {id:0},
  currentCategoryProducts: [],
  currentCategoryProductsMeta: {},
  detailed_product: {},
  detailed_product_id: 0,


};

// getters
const getters = {
  getterCurrentCategory: (state) => {
    return state.currentCategory
  },
  getterCurrentSubcategory: (state) => {
    return state.currentSubcategory;
  },
  getterCategoryProducts: (state) => {
    return state.currentCategoryProducts;
  },
  getterCurrentCategoryProductsMeta: (state) => {
    return state.currentCategoryProductsMeta;
  },

  getCurrentDetailedProduct: (state) => {
    return state.detailed_product
  },
  getCurrentDetailedProductID: (state) => {
    return state.detailed_product_id
  },
  getCurrentDetailedProductCategory(state, getters, rootState, rootGetters) {
    return rootState.auth.user
  },
  getterCategoryProductIds(state) {
    if (state.currentCategoryProducts !== undefined && state.currentCategoryProducts.length > 0) {
      let ids = state.currentCategoryProducts.map(product => product.id)
      return [...new Set(ids)]
    } else {
      return []
    }

  }
};

// mutations
const mutations = {
  setCategoryProducts: (state, payload) => {
    state.currentCategoryProducts = payload
    state.currentCategoryProductsMeta.total = payload.length
  },
  setCurrentCategory: (state, {category, subcategory}) => {
    state.currentCategory = category;
    state.currentSubcategory = subcategory;
  },
  setCurrentDetailProduct: (state, payload) => {
    state.detailed_product = payload;
    state.detailed_product_id = payload.id;
  },
  setCurrentDetailProductID: (state, payload) => {
    state.detailed_product_id = payload;
  },
  setResetCurrentDetailProductinfo() {
    state.detailed_product = {}
    state.detailed_product_id = 0;
  },
  setCurrentDetailProductByID: (state, payload) => {
    let product = state.currentCategoryProducts.find(product => product.id === payload)
    state.detailed_product = product;
  },
};

// actions
const actions = {
  load_category_products: ({commit}, filter_options) => {
    productService.getCategoryProducts(filter_options).then(response => {
      commit('setCategoryProducts', response);
    })
  },

  get_my_favorites({commit}, options) {
    // return new Promise((resolve, reject) => {
    return productService.getMyFavorites(options).then(response => {
      return response
    })
    // })
  },

  delete_my_favorites({commit}, favorite_id) {
    return productService.removeMyFavorites(favorite_id)
      .then(response => {
        return response
      })
  },

  add_my_favorites({commit}, info) {
    return productService.addToMyFavorites(info).then(response => {
      return response
    })
  },


  get_product_comments(context, item_id) {
    return new Promise((resolve, reject) => {
      productService.getProductComments(item_id).then(response => {
        if (response.result) {
          resolve(response.data)
        } else {
          resolve([])
        }
      })
    })
  },

  update_product_comments(context, {comment_id, info}) {
    return new Promise((resolve, reject) => {
      productService.updateProductComment({comment_id, info}).then(response => {
        if (response.result) {
          resolve(response.data)
        } else {
          resolve([])
        }
      })
    })
  },

  delete_product_comment(context, comment_id) {
    return new Promise((resolve, reject) => {
      productService.deleteProductComment(comment_id).then(response => {
        if (response.result) {
          resolve(true)
        } else {
          resolve(false)
        }
      })
    })
  },

  create_product_comment(context, info) {
    return new Promise((resolve, reject) => {
      productService.createProductComment(info).then(response => {
        if (response.comment !== undefined && response.comment.id) {
          resolve(response)
        }
      })
    })
  },

  update_product_comment_thumbs(context, {comment_id, info}) {
    return new Promise((resolve, reject) => {
      productService.updateProductCommentThumbs({comment_id, info}).then(response => {
        resolve(response)
      })
    })
  },

  get_product_byID({commit}, product_id) {
    return productService.getProductByID(product_id).then(response => {
      commit("setCurrentDetailProduct", response.item)
      return response.item
    })
  },

  get_product_IntroQR({commit}, product_id) {
    return productService.getProductIntroQR(product_id).then(response => {
      return response
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
