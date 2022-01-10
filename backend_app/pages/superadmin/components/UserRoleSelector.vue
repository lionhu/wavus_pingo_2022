<script>
import {axios} from "@/plugins/axios"
import {APIServices} from "@/helpers/APIs";

export default {
  name: "user_roles_selector",
  props: ["user", "showModal"],
  components: {
    Switches: () => import('vue-switches'),
  },
  data() {
    return {
      roles: {
        supplier: false,
        staff: false,
        member: false,
        // superadmin: false,
        // client_superadmin: false,
        // client_admin: false,
      },
      errors: []
    };
  },
  computed: {
    isStaff() {
      return this.user.roles.includes("staff");
    },
    isSuperadmin() {
      return this.user.roles.includes("superadmin");
    },
    isSupplier() {
      return this.user.roles.includes("supplier");
    },
    isClientAdmin() {
      return this.user.roles.includes("client");
    },
    isClientSuperadmin() {
      return this.user.roles.includes("client_superadmin");
    },
  },
  watch: {
    user(newVal, oldVal) {
      console.log(newVal)
      if (newVal !== null) {
        this.roles = {
          // superadmin: newVal.roles.includes("superadmin"),
          // client_superadmin: newVal.roles.includes("client_superadmin"),
          // client_admin: newVal.roles.includes("client_admin"),
          staff: newVal.roles.includes("staff"),
          member: newVal.roles.includes("member"),
          supplier:newVal.roles.includes("supplier"),
        }
      }
    },
  },
  methods: {
    updateUserRoleInfo() {
      let new_roles = [];
      if (this.roles.staff) new_roles.push("staff");
      if (this.roles.supplier) new_roles.push("supplier");
      if (this.roles.member) new_roles.push("member");
      // if (this.roles.superadmin) new_roles.push("superadmin");
      // if (this.roles.client_admin) new_roles.push("client_admin");
      // if (this.roles.client_superadmin) new_roles.push("client_superadmin");
      APIServices.post(`auth/users/${this.user.id}/sync_user_role/`, {
        roles: new_roles
      }).then(APIServices.handleResponse)
        .then(response => {
          this.$emit("closeModal", {result: true, user: response.user});
        }).catch(error => {
        console.log(error)
      })
    },
    closeModal() {
      this.$emit("closeModal", {result: false, user: null});
    }
  },
};
</script>

<template>
  <b-modal id="modal-user-roles-selector"
           scrollable title="User Roles"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showModal"
  >
    <form @submit.prevent="updateUserRoleInfo">
      <ul v-if="errors.length" class="text-danger">
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>

      <div class="form-group row d-flex justify-content-around">
        <!--        <b-form-checkbox id="cb_superadmin" v-model="roles.superadmin" name="checkbox-1" :value="true"-->
        <!--                         :unchecked-value="false">-->
        <!--          SuperAdmin-->
        <!--        </b-form-checkbox>-->
        <b-form-checkbox id="cb_staff" v-model="roles.staff" name="checkbox-2" :value="true"
                         :unchecked-value="false">
          スタフ
        </b-form-checkbox>

        <b-form-checkbox id="cb_vendor" v-model="roles.supplier" name="checkbox-2" :value="true"
                         :unchecked-value="false">
          サプライヤー
        </b-form-checkbox>
        <b-form-checkbox id="cb_member" v-model="roles.member" name="checkbox-2" :value="true"
                         :unchecked-value="false">
          一般会員
        </b-form-checkbox>
      </div>
      <!--      <div class="form-group row d-flex justify-content-around">-->
      <!--        <b-form-checkbox id="cb_client_superadmin" v-model="roles.client_superadmin" name="checkbox-2" :value="true"-->
      <!--                         :unchecked-value="false" disabled>-->
      <!--          営業代行-->
      <!--        </b-form-checkbox>-->
      <!--        <b-form-checkbox id="cb_client_admin" v-model="roles.client_admin" name="checkbox-2" :value="true"-->
      <!--                         :unchecked-value="false" disabled>-->
      <!--          代理店-->
      <!--        </b-form-checkbox>-->

      <!--      </div>-->
      <div class="form-group row">
        <div class="col-8 offset-4">
          <button type="submit" class="btn btn-primary">確定</button>
          <button type="reset" class="btn btn-secondary m-l-5 ml-1" @click="closeModal(false)">取消</button>
        </div>
      </div>
    </form>

  </b-modal>

</template>
