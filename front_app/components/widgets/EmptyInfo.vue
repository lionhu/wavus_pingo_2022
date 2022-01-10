<template>
  <div class="row">
    <div class="col-sm-12">
      <div class="text-center section-t-space section-b-space">
        <img src='/images/empty-search.jpg' class="img-fluid" alt/>
        <h3 class="mt-3">{{ message }}</h3>
        <div class="col-12 mt-3">
          <nuxt-link :to="{ path: redirect_url}" class="btn btn-outline">{{ buttonText }}</nuxt-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  name: "empty_info",
  props: ["message","buttonText","redirect_url"],
  data() {
    return {
    };
  },
  components: {
  },

}
</script>

