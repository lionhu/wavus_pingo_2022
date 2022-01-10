<script>

// import {axios} from "@/plugins/axios"

export default {
  name: "logistic_edit",
  props: ["logistic", "showModal", "mode"],
  components: {
    Switches: () => import('vue-switches'),
  },
  data() {
    return {
      local_logistic: {},
      errors: []
    }
  },
  watch: {
    logistic(val, oldval) {
      console.log("logistic", val, oldval)
      if (val !== null) {
        this.local_logistic.id = val.id;
        this.local_logistic.company = val.company;
        this.local_logistic.short_name = val.short_name;
        this.local_logistic.is_valid = val.is_valid;
        this.local_logistic.track_link = val.track_link;
      } else {
        console.log("add")
        this.local_logistic = {
          id: 0,
          company: "",
          short_name: "",
          is_valid: false,
          track_link: ""
        }
      }
    }
  },
  methods: {
    pre_check() {
      this.errors = [];
      if (this.local_logistic.company === "") this.errors.push("会社名が必要です。");
      if (this.local_logistic.short_name === "") this.errors.push("略称が必要です。");
      if (this.local_logistic.track_link === "") this.errors.push("追跡リンクが必要です。");
      console.log("precheck; ", this.errors.length === 0)
      return this.errors.length === 0
    },
    updateLogisticInfo() {
      console.log("pre_check", this.pre_check())
      if (this.pre_check()) {
        if (this.mode === "edit" && this.local_logistic.id) {
          this.$store.dispatch("logistics/updateLogistic", {
            logistic_id: this.local_logistic.id,
            info: this.local_logistic
          });
        }
      } else {
        delete this.local_logistic.id;
        this.$store.dispatch("logistics/createLogistic", this.local_logistic)
      }
      this.errors = [];
      this.$emit("closeModal", {
        mode: this.mode,
        logistic: this.local_logistic,
        result: true
      })
    }

  }
}
</script>

<template>
  <b-modal id="modal-edit-logistic"
           scrollable title="物流会社情報"
           title-class="font-18"
           body-class="p-4"
           hide-footer
           v-if="showModal"
  >
    <form @submit.prevent="updateLogisticInfo">
      <ul v-if="errors.length" class="text-danger">
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-name" class="control-label">会社名
              <span class="text-danger">*</span>
            </label>
            <input type="text" id="field-name" v-model="local_logistic.company" class="form-control"/>

          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-name" class="control-label">略称
              <span class="text-danger">*</span>
            </label>
            <input type="text" id="field-short_name" v-model="local_logistic.short_name" class="form-control"/>

          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-name" class="control-label">追跡リンク
              <span class="text-danger">*</span>
            </label>
            <input type="text" id="field-track_link" v-model="local_logistic.track_link" class="form-control"/>

          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="form-group">
            <label for="field-is_valid" class="control-label">有効化
              <span class="text-danger">*</span>
            </label> <br>
            <switches v-model="local_logistic.is_valid" id="field-is_valid" type-bold="false"
                      color="warning" class="ml-1 mb-0"></switches>

          </div>
        </div>
      </div>
      <div class="form-group row">
        <div class="col-8 offset-4">
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="reset" class="btn btn-secondary m-l-5 ml-1" @click="$emit('closeModal',{})">Cancel</button>
        </div>
      </div>
    </form>

  </b-modal>

</template>
