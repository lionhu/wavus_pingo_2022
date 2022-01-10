<template>
  <div>
    <Header/>
    <Breadcrumbs title="運営会社" breadcrumb_type="static"/>
    <section class="pt-0">
      <div
        class="full-banner parallax row" style="padding: 50px 0; ">
        <div class="col-sm-12 text-center my-auto">
          <img src="/images/logo/wavus-02.png" style="max-width:120px;"/>

          <div class="banner-contain mx-2">
            <h4 class="text-danger text-center">隅々までへ届け、喜びを</h4>
          </div>
        </div>
      </div>
    </section>
    <section class="about-page section-b-space">
      <div class="container clearfix">
        <h4>会社概要</h4>

        <table class="table table-striped">
          <tbody>
          <tr>
            <td style="width: 20%;">社名</td>
            <td>WAVUS株式会社</td>
          </tr>
          <!--<tr>
              <td style="width: 20%;">会社法人等番号</td>
              <td>1010-40-1157668</td>
          </tr>-->
          <tr>
            <td>本店</td>
            <td>東京都港区東新橋２丁目７－３昭和アステック１号館</td>
          </tr>
          <tr>
            <td>設立</td>
            <td>令和3年1月8日</td>
          </tr>
          <tr>
            <td>資本金</td>
            <td>500万円</td>
          </tr>
          <tr>
            <td>取引銀行</td>
            <td>
              <p>
                銀行：　楽天銀行　第三営業支店（253） <br>
                種類：　普通口座<br>
                口座番号：　7117209<br>
                口座名義人：　ウェバス（カ
              </p>
            </td>
          </tr>
          <tr>
            <td>従業員数</td>
            <td>6人（2021年4月）</td>
          </tr>
          <tr>
            <td>代表取締役</td>
            <td>古月　海光(こげつ　かみ)</td>
          </tr>
          <tr>
            <td>事業内容</td>
            <td>
              <ul style="text-align:left;">
                <li>* インターネットを利用した通信販売，情報の収集，管理，処理，提供の各種サービス及 び仲介並びに代金決済システムの導入代行業務</li>
                <li>* デジタルサイネージに関する機器の販売・データ制作・保守</li>
                <li>* インターネットを含むコンピュータシステム，通信システム，制御システムの機器・装置及び付属機器・周辺機器の設計，製造，販売，運用管理，導入設置，保守メンテナンス，コンサルティングの業務
                </li>
                <li>* 電気通信機器，情報通信機器，情報処理機器，放送設備機器，医療機器，電子機器，電気通信のシステムの開発，販売，保守業務及び輸出入業務各種
                </li>
                <li> * 貿易業，売買業，売買の代理業，問屋業及び仲介業，物品の販売及び輸出入業務各種</li>
                <li>* イベント，キャンペーン，展示会，パーティー等の企画，運営及びそれらのコンサルティング
                </li>
                <li>* 広告業及び広告代理店業</li>
                <li> * 市場調査，商品計画，広報，販売促進，PR 等の企画，実施，請負及び支援業務</li>
                <li>* 番組，映画やアニメ等の制作に関わる取材の手配</li>
                <li>* 著作権，著作隣接権，商標権，意匠権等の知的財産権の取得，譲渡，使用許諾及び管理業務
                </li>
                <li> * ウェブサイト，ウェブコンテンツ，その他インターネットを利用した各種サービス等の企画，製作，販売，配信，運営及び管理
                </li>
                <li>* 各種タイアップの企画及び実施</li>
                <li>* 外貨両替，外国為替取引，国内外の有価証券，投資信託及び国内外のベンチャー企業に関する投資及び投資顧問業務
                </li>
                <li>* 株式，有価証券，為替，不動産及び商品先物等の金融商品の投資及び運用に関するコンサルティング
                </li>
                <li>* 企業，団体等に対する新規事業，事業戦略及びM&Aに関する企画，立案，支援及びそれらのコンサルティング並びに投資</li>
                <li>* 労働者派遣事業及び有料職業紹介業 17 前各号に附帯関連する一切の事業</li>
              </ul>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<style scoped>
.font-18{
  font-size:18px;
}
.p-ident-1{
  text-indent:1rem;
}
</style>
<script>
import Header from '../../components/header/header1'
import Footer from '../../components/footer/footer1'
import Breadcrumbs from '../../components/widgets/breadcrumbs'
import {mapGetters} from 'vuex';
export default {
  name:"about_page",
  components: {
    Header,
    Footer,
    Breadcrumbs
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters({
      "company": "system/getterCompanyInfo"
    })
  }
}
</script>
