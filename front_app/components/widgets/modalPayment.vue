<template>
  <b-modal
    id="modal-payment"
    name="modal-payment"
    size="lg"
    centered
    no-close-on-backdrop
    hide-header-close
    :title="$t('checkout.credit_card')"
    :hide-footer="true"
    body-class="modal-payment-body"
    dialog-class="modal-payment-dialog"
    v-if="openPaymentModal">
    <div class="row">
      <div class="col-12 text-right">
        <div class="payment-box">
          <div class="payment-card-bottom">
            <ul>
              <li><a href="#"><img src="/images/icon/visa.png" alt=""></a></li>
              <li><a href="#"><img src="/images/icon/mastercard.png" alt=""></a></li>
              <li><a href="#"><img src="/images/icon/american-express.png" alt=""></a></li>
              <li><a href="#"><img src="/images/icon/jcb.png" alt=""></a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="nichiei-container row" v-show="formLoaded">
        <div id="sq-ccbox col-12" class="position-relative">
          <h4 class="text-white">{{ $t('payment_creditcard.charge_amount') }}
            <span class="ml-3">{{ order_detail.chargeAmount|currency("¥") }}</span>
          </h4>
          <form id="nonce-form" novalidate>
            <div class="errorbox">
              <div class="error" v-for="error in errors" :key=error.message>
                {{ error }}
              </div>
            </div>
            <div id="card-tainer">
              <div class="cardfields card-number" id="sq-card-number">o</div>
              <div class="cardfields expiration-date" id="sq-expiration-date">e</div>
              <div class="cardfields cvv" id="sq-cvv">e</div>
              <!--                                <div class="cardfields postal-code" id="sq-postal-code">e</div>-->
            </div>

            <input type="hidden" id="card-nonce" name="nonce">
            <ul id="errors" class="error" style="display:none"></ul>
          </form>
          <img src='/images/icon/processing.gif' class="processing" v-show="processing">
        </div>
      </div>
      <div class="nichiei-container row" v-show="!formLoaded">
        <div class="col-12">
          <img src='/images/loader2.gif' style="max-width:80px;" alt="">
        </div>
      </div>
      <div class="row">
        <div class="col-6 text-left">
          <button class='btn btn-solid black-btn' @click="closeModal">
            Close
          </button>
        </div>
        <div class="col-6 text-right">
          <button @click="requestCardNonce($event)"
                  class='btn btn-solid pull-right'>{{ $t("cart_info.pay") }}
          </button>
        </div>
      </div>
    </div>
  </b-modal>
</template>
<script>
import Swal from "sweetalert2"
import {mapState, mapGetters} from 'vuex'

