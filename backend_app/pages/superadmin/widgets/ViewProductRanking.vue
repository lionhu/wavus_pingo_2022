<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "SuperAdmin_viewproduct_summary",
  components: {
    // apexchart: () => import("vue-apexcharts"),
  },
  props: ["viewproduct_summary", "header_title", "title"],
  data() {
    return {}
  },
  watch: {
    viewproduct_summary(newVal, oldVal) {
      console.log("newVal, oldVal", newVal, oldVal)
      if (newVal !== undefined) {
        this.refresh_chart();
      }
    }
  },
  mounted() {
    this.refresh_chart();
  },
  methods: {
    refresh_chart() {
      if (this.viewproduct_summary.data !== undefined) {
        var chart_data = this.viewproduct_summary.data
        var chart_labels = this.viewproduct_summary.labels;

        var chartOptions = {
          series: [{
            data: chart_data
          }],
          chart: {
            type: 'bar',
            height: 380
          },
          plotOptions: {
            bar: {
              barHeight: '100%',
              distributed: true,
              horizontal: true,
              dataLabels: {
                position: 'bottom'
              },
            }
          },
          legend: {
            show: false,
          },
          dataLabels: {
            enabled: true,
            textAnchor: 'start',
            style: {
              colors: ['#fff']
            },
            formatter: function (val, opt) {
              return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
            },
            offsetX: 0,
            dropShadow: {
              enabled: true
            }
          },
          stroke: {
            width: 1,
            colors: ['#fff']
          },
          xaxis: {
            categories: this.viewproduct_summary.labels,
          },
          yaxis: {
            labels: {
              show: false
            }
          },
          title: {
            text: this.header_title,
            align: 'center',
            floating: true
          },
          // subtitle: {
          //   text: 'Category Names as DataLabels inside bars',
          //   align: 'center',
          // },
          tooltip: {
            theme: 'dark',
            x: {
              show: false
            },
            y: {
              title: {
                formatter: function () {
                  return ''
                }
              }
            }
          }
        }

        var chart = new ApexCharts(document.querySelector("#vieproduct_chart"), chartOptions);
        chart.render();
      }
    }
  },
}
</script>

<template>
  <div class="card">
    <div class="card-body">
      <h5>{{ header_title }}</h5>
      <div id="vieproduct_chart"></div>
    </div>
  </div>
</template>
