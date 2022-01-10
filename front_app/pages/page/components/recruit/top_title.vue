<template>
  <div>
    <section class=" p-3">
      <div class="container">
        <div class="row">
          <div class="col">
            <div class="col-sm-12 col-md-10 offset-md-1">
              <h4 class="line-height-25">
                WAVUS株式会社は、この度、Happy Share Happy turn. をコンセプトに、会員の利益を最大化するECサイト ‘PinGo Mall’
                にご参加いただけるPinGoパートナー(営業代行)をご募集します。詳細は下記となります。
              </h4>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class=" p-3">
      <div class="container">
        <div class="row">
            <div class="col-sm-12 offset-md-1 col-md-5">
              <h2 style="text-transform:none;">PinGoとは</h2>
              <p class="line-height-15">
                PinGoは、「世界中から選りすぐりの商品を、会員のみなさまにリーズナブルな価格でお届け」し、「会員のみなさまの利益を最大化する」いままでになかった新しいしくみのECサイトです。さらに、商品を使ってくれた人みんなに幸せが戻って来るしくみ。つまり、会員の利益を最大化するECサイト、それがPinGoなのです。
              </p>
            </div>

            <div class="col-sm-12 col-md-5">
              <h2 style="text-transform:none;">PinGoの特長</h2>
              <h3>Best in Global 　　　</h3>
              <p class="line-height-15">PinGoは、世界中のネットワークを駆使して、良いものだけをみなさまにお届けします。</p>
              <h3>Direct to Consumer　</h3>
              <p class="line-height-15">自ら企画、生産した商品を中間流通業者を通さずに、自社のECサイトを通じて顧客に安価に直接販売し、リーズナブルに商品を提供します。</p>
              <h3>Happy share, Happy turn　</h3>
              <p class="line-height-15">PinGoで販売された商品の利益を仲間で分かち合います。商品を使ってくれた人みんなに幸せが戻って来るPinGoならではの仕組みです。</p>

            </div>
          </div>
      </div>
    </section>
    <section class=" p-3">
      <div class="container">
        <div class="row">
            <div class="col-sm-12 offset-md-1">
              <h2 style="text-transform:none;">PinGoパートナー募集要項</h2>
              <h4>応募条件：PinGo事業をご理解及びご賛同いただける会社及び個人</h4>
              <h4>応募期間：2021年9月〜随時</h4>
            </div>
          </div>
      </div>
    </section>
    <section class=" p-3">
      <div class="container">
        <div class="row">
            <div class="col-sm-12 offset-md-1">
              <h2 style="text-transform:none;">PinGoパートナー契約までの流れ</h2>
            </div>
          </div>
      </div>
        <div class="row pt-2 category-m" v-for="step in steps">
            <div class="col-sm-12 col-md-2 offset-md-3">
              <div class="text-center">
                <img :src="step.image" :class="{'icon_pc':!$device.isMobile,'icon_mobile':$device.isMobile}" alt="">
              </div>
            </div>
            <div class="col-sm-12 col-md-4 ml-0 category-wrapper">
              <h4 style="text-transform:none;">{{ step.title }}</h4>
              <div class="content">
                <ul v-if="step.content.length" class="text-left">
                  <li v-for="line in step.content" style="text-transform:none;">
                    {{ line }}
                  </li>
                </ul>
              </div>
            </div>
      </div>
    </section>
  </div>
</template>
<style scoped>
.icon_pc{
  max-width:160px!important;
   }
.icon_mobile{
  max-width:120px!important;
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
      imagepath: require('@/assets/images/parallax/recruit_1.jpg'),
      title: '2021',
      subtitle: 'PinGoパートナー募集',
      text1: '利益をみんなで分かち合うECサイトPinGo！へ',
      text2: 'ご参加いただける方を募集します。',
      steps:[
        {
          image:"/images/icon/recurit_title_1.jpg",
          title:"WAVUS株式会社より、PinGoパートナー希望者様へ説明会を実施",
          content:[
            "＊PinGoの事業内容、PinGoパートナーの条件等をご説明します。"
          ]
        },
        {
          image:"/images/icon/recurit_title_2.jpg",
          title:"PinGoパートナー希望の方との個別面談を実施",
          content:[
            "＊説明会でご興味をもっていただいた方に個別面談を実施します。",
            "＊PinGoパートナー契約について最終意思確認を行い、合意の方にはPinGoパートナー申込書を提出していただきます。"
          ]
        },
        {
          image:"/images/icon/recurit_title_3.jpg",
          title:"PinGoパートナー契約の締結",
          content:[
            "＊PinGoパートナー契約を締結します。",
            "＊PinGoパートナー研修を受講いただいた後、PinGoの一員として活動していただきます。"
          ]
        }
      ]
    }
  }
}
</script>
