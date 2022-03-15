<script>
import { APIServices } from "~/helpers/APIs"

export default {
    name: "supplier_edit",
    props: ["supplier_id", "showModal", "mode"],
    components: {
        Switches: () =>
            import ('vue-switches'),
        "el-autocomplete": () =>
            import ('element-ui/lib/autocomplete'),
    },
    data() {
        return {
            supplier: {},
            supplier_admin_name: "",
            auto_searching: false,
            autocomplete_address: false,
            admin: {
                id: 0,
                name: ""
            },
            errors: [],
            url_CRUD: "store/public/suppliers/",
        };
    },
    watch: {
        supplier_id(val, oldval) {
            console.log("supplier", val, oldval)
            if (val) {
                console.log("edit")
                this.load_supplier(val)
            } else {
                console.log("add")
                this.supplier = {
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
                    user: 0
                }
                this.admin = { id: 0, name: "" }
            }
        }
    },
    methods: {
        check_supplier_info() {
            this.errors = [];
            if (this.supplier.name === "") this.errors.push("名前が必要です。");
            if (this.supplier.postcode === "") this.errors.push("郵便番号が必要です。");
            if (this.supplier.state === "") this.errors.push("都道府県が必要です。");
            if (this.supplier.city === "") this.errors.push("市が必要です。");
            if (this.supplier.town === "") this.errors.push("町村が必要です。");
            if (this.supplier.address_1 === "") this.errors.push("住所１が必要です。");
            if (this.supplier.phone === "") this.errors.push("電話が必要です。");
            if (this.supplier.email === "") this.errors.push("メールが必要です。");
            if (this.supplier.user < 1) this.errors.push("責任者が必要です。");
            console.log("check_supplier; ", this.errors.length === 0)
            console.log(this.errors.length === 0)
            return this.errors.length === 0
        },
        load_supplier(pk) {
            let vm = this;
            APIServices.get(`${this.url_CRUD}${pk}/`)
                .then(APIServices.handleResponse)
                .then(res => {
                    console.log(res)
                    vm.supplier = res
                })
        },
        updatesupplierInfo() {
            if (this.check_supplier_info()) {
                console.log("updatesupplierInfo", this.supplier)

                if (this.mode === "edit" && this.supplier.user) {
                    this.$store.dispatch("suppliers/update_supplier", { supplier_id: this.supplier.id, info: this.supplier });
                }
                if (this.mode === "add") {
                    this.$store.dispatch("suppliers/insert_supplier", this.supplier)
                }
                this.errors = [];
                this.$emit("closeMoal", {
                    mode: this.mode,
                    supplier: this.supplier,
                    result: true
                })
            }

        },
        autocomplete_adminname() {
            let vm = this;
            let user = parseInt(this.supplier.user)
            if (user > 0) {
                this.$axios.post(`/apiauth/users/${user}/get_username/`)
                    .then(response => {

                        console.log(response.data)
                        if (response.data.result) {
                            vm.supplier_admin_name = response.data.username
                        } else {
                            vm.supplier_admin_name = ""
                            vm.supplier.user = 0;
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
            if (this.supplier.postcode.length > 6) {
                var vm = this;
                this.auto_searching = true;

                var url = "https://api.anko.education/zipcode?zipcode=" + this.supplier.postcode;
                fetch(url)
                    .then(function(response) {
                        if (response.ok) {
                            return response.json();
                        }
                    })
                    .then(function(address) {
                        if (address !== undefined) {
                            vm.autocomplete_address = true;
                            vm.supplier.state = address.pref;
                            vm.supplier.city = address.city;
                            vm.supplier.town = address.area;
                        }
                    }).catch((error) => {
                        console.error('Error:', error);
                        vm.autocomplete_address = false;
                    });
                this.auto_searching = false;
            }
        },
        querySearchAsync(queryString, cb) {
            console.log(queryString)
            let url = `auth/users/filter_users?key_str=${queryString}`
            APIServices.get(url)
                .then(APIServices.handleResponse)
                .then((response) => {
                    console.log(response)
                    var selectlist = response.users.map(function(user) {
                        return { id: user.pk, value: user.username }
                    })
                    cb(selectlist)
                })
        },
        handleSelect(item) {
            console.log(item)
            this.supplier.user = item.id;
        },
        closeModal(result) {
            this.$emit("closeMoal", {
                mode: this.mode,
                supplier: this.supplier,
                result: result
            })

        }
    },
};
</script>

<template>
    <b-modal id="modal-edit-supplier" scrollable title="New supplier Information" title-class="font-18" body-class="p-4" hide-footer v-if="showModal">
        <form @submit.prevent="updatesupplierInfo">
            <ul v-if="errors.length" class="text-danger">
                <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label for="field-name" class="control-label">Name<span class="text-danger">*</span></label>
                        <input type="text" id="field-name" v-model="supplier.name" class="form-control" placeholder="会社名" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label for="field-postcode" class="control-label">Postcode<span class="text-danger">*</span></label>
                        <input type="text" v-model="supplier.postcode" id="field-postcode" class="form-control" placeholder="郵便番号" @blur="autocomplete_postcode" />
                    </div>
                </div>
                <div class="col-md-6">

                    <div class="form-group">
                        <label for="field-state" class="control-label">State<span class="text-danger">*</span></label>
                        <input type="text" id="field-state" v-model="supplier.state" class="form-control" placehold="都道府県" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label for="field-city" class="control-label">City<span class="text-danger">*</span></label>
                        <input type="text" id="field-city" v-model="supplier.city" class="form-control" placeholder="東京都" />
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label for="field-town" class="control-label">Town<span class="text-danger">*</span></label>
                        <input type="text" id="field-town" v-model="supplier.town" class="form-control" placeholder="" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label for="field-address1" class="control-label">Address<span class="text-danger">*</span></label>
                        <input type="text" id="field-address1" v-model="supplier.address_1" class="form-control" placeholder="Address_1" />
                        <input type="text" id="field-address2" v-model="supplier.address_2" class="form-control" placeholder="Address_2" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label for="field-phone" class="control-label">Phone<span class="text-danger">*</span></label>
                        <input type="text" id="field-phone" v-model="supplier.phone" class="form-control" placeholder="電話" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label for="field-email" class="control-label">Email<span class="text-danger">*</span></label>
                        <input type="text" id="field-email" v-model="supplier.email" class="form-control" placeholder="メール" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label for="field-email" class="control-label">Website<span class="text-danger">*</span></label>
                        <input type="text" id="field-website" v-model="supplier.website" class="form-control" placeholder="website" />
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group no-margin">
                        <label for="field-admin_id" class="control-label">Admin ID(#{{ supplier.user }})<span
                                                              class="text-danger">*</span></label>
                        <el-autocomplete v-model="admin.username" :fetch-suggestions="querySearchAsync" placeholder="请输入内容" @select="handleSelect"></el-autocomplete>
                        <input type="text" id="field-admin_id" v-model="supplier.user" class="form-control" hidden/>

                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group no-margin">
                        <label class="control-label">{{ supplier_admin_name }}</label>
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
