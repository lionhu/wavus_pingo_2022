<script>
import {mapGetters} from 'vuex'

export default {
  name: "shippingaddress_card",
  props: ["shippingaddress"],
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

    <div class="card p-2 mb-lg-0">
      <table class="table table-borderless table-sm mb-0">
        <tbody>
        <tr>
          <th colspan="2">
            <h5 class="font-15 m-0">{{ shippingaddress.name }}</h5>
          </th>
        </tr>
        <tr>
          <th scope="row">住所:</th>
          <td>
            <address style="font-style:normal;">
              <span class='first-line'>〒{{ shippingaddress.postcode }}</span><br/>
              <span
                class='city'>{{
                  shippingaddress.state
                }}{{ shippingaddress.city }}</span><br/>
              <span class='state'>{{ shippingaddress.town }}</span>
              <span class='state'>{{ shippingaddress.address_1 }}</span>
              <span class='state'>{{ shippingaddress.address_2 }}</span><br/>
            </address>
          </td>
        </tr>
        <tr>
          <th scope="row">Phone :</th>
          <td>{{ shippingaddress.phone }}</td>
        </tr>
        <tr>
          <th scope="row">Email :</th>
          <td>{{ shippingaddress.email }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
