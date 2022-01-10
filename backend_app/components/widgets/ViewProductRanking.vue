<script>
import {mapState} from 'vuex'
import ApexCharts from 'apexcharts'

export default {
  name: "backend_component_viewproduct_ranking",
  props:["viewproduct_rankings"],
  components: {
    apexchart: ApexCharts
  },
  data() {
    return {
      rankings: [],
      // series: [44, 55, 41, 17, 15],
      // chartOptions: {
      //   chart: {
      //     width: 380,
      //     type: 'donut',
      //   },
      //   plotOptions: {
      //     pie: {
      //       startAngle: -90,
      //       endAngle: 270
      //     }
      //   },
      //   dataLabels: {
      //     enabled: false
      //   },
      //   fill: {
      //     type: 'gradient',
      //   },
      //   legend: {
      //     formatter: function (val, opts) {
      //       return val + " - " + opts.w.globals.series[opts.seriesIndex]
      //     }
      //   },
      //   title: {
      //     text: 'Gradient Donut with custom Start-angle'
      //   },
      //   responsive: [{
      //     breakpoint: 480,
      //     options: {
      //       chart: {
      //         width: 200
      //       },
      //       legend: {
      //         position: 'bottom'
      //       }
      //     }
      //   }]
      // },
    }
  },
  mounted() {
    let vm = this;
    if (this.viewproduct_rankings.length){
          vm.draw_viewproducts_chart()
    }
  },
  computed: {
    ...mapState({
      ME: state => state.auth.user
    }),
  },
  methods: {

    getImgUrl(url) {
      return "https://www.pingo.jp/mediafiles/" + url;
    },
    draw_viewproducts_chart() {
      console.log("this.viewproduct_rankings", this.viewproduct_rankings)
      let rankinglist = this.viewproduct_rankings.reduce((result, current) => {
        result.data.push(current.count);
        result.series_name.push(current.product_name);
        return result;
      }, {data: [], series_name: []})


      let options = {
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
          text: 'Most Popular products',
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
      let chart = new ApexCharts(document.querySelector("#rankinglist"), options);

      console.log(options)
      console.log(chart)
      chart.render();
    },
  }
}
</script>

<template>

    <div class="row" v-if="viewproduct_rankings.length">
      <div class="col-xl-4 col-lg-4">
        <div class="card">
          <div class="card-body">
            <h2>Hello</h2>
   <div id="rankinglist"></div>
          </div>
        </div>
      </div>
      <div class="col-xl-8 col-lg-8">
        <div class="card">
          <div class="card-body">
            <div class="table-responsive">
              <h5 class="text-muted font-weight-normal mt-0 text-truncate">Most popular products</h5>
              <table class="table mb-0">
                <thead>
                <tr>
                  <th>#</th>
                  <th class="text-center"></th>
                  <th class="text-center">Product</th>
                </tr>
                </thead>
                <tbody>
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
</template>
