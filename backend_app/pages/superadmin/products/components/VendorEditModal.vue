<script>
import {axios} from "@/plugins/axios"

export default {
  name: "vendor_edit",
  props: ["vendor_id", "showModal", "mode"],
  components: {
    Switches: () => import('vue-switches'),
    "el-autocomplete": () => import('element-ui/lib/autocomplete'),
  },
  data() {
    return {
      vendor: {},
      vendor_admin_name: "",
      auto_searching: false,
      autocomplete_address: false,
      admin: {
        id: 0,
        name: ""
      },
      errors: [],
      url_CRUD:"/admin_back/api/vendors/",
    };
  },
  watch: {
    vendor_id(val, oldval) {
      console.log("vendor", val, oldval)
      if (val) {
        console.log("edit")
        this.load_vendor(val)
      } else {
        console.log("add")
        this.vendor = {
          name: "",
          postcode: "",
          state: "",
          city: "",
          town: "",
          address_1: "",
          address_2: "",
          phone: "",
          email: "",
          website: "",
          admin_id: 0
        }
        this.admin = {id: 0, name: ""}
      }
    }
  },
  methods: {
    check_vendor_info() {
      this.errors = [];
      if (this.vendor.name === "") this.errors.push("名前が必要です。");
      if (this.vendor.postcode === "") this.errors.push("郵便番号が必要です。");
      if (this.vendor.state === "") this.errors.push("都道府県が必要です。");
      if (this.vendor.city === "") this.errors.push("市が必要です。");
      if (this.vendor.town === "") this.errors.push("町村が必要です。");
      if (this.vendor.address_1 === "") this.errors.push("住所１が必要です。");
      if (this.vendor.phone === "") this.errors.push("電話が必要です。");
      if (this.vendor.email === "") this.errors.push("メールが必要です。");
      if (this.vendor.admin_id < 1) this.errors.push("責任者が必要です。");
      console.log("check_vendor; ", this.errors.length === 0)
      console.log(this.errors.length === 0)
      return this.errors.length === 0
    },
    load_vendor(pk) {
      let vm = this;
      axios.get(`${this.url_CRUD}${pk}/`)
        .then(res => {
          console.log(res)
          if (res.data.result) {
            vm.vendor = res.data.vendor
          }
        })
    },
    updateVendorInfo() {
      if (this.check_vendor_info()) {
        if (this.mode === "edit" && this.vendor.id) {
          let vendor_id=this.vendor.id;
          delete this.vendor.id;
          this.$store.dispatch("vendors/update_vendor", {vendor_id:vendor_id, info:this.vendor});
        }
        if (this.mode === "add" ){
          this.$store.dispatch("vendors/insert_vendor", this.vendor)
        }
        this.errors = [];
        this.$emit("closeMoal", {
          mode: this.mode,
          vendor: this.vendor,
          result: true
        })
      }

    },
    autocomplete_adminname() {
      let vm = this;
      let admin_id = parseInt(this.vendor.admin_id)
      if (admin_id > 0) {
        this.$axios.post(`/apiauth/users/${admin_id}/get_username/`)
          .then(response => {

            console.log(response.data)
            if (response.data.result) {
              vm.vendor_admin_name = response.data.username
            } else {
              vm.vendor_admin_name = ""
              vm.vendor.admin_id = 0;
            }
            // return response.json()
          }).catch(error => {
          Swal.showValidationMessage(
            `Request failed: ${error}`
          )
        })
      }

    },
    autocomplete_postcode() {
      // console.log(this.user.postcode.length)
      if (this.vendor.postcode.length > 6) {
        var vm = this;
        this.auto_searching = true;

        var url = "https://api.anko.education/zipcode?zipcode=" + this.vendor.postcode;
        fetch(url)
          .then(function (response) {
            if (response.ok) {
              return response.json();
            }
          })
          .then(function (address) {
            if (address !== undefined) {
              vm.autocomplete_address = true;
              vm.vendor.state = address.pref;
              vm.vendor.city = address.city;
              vm.vendor.town = address.area;
            }
          }).catch((error) => {
          console.error('Error:', error);
          vm.autocomplete_address = false;
        });
        this.auto_searching = false;
      }
    },
    querySearchAsync(queryString, cb) {
      let url = `/apiauth/users/?search=${queryString}`
      this.$axios.get(url).then((response) => {
        console.log(response)
        if (response.data.result && response.data.data.users.total) {
          var selectlist = response.data.data.users.results.map(function (user) {
            return {id: user.id, value: user.username}
          })
          cb(selectlist)
        }
      })
    },
    handleSelect(item) {
      this.vendor.admin_id = item.id;
    },
    closeModal(result) {
      this.$emit("closeMoal", {
        mode: this.mode,
        vendor: this.vendor,
        result: result
      })

    }
  },
};
</script>

