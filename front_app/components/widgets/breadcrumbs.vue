<template>
  <div>
    <div class="breadcrumb-section" v-if="breadcrumb_type!=='static'">
      <div class="container">
        <div class="row">
          <div class="col-sm-6">
            <div class="page-title">
              <h2>{{ currentSubcategory.title }}</h2>
            </div>
          </div>
          <div class="col-sm-6">
            <nav aria-label="breadcrumb" class="theme-breadcrumb">
              <ol class="breadcrumb">
                <li class="breadcrumb-item">
                  <nuxt-link :to="{ path: '/' }">{{ $t("home") }}</nuxt-link>
                </li>
                <li class="breadcrumb-item" v-if="currentCategory.title">
                  <a href="javascript:void(0);" @click="set_category(currentCategory,currentSubcategory)">
                    {{ currentCategory.title }}
                  </a>
                </li>
              </ol>
            </nav>
          </div>
        </div>
      </div>
    </div>
    <div class="breadcrumb-section" v-else>
      <div class="container">
        <div class="row">
          <div class="col-sm-6">
            <div class="page-title">
              <h2>{{ title }}</h2>
            </div>
          </div>
          <div class="col-sm-6">
            <nav aria-label="breadcrumb" class="theme-breadcrumb">
              <ol class="breadcrumb">
                <li class="breadcrumb-item">
                  <nuxt-link :to="{ path: '/' }">{{ $t("home") }}</nuxt-link>
                </li>
<!--                <li class="breadcrumb-item">-->
<!--                  {{ title }}-->
<!--                </li>-->
              </ol>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import {mapGetters} from 'vuex'

export default {
  name: "pingo_breadcrumb",
  props: ["breadcrumb_type", "title"],
  computed: {
    ...mapGetters({
      currentCategory: "products/getterCurrentCategory",
      currentSubcategory: "products/getterCurrentSubategory",
    }),
  },
  methods: {
    set_category: function (category,subcategory) {
      this.$store.commit('products/setCurrentCategory',{
                  category:category,
                subcategory:subcategory})
      this.$router.push('/shop');
    }
  }
}
</script>
