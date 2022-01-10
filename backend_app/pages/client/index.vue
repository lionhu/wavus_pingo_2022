<script>
import {mapState} from 'vuex'
import ApexCharts from 'apexcharts'

export default {
  name: "backend_CA_index",
  components: {
    PageHeader: () => import(/* webpackChunkName: "about" */ '~/components/PageHeaderRole'),
    apexchart: ApexCharts,
    "PointSummaryTrend": () => import("~/components/widgets/PointSummary"),
    "MarginTrend": () => import("~/components/widgets/MarginTrend"),
    "countTo": () => import('vue-count-to'),
  },
  middleware: ['router-auth', 'router-clientadmin'],
  data() {
    return {
      items: [
        {text: 'PINGO'},
        {text: 'Dashboards',active: true}
      ],
      rankings: [],
      viewproduct_rankings: [],
      margins_trend: {},
      viewproduct_chart_data: {}
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
    let url = `/back/clientadmin/api/admin_dashboard/${this.ME.profile.user_id}/summary_info/`;
    console.log(url);
    this.$axios.post(url).then((response) => {
      console.log(response.data)
      console.log(JSON.parse(response.data.data.json_margin_top5))
      if (response.data.result) {
        vm.rankings = JSON.parse(response.data.data.json_margin_top5)
        vm.viewproduct_rankings = JSON.parse(response.data.data.json_viewproducts_top5)
        vm.margins_trend = response.data.data.margins_trend;
        vm.$store.commit("auth/update_user_profile", response.data.data.profile);
        vm.draw_charts();
        vm.draw_ranking();
        vm.draw_viewproducts_chart();
      }
    })
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user
    }),
    page_title() {
      return "ようこそ ! Clients Admin " + this.ME.username;
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
          height: 300,
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
        labels: ["有効ポイント"]
      };

      var chart = new ApexCharts(document.querySelector("#chart"), options);

      chart.render();
    },
    draw_viewproducts_chart() {
      console.log("this.viewproduct_rankings", this.viewproduct_rankings)
      var rankinglist = this.viewproduct_rankings.reduce((result, current) => {
        result.data.push(current.count);
        result.series_name.push(current.product_name);
        return result;
      }, {data: [], series_name: []})

      console.log("rankinglist", rankinglist);

      var options = {
        chart: {
          width: 380,
          type: 'donut',
        },
        series: rankinglist.data,
        labels: rankinglist.series_name,
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
          position: "bottom"
          // formatter: function (val, opts) {
          //   console.log("val",val);
          //   console.log("opts",opts);
          //   return val + " - " + opts.w.globals.series[opts.seriesIndex]
          // }
        },
        title: {
          text: '閲覧商品ランキング',
          align: "center"
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
      };
      var chart = new ApexCharts(document.querySelector("#viewproducts_ranking"), options);

      chart.render();
    },
    draw_ranking() {
      var rankinglist = this.rankings.reduce((result, current) => {
        result.data.push(current.sum);
        result.username.push(current.user_name);
        return result;
      }, {data: [], username: []})

      var chartOptions = {
        series: [
          {
            data: rankinglist.data
          }
        ],
        chart: {
          type: "bar",
          height: 230
        },
        plotOptions: {
          bar: {
            barHeight: "100%",
            distributed: true,
            horizontal: true,
            dataLabels: {
              position: "bottom"
            }
          }
        },
        colors: [
          "#90ee7e",
          "#f48024",
          "#69d2e7"
        ],
        dataLabels: {
          enabled: true,
          textAnchor: "start",
          style: {
            colors: ["#fff"]
          },
          formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val;
          },
          offsetX: 0,
          dropShadow: {
            enabled: true
          }
        },
        stroke: {
          width: 1,
          colors: ["#fff"]
        },
        xaxis: {
          categories: rankinglist.username
        },
        yaxis: {
          labels: {
            show: false
          }
        },
        title: {
          text: "貢献度ランキング",
          align: "center",
          floating: true
        },
        subtitle: {
          text: "Most powerful members supporting you",
          align: "center"
        },
        tooltip: {
          theme: "dark",
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function () {
                return "";
              }
            }
          }
        }
      };
      var chart = new ApexCharts(document.querySelector("#ranking"), chartOptions);

      chart.render();
    }
  }
}
</script>

