// import config from '../data/config'
import {swalService} from "~/helpers/swal.service";

 const state ={
  cart: [],
  // config: config
};

// getters
 const getters = {
  cartItems: (state) => {
    return state.cart
  },
  cartTotalAmount: (state) => {
    if (state.cart === undefined || state.cart.length === 0) {
      return 0;
    }
    return state.cart.reduce((total, item) => {
      return total + (item.variant.price * item.quantity)
    }, 0)
  },
  cartQty: (state) => {
    if (state.cart === undefined || state.cart.length === 0) {
      return 0;
    }
    return state.cart.reduce((total, product) => {
      return total + product.quantity
    }, 0)
  }
};
// mutations
 const mutations = {
  // addToProduct:(state,product) =>{
  //     state.products = product
  // },
  addToCart: (state, payload) => {
    console.log("addToCart",payload)
    const cartItems = state.cart.find(item => item.product.id === payload.product.id && item.variant.id === payload.variant.id);

    delete payload.product.description;
    delete payload.product.package;
    delete payload.product.item_sliderimages;
    delete payload.product.item_variations;

    delete payload.product.targetNum;
    delete payload.product.currentNum;
    delete payload.product.until_at;
    // delete payload.variant.variations;

    console.log("after deleted",payload)
    if (cartItems) {
      cartItems.quantity += 1
    } else {
      state.cart.push({
        product: payload.product,
        variant: payload.variant,
        quantity: 1
      })
    }
    swalService.showToast("success", "カートに追加しました！");

  },
  updateCartQuantity: (state, payload) => {
    let cartIndex = state.cart.findIndex((items, index) => {
      if (items.product.id === payload.item.product.id && items.variant.id === payload.item.variant.id) {
        return true
      }
    })
    if (cartIndex > -1 && payload.qty < 0 && state.cart[cartIndex].quantity === 1) {
      state.cart.splice(cartIndex, 1);
    } else {
      const qty = state.cart[cartIndex].quantity + payload.qty
      state.cart[cartIndex].quantity = qty;
    }
  },
  removeCartItem: (state, payload) => {
    const index = state.cart.indexOf(payload)
    state.cart.splice(index, 1)
  },
  // setProducts:(state,payload)=>{
  //     state.products=payload
  //   },
  emptyCart: (state) => {
    state.cart = []
  }

};
// actions
 const actions = {
  // addToProduct:(context,payload) =>{
  //   context.commit('addToProduct', payload)
  // },
  addToCart: (context, payload) => {
    context.commit('addToCart', payload)
  },
  updateCartQuantity: (context, payload) => {
    context.commit('updateCartQuantity', payload)
  },
  removeCartItem: (context, payload) => {
    context.commit('removeCartItem', payload)
  },
  empty_cart: (context) => {
    context.commit('emptyCart')
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
