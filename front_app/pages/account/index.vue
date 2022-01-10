<template>
  <div>
    <Header/>
    <Breadcrumbs :title="$t('menu.dashboard')" breadcrumb_type="static"/>

    <section class="section-b-space ratio_asos">
      <div class="collection-wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <DashboardNav active_title="dashboard_menu.account_info"/>
            </div>
            <div class="collection-content mt-3 col-lg-9">
              <div class="page-main-content">

                <div class="dashboard-right">
                  <div class="dashboard">
                    <vue-membershipcard :value-fields="valueFields" class="my-3" v-if="valueFields.memberName!==''"/>
                    <div class="welcome-msg">
                      <div v-if="canTransferPoint">
                        <h4><span class="title" v-if="!$device.isMobile"> {{ $t('pointlist.walletID') }}:</span></h4>
                        <h4><span class="theme-color">{{ ME.profile.introcode }}</span></h4>
                      </div>
                    </div>
                    <div class="box-account box-info mt-3">
                      <div class="box-head">
                        <h2>{{ $t('dashboard.account_info') }}</h2>
                      </div>
                      <div class="row mb-3">
                        <div class="col-sm-6">
                          <AvatarLoader/>
                        </div>
                        <div class="col-sm-6">
                          <FamilyTree/>
                        </div>
                      </div>
                      <div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<style>
</style>
<script>
import {mapGetters, mapState} from "vuex"
import VueMembercard from '~/pingo_node_modules/vue-membercard'

export default {
  name: "dashboard",
  middleware: ['authenticated'],
  data() {
    return {
      valueFields: {
        memberName: "",
        memberEmail: "",
        followers: 0,
        points: 0,
        membership: "golden",
        introcode: "",
        url: ''
      }
    };
  },
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    DashboardNav: () => import('~/components/widgets/dashboardnav'),
    FamilyTree: () => import("~/components/widgets/decendants"),
    AvatarLoader: () => import("~/components/widgets/AvatarLoader"),
    "vue-membershipcard": VueMembercard,
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME",
    }),
    canTransferPoint() {
      return this.ME.profile.pointbank_balance > 0 && this.ME.profile.can_transfer_point;
    }
  },
  mounted() {
    var register_url = "https://www.pingo.jp/account/register?introcode="
    register_url = register_url + this.ME.profile.introcode
    this.valueFields = {
      memberName: this.ME.username,
      memberEmail: this.ME.email,
      followers: this.ME.profile.get_descendants_count,
      points: this.ME.profile.pointbank_balance===null?0:this.ME.profile.pointbank_balance,
      membership: "golden",
      introcode: this.ME.profile.introcode,
      url: register_url
    }
  },
  methods: {
    // logout: function () {
    //   this.$store.dispatch('authfack/logout');
    //   this.$router.push({path: '/'})
    // }
  }
}
</script>
