<script>
import {mapState} from 'vuex'
import {axios} from "@/plugins/axios"

export default {
  name: "SuperAdmin_visitlog_summary",
  components: {
    apexchart: () => import("vue-apexcharts"),
  },
  data() {
    return {
      options: {},
      series: [],
      source: "",
      total: 0
    }
  },
  mounted() {
    let vm = this;
    let url = "/apiauth/logins/history_summary/";
    axios.post(url).then(response => {
      if (response.data.result) {

        var json_data = JSON.parse(response.data.data.json_login_summary)
        vm.visitlogs = json_data.reduce(function (result, log) {
          result.labels.push(log.visit_date.split("T")[0]);
          result.series.push(result.total + log.count)
          result.total += log.count;
          return result
        }, {"labels": [], "series": [], "total": 0})

        vm.source = response.data.data.source;
        vm.total = vm.visitlogs.total;
        vm.series = [{
          name: 'series-1',
          data: vm.visitlogs.series
        }]
        vm.options = {
          chart: {
            height: 250,
            type: 'line',
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'straight'
          },
          title: {
            text: `Visit Logs Last Month (${response.data.data.source})`,
            align: 'left'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            categories: vm.visitlogs.labels
          }
        }
        vm.total = vm.visitlogs.total;

      }
    })
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
      <h5>Visit Summary</h5>
      <apexchart class="apex-charts" type="area" height="160" :series="series" :options="options"></apexchart>
    </div>
  </div>
</template>