<template>
  <b-modal id="modal-edit-vendor"
           scrollable title="New Vendor Information"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showModal"
  >
    <form @submit.prevent="updateVendorInfo">
      <ul v-if="errors.length" class="text-danger">
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-name" class="control-label">Name
              <span class="text-danger">*</span>
            </label>
            <input type="text" id="field-name" v-model="vendor.name" class="form-control" placeholder="会社名"/>

          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="field-postcode" class="control-label">Postcode<span class="text-danger">*</span></label>
            <input type="text" v-model="vendor.postcode" id="field-postcode" class="form-control"
                   placeholder="郵便番号" @blur="autocomplete_postcode"/>
          </div>
        </div>
        <div class="col-md-6">

          <div class="form-group">
            <label for="field-state" class="control-label">State<span class="text-danger">*</span></label>
            <input type="text" id="field-state" v-model="vendor.state" class="form-control"
                   placehold="都道府県"/>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="field-city" class="control-label">City<span class="text-danger">*</span></label>
            <input type="text" id="field-city" v-model="vendor.city" class="form-control"
                   placeholder="東京都"/>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="field-town" class="control-label">Town<span class="text-danger">*</span></label>
            <input type="text" id="field-town"
                   v-model="vendor.town" class="form-control" placeholder=""/>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-address1" class="control-label">Address<span class="text-danger">*</span></label>
            <input type="text" id="field-address1" v-model="vendor.address_1" class="form-control"
                   placeholder="Address_1"/>
            <input type="text" id="field-address2" v-model="vendor.address_2" class="form-control"
                   placeholder="Address_2"/>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-phone" class="control-label">Phone<span class="text-danger">*</span></label>
            <input type="text" id="field-phone" v-model="vendor.phone" class="form-control"
                   placeholder="電話"/>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-email" class="control-label">Email<span class="text-danger">*</span></label>
            <input type="text" id="field-email" v-model="vendor.email" class="form-control"
                   placeholder="メール"/>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-email" class="control-label">Website<span class="text-danger">*</span></label>
            <input type="text" id="field-website" v-model="vendor.website" class="form-control"
                   placeholder="website"/>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group no-margin">
            <label for="field-admin_id" class="control-label">Admin ID(#{{ vendor.admin_id }})<span
              class="text-danger">*</span></label>
            <el-autocomplete
              v-model="admin.username"
              :fetch-suggestions="querySearchAsync"
              placeholder="请输入内容"
              @select="handleSelect"
            ></el-autocomplete>
            <input type="text" id="field-admin_id" v-model="vendor.admin_id" class="form-control" hidden/>

          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group no-margin">
            <label class="control-label">{{ vendor_admin_name }}</label>
          </div>
        </div>
      </div>

      <div class="form-group row">
        <div class="col-8 offset-4">
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="reset" class="btn btn-secondary m-l-5 ml-1" @click="closeModal(false)">Cancel</button>
        </div>
      </div>
    </form>

  </b-modal>

</template>
