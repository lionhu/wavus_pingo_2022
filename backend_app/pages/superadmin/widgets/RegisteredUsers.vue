<script>
import {mapState} from 'vuex'
import {axios} from "@/plugins/axios"
import VueApexCharts from "vue-apexcharts";

export default {
  name: "SuperAdmin_users_summary",
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
  // async asyncData({params}) {
  //   if (parseInt(params.id) > 0) {
  //     let url = `/back/store/api/products/${params.id}/`
  //     let productDetail = await axios.$get(url).then((response) => {
  //       if (response.result) {
  //         return response.data
  //       } else {
  //         window.location.href = "/"
  //       }
  //     })
  //     return {getDetail: productDetail}
  //   }
  //   window.location.href = "/"
  // },
  mounted() {
    let vm = this;
    console.log("mounted sync data")
    let url = "/apiauth/users/register_summary/";
    axios.post(url).then(response => {
      console.log("response.data.data", response.data.data)
      if (response.data.result) {

        var json_data = JSON.parse(response.data.data.json)
        vm.visitlogs = json_data.reduce(function (result, log) {
          result.labels.push(log.registered_date.split("T")[0]);
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
            text: `user registed trend (${response.data.data.source})`,
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
      <h5>User Register History</h5>

      <apexchart class="apex-charts" type="area" height="160" :series="series" :options="options"></apexchart>
    </div>
  </div>
</template>
