<template>
  <div>
    <Header/>
    <Breadcrumbs title="FAQ" breadcrumb_type="static"/>
    <section class="faq-section section-b-space my-3">
      <div class="container">
        <div class="row">
          <div class="col-sm-12">

            <b-tabs pills fill content-class="mt-3" active-nav-item-class="theme-bgcolor">
              <b-tab class="accordion theme-accordion" title-link-class="text-muted" :title="section.title"
                     v-for="section in sections" :key="section.id">
                <b-card no-body class="my-3" v-for="(faq, f_index) in section.faqs" :key="f_index"
                        v-if="section.is_valid">
                  <b-card-header header-tag="header" class="p-1" role="tab" v-if="faq.is_valid">
                    <b-button block href="#" v-b-toggle="`accordion-${section.id}-${f_index}`" variant="info">
                      {{ faq.question }}
                    </b-button>
                  </b-card-header>
                  <b-collapse :id="`accordion-${section.id}-${f_index}`" accordion="my-accordion" role="tabpanel"
                              v-if="faq.is_valid">
                    <b-card-body>
                      <b-card-text>
                        <p v-html="faq.answer"></p>
                      </b-card-text>
                    </b-card-body>
                  </b-collapse>
                </b-card>
              </b-tab>
            </b-tabs>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<script>
import {APIServices} from "~/helpers/APIs";

export default {
  name: "front_faq",
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('@/components/widgets/breadcrumbs'),
  },
  data() {
    return {
      show: false,
    }
  },
  async asyncData(){
    const sections_data = await APIServices.get("store/public/sections/?page_size=100&expand=faqs")
        .then(APIServices.handleResponse)
        .then((response) => {
          return response.results;
        })
    console.log("asyncData",sections_data)
    return {
      sections: sections_data
    }
  },
  mounted() {
    // this.$nextTick(() => {
    //   let vm = this;
    //   this.$nuxt.$loading.start();
    //   APIServices.get("store/public/sections/?page_size=100&expand=faqs")
    //     .then(APIServices.handleResponse)
    //     .then((response) => {
    //       vm.sections = response.results;
    //     })
    //   this.$nuxt.$loading.finish();
    // })
  },
  methods: {}
}
</script>
