<template>
  <div>
    <section class="testimonial small-section">
      <div class="container">
        <div class="row" v-if="!$device.isMobile">
          <div class="col-sm-12">
            <div class="swiper-container swiper-container-initialized swiper-container-horizontal">
              <div class="swiper-wrapper testimonial-slider" style="transform: translate3d(0px, 0px, 0px);">
                <div class="swiper-slide swiper-slide-active" style="width: 1370px; margin-right: 20px;">
                  <div class="media">
                    <div class="media-body">
                      <h4>お問合せ窓口</h4>
                      <p>PinGoパートナー事業部</p>
                      <p>
                        担当:榑本（クレモト）
                        　　●電話:050-3697-9239　　●メール: crs@wavus.jp
                        　　●受付時間:平日10時~17時 (土・日・祝日休み)
                      </p>
                    </div>
                    <div class="text-center">
<!--                      <img src="images/icon/recuriting-04.png" alt="#"> <h5>PinGoパートナー事業部 </h5>-->
                      <!--                      <h6>営業代理店事業部</h6>-->
                    </div>
                  </div>
                </div>
              </div>
              <span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span></div>
          </div>
        </div>
        <div class="row" v-else>
          <div class="col-sm-12">
            <div class="swiper-container swiper-container-initialized swiper-container-horizontal">
              <div class="swiper-wrapper testimonial-slider" style="transform: translate3d(0px, 0px, 0px);">
                <div class="swiper-slide swiper-slide-active">
                  <div class="media">
                    <div class="text-center">
<!--                      <img src="images/icon/recuriting-04.png" alt="#">-->
                      <!--                      <h6>営業代理店事業部</h6>-->
                    </div>
                    <div class="media-body">
                      <h4>お問合せ窓口</h4>
                      <p>PinGo営業代理店事業部</p>
                      <p class="text-left">
                        ●担当:榑本（クレモト）
                      </p>
                      <p class="text-left">
                        ●電話:050-3697-9239
                      </p>
                      <p class="text-left">
                        ●メール: crs@wavus.jp
                      </p>
                      <p class="text-left">
                        ●受付時間:平日10時~17時 (土・日・祝日休み)
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<style scoped>
</style>
<script type="text/javascript">
export default {
  data() {
    return {
      imagepath: require('@/assets/images/parallax/recruit_1.jpg'),
      title: '2021',
      subtitle: '営業代理店募集'
    }
  }
}
</script>
