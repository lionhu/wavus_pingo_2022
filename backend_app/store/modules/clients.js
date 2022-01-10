import {clientService} from '~/helpers/client.service';

const user = JSON.parse(localStorage.getItem('user'));

const state = () => ({
  list: [],
  list_meta: {}
})
const actions = {
  load_superadmin_clients({commit}, options) {
    clientService.load_superadmin_clients(options).then(res => {
      console.log("load_superadmin_clients", res)
      commit("setClientList", res)
    })
  },
  load_ONE_client({commit}, client_id) {
    return clientService.load_client(client_id).then(res => {
      return res
    })
  },
  register_client({commit}, client) {
    return clientService.register_clients(client)
      .then(response => {
        console.log(response)
        commit("addClient", response)
        return response
      });
  },
  remove_client({commit}, client_id) {
    return new Promise(resolve => {
      clientService.remove_client(client_id)
        .then(response => {
          if (response.result) {
            commit("removeClient", client_id)
            resolve(true)
          }
        });
    })
  },
  update_client({commit}, {client_id, info}) {
    return clientService.update_client({client_id: client_id, info: info})
      .then(response => {
        commit("updateClient", response)
        return true
      });
  },
};

const mutations = {
  setClientList(state, payload) {
    state.list = payload.results;
    state.list_meta = payload.meta;
  },
  addClient(state, client) {
    state.list.splice(0, 0, client)
  },
  removeClient(state, client_id) {
    var index = state.list.findIndex(client => client.id === client_id)
    console.log(client_id, index)
    if (index > -1) {
      state.list.splice(index, 1)
    }
  },
  updateClient(state, new_client) {
    var index = state.list.findIndex(client => client.id === new_client.id)
    if (index > -1) {
      state.list[index].name = new_client.name;
      state.list[index].description = new_client.description;
      state.list[index].margin_policy = new_client.margin_policy;
    }
  }
};

const getters = {
  getterClientList: (state) => {
    return state.list;
  },
  getterClientListMeta: (state) => {
    return state.list_meta;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
