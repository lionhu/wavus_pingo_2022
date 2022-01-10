<template>
  <div>
    <b-modal
      id="modal_addressbook"
      size="lg"
      centered
      :title="$t('addressbook.title')"
      :hide-footer="true"
      :hide-header-close="true"
      v-if="showModal"
    >
      <div class=" quickview-modal" v-if="shipping_addresses.length">
        <b-card
          :title="$t('addressbook.address.title')"
          v-for="address in shipping_addresses"
          v-bind:key="address.id"
          class="mb-2"
        >
          <template #header>
            <h6 class="mb-0 pingo_inline_block">{{ address.name }}</h6>
            <b-button href="#" class=" pingo_inline_block float-right" variant="danger" @click="deleteAddress(address)">{{$t('addressbook.buttons.delete_address')}}</b-button>
          </template>
          <b-card-text>
            <address style="line-height:1.2rem;">
              〒{{ address.postcode }} {{ address.state }}<br>
              {{ address.town }}{{ address.street }} <br>
              {{ address.address_1 }} <br>
              {{ address.address_2 }}<br/>
              電話：{{ address.phone }} <br>
              メール：{{ address.email }} <br>
            </address>
          </b-card-text>
          <b-button href="#" variant="primary" @click="Select_address(address)">{{$t('addressbook.buttons.use_address')}}</b-button>
        </b-card>
      </div>
      <div  class=" quickview-modal" v-else>
        <h3 class="mt-3 text-center" >
                <strong>登録された送付先はございません。</strong>
              </h3>
      </div>
    </b-modal>
  </div>
</template>
<script>
import {mapGetters,} from 'vuex'
import Swal from "sweetalert2"

export default {
  name:"addressbook",
  props: ['showModal',],
  data() {
    return {}
  },
  computed: {
    ...mapGetters({
      shipping_addresses: "addressbook/getterAddressList",
      shipping_addresses_meta: "addressbook/getterAddressListMeta",
    }),
  },
  methods: {
    closeModal() {
      this.$emit("closeModal")
    },
    deleteAddress(address) {
      let vm = this;
      Swal.fire({
        icon:"warning",
        title: '削除しますか?',
        showCancelButton: true,
        confirmButtonText: `削除`,
      }).then((result) => {
        if (result.isConfirmed) {
          vm.$store.dispatch("addressbook/delete_address",address.id)
        }
      })
    },
    Select_address(address) {
      this.$emit("AddressSelected", address)
    }
  }
}
</script>

<style>
.line-height-3 {
  line-height: 3rem;
}

.pingo_inline_block {
  display: inline-block;
}
</style>
