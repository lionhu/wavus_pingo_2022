<template>
  <div>
    <Header/>
    <Breadcrumbs :title="$t('checkout.title')"/>
    <section class="section-b-space">
      <div class="container">
        <div class="checkout-page">
          <div class="row">
            <div class="col-lg-6 col-xs-12" v-if="neworder.id === 0">
              <div class="checkout-form">
                <div class="checkout-title">
                  <h3>{{ $t('checkout.shippingadress') }}
                    <a href="javascript:void(0);" v-b-modal:modal_shippingaddress class="btn btn-warning"
                       @click="showShippingAddress">
                      <i class="ti-pencil mr-2"></i>{{ $t('addressbook.address.register') }}
                    </a>
                    <a href="javascript:void(0);" v-b-modal:modal_addressbook class="btn btn-warning"
                       @click="showAddressBook">
                      <i class="ti-book mr-2"></i>{{ $t('addressbook.address.title') }}
                    </a>
                  </h3>
                </div>
                <div class="footer-theme partition-f">
                  <div class="sub-title">
                    <div class="footer-contant">
                      <ul class="contact-list" v-if="user.name!==''">
                        <li><i class="fa fa-user"></i>{{ user.name }}</li>
                        <li><i class="fa fa-map-marker"></i>
                          〒{{ user.postcode }} {{ user.state }}{{ user.city }} <br>
                          {{ user.town }}{{ user.address_1 }} <br>
                          {{ user.address_2 }}
                        </li>
                        <li><i class="fa fa-phone"></i>TEL: {{ user.phone }}
                        </li>
                        <li><i class="fa fa-envelope-o"></i>Email:
                          <a href="#">{{ user.email }}</a></li>
                      </ul>
                    </div>
                  </div>
                </div>
                <ul class="address_errors">
                  <li v-for="error in address_errors" class="text-danger">* {{ error }}</li>
                </ul>
              </div>

            </div>
            <div class="col-lg-6 col-xs-12" v-if="cart!==null">
              <div class="checkout-details">
                <div class="order-box">
                  <div class="title-box">
                    <div class="col-12 footer-theme partition-f"
                         v-if="neworder.id">
                      <div class="sub-title">
                        <div class="footer-title"><h4>送付先：</h4></div>
                        <div class="footer-contant">
                          <ul class="contact-list" v-if="user.name!==''">
                            <li><i class="fa fa-user"></i>{{ user.name }}</li>
                            <li><i class="fa fa-map-marker"></i>
                              〒{{ user.postcode }} {{ user.state }}{{ user.city }} <br>
                              {{ user.town }}{{ user.address_1 }} <br>
                              {{ user.address_2 }}
                            </li>
                            <li><i class="fa fa-phone"></i>TEL: {{ user.phone }}
                            </li>
                            <li><i class="fa fa-envelope-o"></i>Email:
                              <a href="#">{{ user.email }}</a></li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="order-box">
                  <div class="title-box">
                    <div>
                      {{ $t('cart_info.product') }}
                      <span>{{ $t('cart_info.total') }}</span>
                    </div>
                  </div>
                  <div class="qty">
                    <div class="mt-3 d-flex justify-content-between align-items-center">
                      <img :src="cart.product.image_url" class="thumbnail" alt="">
                      <div>
                        {{ cart.product.item_name }} <br>
                        X {{ cart.quantity }}
                      </div>
                      <div class="text-right">
                        {{ cartTotal   | currency("¥") }}<br>
                        <span v-if="valid_cartitem_user_self_bonus && POLICIES.USER_SELF">
                            <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                            {{ cart.product.point_rule.policies.user_self * cart.quantity | currency("¥") }}
                          </span>
                      </div>
                    </div>
                    <div class="my-4">
                      <div class="qty-box">
                        <div class="input-group">
                            <span class="input-group-prepend">
                              <button type="button" class="btn quantity-left-minus"
                                      data-type="minus" data-field @click="decrement">
                                <i class="ti-angle-left"></i>
                              </button>
                            </span>
                          <input type="text" name="quantity" class="form-control input-number"
                                 v-model="cart.quantity" :disabled="true"/>
                          <span class="input-group-prepend">
                              <button type="button" class="btn quantity-right-plus"
                                      data-type="plus" data-field @click="increment">
                                <i class="ti-angle-right"></i>
                              </button>
                            </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <ul class="sub-total">
                    <li>
                      {{ $t('cart_info.total') }}
                      <span class="count text-right">{{ cartTotal | currency("¥") }}</span>
                    </li>
