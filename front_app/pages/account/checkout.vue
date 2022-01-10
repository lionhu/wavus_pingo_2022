<template>
  <div>
    <Header/>
    <Breadcrumbs :title="$t('checkout.title')"/>
    <section class="section-b-space">
      <div class="container">
        <div class="checkout-page">
          <div class="row">
            <div class="col-lg-6 col-xs-12" v-if="neworder.id === 0 && cart.length">
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
                  <div class="sub-title" v-if="user.name!==''">
                    <div class="footer-contant">
                      <ul class="contact-list">
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
                  <div class="theme-color" v-else>
                    {{ $t("addressbook.buttons.need_address") }}
                  </div>
                </div>
                <ul class="address_errors">
                  <li v-for="error in address_errors" class="text-danger">* {{ error }}</li>
                </ul>
              </div>

            </div>
            <div class="col-lg-6 col-xs-12">
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
                <div class="order-box" v-if="cart.length">
                  <div class="title-box">
                    <div>
                      {{ $t('cart_info.product') }}
                      <span>{{ $t('cart_info.total') }}</span>
                    </div>
                  </div>
                  <div class="qty">
                    <div v-for="(item,index) in cart" :key="index"
                         class="mt-3 d-flex justify-content-between align-items-center">
                      <img :src="item.variant.thumbimage_url" class="thumbnail" alt="">
                      <div>
                        {{ item.product.item_name }} <br>
                        ({{ item.variant.name }}) X {{ item.quantity }}
                      </div>
                      <div class="text-right">
                        {{ item.variant.price * item.quantity   | currency("¥") }}<br>
                        <span v-if="valid_cartitem_user_self_bonus(item) && policies.USER_SELF">
                            <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                            {{ item.variant.point_rule.policies.user_self * item.quantity | currency("¥") }}
                          </span>
                      </div>
                    </div>
                  </div>
                  <ul class="sub-total">
                    <li>
                      {{ $t('cart_info.total') }}
                      <span class="count text-right">{{
                          cartTotal - point_usage.use_point  | currency("¥")
                        }}</span>
                    </li>
                    <li v-if="policies.USER_SELF && !point_usage.apply_point">
                      <hr>
                      {{ $t('cart_info.get_bonus') }}
                      <span class="count text-right text-danger">
                            <font-awesome-icon :icon="['fas','donate']" class="text-warning mr-2"></font-awesome-icon>
                          {{ cart_user_self_bonus  | currency("¥") }}
                        </span>
                    </li>
                  </ul>
                  <div class="sub-total" v-if="user.name!==''">

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

                  <UsePoint @usepoint="Order_UsePoint($event)" :cartTotal="cartTotal"/>
                </div>
                <div class="payment-box" v-if="user.name!==''">
                  <div class="payment-card-bottom">
                    <ul>
                      <li><img src="/images/icon/visa.png" alt=""></li>
                      <li><img src="/images/icon/mastercard.png" alt=""></li>
                      <li><img src="/images/icon/american-express.png" alt=""></li>
                      <li><img src="/images/icon/jcb.png" alt=""></li>
                    </ul>
                  </div>
                  <a href="javascript:void(0);" class='btn-solid btn pull-right'
                     v-b-modal.modal-payment @click="ShowModalPayment" v-if="pay_by_credit">
                    {{ $t("checkout.credit_card") }}
                  </a>
                  <a href="javascript:void(0);" class='btn-solid btn pull-right' @click="place_order"
                     v-if="!pay_by_credit">
                    お支払い
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

      <modalPayment :openPaymentModal="showPaymentModal" :order_detail="order_detail"
                    @closeModal="closeModalPayment"></modalPayment>
    </section>
    <Footer/>
  </div>
</template>
<script>
import {mapGetters, mapState} from 'vuex'
import {swalService} from "@/helpers/swal.service"
import Swal from "sweetalert2"


