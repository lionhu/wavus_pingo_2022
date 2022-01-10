
<template>
  <b-modal
    id="modal_shippingaddress"
    name="modal_shippingaddress"
    size="lg"
    centered
    :title="$t('addressbook.address.register')"
    :hide-footer="true"
    v-if="showModal">
    <div class="container checkout-page">
      <div class="row mb-3 checkout-form">
        <!--        <ValidationObserver ref="observer" v-slot="{ invalid }" tag="form"-->
        <!--                            @submit.prevent="onSubmit">-->

        <ul>
          <li v-for="error in errors" class="text-danger">* {{ error }}</li>
        </ul>
        <div class="row check-out">
          <div class="form-group col-md-6 col-sm-6 col-xs-12">
            <!--              <ValidationProvider rules="required" v-slot="{ errors }"-->
            <!--                                  name="Name">-->
            <div class="field-label">受取人</div>
            <input type="text" v-model="shipping_address.name" name="Name"
                   :placeholder="$t('checkout.name')"/>
            <!--              </ValidationProvider>-->
          </div>
          <div class="form-group col-md-6 col-sm-6 col-xs-12">
            <!--              <ValidationProvider rules="required|min:6|max:15" v-slot="{ errors }"-->
            <!--                                  name="phone Number">-->

            <div class="field-label">連絡電話番号</div>
            <input type="text" v-model="shipping_address.phone" name="Phone"
                   :placeholder="$t('checkout.phone')"/>
            <!--              </ValidationProvider>-->
          </div>
          <div class="form-group col-12">
            <div class="field-label">メール</div>
            <!--              <ValidationProvider rules="required|email" v-slot="{ errors }"-->
            <!--                                  name="Email">-->
            <input type="text" v-model="shipping_address.email" name="Email Address"
                   :placeholder="$t('checkout.email')"/>
            <!--              </ValidationProvider>-->
          </div>
          <div class="form-group col-md-6 col-sm-6 col-xs-12">
            <div class="field-label" v-if="auto_searching">
              <i class="fa fa-spinner fa-spin text-danger"></i>
            </div>
            <!--              <ValidationProvider rules="required|min:5|max:8" v-slot="{ errors }"-->
            <!--                                  name="Postcode">-->
            <div class="field-label">郵便番号</div>
            <input type="text" v-model="shipping_address.postcode" name="Postcode"
                   @change="autocomplete_postcode"
                   :placeholder="$t('checkout.postcode')"
                   style="background-color: orange"/>
            <!--              </ValidationProvider>-->
          </div>
          <div class="form-group col-md-6 col-sm-6 col-xs-12"
               v-if="!autocomplete_address">
            <!--                                            <div class="field-label">State / County</div>-->
            <!--              <ValidationProvider rules="required" v-slot="{ errors }" name="State">-->

            <div class="field-label">都道府県</div>
            <input type="text" v-model="shipping_address.state" name="State"
                   :placeholder="$t('checkout.state')"/>
            <!--              </ValidationProvider>-->
          </div>

          <div class="form-group col-md-6 col-sm-6 col-xs-12"
               v-if="!autocomplete_address">
            <!--                                            <div class="field-label">City</div>-->
            <!--              <ValidationProvider rules="required" v-slot="{ errors }" name="City">-->

            <div class="field-label">市</div>
            <input type="text" v-model="shipping_address.city" name="City"
                   :placeholder="$t('checkout.city')"/>
            <!--              </ValidationProvider>-->
          </div>

          <div class="form-group col-md-6 col-sm-6 col-xs-12"
               v-if="!autocomplete_address">
            <div class="field-label">町</div>
            <!--              <ValidationProvider rules="required" v-slot="{ errors }" name="Town">-->
            <input type="text" v-model="shipping_address.town" name="Town"
                   :placeholder="$t('checkout.town')"/>
            <!--              </ValidationProvider>-->
          </div>

          <div class="form-group col-12" v-if="autocomplete_address">
            <div class="field-label">都道府県市町村</div>
            <p>{{ shipping_address.state }}{{ shipping_address.city }}{{ shipping_address.town }}</p>
          </div>

          <div class="form-group col-md-12 col-sm-12 col-xs-12">
            <div class="field-label">住所 1</div>
            <!--              <ValidationProvider rules="required" v-slot="{ errors }" name="Address_1">-->
            <input type="text" v-model="shipping_address.address_1" name="Address_1"
                   :placeholder="$t('checkout.address_1')"/>
            <!--              </ValidationProvider>-->
          </div>
          <div class="form-group col-md-12 col-sm-12 col-xs-12">
            <div class="field-label"></div>
            <!--              <ValidationProvider v-slot="{ errors }" name="Address_2">-->
            <div class="field-label">住所 2</div>
            <input type="text" v-model="shipping_address.address_2" name="Address_2"
                   :placeholder="$t('checkout.address_2')"/>
            <!--              </ValidationProvider>-->
          </div>
        </div>
        <!--        </ValidationObserver>-->
      </div>
      <div class="row">
        <div class="col-12 d-flex justify-content-between">
          <button class='btn btn-solid black-btn' @click="$emit('closeModal')">
            {{ $t('buttons.close') }}
          </button>
          <button class='btn btn-solid pull-right' @click="onSubmit">{{ $t('buttons.submit') }}
          </button>
        </div>
      </div>
    </div>
  </b-modal>
