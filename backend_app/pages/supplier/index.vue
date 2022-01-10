<script>
import {mapGetters} from 'vuex'
import {APIServices} from "@/helpers/APIs";

export default {
  name: "backend_index",
  components: {
    PageHeader: () => import(/* webpackChunkName: "about" */ '~/components/Page-header'),
    ProfileCard: () => import(/* webpackChunkName: "about" */ '~/components/widgets/ProfileCard'),
  },
  middleware: 'router-auth',
  data() {
    return {
      title: "",
      items: [
        {text: "ベンダー"},
        {text: "ダッシュボード",active: true}
      ],
    }
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME",
      isSupplier:"authfack/isSupplier"
    })
  },
  mounted() {
    let self=this;
    if (this.isSupplier){
      APIServices.post("store/public/suppliers/retrieve_by_email/",{
        email:this.ME.email
      }).then(APIServices.handleResponse)
        .then(response=>{
          self.$store.commit("suppliers/set_supplier",response.supplier)
      })
    }
    // this.title = `${this.ME.vendor_info.name}`;
  }
}
</script>

<template>

  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row mt-3">
      <div class="col-md-6 col-xs-12">
        <ProfileCard/>
      </div>
    </div>
  </div>
</template>
