<script>
import {mapGetters} from "vuex"
import {APIServices} from "@/helpers/APIs";

export default {
  name: "category_products",
  props: ["category"],
  components: {},
  data() {
    return {
      products: []
    };
  },
  computed: {
    ...mapGetters({}),
  },
  watch: {
    category(newVal, oldVal) {
      if (newVal.id > 0) {
        this.load_category_products()
      }
    }
  },
  methods: {
    load_category_products() {
      let self = this;
      if (this.category.id > 0) {
        let url = `store/public/filter_products/${this.category.id}/ofCategory/`
        APIServices.get(url).then(APIServices.handleResponse)
          .then(response => {
            self.products = response;
          })
      }
    },
    SelectProduct(product_id) {
      this.$emit("SelectProduct", product_id)
    }
  }
};
</script>
<style>
</style>
<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="mr-3">
          <a href="javascript:void(0);" @click="SelectProduct(product.id)"
             v-for="product in products" :key="product.id">
            <img :src="product.thumbimage_url" class="rounded avatar-lg" >
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
