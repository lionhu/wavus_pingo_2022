import {systemService} from '~/helpers/system.service';

const state = () => ({
  menuitems: [],
  sidebar_menuitems: [],
  back_server: process.env.DJANGO_SERVER,

  sections: [],
  sections_meta: {},
  faqs: [],
  faqs_meta: {}
})
const actions = {
  get_system_info({dispatch, commit}) {
    systemService.system_info()
      .then(response => {
        commit("suppliers/set_supplier_list", response.suppliers, {root: true})
        commit("logistics/set_logistic_list", response.logistics, {root: true})
        commit('init', response);
      });
  },
  load_sections({commit}, options) {
    systemService.section_list(options)
      .then(response => {
        commit('setSections', response);

      });
  },
  section_create({commit}, info) {
    return new Promise((resolve, reject) => {
      systemService.section_create(info)
        .then(response => {
            commit('insertSection', response);
            resolve(true)
        });
    })
  },
  section_update({commit}, {section_id, info}) {
    return new Promise((resolve, reject) => {
      systemService.section_update({section_id, info})
        .then(response => {
            commit('updateSection', response);
            resolve(true)
        });
    })
  },
  section_remove({commit}, section_id) {
    return new Promise((resolve, reject) => {
      systemService.section_remove(section_id)
        .then(response => {
            commit('removeSection', section_id);
            resolve(true)
        });
    })
  },




  load_faqs({commit}, options) {
    systemService.faq_list(options)
      .then(response => {
        if (response.result) {
          commit('setFaqs', response.faqs);
        }
      });
  },
  faq_create({commit}, info) {
    return new Promise((resolve, reject) => {
      systemService.faq_create(info)
        .then(response => {
          if (response.id) {
            commit('insertFaq', response);
            resolve(true)
          }
        });
    })
  },
  faq_update({commit}, {faq_id, info}) {
    return new Promise((resolve, reject) => {
      systemService.faq_update({faq_id, info})
        .then(response => {
          if (response.id>0) {
            commit('updateFaq', response);
            resolve(true)
          }
        });
    })
  },
  faq_remove({commit}, {section_id, faq_id}) {
    return new Promise((resolve, reject) => {
      systemService.faq_remove(faq_id)
        .then(response => {
          if (response.result) {
            commit('removeFaq', {_section_id: section_id, _faq_id: faq_id});
            resolve(true)
          }
        });
    })
  },
};

const mutations = {
  setSections(state, payload) {
    state.sections = payload.results;
    state.sections_meta = payload.meta;
  },


  insertSection(state, _section) {
    state.sections.push(_section)
  },
  updateSection(state, _section) {
    let index = state.sections.findIndex(section => section.id === _section.id)
    if (index > -1) {
      state.sections.splice(index, 1, _section)
    }
  },
  removeSection(state, _section_id) {
    let index = state.sections.findIndex(section => section.id === _section_id)
    if (index > -1) {
      state.sections.splice(index, 1)
    }
  },

  setFaqs(state, _faqs) {
    state.faqs = _faqs
  },
  insertFaq(state, _faq) {
    let sectionIndex = state.sections.findIndex(section => section.id === _faq.section)
    if (sectionIndex > -1) {
      state.sections[sectionIndex].faqs.push(_faq)

    }
  },
  updateFaq(state, _faq) {
    let sectionIndex = state.sections.findIndex(section => section.id === _faq.section)
    if (sectionIndex > -1) {
      let index = state.sections[sectionIndex].faqs.findIndex(faq => faq.id === _faq.id)
      if (index > -1) {
        state.sections[sectionIndex].faqs.splice(index, 1, _faq)
      }
    }

  },
  removeFaq(state, {_section_id, _faq_id}) {
    let sectionIndex = state.sections.findIndex(section => section.id === _section_id)
    if (sectionIndex > -1) {
      let index = state.sections[sectionIndex].faqs.findIndex(faq => faq.id === _faq_id)
      if (index > -1) {
        state.sections[sectionIndex].faqs.splice(index, 1)
      }
    }
  },
  init(state, response) {
    state.menuitems = response.menuitems.children;
  },
};

const getters = {
  getterSectionList: (state) => {
    return state.sections;
  },
  getterVendorList: (state) => {
    return state.vendorlist;
  },
  getterBackServer: (state) => {
    return state.back_server;
  },
  // getCategories: (state) => {
  //   let categories = state.menuitems.find(menuitem => menuitem.title === "categories").children
  //   return categories
  // },
  vendorSelectOptions: (state) => {
    return state.vendorlist.map((vendor) => {
      return {value: vendor.id, label: vendor.name}
    })
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
