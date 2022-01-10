<script>
import {mapState} from 'vuex'
import ApexCharts from 'apexcharts'

export default {
  name: "backend_CSA_contribution",
  props:["rankings"],
  components: {
  },
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
    this.draw_ranking();
  },
  methods: {
    draw_ranking() {
      let rankinglist = this.rankings.reduce((result, current) => {
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
          text: "Most contribute members",
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
    <div class="row">
      <div class="col-xs-12 col-lg-4">
        <div class="card">
          <div class="card-body">
            <div id="ranking"></div>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-lg-8">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive">
              <h5 class="text-muted font-weight-normal mt-0 text-truncate">Contributor Member Ranking</h5>
              <table class="table mb-0">
                <thead>
                <tr>
                  <th>#</th>
                  <th class="text-center">Name</th>
                  <th>Points</th>
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
</template>
