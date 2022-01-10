<template>
  <div>
    <b-modal
      id="modal-update-vendor-payment"
      size="lg"
      centered
      title="ベンダー支払"
      :hide-footer="true"
      v-if="showModal">
      <div class="card">
        <div class="card-body">
          <div class="row form">
            <div class="col-6">
              <div class="form-group mb-3">
                <label class="col-form-label">ベンダー支払?</label> <br>
                <switches v-model="info.paid" type-bold="false" color="success"
                          class="ml-1 mb-0"></switches>
              </div>
              <div class="form-group mb-3">
                <label>支払日</label>
                <br/>
                <date-picker v-model="info.paid_at" lang="jp"></date-picker>
              </div>
              <div class="form-group mb-3">
                <h5>支払対象</h5>
                <ul>
                  <li v-for="item in orderitem_ids" :key="item">{{ item }}</li>
                </ul>
              </div>
            </div>
            <div class="col-6 border-left">
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">支払方法</label>
                <div class="col-md-12">
                  <b-form-input for="text" v-model="info.paid_info.method"></b-form-input>
                </div>
              </div>
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">メモ</label>
                <div class="col-md-12">
                  <b-form-input for="text" v-model="info.paid_info.memo"></b-form-input>
                </div>
              </div>
            </div>
            <!-- end col -->
          </div>
          <div class="row">
            <div class="col-12">
              <div class="text-center mt-md-3">
                <b-spinner class="m-2" variant="danger" role="status" v-if="updating"></b-spinner>
                <div class="mb-3">
                  <b-button variant="danger" class="btn-rounded ml-1" @click="update_orderitem">
                    Update
                  </b-button>
                </div>
              </div>
            </div>
            <!-- end col -->
          </div>
        </div>
      </div>
    </b-modal>
  </div>
</template>
<script>
import {orderService} from "~/helpers/order.service"
export default {
  name: "modal_update_vendor_payment",
  props: ['showModal', "orderitem_ids", "orderitem"],
  data() {
    return {
      info: {
        paid_at: new Date(),
        paid: false,
        paid_info: {
          method: "",
          memo: ""
        }
      },
      result: false,
      updating: false,
      status: "COMPLETED",
      aggree: false
    }
  },
  watch: {
    showModal: function (newvalue, oldvalue) {

    if (newvalue && this.orderitem !== null) {
        this.info.paid = this.orderitem.paid;
        var _day=new Date(this.orderitem.paid_at);
        this.info.paid_at = this.orderitem.paid_at!==null?new Date(this.orderitem.paid_at):new Date();
        this.info.paid_info.method = this.orderitem.paid_info.method;
        this.info.paid_info.memo = this.orderitem.paid_info.memo;
      }
    }
  },
  components: {
    Switches: () => import('vue-switches'),
    DatePicker: () => import('vue2-datepicker'),
  },
  methods: {
    close_modal() {
      this.$emit("updateResult", {result: false})
    },
    update_orderitem() {
      var vm = this;
      var orderitem_ids = [];
      if (this.orderitem !== null) {
        orderitem_ids.push(this.orderitem.id);
      } else {
        orderitem_ids = this.orderitem_ids;
      }
      var updateinfo = {
        orderitem_ids: orderitem_ids,
        update_fields: ["pay_vendor"],
        pay_vendor_info: {
          paid_at: this.info.paid_at !== "" ? this.info.paid_at.toISOString() : new Date(),
          paid: this.info.paid,
          paid_info: {
            method: this.info.paid_info.method,
            memo: this.info.paid_info.memo
          }
        }
      };
      orderService.updateOrderItem_BATCH_superadmin(updateinfo)
        .then(response => {
          if (response.length) {
            vm.updating = false;
            vm.$emit("updateResult", {
              result: true,
              update_fields:["payment_vendor"],
              updated_orderitems: response
            })
            vm.$bvModal.hide("modal-update-vendor-payment")
          }
        });
    }
  },
}
</script>
