<script>
import {mapGetters} from "vuex"
import {APIServices} from "@/helpers/APIs";
import {swalService} from "@/helpers/swal.service";
import Swal from "sweetalert2";

export default {
  name: "system_category_setting",
  components: {
    Switches: () => import('vue-switches'),
    "el-tree": () => import('element-ui/lib/tree'),
    "el-button": () => import('element-ui/lib/button')
  },
  data() {
    return {};
  },
  computed: {
    ...mapGetters({}),
  },
  mounted() {
  },
  methods: {
    clear_cache() {
      Swal.fire({
        title: '重要',
        html: "サーバーのキャッシュを全てクリアしますか",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'はい, 削除!',
        showLoaderOnConfirm: true,
      }).then((result) => {
        if (result.isConfirmed) {
          APIServices.post("backend/system/reset_redis/")
            .then(APIServices.handleResponse)
            .then(response => {
              swalService.showToast("success", "Redis Cache Reset!")
            })
        }
      })
    }
  }
};
</script>
<template>
  <div>

    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h5>サーバーキャッシュ　リセット:</h5>
            <div class="row mb-2">
              <div class="col-sm-6 col-xs-12">
                <a href="javascript:void(0);" class="btn btn-danger mb-2" @click="clear_cache"><i
                  class="mdi mdi-plus-circle mr-1"></i> リセット
                </a>
                  <p class="text-muted">商品情報変更、注文情報の変更など、うまく反映しない場合、一旦キャッシュをクリアしたら、ほとんど反映できるようになります。</p>
              </div>
              <div class="col-sm-6 col-xs-12">
                <div class="float-sm-right">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
