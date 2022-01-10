<script>
import {mapState} from 'vuex'


export default {
  name: "backend_index",
  components: {
    PageHeader: () => import(/* webpackChunkName: "about" */ '~/components/Page-header'),
    ProfileCard: () => import(/* webpackChunkName: "about" */ '~/components/widgets/ProfileCard'),
  },
  middleware: 'router-auth',
  data() {
    return {

    }
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user
    })
  },
}
</script>

<template>
  <div class="row">
    <div class="col-md-6 col-xl-12">
      <ProfileCard/>
    </div>
  </div>
</template>
