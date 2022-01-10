<template>
  <ul class="sub-total" v-if="valid_point ">
    <li>
      {{ $t('pointlist.valid_point') }}
      <span class="count text-right text-danger">
        <font-awesome-icon :icon="['fas','donate']" class="text-success mr-2"></font-awesome-icon>
                          {{ valid_point| currency("¥") }}
      </span>
    </li>
    <li v-if="valid_point>=cartTotal">
      ポイントでの支払は可能です。
      <a href="javascript:void(0);" class='btn-solid btn pull-right' @click="pay_by_point" >
                    ポイントで支払を行う
                  </a>
    </li>
  </ul>
</template>
<script>
import {mapGetters} from "vuex"

export default {
  props: ["cartTotal"],
  data() {
    return {
      point_usage: {
        apply_point: false,
        use_point: 0
      },
      valid_point: 0
    };
  },
  components: {},
  computed: {
    ...mapGetters({
      profile: "authfack/profile_info",
    }),
  },
  async fetch() {
    var vm = this;
    await this.$axios.post('/back/store/api/pointbank/retrieve_usable_point/')
      .then(resp => {
        var response_data =resp.data;
        if (response_data.result) {
          vm.valid_point = response_data.point;
          vm.point_usage.use_point=vm.valid_point>=vm.cartTotal?vm.cartTotal:0;
        }
      })
  },
  methods: {
    pay_by_point(){
      this.$emit('usepoint', this.cartTotal);
    }
  }

}
</script>
