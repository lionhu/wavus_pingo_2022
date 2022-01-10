<script>
import {mapGetters} from "vuex"
import {swalService} from "~/helpers/swal.service.js"

export default {
  name: "system_pointpolicy_setting",
  // head() {
  //   return {
  //     script: [
  //       {src: 'https://unpkg.com/element-ui/lib/index.js'}
  //     ],
  //     link: [
  //       {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
  //     ]
  //   };
  // },
  components: {
    Switches: () => import('vue-switches'),
    "el-tree": () => import('element-ui/lib/tree'),
    "el-button": () => import('element-ui/lib/button')
  },
  data() {
    return {
      redis_key: "MARGIN_POLICY",
      key_id: 0,
      point_policy: {
        POLICIES: {
          LEVEL_1: true,
          LEVEL_2: true,
          USER_SELF: false,
          SUPERADMIN: false,
          CLIENTADMIN: false,
          SELF_BOUGHT: {
            APPLY: false,
            LIMIT: 3
          }
        },
        JOIN_BONUS_POLICY: {
          POINT: 1000,
          APPLY: true
        },
        INTRODUCE_POINT_POLICY: {
          POINT: 1000,
          APPLY: true
        }
      }
    }
  }
  ,
  computed: {
    ...
      mapGetters({
        // menuitems_store: "categories/getterCategoryList"
      }),
  }
  ,
  mounted() {
    // this.$store.dispatch("categories/load_superadmin_categorylist")
    let url = `/admin_back/api/system/?filter{key}=${this.redis_key}`;
    let vm = this;
    this.$axios.get(url).then((res) => {
      console.log(res.data.system_infos[0].info)
      if (res.data.result) {
        vm.point_policy = res.data.system_infos[0].info;
        vm.key_id = res.data.system_infos[0].id;
        swalService.showToast("success", "Load SystemInfo successfully!")
      }
    })

  }
  ,
  methods: {
    UpdateSystemInfo() {
      let vm=this;
      if (this.key_id) {
        this.point_policy.JOIN_BONUS_POLICY.POINT=parseInt(this.point_policy.JOIN_BONUS_POLICY.POINT);
        this.point_policy.INTRODUCE_POINT_POLICY.POINT=parseInt(this.point_policy.INTRODUCE_POINT_POLICY.POINT);

        let url = `/admin_back/api/system/${this.key_id}/`;
        this.$axios.put(url, {info:this.point_policy}).then((res) => {
          console.log(res.data)
          if (res.data.result) {
            swalService.showToast("success", "Updated successfully!")
          } else {
            swalService.showToast("error", "Failed to update system information")
          }
        })
      }

    },
    ApplyMarginRule_all_clients() {
      let url = "/admin_back/api/clients/superadmin_reset_margin_policy/";
      this.$axios.post(url).then((res) => {
        if (res.data.result) {
          swalService.showToast("success", "Applied  successfully!")
        } else {
          swalService.showToast("error", "Failed to apply all clients")
        }
      })
    }
  }
}
;
</script>
<style>
.line-title-width {
  min-width: 45px !important;
}
</style>
<template>
  <div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h5>Point Policy Settings:</h5>
            <div class="row mb-2">
              <div class="col-sm-6 col-xs-12">

                <div class="mt-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_superadmin">Client Superadmin</label>
                    <switches v-model="point_policy.POLICIES.SUPERADMIN" id="point_policy_superadmin" type-bold="false"
                              color="warning" class="ml-1 mb-0"></switches>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_client_admin">Client Admin</label>
                    <switches v-model="point_policy.POLICIES.CLIENTADMIN" id="point_policy_client_admin"
                              type-bold="false"
                              color="warning" class="ml-1 mb-0"></switches>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_LEVEL_1">LEVEL_1</label>
                    <switches v-model="point_policy.POLICIES.LEVEL_1" id="point_policy_LEVEL_1" type-bold="false"
                              color="warning"
                              class="ml-1 mb-0"></switches>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_LEVEL_2">LEVEL_2</label>
                    <switches v-model="point_policy.POLICIES.LEVEL_2" id="point_policy_LEVEL_2" type-bold="false"
                              color="warning"
                              class="ml-1 mb-0"></switches>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_USER_SELF">USER_SELF</label>
                    <switches v-model="point_policy.POLICIES.USER_SELF" id="point_policy_USER_SELF" type-bold="false"
                              color="warning" class="ml-1 mb-0"></switches>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_SELF_BOUGHT_APPLY">SELF_BOUGHT</label>
                    <switches v-model="point_policy.POLICIES.SELF_BOUGHT.APPLY" id="point_policy_SELF_BOUGHT_APPLY"
                              type-bold="false" color="warning" class="ml-1 mb-0"></switches>
                  </div>
                  <div class="form-horizontal" v-if="point_policy.POLICIES.SELF_BOUGHT.APPLY">
                    <b-form-group id="example text" label-cols-sm="9" label-cols-lg="9" label="SELF_BOUGHT.LIMIT"
                                  label-for="point_policy_SELF_BOUGHT_LIMIT">
                      <b-form-input type="number" v-model="point_policy.POLICIES.SELF_BOUGHT.LIMIT"
                                    id="point_policy_SELF_BOUGHT_LIMIT"></b-form-input>
                    </b-form-group>
                  </div>
                  <hr>
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_SELF_BOUGHT_APPLY">JOIN_BONUS_POLICY</label>
                    <switches v-model="point_policy.JOIN_BONUS_POLICY.APPLY" id="point_policy_JOIN_BONUS_POLICY_APPLY"
                              type-bold="false" color="warning" class="ml-1 mb-0"></switches>
                  </div>
                  <div class="form-horizontal" v-if="point_policy.JOIN_BONUS_POLICY.APPLY">
                    <b-form-group id="example text" label-cols-sm="9" label-cols-lg="9" label="JOIN_BONUS_POLICY.POINT"
                                  label-for="point_policy_JOIN_BONUS_POLICY">
                      <b-form-input type="number" v-model="point_policy.JOIN_BONUS_POLICY.POINT"
                                    id="point_policy_JOIN_BONUS_POLICY"></b-form-input>
                    </b-form-group>
                  </div>
                  <hr>
                  <div class="d-flex justify-content-between align-items-center">
                    <label for="point_policy_SELF_BOUGHT_APPLY">INTRODUCE_POINT_POLICY</label>
                    <switches v-model="point_policy.INTRODUCE_POINT_POLICY.APPLY"
                              id="point_policy_INTRODUCE_POINT_POLICY_APPLY"
                              type-bold="false" color="warning" class="ml-1 mb-0"></switches>
                  </div>
                  <div class="form-horizontal" v-if="point_policy.INTRODUCE_POINT_POLICY.APPLY">
                    <b-form-group id="example text" label-cols-sm="9" label-cols-lg="9"
                                  label="INTRODUCE_POINT_POLICY.POINT"
                                  label-for="point_policy_INTRODUCE_POINT_POLICY">
                      <b-form-input type="number" v-model="point_policy.INTRODUCE_POINT_POLICY.POINT"
                                    id="point_policy_INTRODUCE_POINT_POLICY"></b-form-input>
                    </b-form-group>
                  </div>
                </div>
              </div>

              <div class="col-sm-6 col-xs-12">
                <b-button pill class="btn-bordered-primary" variant="outline-primary" @click="UpdateSystemInfo">Update
                </b-button>
                <b-button pill class="btn-bordered-danger" variant="outline-danger"
                          @click="ApplyMarginRule_all_clients">Apply to all Clients
                </b-button>
              </div>

              <!-- end col-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
