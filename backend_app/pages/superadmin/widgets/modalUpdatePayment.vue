<template>
  <div>
    <b-modal
      id="modal-update-payment"
      size="lg"
      centered
      title="支払ステータス"
      :hide-footer="true"
      v-if="openModal">
      <div class="card">
        <div class="card-body">
          <div class="row">
            <h5>注文対象：</h5>
            <div class="col-md-12">
              <ul>
                <li v-for="idx in order_ids" :key="idx">#{{idx}}</li>
              </ul>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <div class="mt-3">
                <b-form-group>
                  <b-form-radio v-model="status" name="status_radio" value="CANCELED">決済取消(CANCELED)</b-form-radio>
                  <b-form-radio v-model="status" name="status_radio" value="COMPLETED">決済確定(COMPLETED)
                  </b-form-radio>
                </b-form-group>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <div class="mt-3">
                <b-form-checkbox id="checkbox-aggree" v-model="aggree" name="checkbox-aggree" value="accepted"
                                 unchecked-value="not_accepted">了解です。
                </b-form-checkbox>
                <p class="text-danger">一旦実行したら、変更できなくなります。ご注意ください。</p>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12 d-flex justify-content-around">
              <b-button variant="primary" class="btn-rounded ml-1" @click="close_modal">
                閉じる
              </b-button>
              <b-button variant="danger" class="btn-rounded ml-1" v-if="aggree" @click="update_order">
                <b-spinner class="m-2" variant="warning" role="status" v-if="updating"></b-spinner>
                実行
              </b-button>
            </div>
          </div>
        </div>
      </div>
    </b-modal>
  </div>
</template>
<script>
import {orderService} from "~/helpers/order.service"

export default {
  name: "modal_update_payment",
  props: ['openModal', "order_ids"],
  data() {
    return {
      result: false,
      updating: false,
      status: "COMPLETED",
      aggree: false
    }
  },
  watch: {
    openPaymentStatusModal: function (newvalue, oldvalue) {
      if (newvalue !== null) {
        console.log("openModal: ", newvalue)
      }
    }
  },
  components: {
    Switches: () => import('vue-switches'),
    DatePicker: () => import('vue2-datepicker'),
  },
  methods: {
    close_modal(result,updateinfo,orders) {
      this.$emit("updateResult", {result:result,updateinfo:updateinfo,orders:orders})
    },
    update_order() {
      let vm = this;
      let updateinfo = {
        order_ids: this.order_ids,
        payment_status:this.status,
        update_fields: ["payment_status"],
      };
      console.log(updateinfo)
      orderService.update_batch( updateinfo)
        .then(response => {
          console.log(response)
          if (response.result) {
            vm.updating = false;
            vm.close_modal(true,updateinfo,response.orders)
          }
        });
    }
  },
}
</script>
