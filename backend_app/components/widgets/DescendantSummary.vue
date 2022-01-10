<script>
import {mapState} from 'vuex'

export default {
  name: "SuperAdmin_descendant_summary",
  components: {},
  data() {
    return {}
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user
    }),
  },
}
</script>

<template>
  <div class="card">
    <div class="card-body">
      <div class="d-flex justify-content-between">
        <div>
          <h5 title="Campaign Sent" class="text-muted font-weight-normal mt-0 text-truncate">Followers</h5>
          <h3 class="my-2 py-1">
            <span data-plugin="counterup">{{ ME.profile.get_descendants_count }}</span></h3>
          <p class="mb-0 text-muted"><span class="text-success mr-2">
                  <span class="mdi mdi-arrow-up-bold"></span>
                        3.27%
                    </span> <span class="text-nowrap">Since last month</span></p></div>
        <div class="avatar-sm">
                <span class="avatar-title bg-soft-primary rounded">
                <i class="fe-users font-20 text-primary"></i></span>
        </div>
      </div>
    </div>
  </div>

</template>
