<script>
import {mapState} from 'vuex'
import {APIServices} from "@/helpers/APIs";
import {swalService} from "@/helpers/swal.service";

export default {
  name: "backend_operations",
  components: {
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapState({
    })
  },
  mounted() {
    console.log("operations",this.$route.query)
    if (Object.keys(this.$route.query).includes("type")){
      switch (this.$route.query.type){
        case "comment":
          this.approve_comment(this.$route.query.comment_id,this.$route.query.approved)
      }
    }
  },
  methods:{
    async approve_comment(comment_id,approved){
      this.$nuxt.$loading.start();
      let url=`https://www.pingo.jp/daphne/api/store/public/comments/${comment_id}/approve/?query=${approved}`
      await APIServices.get(url).then(APIServices.handleResponse)
      .then(response=>{
        swalService.showModal("コメント承認状況",`ID:${comment_id}, Approved:${approved}`,"success","center")
      })

      this.$nuxt.$loading.finish();
    }
  }
}
</script>

<template>
  <div>
  </div>
</template>
