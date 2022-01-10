<script>
import {mapState} from 'vuex'

export default {
  name: "backend_index",
  components: {
    PageHeader: () => import(/* webpackChunkName: "about" */ '~/components/Page-header')
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
  mounted() {
    console.log(this.ME)
    if (this.ME.role !== undefined && this.ME.role !== "") {
      this.$router.push(
        this.$route.query.redirectFrom || {
          path: `/${this.ME.role}/`
        }
      );
    }
  }
}
</script>

<template>
  <div>
  </div>
</template>
