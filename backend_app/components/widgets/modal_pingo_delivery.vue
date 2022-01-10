<template>
  <div>
    <b-modal
      id="modal_pingo_delivery"
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
                <small class="text-danger">COMPLETED 注文の配達情報の変更は出来かねます。</small>
                <ul>
                  <li v-for="item in orderitem_ids" :key="item">{{ item }}</li>
                </ul>
              </div>
            </div>
            <div class="col-6 border-left">
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">物流業者</label>
                <div class="col-md-12">
                  <b-form-select v-model="info.logistic_id" @change="deliverinfo_changed">
                    <b-form-select-option :value="logistic.id" v-for="logistic in logistic_options" :key="logistic.id">
                      {{ logistic.company }}
                    </b-form-select-option>
                  </b-form-select>

                </div>
              </div>
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">追跡番号</label>
                <div class="col-md-12">
                  <b-form-input for="text" v-model="info.delivery_info.track_no"
                                @keyup="deliverinfo_changed"></b-form-input>
                </div>
              </div>
              <div class="form-group mb-3">
                <label class="col-md-6 col-form-label">追跡リンク</label>
                <div class="col-md-12">
                  <a :href="info.delivery_info.track_link">{{ info.delivery_info.track_link }}</a>
                  <b-form-input for="text" v-model="info.delivery_info.track_link" hidden></b-form-input>
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
import {pingoproductService} from "~/helpers/pingoproduct.service"

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
        this.info.logistic_id = this.orderitem.logistic !== null ? this.orderitem.logistic.id : 0;
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
    deliverinfo_changed() {
      let logistic = this.logistic_options.find(logistic => logistic.id === this.info.logistic_id)
      this.info.delivery_info.track_link = logistic.track_link !== null ? logistic.track_link.replace("{}", this.info.delivery_info.track_no) : this.info.delivery_info.track_no;
    },
    update_orderitem() {
      let vm = this;
      let orderitem_ids = [];
      if (this.orderitem !== null) {
        orderitem_ids.push(this.orderitem.id);
      } else {
        orderitem_ids = this.orderitem_ids;
      }
      let update_info = {
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
      console.log(update_info)

      this.updating = true;
      this.$store.dispatch("pingoproducts/superadmin_batch_update_orders", update_info)
        .then(response => {
          console.log(response)
          vm.updating = false;
          vm.$emit("updateResult", {
            update_fields: ["delivery"],
            update_info: update_info
          })
          vm.$bvModal.hide("modal_pingo_delivery")
        });
    },
  },
}
</script>
