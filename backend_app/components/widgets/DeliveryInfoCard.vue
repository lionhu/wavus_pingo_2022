<script>
import {mapGetters} from 'vuex'

export default {
  name: "delivery_info_card",
  props: ["delivery_info"],
  components: {},
  data() {
    return {}
  },
  mounted() {
  },
  computed: {
    ...mapGetters({}),
  },
  methods: {}
}
</script>

<template>

  <div>
    <h4 class="font-15 mb-2">配送情報</h4>

    <div class="card p-2 mb-lg-0" v-if="delivery_info.delivered">
      <div class="text-center">
        <div class="my-2">
          <i class="mdi mdi-truck-fast h1 text-muted"></i>
        </div>
        <h5><b>{{ delivery_info.logistic.company }}</b></h5>
        <div class="mt-2 pt-1">
          <p class="mb-1">
            <span class="font-weight-semibold">追跡番号 :</span>
            <a
              :href="delivery_info.delivery_info.track_link">{{ delivery_info.delivery_info.track_no }}</a>
          </p>
          <p class="mb-1">
            <span class="font-weight-semibold">発送日 :</span>
            {{ delivery_info.delivered_at |short_date }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
