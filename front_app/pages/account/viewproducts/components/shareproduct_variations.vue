<template>
  <div>
    <ul v-if="item_variations.length">
      <li v-for="variant in item_variations" :key="variant.id"
          class="row line-height-3 my-2 py-2 border-bottom-grey ">
        <div class="col-12 d-flex justify-content-around align-items-center">
          <div>
            <h5>{{ variant.name }}</h5>
            <p>{{ variant.description }}</p>
          </div>

          <b-button pill variant="outline-success">
            {{ variant.price | currency("¥") }}
          </b-button>
          <div class="text-left">
            <!--                  <span class="d-block theme-color">{{ variant.price|currency("¥") }}</span>-->
            <img :src="variant.image_url" style="width: 80px;">
          </div>
        </div>
        <div v-if="variant.point_rule.is_valid" v-show-slide="show_variation_slide_info(variant)" class="col-12">
          <h4 class="mt-2 theme-color">紹介ポイント</h4>
          <div class="row" v-if="isClientSuperAdmin||isSuperAdmin">
            <div class="col-6">{{ $t("organization.client_superadmin") }}</div>
            <div class="col-6">
              <b-button pill block variant="outline-danger">
                <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                {{
                  variant.point_rule.policies.client_superadmin | currency("")
                }}
              </b-button>
            </div>
          </div>
          <div class="row" v-if="isClientAdmin||isClientSuperAdmin||isSuperAdmin">
            <div class="col-6">{{ $t("organization.client_admin") }}</div>
            <div class="col-6">
              <b-button pill block variant="outline-danger">
                <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                {{
                  variant.point_rule.policies.client_admin | currency("")
                }}
              </b-button>
            </div>
          </div>
          <div class="row" v-if="policies.LEVEL_2">
            <div class="col-6">{{ $t("organization.level_2") }}</div>
            <div class="col-6">
              <b-button pill block variant="outline-danger">
                <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                {{
                  variant.point_rule.policies.level_2 | currency("")
                }}
              </b-button>
            </div>
          </div>
          <div class="row" v-if="policies.LEVEL_1">
            <div class="col-6">{{ $t("organization.level_1") }}</div>
            <div class="col-6">
              <b-button pill block variant="outline-danger">
                <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                {{
                  variant.point_rule.policies.level_1 | currency("")
                }}
              </b-button>
            </div>
          </div>
        </div>
        <div class="col-12 text-center">
          <a href="javascript:void(0);" class="btn btn-solid" @click="toggleFeatures(variant)">ポイント詳細</a>
        </div>
      </li>
    </ul>
    <b-button size="lg" class="btn-danger text-white d-block mx-auto" v-else>
      売り切れ
    </b-button>
  </div>
</template>
<script>
import {mapGetters} from "vuex";

export default {
  props: ['item_variations'],
  data() {
    return {
      show_slide_flags: [],
    }
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME",
      loggedIn: "authfack/loggedIn",
      policies: 'authfack/policies',
      isClientAdmin: "authfack/isClientAdmin",
      isClientSuperAdmin: "authfack/isClientSuperAdmin",
      isSuperAdmin: "authfack/isSuperadmin",
    }),
  },
  mounted() {
    let self =this;
    if (this.item_variations.length > 0) {
      self.show_slide_flags = []
      this.item_variations.forEach(variation => {
        self.show_slide_flags.push({id: variation.id, show: false})
      })
    }
  },
  methods: {
    show_variation_slide_info(variation) {
      if (this.show_slide_flags.length === 0) return false;
      let index = this.show_slide_flags.findIndex(slide => slide.id === variation.id)
      if (index > -1) {
        return this.show_slide_flags[index].show;
      }
    },
    toggleFeatures(variation) {
      let index = this.show_slide_flags.findIndex(slide => slide.id === variation.id)
      if (index > -1) {
        this.show_slide_flags[index].show = !this.show_slide_flags[index].show;
      }
    },
  }
}
</script>

<style>
.line-height-3 {
  line-height: 3rem;
}
</style>
