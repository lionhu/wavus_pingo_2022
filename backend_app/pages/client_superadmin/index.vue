<script>
import {mapState} from 'vuex'
import ApexCharts from 'apexcharts'

export default {
  name: "backend_CSA_index",
  components: {
    PageHeader: () => import(/* webpackChunkName: "about" */ '~/components/Page-header'),
    apexchart: ApexCharts,
    ViewProductRanking: () => import("@/components/widgets/ViewProductRanking.vue"),
    ContributorRanking: () => import("@/components/widgets/ContributorRanking.vue")
  },
  middleware: ['router-auth', 'router-clientsuperadmin'],
  data() {
    return {
      items: [
        {
          text: 'PINGO'
        },
        {
          text: 'Dashboards'
        },
        {
          text: 'Sales',
          active: true
        }
      ],
      rankings: [],
      viewproduct_rankings: [],
      viewproduct_chart_data: {},
      series: [44, 55, 41, 17, 15],
      chartOptions: {
        chart: {
          width: 380,
          type: 'donut',
        },
        plotOptions: {
          pie: {
            startAngle: -90,
            endAngle: 270
          }
        },
        dataLabels: {
          enabled: false
        },
        fill: {
          type: 'gradient',
        },
        legend: {
          formatter: function (val, opts) {
            return val + " - " + opts.w.globals.series[opts.seriesIndex]
          }
        },
        title: {
          text: 'Gradient Donut with custom Start-angle'
        },
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
      },
    }
  },
  head() {
    return {
      title: 'Client Admin Dashboard | PINGO Backend',
      // script: [
      //   {src: 'https://cdn.jsdelivr.net/npm/apexcharts'}
      // ],
      // link: [
      //   {rel: 'stylesheet', href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'}
      // ]
    };
  },
  mounted() {
    let vm = this;
    let url = `/back/store/api/clientadmin/${this.ME.profile.user_id}/summary_info/`;
    console.log(url);
    this.$axios.post(url).then((response) => {
      console.log(response.data)
      console.log(JSON.parse(response.data.data.json_margin_top5))
      if (response.data.result) {
        vm.rankings = JSON.parse(response.data.data.json_margin_top5)
        vm.draw_charts();
        console.log("response.data.data.json_viewproducts_top5", response.data.data.json_viewproducts_top5)
        if (response.data.data.json_viewproducts_top5 !== null) {
          vm.viewproduct_rankings = JSON.parse(response.data.data.json_viewproducts_top5)
          vm.$store.commit("auth/update_user_profile", response.data.data.profile);
        }
      }
    })
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user
    }),
    page_title() {
      return "Welcome ! Clients Admin " + this.ME.username;
    },
    point_balance() {
      if (this.ME.profile.point_balance === null || this.ME.profile.point_balance === undefined) return 0;
      return this.ME.profile.point_balance
    },
    validpoint_percentage() {
      return parseInt(this.validpoint_balance / this.point_balance * 100);
    },
    validpoint_balance() {
      if (this.ME.profile.validpoint_balance === null || this.ME.profile.validpoint_balance === undefined) return 0;
      return this.ME.profile.validpoint_balance
    },
    invalidpoint_balance() {
      if (this.ME.profile.invalidpoint_balance === null || this.ME.profile.invalidpoint_balance === undefined) return 0;
      return this.ME.profile.invalidpoint_balance
    }
  },
  methods: {
    getImgUrl(url) {
      return "https://www.pingo.jp/mediafiles/" + url;
    },
    draw_charts() {
      var options = {
        chart: {
          height: 280,
          type: "radialBar",
        },

        series: [this.validpoint_percentage],
        colors: ["#20E647"],
        plotOptions: {
          radialBar: {
            hollow: {
              margin: 0,
              size: "70%",
              background: "#293450"
            },
            track: {
              dropShadow: {
                enabled: true,
                top: 2,
                left: 0,
                blur: 4,
                opacity: 0.15
              }
            },
            dataLabels: {
              name: {
                offsetY: -10,
                color: "#fff",
                fontSize: "13px"
              },
              value: {
                color: "#fff",
                fontSize: "30px",
                show: true
              }
            }
          }
        },
        fill: {
          type: "gradient",
          gradient: {
            shade: "dark",
            type: "vertical",
            gradientToColors: ["#87D4F9"],
            stops: [0, 100]
          }
        },
        stroke: {
          lineCap: "round"
        },
        labels: ["Valid points"]
      };

      var chart = new ApexCharts(document.querySelector("#chart"), options);

      chart.render();
    },
  }
}
</script>

<template>
  <div>
    <PageHeader :title="page_title" :items="items"/>
    <div id="chart"></div>

    <div class="row">
      <div class="col-lg-4 col-xs-6">
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
                    </span> <br> <span class="text-nowrap">Since last month</span></p></div>
              <div class="avatar-sm">
                <span class="avatar-title bg-soft-primary rounded">
                <i class="fe-users font-20 text-primary"></i></span>
              </div>
            </div>
          </div>
        </div>

      </div>
      <div class="col-lg-4 col-xs-6">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h5 title="Campaign Sent" class="text-muted font-weight-normal mt-0 text-truncate">Valid Points</h5>
                <h3 class="my-2 py-1">
                  <span data-plugin="counterup">{{ validpoint_balance | currency("¥") }}</span></h3>
                <p class="mb-0 text-muted"><span class="text-success mr-2">
                  <span class="mdi mdi-arrow-up-bold"></span>
                       {{ invalidpoint_balance | currency("¥") }}
                    </span> <br> <span class="text-nowrap">Waiting for approval</span>
                </p>
              </div>
              <div class="avatar-sm">
                <span class="avatar-title bg-soft-primary rounded">
                <i class="fe-dollar-sign font-20 text-primary"></i></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ContributorRanking :rankings="rankings"/>
    <ViewProductRanking :viewproduct_rankings="viewproduct_rankings"/>
  </div>
</template>
