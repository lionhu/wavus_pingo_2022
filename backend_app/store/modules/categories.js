import {categoryService} from '~/helpers/category.service';
import {swalService} from "~/helpers/swal.service";

const state = () => ({
  list: [],
  list_meta:{}
})
const getters = {
  getProductCategories: (state) => {
    let shop_category_index = state.list.findIndex(category => category.title == "ROOT_SHOP_MENU")
    if(shop_category_index>-1){
      return state.list[shop_category_index].children;
    }
    return []
  },
  getterCategoryList: (state) => {
    return state.list;
  }
}
const actions = {
  load_superadmin_categorylist({dispatch, commit}) {
    categoryService.getAll().then(res => {
      commit("setList", res)
    })
  },







  AddCategory({commit}, category) {
    return new Promise((resolve, reject) => {
      categoryService.insert(category).then(res => {
        resolve(res)
      })
    })
  },
  updateCategory({commit}, category) {
    return new Promise((resolve, reject) => {
      categoryService.update(category).then(res => {
        console.log("after update category",res)
        resolve(res)
      })
    })
  },
  deleteCategory({commit}, category_id) {
    return new Promise((resolve, reject) => {
      categoryService.remove(category_id).then(res => {
        resolve(res)
      })
    })
  },
};

const mutations = {
  setList(state, payload) {
    console.log("categories setList",payload)
    state.list = payload.results;
    state.list_meta = payload.meta;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