export default {
  name: "paymentModal",
  props: ["openPaymentModal", "order_detail"],
  data: function () {
    return {
      errors: [],
      postcode: "3360031",
      order: {
        id: 0,
        slug: "",
        Qty: 0,
        TaxedTotal: 0
      },
      formLoaded: false,
      payment_result: false,
      processing: false
    };
  },
  watch: {
    openPaymentModal: function () {
      if (!this.openPaymentModal) {
        return 1;
      }
      this.load_order();
    }
  },
  computed: {
    ...mapGetters({
      back_server: "system/getterBackServer"
    }),
    chargeAmount: function () {
      if (this.order.point_usage === undefined || !this.order.point_usage.apply_point) {
        return this.order.TaxedTotal;
      }
      return this.order.point_usage.apply_point ? this.order.TaxedTotal - this.order.point_usage.use_point : this.order.TaxedTotal;
    }
  },
  methods: {
    load_order() {

      let vm = this;
      this.init_paymentForm();
      this.paymentForm.build();
    },
    init_paymentForm() {
      let vm = this;
      let locationId = "LBA3S5H6B914E";
      let applicationId = "sandbox-sq0idb-W7v96oQuEI-T1jDlEXuNWA";
      vm.paymentForm = new SqPaymentForm({
        autoBuild: false,
        applicationId: applicationId,
        locationId: locationId,
        inputClass: "sq-input",
        // Initialize the payment form elements

        // Customize the CSS for SqPaymentForm iframe elements
        inputStyles: [
          {
            fontSize: ".9em"
          }
        ],

        // Initialize the credit card placeholders
        cardNumber: {
          elementId: "sq-card-number",
          placeholder: vm.$root.$t('payment_creditcard.sq-card-number')
        },
        cvv: {
          elementId: "sq-cvv",
          placeholder: vm.$root.$t('payment_creditcard.sq-cvv')
        },
        expirationDate: {
          elementId: "sq-expiration-date",
          placeholder: vm.$root.$t('payment_creditcard.sq-expiration-date')
        },
        postalCode: false,

        // SqPaymentForm callback functions
        callbacks: {
          // methodsSupported: function (methods) {
          // that.applePay = methods.applePay;
          // that.masterpass = methods.masterpass;
          // },
          createPaymentRequest: function () {
            var paymentRequestJson;
            return paymentRequestJson;
          },
          validateShippingContact: function (contact) {
            var validationErrorObj;
            return validationErrorObj;
          },

          cardNonceResponseReceived: function (errors, nonce, cardData) {
            const errorList = document.getElementById("errors");
            if (errors) {
              let error_html = "";
              for (var i = 0; i < errors.length; i++) {
                error_html += "<li> " + errors[i].message + " </li>";
              }
              errorList.innerHTML = error_html;
              errorList.style.display = 'inline-block';
              return;
            }
            errorList.style.display = 'none';
            errorList.innerHTML = "";
            // Assign the nonce value to the hidden form field
            document.getElementById("card-nonce").value = nonce;

            var new_orderdata = vm.order_detail;
            new_orderdata.nonce = nonce;

            console.log(new_orderdata)
            vm.$store.dispatch("orders/placeOrder", new_orderdata)
              .then(function (response) {
                if (response.result) {
                  vm.payment_result = true;
                  Swal.fire({
                    icon: 'success',
                    title: '支払い完了',
                    html: '注文の支払いは完了いたしました。<br> ありがとうございました！',
                    footer: `ポイント残高：${response.data.pointbank_balance}`
                  }).then((result) => {
                    if (result.isConfirmed) {
                      vm.$store.commit("authfack/setPointBalance", response)
                      vm.$store.dispatch("cart/empty_cart");
                      vm.$router.push("/sharebuy")
                    }
                  })
                }
              }).catch(error=>{
              console.log("place orderdata error")
              console.log(error)
              if(error.data.message.includes("insufficient stock")){
                Swal.fire({
                  icon:"error",
                  html:"大変申し訳ございませんでした。在庫不足でした。"
                })
                vm.$emit("closeModal")
              }
            });

          },
          paymentFormLoaded: function () {
            vm.formLoaded = true;
            vm.paymentForm.focus("cardNumber");
            /* HANDLE AS DESIRED */
          }
        }
      });
    },
    requestCardNonce: function (event) {
      this.processing = true;
      // Don't submit the form until SqPaymentForm returns with a nonce
      event.preventDefault();

        this.paymentForm.requestCardNonce();


    },
    closeModal() {
      this.$emit("closeModal")
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/deep/ .modal-payment-body {
  background: rgb(2, 0, 36);
  background: linear-gradient(360deg, rgb(65 57 197) 0%, rgba(27, 27, 193, 1) 27%, rgba(0, 212, 255, 1) 100%);

}

/deep/ .modal-payment-dialog {
  max-width: 400px;
}

.sq-input {
  border: 1px solid rgb(223, 223, 223);
  outline-offset: -2px;
  margin-bottom: 5px;
  display: inline-block;
  border: none;
  color: #32325d;
  line-height: 18px;
  font-family: "Helvetica Neue", Helvetica, sans-serif;
  font-size: 16px;
  height: 18px;
  -webkit-font-smoothing: antialiased;
}

.sq-input ::placeholder {
  color: #aab7c4;
  opacity: 0.5;
}

/* Define how SqPaymentForm iframes should look when they have focus */

/* Define how SqPaymentForm iframes should look when they contain invalid values */

.sq-input--error {
  outline: 3px auto rgb(255, 97, 97);
}

.errorbox {
  line-height: 14px;
  text-align: left;
}

.error {
  float: left;
  width: calc((100% - 56px));
  margin: 16px 16px 16px 0;
  border: 1px solid #E02F2F;
  border-radius: 6px;
  background-color: white;
  font-size: 16px;
  padding: 24px;
}

/* Customize the "Pay with Credit Card" button */

.button-credit-card {
  min-width: 200px;
  min-height: 20px;
  padding: 0;
  margin: 5px;
  line-height: 20px;
  box-shadow: 2px 2px 1px rgb(200, 200, 200);
  background: rgb(255, 255, 255);
  border-radius: 5px;
  border: 1px solid rgb(200, 200, 200);
  font-weight: bold;
  cursor: pointer;
}

.card-number {
  width: 100%;
}

.modal .payButton {
  margin-left: 0px;
  position: absolute;
  bottom: 0px;
  width: 400px;
}

/* Customize the "{{Wallet}} not enabled" message */

.wallet-not-enabled {
  min-width: 200px;
  min-height: 40px;
  max-height: 64px;
  padding: 0;
  margin: 10px;
  line-height: 40px;
  background: #eee;
  border-radius: 5px;
  font-weight: lighter;
  font-style: italic;
  font-family: inherit;
  display: block;
}

/* Customize the Apple Pay on the Web button */

.button-apple-pay {
  min-width: 200px;
  min-height: 40px;
  max-height: 64px;
  padding: 0;
  margin: 10px;
  background-image: -webkit-named-image(apple-pay-logo-white);
  background-color: black;
  background-size: 100% 60%;
  background-repeat: no-repeat;
  background-position: 50% 50%;
  border-radius: 5px;
  cursor: pointer;
  display: none;
}

/* Customize the Masterpass button */

.button-masterpass {
  min-width: 200px;
  min-height: 40px;
  max-height: 40px;
  padding: 0;
  margin: 10px;
  background-image: url(https://static.masterpass.com/dyn/img/btn/global/mp_chk_btn_147x034px.svg);
  background-color: black;
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: 50% 50%;
  border-radius: 5px;
  border-color: rgb(255, 255, 255);
  cursor: pointer;
}

#sq-walletbox {
  text-align: center;
  vertical-align: top;
  font-weight: bold;
}

#sq-ccbox {
  margin: 50px auto;
  padding: 0px 10px;
  text-align: center;
  vertical-align: top;
  font-weight: bold;
  max-width: 315px;
  max-height: 80px;
}

.expiration-date, .cvv, .postal-code {
  width: 30%;
  display: inline-block;
}

#card-tainer {
  text-align: left;
  margin-top: 8px;
  background-color: white;
  height: 80px;
  padding: 10px 12px;
  border-radius: 4px;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  border-bottom-left-radius: 4px;
  border: 1px solid transparent;
  box-shadow: 0 1px 3px 0 #e6ebf1;
  -webkit-transition: box-shadow 150ms ease;
  transition: box-shadow 150ms ease;
  box-sizing: border-box;
}


.bg-gradient-blue {
  background: rgb(2, 0, 36);
  background: linear-gradient(360deg, rgba(2, 0, 36, 1) 0%, rgba(27, 27, 193, 1) 27%, rgba(0, 212, 255, 1) 100%);
}

.nichiei-container {
  max-width: 500px;
  margin: 20px auto;
}

.processing {
  width: 220px;
  resize: auto;
  position: absolute;
  top: -40px;
  right: -40px;
}

@media (min-width: 360px) {
  #sq-ccbox {
    max-width: 400px;
    max-height: 120px;
  }
}
</style>
