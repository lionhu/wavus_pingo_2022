<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "SuperAdmin_unapproveduserpoints_summary",
  components: {
    apexchart: () => import("vue-apexcharts"),
  },
  props: ["unapprovedpoints_data", "header_title", "title"],
  data() {
    return {}
  },
  watch: {
    unapprovedpoints_data(newVal, oldVal) {
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
    TranslatedLabels(data){
      let vm=this;
      let new_data=data.map(item =>{
        item.name=vm.$t(`menuitems.ecommerce.points.type.${item.name}`)
        return item
      })
      return new_data;
    },
    refresh_chart() {
      if (this.unapprovedpoints_data.data !== undefined) {
        var translated_data=this.TranslatedLabels(this.unapprovedpoints_data.data);
        console.log(translated_data)
        const chart_data = translated_data;
        const chart_labels =this.unapprovedpoints_data.labels;
        var options = {
          series: chart_data,
          chart: {
            type: 'bar',
            height: 350,
            stacked: true,
          },
          plotOptions: {
            bar: {
              horizontal: false,
            },
          },
          stroke: {
            width: 1,
            colors: ['#fff']
          },
          title: {
            text: this.title
          },
          xaxis: {
            categories: chart_labels,
            labels: {
              formatter: function (val) {
                return val
              }
            }
          },
          yaxis: {
            title: {
              text: undefined
            },
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return val
              }
            }
          },
          fill: {
            type: 'gradient',
          },
          legend: {
            position: 'bottom',
            horizontalAlign: 'left',
            offsetX: 40
          },
          // labels: chart_labels
        };

        var chart = new ApexCharts(document.querySelector("#unapproveduserchart"), options);
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
      <div id="unapproveduserchart"></div>
    </div>
  </div>
</template>
