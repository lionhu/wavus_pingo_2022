<template>
  <div class="row">
    <div class="col-4">
      <div class="nichiei_wrapper">
        <img :src='item.variation.thumbimage_url' class="thumbnail">
        <span class="number">{{ number }}</span>
      </div>
    </div>
    <div class="col-8 d-flex justify-content-between align-items-center">
      <span class="d-none d-sm-block">
        {{ item.variation.name }} <br>
        SKU {{ item.variation.sku }}</span>
      <div class="ml-3">
        <a href="javascript:void(0);" class="text-danger" v-if="!item.delivered">
          <span>未発送</span>
        </a>
        <a :href="item.delivery_info.track_link" class="text-primary" v-else>
          追跡番号：{{ item.delivery_info.track_no }} <br>
          発送日：{{ item.delivered_at|short_date }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from "vuex"

export default {
  props: ["item", "number"],
  computed: {
    ...mapGetters({
      back_server: 'system/getterBackServer'
    }),
  },
  methods: {
  }
}
</script>
<style>
.nichiei_wrapper {
  position: relative;
  display: inline-block;
  margin: 10px;
  border: #dedada 2px solid;
}

.thumbnail {
  max-width: 80px;
}

.number {
  position: absolute;
  background: var(--theme-deafult);
  width: 20px;
  height: 20px;
  color: white;
  border-radius: 20px;
  text-align: center;
  font-size: 12px;
  line-height: 14px;
  font-weight: 600;
  /*top: 20%;*/
  right: -8px;
  padding: 3px;
}

.variation_label {
  position: absolute;
  bottom: 0px;
  left: 0px;
  margin: 0 5px;
  width: 100%;
  background: grey;
  padding: 2px 5px;
  color: white;
  text-align: center;
}
</style>
