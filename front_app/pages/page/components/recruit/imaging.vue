<template>
  <div>
    <section class=" p-3">
      <div class="container">
        <div class="row">
          <div class="col-sm-12 offset-md-1 col-md-10">
            <h2 style="text-transform:none;">PinGoパートナーの概要</h2>
          </div>
        </div>
      </div>
      <div class="row pt-3">
        <div class="col-sm-12 offset-md-1 col-md-10 text-center">
          <img :src="imagepath" v-bind:class="{'width_100':$device.isMobile,'width_60':!$device.isMobile,}">
        </div>
      </div>

      <div class="row pt-3 category-m">
        <div class="col-sm-12 offset-md-2 col-md-4 ">
          <h3 class="text-left bottom_theme_color_line" style="text-transform:none;">/PinGoパートナーの業務内容</h3>
          <p class="text-left line-height-15">
            PinGoパートナーには、PinGoビジネス拡大のために、以下の業務を積極的に推進してください。特に情報発信力の高い(KOL)会員の獲得を期待します。
          </p>
        </div>
        <div class="col-sm-12 col-md-4 category-wrapper left_theme_color_line">
          <h4 class="text-left theme-color">新規会員の獲得</h4>
          <p class="text-left line-height-15">・PinGoサイトへの新規の会員を多く獲得すること。<br>
            ・情報発信力の高いKOLの会員獲得を期待。</p>

          <h4 class="text-left theme-color">商品情報の発信</h4>
          <p class="text-left line-height-15">・PinGo取扱商品を自らのSNS等で情報発信、拡散し、商品PRすること。 <br>
            ・勧誘した新規会員(KOL等)からの商品情報の発信を促すこと。</p>

          <h4 class="text-left theme-color">会員の購買促進</h4>
          <p class="text-left line-height-15">・PinGoの商品を購入してもらうよう、会員へ働きかけること。</p>


        </div>
      </div>
      <div class="row pt-3 category-m">
        <div class="col-sm-12 offset-md-2 col-md-4 ">
          <h3 class="text-left bottom_theme_color_line">/商品情報の発信</h3>
          <p class="text-left line-height-15">
            PinGo会員が、購入した商品や魅力を感した商品をPRしていただける機能を用意しています。(右の図)
          </p>
          <p class="text-left line-height-15">
            各商品ごとに用意したSNS拡散用の商品ページをtwitter/Instagram/FACEBOOK等で発信していただけます。
          </p>
          <p class="text-left line-height-15">
            ★PinGoパートナーが発信した商品ページを経由してこ購入頂いた方の購入実績に応じて、ポイントが還元されます)
          </p>
        </div>
        <div class="col-sm-12 col-md-4 category-wrapper left_theme_color_line">
          <img src='/images/about/recruiting_2.png' style="width:100%;" alt="">
        </div>
      </div>
    </section>
  </div>
</template>
<style scoped>
.bottom_theme_color_line {
  border-bottom: #ff4c3b solid 5px !important;
}

.left_theme_color_line {
  border-left: #ff4c3b solid 5px !important;
}

.circle img {
  max-width: 160px !important;
}

.width_100{
  width: 100%!important;
}
.width_60{
  width: 60%!important;
}

.line-height-25{
  line-height:2.5rem!important;
}
.line-height-15{
  line-height:1.5rem!important;
}
</style>
<script type="text/javascript">
export default {
  data() {
    return {
      imagepath: '/images/about/recruiting.png',
      title: '2021',
      subtitle: 'PinGoパートナー募集',
    }
  }
}
</script>
