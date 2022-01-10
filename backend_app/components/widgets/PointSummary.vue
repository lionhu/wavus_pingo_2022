<script>
import {mapState} from 'vuex'
import {axios} from "@/plugins/axios"

export default {
  name: "SuperAdmin_point_summary",
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
  created() {
    let url = "/back/store/api/margins/summary/"
    let vm = this;
    axios.post(url).then(response => {
      console.log("response.data.data", response.data.data)
      if (response.data.result) {

        var json_data = JSON.parse(response.data.data.json)
        vm.visitlogs = json_data.reduce(function (result, log) {
          result.labels.push(log.occur_date.split("T")[0]);
          result.series.push(result.total + log.total)
          result.total += log.total;
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
            type: 'area',
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
            text: `Valid points trend (${response.data.data.source})`,
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
    point_balance() {
      if (this.ME.profile.point_balance === null || this.ME.profile.point_balance === undefined) return 0;
      return this.ME.profile.point_balance
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
}
</script>

<template>
  <div class="row">
    <div class="col-xs-12 col-md-6">
      <div class="card">
        <div class="card-body">
          <div class="d-flex justify-content-between">
            <div>
              <h5 title="Campaign Sent" class="text-muted font-weight-normal mt-0 text-truncate">有効なポイント</h5>
              <h3 class="my-2 py-1">
                <span data-plugin="counterup">{{ this.ME.profile.validpoint_balance | currency("¥") }}</span></h3>
              <p class="mb-0 text-muted"><span class="text-success mr-2">
                  <span class="mdi mdi-arrow-up-bold"></span>
                       {{ invalidpoint_balance | currency("¥") }}
                    </span> <span class="text-nowrap">承認待ち</span></p></div>
            <div class="avatar-sm">
                <span class="avatar-title bg-soft-primary rounded">
                <i class="fe-dollar-sign font-20 text-primary"></i></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-xs-12 col-md-6">
      <div class="card">
        <div class="card-body">

          <apexchart class="apex-charts" type="area" height="160" :series="series" :options="options"></apexchart>

        </div>
      </div>
    </div>
  </div>

</template>
