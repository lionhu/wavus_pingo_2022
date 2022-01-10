<script>
import {mapState, mapGetters} from 'vuex'
import {APIServices} from "~/helpers/APIs.js"

export default {
  name: "backend_SuperAdmin_index",
  components: {
    PageHeader: () => import(/* webpackChunkName: "about" */ '~/components/Page-header'),
    // DescendantSummary: () => import("@/components/widgets/DescendantSummary"),
    // PointSummary: () => import("@/components/widgets/PointSummary"),
    // VisitLogSummary: () => import("./widgets/VisitLogSummary"),
    // RegisteredUsers: () => import("./widgets/RegisteredUsers"),
    // PointUserRanking: () => import("./widgets/PointUserRanking"),
    // UnapprovedPoints: () => import("./widgets/UnapprovedPoint"),
    // UnapprovedUserPoint: () => import("./widgets/UnapprovedUserPoint"),
    // ViewProductRanking: () => import("./widgets/ViewProductRanking")
  },
  middleware: ['router-auth', 'router-superadmin'],
  head() {
    return {
      title: 'Client Admin Dashboard | PINGO Backend',
      script: [
        {src: 'https://unpkg.com/element-ui/lib/index.js'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      ]
    };
  },
  data() {
    return {
      items: [
        {text: 'PINGO'},
        {text: 'Dashboards'},
        {text: 'Sales',active: true}
      ],
    }
  },
  async asyncData() {
    const response_data = await APIServices.get("backend/dashboard/get_charts/")
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      })
    console.log("asyncData",response_data)
    return {
      unApprovedPoints: {
        labels: response_data.margin_summary.labels.length ? response_data.margin_summary.labels : [],
        data: response_data.margin_summary.labels.length ? response_data.margin_summary.datasets[0].data : []
      },
      unApprovedUserPoints: {
        labels: response_data.user_margin_summary.labels.length ? response_data.user_margin_summary.labels : [],
        data: response_data.user_margin_summary.labels.length ? response_data.user_margin_summary.datasets : []
      },
      user_ranking: {
        labels: response_data.user_ranking.labels.length ? response_data.user_ranking.labels : [],
        data: response_data.user_ranking.labels.length ? response_data.user_ranking.datasets[0].data : []
      }
    }
  },
  mounted() {
    this.$store.dispatch("categories/load_superadmin_categorylist")
  },
  methods: {},
  computed: {
    ...mapState({
      ME: state => state.auth.user
    }),
    page_title() {
      return "Welcome ! Clients Admin " + this.ME.username;
    },
    hasUnapprovedPoints() {
      return this.unApprovedPoints.data.length;
    },
    hasunApprovedUserPoints() {
      return this.unApprovedUserPoints.data.length;
    },
    hasUserRanking() {
      return this.user_ranking.data.length;
    }
  },
}
</script>

<template>
  <div>
    <PageHeader :title="page_title" :items="items"/>

    <div class="row">
      <div class="col-md-6 col-xs-12">
        <UnapprovedPoints :unapprovedpoints_data="unApprovedPoints"
                          header_title="未承認ポイント"
                          title="カテゴリ別"
                          v-if="hasUnapprovedPoints"
        />
      </div>
      <div class="col-md-6 col-xs-12">
        <UnapprovedUserPoint :unapprovedpoints_data="unApprovedUserPoints"
                             header_title="未承認ポイント"
                             title="ユーザー別(Top3)"
                             v-if="hasunApprovedUserPoints"
        />
      </div>
    </div>
    <PointUserRanking :user_ranking="user_ranking"
                      header_title="持ちポイントランキング"
                      title="ユーザー別(Top3)"
                      v-if="hasUserRanking"
    ></PointUserRanking>


  </div>
</template>
