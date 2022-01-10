<script src="../../../store/orders.js"></script>
<template>
  <div>
    <b-modal
      id="modal-delivery"
      size="lg"
      centered
      title="配達情報"
      :hide-footer="true"
      v-if="openDeliveryModal">

      <div class="card">
        <div class="card-body">
          <div class="row form">
            <div class="col-6">
              <div class="form-group mb-3">
                <label class="col-form-label">配達済み?</label> <br>
                <switches v-model="info.delivered" type-bold="false" color="success"
                          class="ml-1 mb-0"></switches>
              </div>
              <div class="form-group mb-3">
                <label>配達日</label>
                <br/>
                <date-picker v-model="info.delivered_at" lang="jp"></date-picker>
              </div>
              <div class="form-group mb-3">
                <h5>配達対象</h5>
                <ul>
                  <li v-for="item in orderitem_ids" :key="item">{{ item }}</li>
                </ul>
              </div>
            </div>
            <div class="col-6 border-left">
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">物流業者</label>
                <div class="col-md-12">
                  <b-form-select v-model="info.logistic_id">
                    <b-form-select-option :value="logistic.id" v-for="logistic in logistic_options" :key="logistic.id">
                      {{
                        logistic.company
                      }}
                    </b-form-select-option>
                  </b-form-select>

                </div>
              </div>
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">追跡番号</label>
                <div class="col-md-12">
                  <b-form-input for="text" v-model="info.delivery_info.track_no"></b-form-input>
                </div>
              </div>
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">追跡リンク</label>
                <div class="col-md-12">
                  <b-form-input for="text" v-model="info.delivery_info.track_link"></b-form-input>
                </div>
              </div>
            </div>
            <!-- end col -->
          </div>
          <div class="row">
            <div class="col-12">
              <div class="text-center" v-if="result">
                <h2 class="mt-0">
                  <i class="mdi mdi-check-all"></i>
                </h2>
                <h3 class="mt-0">Thank you !</h3>

                <p class="w-75 mb-2 mx-auto">
                  Successfully updated!
                </p>
              </div>
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
import {mapGetters} from 'vuex'

export default {
  name: "delivery_modal_component",
  props: ['openDeliveryModal', "orderitem_ids", "orderitem"],
  data() {
    return {
      info: {
        update_fields: ["delivery"],
        delivered_at: new Date(),
        delivered: false,
        logistic_id: "",
        delivery_info: {
          track_no: "",
          track_link: "",
        }
      },
      // logistic_options: [
      //   "ヤマト",
      //   "日本郵政"
      // ],
      result: false,
      updating: false
    }
  },
  watch: {
    openDeliveryModal: function (newvalue, oldvalue) {
      if (newvalue && this.orderitem !== null) {
        this.info.delivered = this.orderitem.delivered;
        var _day = new Date(this.orderitem.delivered_at);
        this.info.delivered_at = this.orderitem.delivered_at !== null ? new Date(this.orderitem.delivered_at) : new Date();
        this.info.delivery_info.track_link = this.orderitem.delivery_info.track_link;
        this.info.delivery_info.track_no = this.orderitem.delivery_info.track_no;
        this.info.logistic_id = this.orderitem.logistic!==null?this.orderitem.logistic.id:0;
      }
    }
  },
  computed: {
    ...mapGetters({
      logistic_options: "logistics/getterLogistics"
    }),
  },
  components: {
    Switches: () => import('vue-switches'),
    DatePicker: () => import('vue2-datepicker'),
  },
  methods: {
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
        update_fields: ["delivery"],
        delivered_at: this.info.delivered_at !== "" ? this.info.delivered_at.toISOString() : new Date(),
        delivered: this.info.delivered,
        logistic_id: this.info.logistic_id,
        delivery_info: {
          track_no: this.info.delivery_info.track_no,
          track_link: this.info.delivery_info.track_link,
        }
      };
      this.$store.dispatch("orders/updateOrderItemInfo_superadmin", updateinfo)
        .then(response => {
          if (response) {
            vm.updating = false;
            vm.$emit("updateResult", {
              result: true,
              update_fields: ["delivery_info"],
              updated_orderitems: response.orderitems
            })
            vm.$bvModal.hide("modal-delivery")
          }
        });
    },
    expandRowChange(row, expandedRows) {
      let vm = this;
      if (row.status === "NEW") {
        let info = {orderitem_id: row.id, status: "PROCESSING"}
        this.$store.dispatch("orders/update_orderitem_status", info)
          .then(res => {
            console.log("status changed result", res)
            let itemIndex = vm.orderitems.findIndex(item => item.id === parseInt(res.orderitem_id))
            if (itemIndex > -1) {
              vm.orderitems[itemIndex].status = res.status;
            }
          })
      }
    }
  },
}
</script>
