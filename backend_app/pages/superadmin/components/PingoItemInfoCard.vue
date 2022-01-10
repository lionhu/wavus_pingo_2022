<script>
import {mapGetters} from 'vuex'
import Swal from "sweetalert2"

export default {
  name: "pingoitem_info_card",
  props: ["pingo_product", "multipleSelection"],
  components: {},
  data() {
    return {}
  },
  mounted() {
  },
  computed: {
    ...mapGetters({}),
    progress_ratio() {
      if(this.pingo_product.currentNum===0 || this.pingo_product.targetNum===0 ) return 0;
      return parseInt(this.pingo_product.currentNum / this.pingo_product.targetNum * 100)
    },
    PurchasePrice() {
      return  this.pingo_product.purchase_price
    },
    SellPrice() {
      return  this.pingo_product.discount_price
    },
  },
  methods: {
    async DeleteOrders() {
      let vm = this;
      if (this.multipleSelection.length) {
        await Swal.fire({
          title: '本当に削除しますか?',
          icon: "warning",
          html: "削除してしまうと、戻せないので、再確認ください！",
          showCancelButton: true,
          confirmButtonText: '削除',
          showLoaderOnConfirm: true,
          preConfirm: (login) => {
            return this.$store.dispatch("pingoproducts/superadmin_remove_product_orders", this.multipleSelection)
              .then((response) => {
                if (!response) {
                  throw new Error("Failed to remove orders")
                }
                return response;
              }).catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          },
          allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
          if (result.isConfirmed) {
            vm.$emit("DeleteOrders", this.multipleSelection)
          }
        })
      } else {
        Swal.fire({
          title: "Ooops!",
          html: "削除対象を選択してください！",
          icon: "error"
        })
      }
    },
    EstablishOrders() {
      let vm = this;
      Swal.fire({
        title: '本当に成立させますか?',
        icon: "warning",
        html: "成立してしまうと、戻せないので、再確認ください！",
        showCancelButton: true,
        confirmButtonText: `成立させます`,
        showLoaderOnConfirm: true,
        preConfirm: (login) => {
          return vm.$store.dispatch("pingoproducts/superadmin_establish_orders", this.pingo_product.id)
            .then((response) => {
              // if (!response) {
              //   throw new Error("Failed to remove orders")
              // }
              return response;
            }).catch(error => {
              Swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        if (result.isConfirmed) {
          vm.$emit("EstablishOrders", result.value)
        }
      })
    },
    ReleaseOrders() {
      let vm = this;
      Swal.fire({
        title: '本当に募集失敗にしますか?',
        icon: "warning",
        html: "募集失敗にしてしまうと、戻せないので、再確認ください！",
        showCancelButton: true,
        confirmButtonText: `募集失敗にします`,
        showLoaderOnConfirm: true,
        preConfirm: (login) => {
          return vm.$store.dispatch("pingoproducts/superadmin_release_orders", this.pingo_product.id)
            .then((response) => {
              return response;
            }).catch(error => {
              Swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        if (result.isConfirmed) {
          vm.$emit("ReleaseOrders", result.value)
        }
      })
    },
  }
}
</script>

<template>
  <div class="card">
    <div class="card-body">
      <div class="row">
        <div class="col-lg-5">
          <div class="row justify-content-center">
            <div class="col-xl-8">
              <div id="product-carousel" class="carousel slide product-detail-carousel" data-ride="carousel">
                <div class="carousel-inner">
                  <div class="carousel-item active">
                    <img :src="pingo_product.image_url" alt="product-img" id="myImage" class="img-fluid"/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-7">
          <div>
            <h4 class="mb-1">
              {{ pingo_product.item_name }}
              <b-badge pill class="float-right" :variant="$t(`pingo_order.type.${pingo_product.status}.class`)">
                {{$t(`pingo_order.type.${pingo_product.status}.text`)}}
              </b-badge>
            </h4>

            <div class="mt-3">
              <h6 class="text-danger text-uppercase">仕入価格：{{ pingo_product.purchase_price | currency("¥") }}</h6>
              <h6 class="text-danger text-uppercase">通常価格：{{ pingo_product.price | currency("¥") }}</h6>
              <h4>
                販売価格 :<b>{{ pingo_product.discount_price| currency("¥") }}</b>
              </h4>
            </div>
            <hr/>

            <div>
              <div class="mt-3">
                <h5 class="font-size-14">トモ買イベント詳細 :</h5>
                <div class="row">
                  <div class="col-md-12">
                    <ul class="list-unstyled product-desc-list">
                      <li>
                        <span class="list_title">目標売上:</span>
                        {{ pingo_product.targetNum * SellPrice |currency("¥") }}
                      </li>
                      <li>
                        <span class="list_title">目標販売数量:</span>
                        {{ pingo_product.targetNum |currency("") }}
                      </li>
                      <li>
                        <span class="list_title">現在販売数量:</span>
                        {{ pingo_product.currentNum |currency("") }}
                      </li>
                      <li>
                        <span class="list_title">締切日:</span>
                        {{ pingo_product.until_at | short_datetime }}
                      </li>
                      <li>
                        <span class="list_title">{{ progress_ratio }}%</span>
                        <div class="progress progress-sm">
                          <div class="progress-bar bg-success" role="progressbar"
                               :style="`width: ${progress_ratio}%`" :aria-valuenow="progress_ratio"
                               aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div class="d-flex justify-content-between" v-if="pingo_product.status ==='RECRUITING'">
              <button type="button" class="btn btn-success waves-effect waves-light" @click="EstablishOrders">
                <span class="btn-label"><i class="ri-chat-check-fill"></i></span>トモ買成立にする
              </button>
              <button type="button" class="btn btn-primary waves-effect waves-light" @click="ReleaseOrders">
                <span class="btn-label"><i class="ri-chat-delete-fill"></i></span>トモ買失敗にする
              </button>
            </div>
            <div class="d-flex justify-content-between mt-3" v-if="pingo_product.status ==='RECRUITING'">
              <button type="button" class="btn btn-danger waves-effect waves-light" @click="DeleteOrders">
                <span class="btn-label"><i class="ri-delete-bin-2-fill"></i></span>注文削除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