<!--                    <li v-if="POLICIES.USER_SELF && !point_usage.apply_point">-->
<!--                      <hr>-->
<!--                      {{ $t('cart_info.get_bonus') }}-->
<!--                      <span class="count text-right text-danger">-->
<!--                            <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>-->
<!--                          {{ cart_user_self_bonus  | currency("¥") }}-->
<!--                        </span>-->
<!--                    </li>-->
                  </ul>
                  <div class="sub-total">

                    <form class="theme-form">
                      <div class="form-row">
                        <div class="col-md-12">
                          <label for="message">{{ $t('contact.message') }}</label>
                          <textarea
                            class="form-control"
                            placeholder="Write Your Message"
                            id="message"
                            v-model="message"
                            name="message"
                            rows="3"
                          ></textarea>
                        </div>
                      </div>
                    </form>
                  </div>
                  <UsePoint @usepoint="Order_UsePoint" :cartTotal="cartTotal"/>
                </div>
                <div class="payment-box">
                  <div class="payment-card-bottom">
                    <ul>
                      <li><a href="#"><img src="/images/icon/visa.png" alt=""></a></li>
                      <li><a href="#"><img src="/images/icon/mastercard.png" alt=""></a></li>
                      <li><a href="#"><img src="/images/icon/american-express.png" alt=""></a></li>
                      <li><a href="#"><img src="/images/icon/jcb.png" alt=""></a></li>
                    </ul>
                  </div>
                  <a href="javascript:void(0);" class='btn-solid btn pull-right'
                     v-b-modal.modal-payment @click="ShowModalPayment">
                    {{ $t("checkout.credit_card") }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <ShippingAddressModal @closeModal="closeShippingAddressModal" :showModal="showShippingAddressModal"/>
      <AddressBookModal @closeModal="closeAddressBookModal" @AddressSelected="AddressSelected"
                        :showModal="showAddressBookModal"/>

      <modalPayment :openPaymentModal="showPaymentModal" :message="message"
                    @closeModal="closeModalPayment"></modalPayment>
    </section>
    <Footer/>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'
import {swalService} from "@/helpers/swal.service"
import Swal from "sweetalert2"


export default {
  name: "pingo_checkout",
  middleware: ['authenticated', "isNotEmptyPingoCart"],
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    UsePoint: () => import("~/components/widgets/use_point"),
    ShippingAddressModal: () => import("~/components/widgets/modalShippingAddress"),
    AddressBookModal: () => import("~/components/widgets/modalAddressBook.vue"),
    modalPayment: () => import('../components/modalPayment'),
  },
  computed: {
    ...mapGetters({
      cart: 'pingoproducts/getterCart',
      POLICIES: 'authfack/policies',
    }),
    cartTotal() {
      return this.cart.product.discount_price * this.cart.quantity
    },
    pay_by_credit() {
      return !!(this.cartTotal - this.point_usage.use_point)
    },
    cart_user_self_valid() {
      return !this.point_usage.apply_point;
    },
    cart_user_self_bonus() {
      if (!this.cart.product.point_rule.is_valid) return 0;
      return parseInt(this.cart.product.point_rule.policies.user_self) * this.cart.quantity
    },
    valid_cartitem_user_self_bonus() {
      if (this.point_usage.apply_point || !this.cart.product.point_rule.is_valid) {
        return false;
      }
      return parseInt(this.cart.product.point_rule.policies.user_self) > 0;
    },
  },
  data() {
    return {
      user: {
        id: 0,
        name: '',
        phone: '',
        email: '',
        postcode: '',
        address_1: '',
        address_2: '',
        state: '',
        city: '',
        town: '',
      },
      address_errors: [],
      point_usage: {
        apply_point: false,
        use_point: 0
      },
      message: "",
      checkout: false,
      errors: [],
      payment: "credit",
      autocomplete_address: false,
      neworder: {
        id: 0,
        slug: "",
        Qty: 0,
        Total: 0
      },
      invalid: true,
      showPaymentModal: false,
      showPointPaymentModal: false,
      flagPayLater: false,
      showShippingAddressModal: false,
      showAddressBookModal:false,
      edit_user_id: 0,
      order_detail: {}
    }
  },
  mounted() {
    this.$store.dispatch("authfack/refresh_pointBalance");
    this.$store.dispatch("addressbook/load_address_list")
  },
  methods: {
    precheck_address() {
      this.address_errors = [];
      if (this.user.name === "") {
        this.address_errors.push("受取人の名前が必要です。")
      }
      if (this.user.phone === "") {
        this.address_errors.push("連絡電話が必要です。")
      }
      if (this.user.email === "") {
        this.address_errors.push("連絡用メールアドレスが必要です。")
      }
      if (this.user.postcode === "") {
        this.address_errors.push("郵便番号が必要です。")
      }
      if (this.user.state === "") {
        this.address_errors.push("都道府県の情報が必要です。")
      }
      if (this.user.city === "") {
        this.address_errors.push("市の情報がが必要です。")
      }
      if (this.user.town === "") {
        this.address_errors.push("市町村情報が必要です。")
      }
      if (this.user.address_1 === "") {
        this.address_errors.push("住所が必要です。")
      }
      return this.address_errors.length === 0;
    },
    closeShippingAddressModal(address) {
      if (address) {
        this.user = address;
        this.$store.commit("addressbook/setOrderAddress",address)
      }
      this.address_errors = [];
      this.showShippingAddressModal = false;
    },
    showShippingAddress() {
      // this.place_order();
      this.showShippingAddressModal = true;
      this.edit_user_id = this.user;
    },
    increment() {
      let quantity = this.cart.quantity;
      this.$store.commit('pingoproducts/setCartQuantity', quantity + 1)
    },
    decrement() {
      let quantity = this.cart.quantity;
      if (quantity >= 2) {
        this.$store.commit('pingoproducts/setCartQuantity', quantity - 1)
      }
    },
    PayOrderByPoint() {
      let vm = this;
      if (this.precheck_address()) {
        let url = "/back/store/api/pingo_orders/create_byPoint/"

        console.log(this.order_detail)
        // this.$axios.$post(url, this.order_detail)
        //   .then(response => {
        //     if (response.result) {
        //       swalService.showModal("Success!", "Order Completed", "success")
        //       vm.$store.commit("authfack/update_pointbank_balance", response.pointbank_balance);
        //       vm.$store.dispatch("pingoproducts/empty_cart");
        //       vm.$router.push("/tomobuy")
        //     } else {
        //       swalService.showModal("Oops!", "Order Failed", "error")
        //     }
        //   })
      } else {
        Swal.fire({
          title: 'Error!',
          text: '送付先の情報は必須です。ご入力してください！',
          icon: 'error'
        })
      }
    },
    place_order() {
      if (this.precheck_address()) {
        let chargeAmount = this.cartTotal
        if (this.point_usage.apply_point) {
          chargeAmount = this.cartTotal - this.point_usage.use_point;
          this.showalert_pointusage()
        }
        this.order_detail = {
          type: "PINGO",
          product_id: this.cart.product.id,
          json_product: this.cart.product,
          message: this.message,
          chargeAmount: chargeAmount,
          price: this.cart.product.discount_price,
          quantity: this.cart.quantity,
          total: this.cartTotal,
          point_usage: this.point_usage,
          json_shippingaddress: this.user,
        };
        return true;
      } else {
        Swal.fire({
          title: 'Error!',
          text: '送付先の情報は必須です。ご入力してください！',
          icon: 'error'
        })
        return false;
      }
    },
    showalert_pointusage() {
      Swal.fire({
        icon: "warning",
        html: 'ポイントをご利用した場合、購入ポイントの付与はご対応致しません。<br> ご了承ください。',
        showCancelButton: true,
        confirmButtonText: '了解'
      }).then((result) => {
        return !!result.isConfirmed;
      })
    },
    ShowModalPayment() {
      if (this.place_order()) {
        this.showPaymentModal = true;
      }
    },
    showAddressBook() {
      this.showAddressBookModal = true;
    },
    AddressSelected(address) {
      if (address.id) {
        console.log("selected assress", address)
        this.user = address;
        this.$store.commit("addressbook/setOrderAddress",address)
        this.showAddressBookModal = false;
      }
    },
    closeAddressBookModal() {
      this.showAddressBookModal = false;
    },
    closeModalPayment() {
      this.showPaymentModal = false;
      this.$router.push("/account")
    },
    closeModalPointPayment() {
      this.showPointPaymentModal = false;
      this.$router.push("/account")
    },
    Order_UsePoint(point_usage) {
      let vm = this;
      if (point_usage > 0) {
        this.point_usage.apply_point = point_usage;
        this.point_usage.apply_point = true;
        Swal.fire({
          icon: "warning",
          html: 'ポイントをご利用した場合、購入ポイントの付与はご対応致しません。<br> ご了承ください。',
          showCancelButton: true,
          confirmButtonText: '了解'
        }).then((result) => {
          if (result.isConfirmed) {
            vm.order_detail = {
              payment_methos: "POINT",
              product_id: vm.cart.product.id,
              variant_id: vm.cart.product.id,
              json_product: vm.cart.product,
              quantity: parseInt(vm.cart.quantity),
              message: vm.message,
              json_shippingaddress: vm.user,
              point_usage: {"use_point": point_usage, "apply_point": true},
              chargeAmount: 0,
              price:vm.cart.product.discount_price,
              total:point_usage,
            };
            vm.PayOrderByPoint();
          }
          // return !!result.isConfirmed;
        })
      }
    },
  }
}
</script>
<style>
ul.address_errors li {
  display: block !important;
}
</style>
