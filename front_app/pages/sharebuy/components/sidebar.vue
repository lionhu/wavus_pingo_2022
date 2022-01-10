<template>
  <div>
    <div class="row">
      <div class="col-xl-12">
        <div class="filter-main-btn" @click="filter=!filter">
            <span class="filter-btn btn btn-theme">
              <i class="fa fa-filter" aria-hidden="true"></i> Filter
            </span>
        </div>
      </div>
    </div>
    <div class="collection-filter" style="width:100%!important" :class="{ 'openFilterbar' : filter }">
      <div class="collection-filter-block">
        <div class="collection-mobile-back">
        <span class="filter-back" @click="filter = !filter">
          <i class="fa fa-angle-left" aria-hidden="true"></i> back home
        </span>
        </div>
        <div class="collection-collapse-block open">
          <h3 class="collapse-block-title" v-b-toggle.category>{{ $t('menu.category') }}</h3>
          <b-collapse id="category" visible accordion="myaccordion" role="tabpanel">
            <div class="collection-collapse-block-content mt-3">
<!--              <h5><a href="javascript:void(0);"  class="text-muted" @click="selectCategory({},{})">{{$t("menu.all")}}</a></h5>-->
              <div v-for="category in categories">
                <ul v-if="category.regular_product_count">
                  <li v-for="subcategory in category.children"
                      class="d-block d-flex justify-content-between line-height-2">
                    <a href="javascript:void(0);" @click="selectCategory(category,subcategory)" class="text-muted"
                       v-if="subcategory.regular_product_count">
                      {{ subcategory.title }}
                      <span class="pingo_category_menusidebar-count"
                            v-if="subcategory.regular_product_count">{{ subcategory.regular_product_count }}</span>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </b-collapse>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>

.line-height-2 {
  line-height: 2rem !important;
}

.pingo_category_menusidebar-count {
  background: #ff4c3b;
  width: 20px;
  height: 20px;
  color: white;
  /*border-radius: 20px;*/
  text-align: center;
  font-size: 12px;
  line-height: 14px;
  font-weight: 600;
  margin-left: 1rem;
  padding: 3px;
}
</style>
<script>
import {mapState, mapGetters} from 'vuex'

export default {
  data() {
    return {
      bannerimagepath: '/images/side-banner.png',
      applyFilter: [],
      activeItem: 'category',
      filter: false,
    }
  },
  computed: {
    ...mapState({
      categories: state => state.system.categories,
    }),
  },
  mounted() {
    // this.$emit('priceVal', this.value)
  },
  methods: {
    isActive(filterItem) {
      return this.applyFilter.indexOf(filterItem) > -1
    },
    appliedFilter(val) {
      this.$emit('allFilters', this.applyFilter)
    },
    selectCategory(category, subcategory) {
      this.$store.commit('products/setCurrentCategory', {
        category: category,
        subcategory: subcategory
      })
      this.filter = false;
    },
    getCategoryFilter_all() {
      this.$emit('allFilters');
      this.filter = false;
    },
  }
}
</script>
