<template>
  <section class="section-t-space section-b-space p-t-0 ratio_40">
    <div class="container">
      <div class="row partition2">
        <div class="col-md-6" v-for="service in services">
          <a :href="service.url">
            <div class="collection-banner p-right text-center">
              <div class="img-part">
                <img v-prlx :src="service.imagepath_pc" alt=""
                     class="img-fluid bg-img"></div>
              <!--            <div class="contain-banner">-->
              <!--              <div><h4 class="text-white">50% off</h4>-->
              <!--                <h2>men</h2></div>-->
              <!--            </div>-->
            </div>
          </a>
        </div>
      </div>
    </div>
  </section>
</template>
<script>

import NoSSR from 'vue-no-ssr'

export default {
  name: "services",
  data() {
    return {
      services: [
        {
          imagepath_pc: '/images/banners/services_1.svg',
          imagepath_mobile: '/images/banners/happyshare_mobile.jpg',
          url: '/sharebuy/all',
          // title: 'Pingo.jp',
          // subtitle: 'START 2021',
          alignclass: 'p-left'
        },
        {
          imagepath_pc: '/images/banners/services_2.svg',
          imagepath_mobile: '/images/home-banner/1.jpg',
          url: '/tomobuy',
          // title: 'Happy Share Happy Turn.',
          // subtitle: 'さあ、PinGoしよう！',
          alignclass: 'p-left'
        }
      ]
    }
  },

  components: {
    'no-ssr': NoSSR
  },
  methods: {}
}
</script>
