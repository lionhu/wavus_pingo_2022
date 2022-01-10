<template>
  <ul class="sub-total" v-if="pointbank_balance">
    <li>
      {{ $t('pointlist.valid_point') }}
      <span class="count text-right text-danger">
        <font-awesome-icon :icon="['fas','donate']" class="text-success mr-2"></font-awesome-icon>
                          {{ pointbank_balance| currency("¥") }}
      </span>
    </li>
    <li>
      利用ポイント数:
      <input type="number" class="count text-primary" id="usepoint" name="usepoint" style="height:1.5rem;"
                       @input="check_pointUsage"
                       v-model.number="point_usage.use_point">
    </li>
  </ul>
</template>
<script>
import {mapGetters} from 'vuex';
export default {
  name:"user_point",
  props: ["cartTotal"],
  data() {
    return {
      point_usage: {
        apply_point: false,
        use_point: 0
      }
    };
  },
  computed:{
    ...mapGetters({
      pointbank_balance :"authfack/pointbank_balance"
    })
  },
  mounted(){
    this.$store.dispatch("authfack/refresh_pointBalance");
  },
  methods: {
    check_pointUsage() {
      this.point_usage.apply_point = !!parseInt(this.point_usage.use_point);
      var max = this.cartTotal >= this.pointbank_balance ? this.pointbank_balance : this.cartTotal;
      if (this.point_usage.use_point > max) {
        this.point_usage.use_point = max;
      }
      if (this.point_usage.use_point < 0) {
        this.point_usage.use_point = 0;
      }
      this.$emit('usepoint', this.point_usage);
    },
  }

}
</script>
