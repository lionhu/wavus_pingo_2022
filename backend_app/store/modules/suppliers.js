import {supplierService} from '~/helpers/supplier.service';
import Swal from 'sweetalert2'

const state = () => ({
  supplier:{},
  list: [],
  list_meta: {}
})
const actions = {
  load_supplier_list({dispatch, commit}, options) {
    return supplierService.getAll(options).then(response => {
      return response
    })
  },
  load_supplier({dispatch, commit}, supplier_id) {
    commit("setSupplierList", [])
    supplierService.getOne(supplier_id).then(res => {
      if (res.total) {
        console.log(res)
        commit("setSupplierList", res)
      }
    })
  },
  update_supplier({commit}, {supplier_id, info}) {
    supplierService.updateInfo({supplier_id: supplier_id, info: info}).then(res => {
      if (res.id > 0) {
        commit("updatesupplier", res)
        Swal.fire("Success", "スプライヤー情報は更新されました", "success");
      }
    })
  },
  insert_supplier({commit}, supplier) {
    supplierService.insert(supplier).then(res => {
      console.log(res)
      commit("addsupplier", res)
      Swal.fire("Success", "スプライヤー情報は追加されました", "success");

    })
  },
  remove_supplier({commit}, supplier_id) {
    return supplierService.remove(supplier_id).then(res => {
      if (res.result) {
        commit("removesupplier", supplier_id)
        return true
      }
    })
  }

};

const mutations = {
  set_supplier_list(state, suppliers) {
    state.list = suppliers;
  },
  set_supplier(state, supplier) {
    state.supplier = supplier;
  },


  // before renewal
  setSupplierList(state, payload) {
    console.log("setSupplierList", payload)
    state.list = payload.results;
    state.list_meta = payload.meta;
  },
  addsupplier(state, supplier) {
    state.list.push(supplier);
  },
  updatesupplier(state, _supplier) {
    const index = state.list.findIndex(supplier => supplier.id === _supplier.id)

    if (index > -1) {
      state.list.splice(index, 1, _supplier);
    }
  },
  removesupplier(state, supplier_id) {
    console.log(supplier_id)
    const index = state.list.findIndex(supplier => supplier.id === supplier_id)
    console.log(index)
    if (index > -1) {
      state.list.splice(index, 1);
    }
  },
};

const getters = {
  getterSupplierList: (state) => {
    return state.list;
  },
  getterSupplierListMeta: (state) => {
    return state.list_meta;
  },
  getterSupplier: (state) => {
    return state.supplier;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
