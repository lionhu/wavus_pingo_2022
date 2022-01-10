<template>
  <div>
    <Header/>
    <Breadcrumbs :title="$t('payment_creditcard.pay_by_card')"/>
    <section class="section-b-space bg-gradient-blue">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <h6 class="text-white">{{ $t("cart_info.product") }}: <span
              class="ml-2"> {{ product.item_name }}</span></h6>
            <h6 class="text-white"><span class="inline-block ml-4">(</span>{{ variant.name }})</h6>
            <h6 class="text-white">{{ $t("cart_info.total") }}: <span
              class="ml-2">{{ order_data.TaxedTotal|currency("¥") }}</span>
            </h6>
          </div>
        </div>
        <div class="nichiei-container row" v-show="formLoaded">
          <div id="sq-ccbox col-12" class="position-relative">
            <form id="nonce-form" novalidate>
              <!--                            <div class="errorbox">-->
              <!--                                <div class="error" v-for="error in errors" :key=error.message>-->
              <!--                                    {{error}}-->
              <!--                                </div>-->
              <!--                            </div>-->
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
          <div class="col-6 offset-6">
            <button @click="requestCardNonce($event)"
                    class='productPurchase payButton btn btn-solid pull-right'>{{ $t("cart_info.pay") }}
            </button>
          </div>

        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>

<script>
import Swal from "sweetalert2"
import {mapGetters} from 'vuex'

export default {
  name: "paymentForm_pingo",
  data: function () {
    return {
      errors: [],
      postcode: "3360031",
      order: {
        id: 0,
        slug: "",
        Qty: 0,
        Total: 0
      },
      order_data: {},
      formLoaded: false,
      payment_result: false,
      processing: false,
      product: {},
      variant: {},
      shippingaddress: {}
    };
  },
  computed: {
    ...mapGetters({
      back_server: "system/getterBackServer"
    }),
  },
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
  },
  watch: {
    showPaymentForm: function () {
      if (!this.showPaymentForm) {
        return 1;
      }
      this.paymentForm.build();
    }
  },
  mounted: function () {
    var vm = this;
    var order_data = this.$route.params.order_data;
    console.log(order_data)
    if (order_data === undefined) {
      this.$router.push("/tomobuy")
    }
    this.order_data = order_data;

    if (order_data.product !== undefined && order_data.variant !== undefined && order_data.shippingaddress !== undefined) {
      this.product = order_data.product;
      this.variant = order_data.variant;
      this.shippingaddress = order_data.shippingaddress;
    } else {
      this.$router.push("/tomobuy")
    }

    let locationId = "EX4V10MCHTESW";
    let applicationId = "sandbox-sq0idb-3qfeC9ngaTXXppO9Jl_dCA";
    let that = this;
    this.paymentForm = new SqPaymentForm({
      autoBuild: false,
      applicationId: applicationId,
      locationId: locationId,
      inputClass: "sq-input",

      inputStyles: [
        {
          fontSize: ".9em"
        }
      ],
      cardNumber: {
        elementId: "sq-card-number",
        placeholder: this.$root.$t('payment_creditcard.sq-card-number')
      },
      cvv: {
        elementId: "sq-cvv",
        placeholder: this.$root.$t('payment_creditcard.sq-cvv')
      },
      expirationDate: {
        elementId: "sq-expiration-date",
        placeholder: this.$root.$t('payment_creditcard.sq-expiration-date')
      },
      postalCode: false,

      // SqPaymentForm callback functions
      callbacks: {
        /*
           * callback function: methodsSupported
           * Triggered when: the page is loaded.
           */
        methodsSupported: function (methods) {
          // Only show the button if Apple Pay for Web is enabled
          // Otherwise, display the wallet not enabled message.
          // that.applePay = methods.applePay;
          // that.masterpass = methods.masterpass;
        },

        /*
           * Digital Wallet related functions
           */
        createPaymentRequest: function () {
          var paymentRequestJson;
          /* ADD CODE TO SET/CREATE paymentRequestJson */
          return paymentRequestJson;
        },
        validateShippingContact: function (contact) {
          var validationErrorObj;
          /* ADD CODE TO SET validationErrorObj IF ERRORS ARE FOUND */
          return validationErrorObj;
        },

        /*
           * callback function: cardNonceResponseReceived
           * Triggered when: SqPaymentForm completes a card nonce request
           */
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

          // POST the nonce form to the payment processing page
          // document.getElementById("nonce-form").submit();

          delete that.product.variations;
          var pingo_orderdata = {
            nonce: nonce,
            type: "PINGO",
            shippingaddress: that.shippingaddress,
            product: that.product,
            variant: that.variant,
            product_id: that.product.id,
            variant_id: that.variant.id,
            quantity: 1,
            total: that.variant.price,
            Tax_rate: that.order_data.Tax_rate,
            Tax: that.order_data.Tax,
            TaxedTotal: that.order_data.TaxedTotal
          };
          // console.log(pingo_orderdata);
          that.$axios.$post
          (that.back_server + "/back/store/api/squarepayment/create_pingo/", pingo_orderdata)
            .then(function (response) {
              console.log(response)
              if (response.result) {
                that.payment_result = true;

                var updateinfo = {
                  "product_id": that.product.id,
                  "currentNum": response.currentNum
                }
                that.$store.dispatch("system/updatePingoProduct", updateinfo)
                Swal.fire({
                  icon: 'success',
                  title: '支払いは完了！',
                  html: '注文の支払いは完了いたしました。<br> ありがとうございました！',
                  footer: '<a href="/sharebuy">' + that.$root.$t("cart_info.continue_shopping") + '</a>'
                });
                that.$router.push("/tomobuy")

              }
            });

        },
        /*
           * callback function: paymentFormLoaded
           * Triggered when: SqPaymentForm is fully loaded
           */
        paymentFormLoaded: function () {
          that.formLoaded = true;
          // that.paymentForm.focus("cardNumber");
          /* HANDLE AS DESIRED */
        }
      }
    });
    this.paymentForm.build();
  },
  methods: {
    requestCardNonce: function (event) {
      this.processing = true;
      event.preventDefault();
      this.paymentForm.requestCardNonce();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
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

.expiration-date,
.cvv,
.postal-code {
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

.width-20 {
  width: 20px;
}

@media (min-width: 360px) {
  #sq-ccbox {
    max-width: 400px;
    max-height: 120px;
  }
}
</style>
