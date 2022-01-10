<script>

export default {
  name: "order_detail_shippingaddress",
  props: ["shippingaddress"],
};
</script>

<template>
  <div>
    <h4 class="font-15 mb-2">郵送先情報</h4>

    <div class="card p-2 mb-lg-0">
      <table class="table table-borderless table-sm mb-0">
        <tbody>
        <tr>
          <th colspan="2">
            <h5 class="font-15 m-0">{{ shippingaddress.name }}</h5>
          </th>
        </tr>
        <tr>
          <th scope="row">Address:</th>
          <td>〒{{ shippingaddress.postcode }}{{
              shippingaddress.state
            }}{{ shippingaddress.city }} <br>
            {{ shippingaddress.town }}{{ shippingaddress.address_1 }} <br>
            {{ shippingaddress.address_2 }}
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