export default {
  name: "checkout",
  middleware: ['authenticated', "isNotEmptyCart"],
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    UsePoint: () => import("~/components/widgets/use_point"),
    ShippingAddressModal: () => import("~/components/widgets/modalShippingAddress"),
    AddressBookModal: () => import("~/components/widgets/modalAddressBook"),
    modalPayment: () => import('~/components/widgets/modalPayment'),
  },
  computed: {
    ...mapGetters({
      cart: 'cart/cartItems',
      cartTotal: 'cart/cartTotalAmount',
      cartQty: 'cart/cartQty',
      profile: 'authfack/profile_info',
      back_server: "system/getterBackServer",
      policies: 'authfack/policies',
    }),
    // ...mapState({
    //   address: state => state.authfack.user.address
    // }),
    pay_by_credit() {
      return this.cartTotal - this.point_usage.use_point ? true : false
    },
    cart_user_self_valid() {
      return !this.point_usage.apply_point;
    },
    cart_user_self_bonus() {
      if (!this.cart_user_self_valid) {
        return 0
      }
      let total_bonus = this.cart.reduce((bonus, cartitem) => {
        let current_self_bonus = cartitem.variant.point_rule.is_valid ? parseInt(cartitem.variant.point_rule.policies.user_self) * cartitem.quantity : 0;

        return bonus + current_self_bonus;
      }, 0)
      return total_bonus;
    }
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
      button_style: {
        label: 'checkout',
        size: 'medium', // small | medium | large | responsive
        shape: 'pill', // pill | rect
        color: 'blue' // gold | blue | silver | black
      },
      errors: [],
      payment: "credit",
      autocomplete_address: false,
      neworder: {
        id: 0,
        slug: "",
        Qty: 0,
        Total: 0
      },
      quickviewproduct: {
        price: 100
      },
      invalid: true,
      showPaymentModal: false,
      showPointPaymentModal: false,
      flagPayLater: false,
      showShippingAddressModal: false,
      edit_user_id: 0,
      order_detail: {},
      showAddressBookModal: false
    }
  },
  mounted() {
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
      }
      this.address_errors = [];
      this.showShippingAddressModal = false;
    },
    showShippingAddress() {
      // this.place_order();
      this.showShippingAddressModal = true;
      this.edit_user_id = this.user;
    },
    showAddressBook() {
      this.showAddressBookModal = true;
    },
    closeAddressBookModal() {
      this.showAddressBookModal = false;
    },
    AddressSelected(address) {
      if (address.id) {
        console.log("selected assress", address)
        this.user = address;
        this.showAddressBookModal = false;
      }
    },
    valid_cartitem_user_self_bonus(cartitem) {
      if (this.point_usage.apply_point || !cartitem.variant.point_rule.is_valid) {
        return false;
      }
      return cartitem.variant.point_rule.policies.user_self > 0;
    },
    place_order() {
      let vm = this;
      if (this.precheck_address()) {
        let chargeAmount = this.cartTotal
        if (this.point_usage.apply_point) {
          chargeAmount = this.cartTotal - this.point_usage.use_point;
          Swal.fire({
            icon: "warning",
            html: 'ポイントをご利用した場合、購入ポイントの付与はご対応致しません。<br> ご了承ください。',
            showCancelButton: true,
            confirmButtonText: '了解',
            allowOutsideClick: () => !Swal.isLoading()
          }).then((result) => {
            console.log("confirm result", !!result.isConfirmed)
            if (result.isConfirmed) {
              let order_detail = {
                json_shippingaddress: vm.user,
                cart_items: vm.cart,
                Total: vm.cartTotal,
                Qty: vm.cartQty,
                chargeAmount: chargeAmount,
                point_usage: vm.point_usage,
                message: vm.message,
                order_bonus: {
                  self_order_bonus_valid: vm.cart_user_self_valid,
                  self_order_bonus_point: vm.cart_user_self_bonus
                }
              };
              vm.order_detail = order_detail;
              this.$store.dispatch("orders/placeOrder", order_detail)
                .then(response => {
                  if (response.result) {
                    Swal.fire({
                      icon: 'success',
                      title: '支払い完了',
                      html: '注文の支払いは完了いたしました。<br> ありがとうございました！',
                      footer: `ポイント残高：${response.data.pointbank_balance}`
                    }).then((result) => {
                      if (result.isConfirmed) {
                        vm.$store.dispatch("cart/empty_cart");
                        vm.$router.push("/sharebuy")
                      }
                    })
                  } else {
                    swalService.showModal("Oops!", "Order Failed", "error")
                  }
                })
            } else {
              return false;
            }
          })
        }
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
        confirmButtonText: '了解',
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        console.log("showalert_pointusage", result.isConfirmed)
        return !!result.isConfirmed;
      })
    },
    ShowModalPayment() {
      if (this.precheck_address()) {
        var chargeAmount = this.cartTotal
        if (this.point_usage.apply_point) {
          chargeAmount = this.cartTotal - this.point_usage.use_point;
          this.showalert_pointusage()
        }
        if (chargeAmount < 100) {
          Swal.fire({
            icon: 'warning',
            title: 'カード決済金額の確認',
            html: 'カード決済金額は100円以上が必要です。<br> 再確認ください',
            footer: `カード決済金額：${chargeAmount}`
          })
        } else {
          var order_detail = {
            json_shippingaddress: this.user,
            cart_items: this.cart,
            Total: this.cartTotal,
            Qty: this.cartQty,
            chargeAmount: chargeAmount,
            point_usage: this.point_usage,
            message: this.message,
            order_bonus: {
              self_order_bonus_valid: this.cart_user_self_valid,
              self_order_bonus_point: this.cart_user_self_bonus
            }
          };
          this.order_detail = order_detail;
          this.showPaymentModal = true;
        }
      }
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
      this.point_usage = point_usage;
    },
  }
}
</script>
<style>
ul.address_errors li {
  display: block !important;
}
</style>
