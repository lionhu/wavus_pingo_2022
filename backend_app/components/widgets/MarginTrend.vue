<script>
import {mapState} from 'vuex'
import ApexCharts from 'apexcharts'

export default {
  name: "clientadmin_margin_trend",
  props: ["trend_data"],
  data() {
    return {}
  },
  watch: {
    trend_data(newVal, oldVal) {
      let options = {
        chart: {
          height: 350,
          type: 'bar',
        },
        plotOptions: {
          bar: {
            borderRadius: 10,
            dataLabels: {
              position: 'top', // top, center, bottom
            },
          }
        },
        dataLabels: {
          enabled: true,
          // formatter: function (val) {
          //   return val + "%";
          // },
          offsetY: -20,
          style: {
            fontSize: '12px',
            colors: ["#304758"]
          }
        },
        series: [{
          name: 'Trend',
          data: newVal.datasets[0].data
        }],
        xaxis: {
          categories: newVal.labels,
          position: 'top',
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          crosshairs: {
            fill: {
              type: 'gradient',
              gradient: {
                colorFrom: '#D8E3F0',
                colorTo: '#BED1E6',
                stops: [0, 100],
                opacityFrom: 0.4,
                opacityTo: 0.5,
              }
            }
          },
          tooltip: {
            enabled: true,
          }
        },
        // yaxis: {
          // axisBorder: {
          //   show: false
          // },
          // axisTicks: {
          //   show: false,
          // },
          // labels: {
          //   show: false,
          //   formatter: function (val) {
          //     return val + "%";
          //   }
          // }

        // },
        title: {
          text: 'ポイント獲得状況',
          floating: true,
          offsetY: 330,
          align: 'center',
          style: {
            color: '#444'
          }
        }
      }
      var chart = new ApexCharts(document.querySelector("#margin_trend_chart"), options);

      chart.render();
    }
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
      <div id="margin_trend_chart"/>
    </div>
  </div>

</template>
