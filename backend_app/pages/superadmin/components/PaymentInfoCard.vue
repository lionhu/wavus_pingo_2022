<script>
import {mapGetters} from 'vuex'

export default {
  name: "payment_info_card",
  props: ["payment_info"],
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
    <h4 class="font-15 mb-2">支払情報</h4>

    <div class="card p-2 mb-lg-0">
      <table class="table table-borderless table-sm mb-0">
        <tbody>
        <tr>
          <th scope="row">支払方法:</th>
          <td>{{ payment_info.payment_method }}</td>
        </tr>
        <tr>
          <th scope="row">支払状態 :</th>
          <td>{{ payment_info.payment_status }}</td>
        </tr>
<!--        <tr>-->
<!--          <th scope="row">PaymentID :</th>-->
<!--          <td>{{ payment_info.payment_id }}</td>-->
<!--        </tr>-->
        </tbody>
      </table>
    </div>
  </div>
</template>
