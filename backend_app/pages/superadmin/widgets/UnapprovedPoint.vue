<script>
import VueApexCharts from "vue-apexcharts";
export default {
  name: "SuperAdmin_unapprovedpoints_summary",
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
    TranslatedLabels(labels){
      let vm=this;
      let new_labels=labels.map(item =>{
        let dict_key=`menuitems.ecommerce.points.type.${item}`
        return vm.$t(dict_key)
      })
      return new_labels;
    },
    refresh_chart() {
      if (this.unapprovedpoints_data.data !== undefined){
        const chart_data = this.unapprovedpoints_data.data;
        const chart_labels = this.TranslatedLabels(this.unapprovedpoints_data.labels)
        var options = {
          series: chart_data,
          chart: {
            height: 350,
            type: 'donut',
          },
          plotOptions: {
            pie: {
              startAngle: -90,
              endAngle: 270
            }
          },
          labels: chart_labels,
          // dataLabels: {
          //   enabled: true,
          //   labels: chart_data.labels,
          // },
          fill: {
            type: 'gradient',
          },
          legend: {
            position:"bottom",
             horizontalAlign: 'left',
            formatter: function (val, opts) {
              return val + " - " + opts.w.globals.series[opts.seriesIndex]
            }
          },
          title: {
            text: this.title
          }
        };

        var chart = new ApexCharts(document.querySelector("#unapprovedchart"), options);
        chart.render();
      }
    }
  },
}
</script>

<template>
  <div class="card">
    <div class="card-body">
      <h5>
        {{ header_title }}
        <nuxt-link to="/superadmin/points" class="btn btn-rounded btn-outline-info inline-block float-right btn-sm">Details</nuxt-link>
      </h5>
      <div id="unapprovedchart"></div>
    </div>
  </div>
</template>
