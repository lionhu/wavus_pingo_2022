<script>
import {VueSimplebar} from 'vue-simplebar'
import {axios} from "@/plugins/axios"
import {swalService} from "~/helpers/swal.service"

export default {
  data() {
    return {
      config: {
        handler: this.handleRightBarClick,
        middleware: this.middleware,
        events: ["click"]
      },
    };
  },
  methods: {
    handleRightBarClick(e, el) {
      this.$parent.hideRightSidebar();
    },
    middleware(event, el) {
      return !event.target.classList.contains("toggle-right");
    },
    reset_rediscache() {
      axios.post("/back/store/api/system/reset_redis/").then((res) => {
        if (res.data.result) {
          swalService.showToast("success", "Redis Cached was refreshed!","top-start")
        } else {
          console.log(res.data.error_message)
          swalService.showToast("error", "Redis Cached was failed","top-start")
        }
      })
    },
    backup_db(){
      axios.post("/back/store/api/system/backup_db/").then((res) => {
        if (res.data.result) {
          swalService.showToast("success", "DB was backuped!","top-start")
        } else {
          console.log(res.data.error_message)
          swalService.showToast("error", "Failed to backup_db database","top-start")
        }
      })
    }
  },

  components: {
    VueSimplebar
  },
};
</script>

<template>
  <div>
    <!-- Right Sidebar -->
    <div class="right-bar" v-click-outside="config">
      <vue-simplebar class="h-100">
        <b-tabs content-class="pt-0" justified class="nav-bordered">
          <b-tab active>
            <template v-slot:title>
              <i class="mdi mdi-cog-outline d-block font-22 my-1"></i>
            </template>

            <h6 class="font-weight-medium px-3 m-0 py-2 font-13 text-uppercase bg-light">
              <span class="d-block py-1">Theme Settings</span>
            </h6>

            <div class="p-3">

              <button class="btn btn-danger btn-block mt-4" id="resetBtn" @click="reset_rediscache()">
                Reset Redis Cache
              </button>
            </div>
            <div class="p-3">

              <button class="btn btn-danger btn-block mt-4" id="backupBtn" @click="backup_db()">
                Backup DB
              </button>
            </div>
          </b-tab>
        </b-tabs>
        <!-- Nav tabs -->
      </vue-simplebar>
      <!-- end slimscroll-menu-->
    </div>
    <!-- /Right-bar -->

    <!-- Right bar overlay-->
    <div class="rightbar-overlay"></div>
  </div>
</template>
