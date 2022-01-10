<script>
import {mapGetters, mapState} from "vuex"
import {swalService} from "~/helpers/swal.service"
import Swal from 'sweetalert2'
import {axios} from "@/plugins/axios";
import CKEditor from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

// const empty_product = {
//   id: 0,
//   item_name: "",
//   is_valid: false,
//   rate: 0,
//   vendor: {
//     id: 0,
//     name: ""
//   },
//   category: {
//     id: 0,
//     title: ""
//   },
//   type: "",
//   pingo_currentNum: 0,
//   pingo_targetNum: 10,
//   pingo_until_at: ""
// };
export default {
  name: "faqs_list",
  head() {
    return {
      title: `${this.title} | PINGO`,
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  components: {
    Switches: () => import('vue-switches'),
    "el-collapse-item": () => import('element-ui/lib/collapse-item'),
    "el-collapse": () => import('element-ui/lib/collapse'),
    ckeditor: CKEditor.component,
  },
  data() {
    return {
      title: "FAQs",
      items: [
        {text: "PinGo"},
        {text: "eCommerce"},
        {text: "FAQs", active: true}
      ],
      faqs: [],
      faq: {
        id: 0,
        question: "",
        answer: "",
        index: 0,
        is_valid: false,
        section: 0
      },
      faq_mode: "add",
      section: {
        id: 0,
        title: "",
        index: 0,
        is_valid: false
      },
      section_mode: "add",
      Faq_CRUD_URL: '/back/store/api/faqs/',
      Section_CRUD_URL: '/back/store/api/sections/',
      editor: ClassicEditor,
      editorData: "<p>Content of the editor.</p>",
    };
  },
  computed: {
    ...mapGetters({
      sections: "system/getterSectionList"
    }),
  },
  mounted() {
    let options = "?page_size=100&page=1"
    this.$store.dispatch("system/load_sections", options)
  },
  methods: {
    reset_faq() {
      this.faq = {
        id: 0,
        question: "",
        answer: "",
        index: 0,
        is_valid: false
      }
    },
    reset_section() {
      this.section = {
        id: 0,
        title: "",
        index: 0,
        is_valid: false
      }
    },
    load_sections() {
      let vm = this;
      axios.get(this.Section_CRUD_URL).then((response) => {
        if (response.data.result) {
          vm.sections = response.data.data.sections;
        }
      })
    },
    showModalSection(mode, section) {
      this.section_mode = mode;
      if (mode === 'edit') {
        this.section.id = section.id;
        this.section.title = section.title;
        this.section.index = section.index;
        this.section.is_valid = section.is_valid;
      } else {
        this.reset_section();
      }
      this.$bvModal.show("modelSection")
    },
    async RemoveSection(section_id) {
      let vm = this;

      Swal.fire({
        title: '再確認?',
        html: "本当に削除しますか？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、確定!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            return vm.$store.dispatch("system/section_remove", section_id)
              .then((response) => {
                return {result: true}
              })
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.result) {
          swalService.showToast("success", "削除しました!")
        }
      })

    },
    AddOrUpdateSection() {
      let vm = this;
      if (vm.section.title !== '') {
        if (vm.section_mode === "add") {
          delete vm.section.id;
          vm.$store.dispatch("system/section_create", vm.section).then(response => {
            if (response) {
              swalService.showToast("success", "News section was added")
              vm.$bvModal.hide("modelSection")
            }
          })
        } else {
          console.log(vm.section.id)
          vm.section.index = parseInt(vm.section.index)
          vm.$store.dispatch("system/section_update", {section_id: vm.section.id, info: vm.section})
            .then(response => {
              if (response) {
                swalService.showToast("success", "News section was updated")
                vm.$bvModal.hide("modelSection")
              }
            })
        }
      }
    },


    showModalFaq(mode, section, faq) {

      this.faq_mode = mode;
      if (mode === 'edit') {
        this.faq.id = faq.id;
        this.faq.question = faq.question;
        this.faq.section = section.id;
        this.faq.answer = faq.answer;
        this.faq.index = faq.index;
        this.faq.is_valid = faq.is_valid;
      } else {
        this.reset_faq();
        this.faq.section = section.id;
      }
      // this.faq.section = section.id;
      this.$bvModal.show("modelFaq");
      console.log("show faq edit", this.faq)
    },
    AddOrUpdateFaq() {
      let vm = this;
      vm.faq.index = parseInt(vm.faq.index)
      if (vm.faq.question !== '' && vm.faq.answer !== '') {
        if (vm.faq_mode === "add") {
          delete vm.faq.id;
          vm.$store.dispatch("system/faq_create", vm.faq).then((response) => {
            swalService.showToast("success", "New faq was added")
            vm.$bvModal.hide("modelFaq")
          })
        } else {
          vm.$store.dispatch("system/faq_update", {faq_id: vm.faq.id, info: vm.faq})
            .then((response) => {
              swalService.showToast("success", "Faq was updated!")
              vm.$bvModal.hide("modelFaq")
            })
        }
      }
    },
    removeFAQ(section_id, faq_id) {
      let vm = this;
      Swal.fire({
        title: '再確認?',
        html: "本当に削除しますか？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、確定!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            return vm.$store.dispatch("system/faq_remove", {section_id: section_id, faq_id: faq_id})
              .then((response) => {
                vm.$bvModal.hide("modelFaq")
                return {result: true}
              })
          }
        },
        allowOutsideClick: () => false
      }).then((result) => {
        if (result.isConfirmed && result.value.result) {
          swalService.showToast("success", "Faq was updated!")
        }
      })
    }
  },
  middleware: ['router-auth', 'router-superadmin'],
};
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items"/>

    <div class="row mb-3">
      <div class="col-12 text-right">
        <b-button variant="warning" @click="showModalSection('add',null)">Section追加</b-button>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card" v-for="section in sections" :key="section.id">
          <div class="card-header  ribbon-box d-flex justify-content-between">

            <div class="ribbon ribbon-purple float-left">
              {{ section.index }} <i :class="{'fe-eye':section.is_valid,'fe-eye-off':!section.is_valid}"></i>
            </div>
            <div class="inline-block">
              {{ section.title }}
              <a href="javascript:void(0);" class="inline-block" @click="showModalSection('edit',section)">
                <i class="fe-edit"></i>
              </a>
            </div>

            <b-button variant="danger"><i class="fe-trash" @click="RemoveSection(section.id)"></i>
            </b-button>
          </div>
          <div class="card-body">
            <h4 class="text-right">
              <b-button variant="success">
                <i class="fe-plus-circle" @click="showModalFaq('add',section,null)"></i>
              </b-button>
            </h4>
            <el-collapse accordion>
              <el-collapse-item v-for="faq in section.faqs" :key="faq.id">
                <template slot="title">
                  <b-badge variant="primary" pill class="mr-3">{{ faq.index }}<i
                    :class="{'fe-eye':faq.is_valid,'fe-eye-off':!faq.is_valid}"></i></b-badge>
                  <div v-html="faq.question"></div>
                </template>
                <div v-html="faq.answer"></div>
                <div class="d-flex justify-content-between mt-5">
                  <b-button variant="success"><i class="fe-trash" @click="removeFAQ(section.id,faq.id)"></i></b-button>
                  <b-button variant="primary"><i class="fe-edit" @click="showModalFaq('edit',section,faq)"></i>
                  </b-button>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </div>
    </div>


    <b-modal id="modelSection" scrollable :title="this.section_mode==='edit'?'編集':'新規'" title-class="font-18"
             body-class="p-4" hide-footer>
      <div class="card">
        <div class="card-body">
          <form>
            <div class="form-row">
              <b-form-group class="col-md-6" label="有効化" label-for="section_is_valid">
                <input id="section_is_valid" v-model="section.is_valid" type="checkbox"/>
              </b-form-group>
              <b-form-group class="col-md-6" label="並び順番" label-for="section_index">
                <b-form-input type="text" id="section_index" v-model="section.index"></b-form-input>
              </b-form-group>
            </div>

            <b-form-group label="タイトル" label-for="section_title">
              <b-form-input type="text" id="section_title" v-model="section.title"></b-form-input>
            </b-form-group>
          </form>
        </div>
        <div class="card-footer">
          <b-button variant="primary" @click="AddOrUpdateSection">Submit</b-button>
        </div>
      </div>

    </b-modal>
    <b-modal id="modelFaq" size="lg" scrollable title="FAQ情報" title-class="font-18"
             body-class="p-4" hide-footer>

      <div class="card">
        <div class="card-body">
          <form>
            <div class="form-row">
              <b-form-group class="col-md-6" label="有効化" label-for="faq_is_valid">
                <input id="faq_is_valid" v-model="faq.is_valid" type="checkbox"/>
              </b-form-group>
              <b-form-group class="col-md-6" label="並び順番" label-for="faq_index">
                <b-form-input type="text" id="faq_index" v-model="faq.index"></b-form-input>
              </b-form-group>
            </div>

            <b-form-group label="ご質問" label-for="faq_question">
              <b-form-input type="text" id="faq_question" v-model="faq.question"></b-form-input>
            </b-form-group>
            <b-form-group label="回答内容" label-for="faq_answer">
              <ckeditor id="faq_answer" v-model="faq.answer" :editor="editor"></ckeditor>
            </b-form-group>
          </form>
        </div>
        <div class="card-footer">
          <b-button variant="primary" @click="AddOrUpdateFaq" class="float-right">確定</b-button>
        </div>
      </div>

    </b-modal>

  </div>
</template>