</template>
<script>
import {swalService} from "~/helpers/swal.service"
import {ValidationProvider, ValidationObserver} from 'vee-validate/dist/vee-validate.full.esm'
import {axios} from "@/plugins/axios"
import {mapGetters} from "vuex"

export default {
  name: "shippingAddressModal",
  props: ["showModal"],
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  computed: {
    ...mapGetters({
      ME: 'authfack/ME',
    }),
  },
  data: function () {
    return {
      shipping_address: {
        user: 0,
        name: "",
        phone: '',
        postcode: "",
        email: "",
        state: "",
        city: "",
        town: "",
        address_1: "",
        address_2: ""
      },
      autocomplete_address: false,
      auto_searching: false,
      invalid: true,
      errors: [],
    };
  },
  watch: {
    showModal(newval, oldval) {
      // this.load_shippingaddress();
    }
  },
  mounted() {
    // this.load_shippingaddress()
  },
  methods: {
    // load_shippingaddress() {
    //   let vm = this;
    //   let url = `/back/store/api/shippingadress/get_user_shippingaddress/`
    //   axios.$post(url).then((res) => {
    //     if (res.result && res.data.shipping_address) {
    //       vm.shipping_address = res.data.shipping_address
    //     }
    //   })
    // },
    precheck() {
      if (this.shipping_address.name === "") {
        this.errors.push("受取人が必要です。")
      }
      if (this.shipping_address.phone === "") {
        this.errors.push("連絡用電話が必要です。")
      }
      if (this.shipping_address.postcode === "") {
        this.errors.push("郵便番号が必要です。")
      }
      if (this.shipping_address.state === "") {
        this.errors.push("都道府県が必要です。")
      }
      if (this.shipping_address.town === "") {
        this.errors.push("町が必要です。")
      }
      if (this.shipping_address.city === "") {
        this.errors.push("市が必要です。")
      }
      if (this.shipping_address.address_1 === "") {
        this.errors.push("住所 1が必要です。")
      }
      return this.errors.length === 0;
    },
    onSubmit() {
      var vm = this;
      if (this.precheck()) {
        vm.shipping_address.user = this.ME.profile.user_id;

        this.$store.dispatch("addressbook/add_address", vm.shipping_address)
          .then(shipping_address => {
            console.log("address ?")
            if (shipping_address.id>0) {
              console.log("address added",shipping_address)
              swalService.showToast("success", "住所更新いたしました!");
              vm.$emit("closeModal", shipping_address)
            }
          }).catch(err => {
          console.error(err);
        })
      }
    },
    autocomplete_postcode() {
      if (this.shipping_address.postcode.length > 4) {
        var vm = this;
        this.auto_searching = true;

        var url = "https://api.anko.education/zipcode?zipcode=" + this.shipping_address.postcode;
        fetch(url)
          .then(function (response) {
            if (response.ok) {
              return response.json();
            }
          })
          .then(function (address) {
            if (address !== undefined) {
              vm.autocomplete_address = true;
              vm.shipping_address.state = address.pref;
              vm.shipping_address.city = address.city;
              vm.shipping_address.town = address.area;
            }
          }).catch((error) => {
          console.error('Error:', error);
          vm.autocomplete_address = false;
        });
        this.auto_searching = false;
      }
    },
  }
};
</script>

