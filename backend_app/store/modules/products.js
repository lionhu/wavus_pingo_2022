import {productService} from '~/helpers/product.service';

const state = () => ({
  list: [],
  product: {},
  product_id: 0,

  copy_product: {}
})
const actions = {
  load_list({dispatch, commit}, options) {
    commit("setList", [])
    productService.getAll(options).then(response => {
      commit("setList", response)
    })
  },
  load_product({dispatch, commit}, product_id) {
    return productService.getProduct(product_id).then(response => {
      return response
    })
  },
  load_category_products({dispatch, commit}, filterOptions) {
    return productService.getCategoryProducts(filterOptions).then(response => {
      return response
    })
  },
  search_products({dispatch, commit}, filterOptions) {
    return new Promise((resolve, reject) => {
      productService.getSearchProducts(filterOptions).then(response => {
        resolve(response)
      })
    })
  },
  update_product({commit}, {info, product_id}) {
    return productService.updateInfo({
      info: info, product_id: product_id
    }).then(response => {
      console.log("action", response)
      commit("updateProduct", response)
      return response
    })
  },
  create_product({commit}, productInfo) {
    return  productService.admin_create(productInfo).then(response => {
        return response
      })
  },
  remove_product({commit}, product_id) {
    return new Promise((resolve, reject) => {
      productService.remove(product_id).then(response => {
        resolve(response)
      })
    })
  },
  remove_product_batch({commit}, ids) {
    return new Promise((resolve, reject) => {
      productService.remove_batch(product_id).then(response => {
        resolve(response)
      })
    })
  },
  remove_slider({commit}, sliderimage_id) {
    return new Promise((resolve, reject) => {
      productService.remove_sliderimage(sliderimage_id).then(response => {
        resolve(response)
      })
    })
  },
  create_variation({commit}, info) {
    return productService.create_variation(info)
      .then(response => {
        return response
      })
  },
  update_variation({commit}, {variation_id, info}) {
    return productService.update_variation({variation_id, info})
      .then(response => {
        console.log("update_variation", response)
        return response
      })
  },
  delete_variation({commit}, variation_id) {
    return new Promise((resolve, reject) => {
      productService.delete_variation(variation_id).then(response => {
        if (response.result) {
          resolve(response)
        }
      })
    })
  },


  create_pingoproduct({commit}, productInfo) {
    return new Promise((resolve, reject) => {
      productService.create_pingoproduct(productInfo).then(response => {
        if (response.item.id) {
          resolve(response)
        }
      })
    })
  },


};

const mutations = {
  setCopyProduct(state, payload) {
    state.copy_product = payload;
  },
  setList(state, list) {
    state.list = list;
  },
  setProduct(state, product) {
    state.product = product;
  },
  setProductID(state, product_id) {
    state.product_id = product_id;
  },
  updateProduct(state, _product) {
    if (state.list.length) {
      const index = state.list.results.findIndex(product => product.id === _product.id)
      if (index > -1) {
        state.list.results.splice(index, 1, _product);
      }
    }
  },
};

const getters = {
  getterProduct: (state) => {
    return state.product;
  },
  getterProductID: (state) => {
    return state.product_id;
  },
  getterCopyProduct(state) {
    return state.copy_product;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
