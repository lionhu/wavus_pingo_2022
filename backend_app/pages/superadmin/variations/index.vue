<script>
import {APIServices} from "@/helpers/APIs";
import {swalService} from "@/helpers/swal.service";

export default {
  name: "edit_product_variation_table",
  components: {
    VariationModal: () => import('./components/VariationModal'),
    VariationList: () => import('../components/VariationList'),
    CategoryTree: () => import('~/components/widgets/CategoryTree'),
    CategoryProducts: () => import('~/components/widgets/CategoryProducts'),
  },
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
  data() {
    return {
      title: "商品在庫",
      items: [
        {text: "PINGO",},
        {text: "eCommerce",},
        {text: "商品在庫", active: true,}
      ],
      modeAdd: false,
      variations: [],
      select_category:{},
      select_product_id:0
    };
  },
  mounted() {
  },
  methods: {
    CategorySelect({data,node}){
      this.select_category=data;
      console.log("Category Select",this.select_category)
    },
    SelectProduct(product_id){
      let self=this;
      if (product_id > 0) {
        let url = `store/public/filter_variations/${product_id}/ofProduct/`
        APIServices.get(url).then(APIServices.handleResponse)
          .then(response => {
            self.variations=response;
          })
      }
    },
    ReplaceVariation(_variation) {
      let self = this;
      self.showVariationModal = false;
      let index = self.variations.findIndex(variation => variation.id === _variation.id)
      if (index > -1) {
        self.variations.splice(index, 1, _variation);
        swalService.showModal("Success", "更新されました!", "success")
      }

    },

  }
};
</script>
<template>
  <div>

    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-6">
        <CategoryTree @clickNode="CategorySelect"/>
      </div>
      <div class="col-6">
        <CategoryProducts :category="select_category"
                          @SelectProduct="SelectProduct"
        />
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <div class="row">
          <VariationList :variations="variations" @ReplaceVariation="ReplaceVariation"/>
        </div>
      </div>
    </div>
  </div>

</template>
