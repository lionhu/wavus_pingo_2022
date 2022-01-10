<template>
  <div>
    <section class="p-0 mt-3">
      <div class="container">
        <div class="row mt-2 d-flex h-100">
          <div class="col-xs-12 col-md-6 text-center  my-auto">
            <img :src="howitworks_1" style="max-width:360px" class="p-2"/>
          </div>
          <div class="col-xs-12 col-md-6 category-m my-auto">
            <h3 class="theme-color my-3">D2C/Direct to Consumer</h3>
            <div class="category-wrapper p-3">
              <h5 class="text-left">
                {{ $t("pingo.about") }}、自社が企画した商品を工場生産から保管・商品管理、配送に至るまで
                一括して自社管理の下で実施します。
              </h5>
              <h5 class="text-left">
                それによって、よい商品を安い価格でみなさまに提供することを実現します。
                商品情報はSNSなどで随時お知らせし、
                みなさまのご意見を伺いながら、お好みに合った商品を取り揃えて参ります。
              </h5>
            </div>
          </div>
        </div>
        <div class="row mt-2  d-flex h-100">
          <div class="col-xs-12 col-md-6 category-m my-auto">
            <h3 class="theme-color my-3" >Happy Share, Happy Turn</h3>
            <div class="category-wrapper p-3 ">
              <h5 class="text-left">
                {{ $t("pingo.text") }}、サイトで販売された商品の利益(ポイント)を消費者仲間で分かち合うことです。 <br>
                たとえば、あなたがいいなぁと思った商品を「SNSや口コミ」で紹介すると、
                あなたの紹介から、その商品を購入した人のポイントがあなたにも戻ってくるというしくみです。 <br>


              </h5>
              <h5 class="text-left">
                ポイントは、自分が直接した紹介した「直接紹介者」と、その直接紹介者が紹介した「間接紹介者」が
                商品を購入した際に還元されます。 <br>
                もちろん、商品を購入した人も自ら、新たな人に商品を紹介することができ、同様にポイントが還元されます。
              </h5>
              <h5 class="text-left">
                こうして、{{ $t("pingo.text") }}のハッピーの輪が広がっていきます。
              </h5>
            </div>
          </div>
          <div class="col-xs-12 col-md-6 text-center my-auto">
            <img :src="howitworks_2" style="max-width:360px" class="p-2"/>
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
      howitworks_1: '/images/pingo/howitworks/11.jpg',
      howitworks_2: '/images/pingo/howitworks/12.jpg',
      title: 'PinGo.JP',
      subtitle: '2021',
      text: 'Start',
      title_style: 'theme-color',
      subtitle_style: 'theme-color',
      text_style: 'text-danger',
    }
  }
}
</script>
