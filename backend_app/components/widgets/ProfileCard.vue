<script>
import {mapGetters} from 'vuex'
import Swal from "sweetalert2"
import {supplierService} from "~/helpers/supplier.service"

export default {
  name: "backend_profilecard",
  components: {},
  data() {
    return {}
  },
  mounted() {

  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME",
      mySupplierInfo: "suppliers/getterSupplier"
    }),
  },
  methods: {
    async update_supplier_info(info) {
      let self = this;
      await Swal.fire({
        title: '再確認?',
        html: "本当に変更しますか？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい、確定!',
        showLoaderOnConfirm: true,
        preConfirm: (confirm) => {
          if (confirm) {
            return supplierService.updateInfo({
              supplier_id: this.mySupplierInfo.id,
              info: info
            }).then(updated_supplier => {
              console.log(updated_supplier)
              if (updated_supplier.id) {
                self.$store.commit("suppliers/set_supplier", updated_supplier)
                Swal.fire({
                  title: "Success",
                  icon: "success",
                  html: `変更されました。`
                })
              }
            })
          }
        },
        allowOutsideClick: () => false
      })


    },
    async changeMail() {
      const {value: email} = await Swal.fire({
        title: '通知用メールアドレス変更',
        input: 'email',
        inputValue: this.mySupplierInfo.email,
        inputLabel: `登録中のメールアドレス　${this.mySupplierInfo.email}`,
        inputPlaceholder: '新しいメールアドレス'
      })

      if (email!==undefined && email.length > 3) {
        let info = {
          "name": this.mySupplierInfo.name,
          "email": email,
          "user": this.mySupplierInfo.user
        }
        await this.update_supplier_info(info)
      }
    },
    async changePhone() {
      const {value: phone} = await Swal.fire({
        title: '通知用電話の変更',
        input: 'text',
        inputValue: this.mySupplierInfo.phone,
        inputLabel: `登録中の通知用電話　${this.mySupplierInfo.phone}`,
        inputPlaceholder: '通知用電話番号'
      })

      if (phone!==undefined && phone.length>3) {
        let info = {
          "name": this.mySupplierInfo.name,
          "phone": phone,
          "user": this.mySupplierInfo.user
        }
        await this.update_supplier_info(info)
      }
    }
  }
}
</script>

<template>
  <div class="card">
    <div class="card-body text-center">
      <img :src="ME.avatar_thumb_url" class="rounded-circle avatar-xl img-thumbnail" alt="profile-image"/>
      <h4 class="mt-3 mb-0">{{ ME.username }}</h4>
      <!--      <p class="text-muted">@{{ ME.isVendor.vendor_name }}</p>-->

      <div class="text-left mt-3">
        <b-badge pill variant="primary">サプライヤー情報</b-badge>

        <div class="table-responsive">
          <table class="table table-borderless table-sm">
            <tbody>
            <tr>
              <th scope="row">電話 :</th>
              <td class="text-muted">
                {{ mySupplierInfo.phone }}
                <a href="javascript:void(0);" @click="changePhone">
                  <b-badge pill variant="warning" class="float-right">通知電話の変更</b-badge>
                </a>
              </td>
            </tr>
            <tr>
              <th scope="row">メール :</th>
              <td class="text-muted">{{ mySupplierInfo.email }}
                <a href="javascript:void(0);" @click="changeMail">
                  <b-badge pill variant="warning" class="float-right">通知メール変更</b-badge>
                </a>
              </td>
            </tr>
            <tr>
              <th scope="row">住所 :</th>
              <td class="text-muted">
                〒{{ mySupplierInfo.postcode }}{{ mySupplierInfo.state }}{{ mySupplierInfo.city }} <br>
                {{ mySupplierInfo.town }}{{ mySupplierInfo.address_1 }} <br>
                {{ mySupplierInfo.address_2 }}
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>

      <ul class="social-list list-inline mt-3 mb-0">
        <li class="list-inline-item">
          <a href="javascript: void(0);" class="social-list-item border-purple text-purple">
            <i class="mdi mdi-facebook"></i>
          </a>
        </li>
        <li class="list-inline-item">
          <a href="javascript: void(0);" class="social-list-item border-danger text-danger">
            <i class="mdi mdi-google"></i>
          </a>
        </li>
        <li class="list-inline-item">
          <a href="javascript: void(0);" class="social-list-item border-info text-info">
            <i class="mdi mdi-twitter"></i>
          </a>
        </li>
        <li class="list-inline-item">
          <a href="javascript: void(0);" class="social-list-item border-secondary text-secondary">
            <i class="mdi mdi-github"></i>
          </a>
        </li>
      </ul>
    </div>
    <!-- end card-box -->
  </div>
</template>
