<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "SuperAdmin_userpointbank_summary",
  components: {
    apexchart: () => import("vue-apexcharts"),
  },
  props: ["user_ranking", "header_title", "title"],
  data() {
    return {}
  },
  watch: {
    unapprovedpoints_data(newVal, oldVal) {
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
      if (this.user_ranking !== undefined) {
        const chart_data = this.user_ranking.data;
        const chart_labels = this.user_ranking.labels
        var options = {
          series:[{
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
            colors: ['#33b2df', '#546E7A', '#d4526e', '#13d8aa', '#A5978B', '#2b908f', '#f9a3a4', '#90ee7e',
              '#f48024', '#69d2e7'
            ],
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
              categories: chart_labels,
            },
            yaxis: {
              labels: {
                show: false
              }
            },
            title: {
                text: '*承認済み、お客様が買い物に使えるポイント。',
                align: 'left',
                floating: true
            },
            fill:{
            type: 'gradient',
            },
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

        var chart = new ApexCharts(document.querySelector("#userpointbank"), options);
        chart.render();
      }
    }
  },
}
</script>

<template>
  <div className="card">
    <div className="card-body">
      <h5>
        {{ header_title }}
        <nuxt-link to="/superadmin/pointbanks" class="btn btn-rounded btn-outline-info inline-block float-right btn-sm">Details</nuxt-link>
      </h5>
      <div id="userpointbank"></div>
    </div>
  </div>
</template>
