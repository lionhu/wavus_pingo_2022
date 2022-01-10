<template>
  <div id="mySidenav" class="sidenav" :class="{ openSide:leftSidebarVal }">
    <a class="sidebar-overlay" @click="closeLeftBar(leftSidebarVal)"></a>
    <nav>
      <a @click="closeLeftBar(leftSidebarVal)">
        <div class="sidebar-back text-left">
          <i class="fa fa-angle-left pr-2" aria-hidden="true"></i> Back
        </div>
      </a>

      <a href="javascript:void(0);" @click="set_category({id:0},{id:0})" class="d-block btn btn-solid text-center mt-3">
        {{ $t("services.share_sales.title") }}
      </a>
      <ul id="share_sub-menu" class="sidebar-menu">
        <li v-for="category in categories" :key="category.id">
          <a href="javascript:void(0)" @click="setActive(category.title)" v-if="category.regular_product_count">
            {{ category.title }}
            <span class="sub-arrow"></span>
          </a>
          <ul :class="{ opensub1: isActive(category.title) }" v-if="category.regular_product_count">
            <li v-for="subcategory in category.children" v-if="subcategory.regular_product_count">
              <a href="javascript:void(0);" @click="set_category(category,subcategory)">
                <i :class="`${subcategory.icon}`" v-if="subcategory.icon"></i>{{ subcategory.title }}
              </a>
            </li>
          </ul>
        </li>
      </ul>
      <a href="javascript:void(0);" @click="selectPingoCategory(0)" class="d-block btn btn-solid text-center mt-3">
        {{ $t("services.tomo_sales.title") }}
      </a>
      <div v-for="category in categories">
        <ul v-if="category.pingo_product_count" class="sidebar-menu">
          <li v-for="subcategory in category.children" class="d-block d-flex justify-content-between line-height-4">
            <a href="javascript:void(0);" @click="selectPingoCategory(subcategory.id)"
               v-if="subcategory.pingo_product_count">
              {{ subcategory.title }}
              <span class="pingo_category_menusidebar-count"
                    v-if="subcategory.pingo_product_count">{{ subcategory.pingo_product_count }}</span>
            </a>

          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<style scoped>

.line-height-4 {
  line-height: 4rem !important;
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
  name:"left-sidebar",
  props: ['leftSidebarVal'],
  data() {
    return {
      activeItem: 'clothing'
    }
  },
  computed: {
    ...mapState({
      categories: state => state.system.categories,
      active_category: state => state.products.current_category_id
    }),
    ...mapGetters({
      GrouponServiceStatus: "system/gettersGrouponBuyServiceStatus"
    })
  },
  mounted() {

    // this.$store.dispatch("cart/copyProducts",this.$store.state.products.productlist);
    // this.load_category_products(3)
  },
  methods: {
    closeLeftBar(val) {
      val = false
      this.$emit('closeVal', val)
    },
    isActive: function (menuItem) {
      return this.activeItem === menuItem
    },
    setActive: function (menuItem) {
      if (this.activeItem === menuItem) {
        this.activeItem = ''
      } else {
        this.activeItem = menuItem
      }
    },
    set_category: function (category, subcategory) {
      this.$store.commit('products/setCurrentCategory', {
        category: category,
        subcategory: subcategory
      })

      this.$emit("closeVal")
      this.$router.push('/sharebuy');
    },
    selectPingoCategory(category_id) {
      this.$store.commit("pingoproducts/setCurrentCategoryID",category_id);
      this.$emit("closeVal")
      this.$router.push("/tomobuy/?from_toppage=true");
    },
    show_pingo() {
      this.$emit("closeVal")
      this.$router.push('/tomobuy');
    }
  }
}
</script>
