<template>
  <div>
    <section v-inview:parent="'animate'">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 offset-lg-2">
            <div class="title3">

              <h4 :animate-toggle="'fadeInLeft'">Happy Share, Happy Turn.</h4>
              <!--              <h2 class="title-inner3" :animate-toggle="'fadeInUp'" v-if="$device.isMobile">PinGoとは？ </h2>-->
              <h2 class="title-inner3 pt-2" :animate-toggle="'fadeInUp'" style="text-transform:inherit;">
                {{ $t("pingo.about") }} </h2>
              <div class="line"></div>
            </div>
            <div class="about-text">
              <h4 class="line-height-2rem text-muted" :animate-toggle="'fadeInUp'">
                {{ $t("pingo.text") }}は世界中から選りすぐりの商品だけをみなさまにリーズナブルな価格でお届けするECサイトです。
                さらに、商品を使ってくれた人みんなに幸せが戻って来るしくみ。<span
                class="theme-color font-weight-bold text-center">それが{{ $t("pingo.text") }}なのです!</span>
              </h4>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="pb-0 ratio2_1" v-inview:parent="'animate'">
      <div class="container">
        <div class="row partition2">
          <div class="col-md-6 " v-for="(item, index) in items" :key="index">
            <div class="collection-banner p-right text-center">
              <div class="img-part">
                <img :src="item.imagepath" class="img-fluid" v-prlx="{ mobileMaxWidth: 500,speed: 0.4 }"/>
              </div>
              <div class="contain-banner text-right">
                <div>
                  <h4 style="text-transform:none;">{{ item.subtitle }}</h4>
                  <h2 :class="item.title_color" style="text-transform:none;">{{ item.title }}</h2>
                </div>
              </div>
            </div>
            <div :animate-toggle="'fadeInUp'">
              <h4 v-html="item.description" class="mt-3 text-center text-secondary"></h4>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script type="text/javascript">
export default {
  data() {
    return {
      items: [
        {
          imagepath: '/images/pingo/howitworks/sub-banner1.jpg',
          title: 'Direct to Consumer',
          title_color: 'text-white',
          subtitle: 'PinGoの特長１',
        },
        {
          imagepath: '/images/pingo/howitworks/sub-banner2.jpg',
          title: 'Happy Share, Happy Turn',
          title_color: 'text-white',
          subtitle: 'PinGoの特長２',
        }
      ]
    }
  }
}
</script>
