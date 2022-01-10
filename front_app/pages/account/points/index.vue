<template>
  <div>
    <Header/>
    <Breadcrumbs :title="$t('menu.dashboard')" breadcrumb_type="static"/>

    <section class="section-b-space ratio_asos">
      <div class="collection-wrapper">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <DashboardNav active_title="dashboard_menu.points"/>
            </div>
            <div class="collection-content mt-3 col-lg-9">
              <div class="page-main-content">
                <PointList/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<script>
import {mapGetters, mapState} from "vuex"

export default {
  name: "dashboard",
  middleware: ['authenticated'],
  data() {
    return {};
  },
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('~/components/widgets/breadcrumbs'),
    DashboardNav: () => import('~/components/widgets/dashboardnav'),
    PointList: () => import('./pointlist'),
  }

}
</script>