<template>
  <div>
    <PageHeader :title="page_title" :items="items" role="client_admin"/>
    <div class="row">
      <div class="col-md-4">
        <div class="widget-rounded-circle card">
          <div class="card-body">
            <div class="row">
              <div class="col-6">
                <div class="avatar-lg rounded-circle bg-icon-success">
                  <i class="ri-auction-fill font-24 avatar-title text-white"></i>
                </div>
              </div>
              <div class="col-6">
                <div class="text-right">
                  <h3 class="text-dark mt-1">
                                    <span>
                                        <countTo :end-val="validpoint_balance" :duration="1500"></countTo>
                                    </span>
                  </h3>
                  <p class="text-muted mb-1 text-truncate">有効ポイント</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="widget-rounded-circle card">
          <div class="card-body">
            <div class="row">
              <div class="col-6">
                <div class="avatar-lg rounded-circle bg-icon-warning">
                  <i class="ri-coin-fill font-24 avatar-title text-white"></i>
                </div>
              </div>
              <div class="col-6">
                <div class="text-right">
                  <h3 class="text-dark mt-1">
                                    <span>
                                        <countTo :end-val="invalidpoint_balance" :duration="1500"></countTo>
                                    </span>
                  </h3>
                  <p class="text-muted mb-1 text-truncate">承認待ちポイント</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="widget-rounded-circle card">
          <div class="card-body">
            <div class="row">
              <div class="col-6">
                <div class="avatar-lg rounded-circle bg-icon-primary">
                  <i class="ri-folder-user-line font-24 avatar-title text-white"></i>
                </div>
              </div>
              <div class="col-6">
                <div class="text-right">
                  <h3 class="text-dark mt-1">
                    <span><countTo :end-val="ME.profile.get_descendants_count" :duration="1500"></countTo></span>
                  </h3>
                  <p class="text-muted mb-1 text-truncate">フォロワー人数</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <MarginTrend :trend_data="margins_trend"/>
      </div>
      <div class="col-md-6">
        <div id="chart"></div>
      </div>
    </div>

    <div class="row">
      <div class="col-xl-4 col-lg-4">
        <div class="card">
          <div class="card-body">
            <div id="ranking"></div>
          </div>
        </div>
      </div>
      <div class="col-xl-8 col-lg-8">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive">
              <h5 class="text-muted font-weight-normal mt-0 text-truncate">貢献度ランキング</h5>
              <small class="text-muted">* 消費したポイントは含まれていないです。現時点持っているポイントより大きいです。</small>
              <table class="table mb-0">
                <thead>
                <tr>
                  <th>#</th>
                  <th class="text-center">ユーザー名</th>
                  <th>貢献ポイント総数</th>
                </tr>
                </thead>
                <tbody v-if="rankings.length">
                <tr v-for="(ranking,index) in rankings" :key="index">
                  <th scope="row">{{ index + 1 }}</th>
                  <td class="text-center">{{ ranking.user_name }}</td>
                  <td class="text-right">{{ ranking.sum|currency("¥") }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-xl-4 col-lg-4">
        <div class="card">
          <div class="card-body">
            <div id="viewproducts_ranking">
              <!--              <apexchart type="donut" width="380" :options="viewproduct_chart_data.chartOptions" :series="viewproduct_chart_data.series"></apexchart>-->
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-8 col-lg-8">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive">
              <h5 class="text-muted font-weight-normal mt-0 text-truncate">閲覧商品ランキング</h5>
              <table class="table mb-0 ">
                <thead>
                <tr>
                  <th>#</th>
                  <th class="text-center"></th>
                  <th class="text-center">商品名</th>
                </tr>
                </thead>
                <tbody v-if="viewproduct_rankings.length">
                <tr v-for="(ranking,index) in viewproduct_rankings" :key="index">
                  <th scope="row">{{ index + 1 }}</th>
                  <td class="text-center">
                    <img :src="getImgUrl(ranking.url)" style="max-width:80px" alt="">
                  </td>
                  <td class="text-center">{{ ranking.product_name }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
