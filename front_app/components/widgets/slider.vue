<template>
  <div>
    <no-ssr>
      <section class="p-0">
        <div class="slide-1 home-slider">
          <div v-swiper:mySwiper="swiperOption">
            <div class="swiper-wrapper">
              <div class="swiper-slide">
                <div class="home  text-center fit-image"
                     style="background-position: bottom right;"
                     v-bind:style="{ 'background-image': 'url(' + getItemImage(items[0]) + ')' }">
                  <div class="container" v-if="$device.isMobile">
                    <div class="row">
                      <div class="col">
                        <div class="slider-contain" style="text-align:left!important;">
                          <div style="margin-top:-50px!important;">
                            <h3 class=" theme-color">さぁ、みんなで</h3>
                            <h1 class=" theme-color" style="text-transform:none;font-size: 33px!important;">
                              PinGoしよう！</h1>
                            <h1 class=" theme-color" style="text-transform:none;font-size: 20px!important;">Happy Share,
                              Happy Turn</h1>
                            <h2 class=" theme-color pt-4">Start 2021</h2>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="container" v-else>
                    <div class="row">
                      <div class="col">
                        <div class="slider-contain">
                          <div>
                            <h3 class=" theme-color">さぁ、みんなで</h3>
                            <h1 class=" theme-color" style="text-transform:none;">
                              PinGoしよう！</h1>
                            <h1 class=" theme-color" style="text-transform:none;">Happy Share,
                              Happy Turn</h1>
                            <h2 class=" theme-color pt-4">Start 2021</h2>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="swiper-slide">
                <div class="home  text-center fit-image"
                     style="background-position: center;"
                     v-bind:style="{ 'background-image': 'url(' + getItemImage(items[1]) + ')' }">
                  <div class="container" v-if="!$device.isMobile">
                    <div style="position:absolute;margin-top: 5%;left: 20%;">
                      <img src="/images/banners/buyservices_3.png" style="width:60%;">
                    </div>
                    <div class="row">
                      <div class="col-6">
                        <div>
                          <img src="/images/banners/buyservices_1.png" style="max-width:350px;margin-top: 35%;">
                        </div>
                      </div>
                      <div class="col-6">
                        <div>
                          <img src="/images/banners/buyservices_2.png" style="max-width:350px;margin-top: 35%;">
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="container" v-else>
                    <div style="position:absolute;margin-top: 15%;left: 10%;">
                      <img src="/images/banners/buyservices_3.png" style="width:80%;">
                    </div>
                    <div class="row">
                      <div class="col-6">
                        <div>
                          <img src="/images/banners/buyservices_1.png" style="width:100%;margin-top: 140%;">
                        </div>
                      </div>
                      <div class="col-6">
                        <div>
                          <img src="/images/banners/buyservices_2.png" style="width:100%;margin-top: 100%;">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="swiper-slide">
                <div class="home  text-center fit-image"
                     style="background-position: center;"
                     v-bind:style="{ 'background-image': 'url(' + getItemImage(items[2]) + ')' }">
                  <div class="container">
                    <div class="row">
                      <div class="col">
                        <div class="slider-contain" style="text-align:left!important;" v-if="$device.isMobile">
                          <div style="margin-top:-50px!important;">
                            <h1 style="text-transform:none;" class="text-white">{{ items[2].title }}</h1>
                            <h1 class="text-white">{{ items[2].subtitle }}</h1>
                            <h2 style="text-transform:none;" class="text-white line-height-4 pt-3">{{
                                items[2].text1
                              }}</h2>
                            <a href="/page/recruiting" class="btn btn-solid "
                               style="border: 2px solid #f7f0f0!important">詳細はこちらへ</a>
                          </div>
                        </div>

                        <div class="slider-contain" style="text-align:left!important;" v-else>
                          <div style="margin-top:-50px!important;">
                            <h1 style="text-transform:none;" class="text-white">{{ items[2].title }}</h1>
                            <h1 class="text-white">{{ items[2].subtitle }}</h1>
                            <h2 style="text-transform:none;" class="text-white pt-3">{{ items[2].text1 }}</h2>
                            <a href="/page/recruiting" class="btn btn-solid "
                               style="border: 2px solid #f7f0f0!important">詳細はこちらへ</a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div slot="pagination" class="swiper-pagination"></div>
          </div>
        </div>
      </section>
    </no-ssr>

    <!-- Home slider end -->
  </div>
</template>
<style scoped>
.fit-image {
  background-size: cover !important;
  background-repeat: no-repeat !important;
}

.height_130 {
  height: 130vh !important
}

.height_45 {
  height: 45vh !important
}
</style>
<script>
import NoSSR from 'vue-no-ssr'
// import VideoPlayer from 'nuxt-video-player'
// require('nuxt-video-player/src/assets/css/main.css')


export default {
  name: "slider",
  data() {
    return {
      swiperOption: {
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
        slidesPerView: 1,
        loop: true,
        pagination: {
          el: '.swiper-pagination',
          clickable: true,
        },
      },
      items: [
        {
          imagepath_pc: '/images/banners/top_slider_1.jpg',
          imagepath_mobile: '/images/banners/top_slider_1.jpg',
          // imagepath_pc: require('@/assets/images/banners/happyshare.jpg'),
          // imagepath_mobile: require('@/assets/images/banners/happyshare_mobile.jpg'),
          // title: 'Pingo.jp',
          // subtitle: 'START 2021',
          alignclass: 'p-left'
        },
        {
          imagepath_pc: '/images/banners/buyservices_bg.jpg',
          imagepath_mobile: '/images/banners/buyservices_bg.jpg',
          title: 'Happy Share Happy Turn.',
          subtitle: 'さあ、PinGoしよう！',
          alignclass: 'p-left'
        },
        {
          imagepath_pc: require('@/assets/images/parallax/recruit_1.jpg'),
          imagepath_mobile: require('@/assets/images/parallax/recruit_1.jpg'),
          title: 'PinGo',
          subtitle: 'パートナー募集',
          text1: 'PinGoを一緒に広めてくれる仲間を募集します！',
        }
      ],
    }
  },

  components: {
    'no-ssr': NoSSR,
    // VideoPlayer
  },
  methods: {
    getItemImage(item) {
      if (this.$device.isDesktop) {
        return item.imagepath_pc;
      } else if (this.$device.isMobile) {
        return item.imagepath_mobile;
      }
    }
  }
}
</script>
