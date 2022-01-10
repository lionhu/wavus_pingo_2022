<script>
export default {
  name: "client_pointpolicy",
  props: ["client", "showEditClientPointPolicyModal"],
  components: {
    Switches: () => import('vue-switches'),
  },
  data() {
    return {
      point_policy: {
          LEVEL_1: true,
          LEVEL_2: true,
          USER_SELF: false,
          SUPERADMIN: false,
          CLIENTADMIN: false,
          SELF_BOUGHT: {
            APPLY: false,
            LIMIT: 3
        },
      }
    };
  },
  watch: {
    client() {
      let vm = this;
      this.$store.dispatch("clients/load_ONE_client", this.client.id)
        .then(response => {
          console.log("load_ONE_client",response.margin_policy)
          vm.point_policy = response.margin_policy;
        }).catch(err => {
        vm.$emit("result", false)
      })
    }
  },
  methods: {
    updateClientInformation() {
      let vm = this;
      vm.$store.dispatch("clients/update_client", {
        client_id: vm.client.id,
        info: {
          margin_policy: vm.point_policy
        }
      }).then((response) => {
        vm.$emit("result", true)
      })
    },
  },
};
</script>

<template>

  <b-modal id="modal_client_pointpolicy"
           scrollable
           centered
           title="Edit Points Policy Information"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showEditClientPointPolicyModal"
  >
    <form @submit.prevent="updateClientInformation">
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <h5>Point Policy Settings:</h5>
              <div class="row mb-2">
                <div class="col-12">

                  <div class="mt-3">
                    <div class="d-flex justify-content-between align-items-center">
                      <label for="point_policy_superadmin">Client Superadmin</label>
                      <switches v-model="point_policy.SUPERADMIN" id="point_policy_superadmin"
                                type-bold="false"
                                color="warning" class="ml-1 mb-0"></switches>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <label for="point_policy_client_admin">代理店</label>
                      <switches v-model="point_policy.CLIENTADMIN" id="point_policy_client_admin"
                                type-bold="false"
                                color="warning" class="ml-1 mb-0"></switches>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <label for="point_policy_LEVEL_1">LEVEL_1</label>
                      <switches v-model="point_policy.LEVEL_1" id="point_policy_LEVEL_1" type-bold="false"
                                color="warning"
                                class="ml-1 mb-0"></switches>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <label for="point_policy_LEVEL_2">LEVEL_2</label>
                      <switches v-model="point_policy.LEVEL_2" id="point_policy_LEVEL_2" type-bold="false"
                                color="warning"
                                class="ml-1 mb-0"></switches>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <label for="point_policy_USER_SELF">購入者本人</label>
                      <switches v-model="point_policy.USER_SELF" id="point_policy_USER_SELF" type-bold="false"
                                color="warning" class="ml-1 mb-0"></switches>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="form-group row">
        <div class="col-8 offset-4">
          <button type="submit" class="btn btn-primary">確定</button>
        </div>
      </div>
    </form>

  </b-modal>

</template>
