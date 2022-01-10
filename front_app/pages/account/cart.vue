<template>
  <div>
    <Header/>
    <Breadcrumbs title="カート" breadcrumb_type="static"/>
    <section class="cart-section section-b-space">
      <div class="container">
        <div class="row">
          <div class="col-sm-12">
            <table class="table cart-table table-responsive-xs" v-if="cart.length">
              <thead>
              <tr class="table-head">
                <th scope="col">{{ $t('productname') }}</th>
              </tr>
              </thead>
              <tbody v-for="(item,index) in cart" :key="index">
              <tr>
                <td>
                  <img :src="item.variant.thumbimage_url" style="width: 160px;"/>
                  <div>{{ item.product.item_name }} <br> {{ item.variant.name }}</div>
                  <div class="mobile-cart-content row">
                    <div class="col-xs-3">
                      <div class="qty-box">
                        <div class="input-group">
                                                    <span class="input-group-prepend">
                                                      <button type="button" class="btn quantity-left-minus"
                                                              data-type="minus" data-field
                                                              @click="decrement(item)">
                                                        <i class="ti-angle-left"></i>
                                                      </button>
                                                    </span>
                          <input type="text" name="quantity" class="form-control input-number"
                                 v-model="item.quantity"/>
                          <span class="input-group-prepend">
                                                      <button type="button" class="btn quantity-right-plus"
                                                              data-type="plus" data-field
                                                              @click="increment(item)">
                                                        <i class="ti-angle-right"></i>
                                                      </button>
                                                    </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="mobile-cart-content row">
                    <div class="col-xs-3">
                      <h2 class="td-color">{{ item.variant.price | currency("¥") }}</h2>
                    </div>
                  </div>
                  <div class="mobile-cart-content row">
                    <div class="col-xs-3">
                      <h2 class="td-color">
                        <a class="icon" @click="removeCartItem(item)">
                          <i class="ti-close"></i>
                        </a>
                      </h2>
                    </div>
                  </div>
                </td>
                <td>
                  <h2>{{ item.variant.price | currency("¥") }}</h2>
                </td>
                <td>
                  <div class="qty-box">
                    <div class="input-group">
                                            <span class="input-group-prepend">
                                              <button type="button" class="btn quantity-left-minus" data-type="minus"
                                                      data-field
                                                      @click="decrement(item)">
                                                <i class="ti-angle-left"></i>
                                              </button>
                                            </span>
                      <input type="text" name="quantity" class="form-control input-number"
                             v-model="item.quantity"/>
                      <span class="input-group-prepend">
                                              <button type="button" class="btn quantity-right-plus" data-type="plus"
                                                      data-field
                                                      @click="increment(item)">
                                                <i class="ti-angle-right"></i>
                                              </button>
                                            </span>
                    </div>
                  </div>
                </td>
                <td>
                  <a href="javascript:void(0);" class="icon" @click="removeCartItem(item)">
                    <i class="ti-close"></i>
                  </a>
                </td>
                <td>
                  <h2 class="td-color">{{ item.variant.price * item.quantity | currency("¥") }}</h2>
                </td>
              </tr>
              </tbody>
            </table>
            <table class="table cart-table table-responsive-md" v-if="cart.length">
              <tfoot>
              <tr>
                <td>{{ $t('cart_info.total') }}:</td>
                <td>
                  <h2>{{ cartTotal | currency("¥") }}</h2>
                </td>
              </tr>
              </tfoot>
            </table>
            <div class="col-sm-12 empty-cart-cls text-center" v-if="!cart.length">
              <img src='/images/icon-empty-cart.png' style="max-width:256px;" class="img-fluid" alt="empty cart"/>
              <h3 class="mt-3" v-if="!$device.isMobile">
                <strong>お客様のカートに商品はありません。</strong>
              </h3>
              <h4 class="text-muted" v-else>
                <strong>お客様のカートに商品はありません。</strong>
              </h4>
              <div class="col-12">
                <nuxt-link :to="{ path: '/'}" class="btn btn-solid">{{ $t('continue_shopping') }}
                </nuxt-link>
              </div>
            </div>
          </div>
        </div>
        <div class="row cart-buttons" v-if="cart.length">
          <div class="col-6">
            <nuxt-link :to="{ path: '/'}" :class="'btn btn-solid'">{{ $t('continue_shopping') }}</nuxt-link>
          </div>
          <div class="col-6">
            <nuxt-link :to="{ path: '/account/checkout'}" :class="'btn btn-solid'">
              {{ $t('cart_info.checkout') }}
            </nuxt-link>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'
import Header from '~/components/header/header1'
import Footer from '~/components/footer/footer1'
import Breadcrumbs from '~/components/widgets/breadcrumbs'

export default {
  middleware: 'authenticated',
  data() {
    return {
      counter: 1
    }
  },
  components: {
    Header,
    Footer,
    Breadcrumbs
  },
  computed: {
    ...mapGetters({
      cart: 'cart/cartItems',
      cartTotal: 'cart/cartTotalAmount',
      back_server: 'system/getterBackServer',
    })
  },
  methods: {
    removeCartItem: function (item) {
      this.$store.dispatch('cart/removeCartItem', item)
    },
    increment(item, qty = 1) {
      this.$store.dispatch('cart/updateCartQuantity', {
        item: item,
        qty: qty
      })
    },
    decrement(item, qty = -1) {
      this.$store.dispatch('cart/updateCartQuantity', {
        item: item,
        qty: qty
      })
    }
  }
}
</script>
