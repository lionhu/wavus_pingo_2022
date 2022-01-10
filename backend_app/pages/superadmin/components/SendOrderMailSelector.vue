<script>
import {APIServices} from "@/helpers/APIs";
import {swalService} from "@/helpers/swal.service";

export default {
  name: "Send_order_mail_selector",
  props: ["order", "showModal"],
  components: {
    Switches: () => import('vue-switches'),
  },
  data() {
    return {
      isLoading: false,
      user: false,
      supplier: false,
      mailType: {
        label: "",
        value: ""
      },
      mail_type_options: [
        {label: "新規注文通知", value: "NEW"},
        {label: "PROCESSING", value: "PROCESSING"},
        {label: "DELIVERING", value: "DELIVERING"},
        {label: "COMPLETED", value: "COMPLETED"}
      ]
    };
  },
  computed: {},
  watch: {},
  methods: {
    closeModal() {
      console.log("closeModal")
      this.$emit("closeModal");
    },
    SendOrderNotification() {
      let self=this;
      let data = {
        mail_type: this.mailType.value,
        to_user: this.user,
        to_supplier: this.supplier
      }
      this.isLoading = true;
      let url = `store/public/orders/${this.order.id}/send_notify_email/`
      APIServices.post(url, data).then(APIServices.handleResponse)
        .then(response => {
          swalService.showToast("success", "送信完了しました")
          self.isLoading = false;
          self.$emit("closeModal");
        })
    },
    change_mail_type(val) {
      this.mailType = val;
    }
  },
};
</script>

<template>
  <b-modal id="modal-send-order-mail-selector"
           scrollable title="送付先及び種類の選択"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showModal"
  >
    <form>
      <div class="form-group row d-flex justify-content-around">
        <b-form-checkbox id="user" v-model="user" name="checkbox-2" :value="true"
                         :unchecked-value="false">
          ユーザー
        </b-form-checkbox>

        <b-form-checkbox id="supplier" v-model="supplier" name="checkbox-2" :value="true"
                         :unchecked-value="false">
          サプライヤー
        </b-form-checkbox>
      </div>
      <div class="form-group row">
        <div class="col text-center">
          <b-dropdown variant="warning" v-model="mailType">
            <template v-slot:button-content>
              Status: {{ mailType.label }}
              <i class="mdi mdi-chevron-down"></i>
            </template>
            <b-dropdown-item v-for="item in mail_type_options" :key="item.value" @click="change_mail_type(item)">
              {{ item.label }}
            </b-dropdown-item>
          </b-dropdown>
        </div>
      </div>
      <div class="form-group row">
        <div class="col text-right">
          <b-button variant="primary" v-bind:disabled="isLoading" class="btn-rounded ml-1"
                    @click="SendOrderNotification">
            <b-spinner small v-if="isLoading"></b-spinner>&nbsp;&nbsp;確定
          </b-button>
        </div>
      </div>
    </form>

  </b-modal>

</template>
