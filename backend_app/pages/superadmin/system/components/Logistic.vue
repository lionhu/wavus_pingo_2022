<script>
import {mapGetters} from "vuex"

export default {
  name: "system_logistic_setting",
  components: {
    "el-table": () => import('element-ui/lib/table'),
    "el-table-column": () => import('element-ui/lib/table-column'),
    Switches: () => import('vue-switches'),
    LogisticModal: () => import('../../components/LogisticModal'),
  },
  data() {

    return {
      mode: "add",
      logistic: {},
      showModal: false,
    };
  },
  computed: {
    ...mapGetters({
      menuitems_store: "categories/getterCategoryList",
      logistics: "logistics/getterLogistics"
    }),
  },
  mounted(){
    this.$store.dispatch("logistics/load_Logistic_list")
  },
  methods: {
    show_logistic_edit(logistic) {
      this.mode = "edit";
      this.logistic = logistic;
      this.showModal = true;
    },
    closeModal(info) {
      console.log(info);
      this.showModal = false;
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
            <h5>物流会社:</h5>
            <el-table
              :data="logistics"
              style="width: 100%"
            >
              <el-table-column label="ID" width="80" sortable prop="id">
              </el-table-column>
              <el-table-column
                label="会社名"
                sortable
                width="160"
                prop="company">
                <template slot-scope="scope">
                  {{ scope.row.company }} <br>
                  ({{ scope.row.short_name }} )
                </template>
              </el-table-column>
              <el-table-column label="追跡リンク" prop="track_link">
              </el-table-column>
              <el-table-column label="有効性" width="80">
                <template slot-scope="scope">
                  {{ scope.row.is_valid }}
                </template>
              </el-table-column>
              <el-table-column
                label="Action">
                <template slot-scope="scope">
                  <ul class="list-inline table-action m-0">
                    <li class="list-inline-item">
                      <a href="javascript:void(0);" v-b-modal:modal-edit-logistic @click="show_logistic_edit(scope.row)"
                         class="action-icon text-success">
                        <i class="fe-edit"></i>
                      </a>
                    </li>
<!--                    <li class="list-inline-item" v-if="!scope.row.is_paid">-->
<!--                      <a href="javascript:void(0);" class="action-icon text-danger"-->
<!--                         @click="removeOrder(scope.row.id)">-->
<!--                        <i class="fe-trash"></i></a>-->
<!--                    </li>-->
                  </ul>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </div>
    <LogisticModal :mode="mode" :logistic="logistic" :showModal="showModal" @closeModal="closeModal"/>
  </div>
</template>
