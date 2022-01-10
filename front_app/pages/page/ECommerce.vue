<template>
  <div>
    <Header/>
    <Breadcrumbs title="利用規約" 　breadcrumb_type="static"/>
    <section class="about-page section-b-space">
      <div class="container">
        <div class="row">
          <div class="col-lg-12 padding-sm-5">
            <h2 class="text-center">ご利用規約</h2>
            <div class="nuxt-content-container pt-3">
              <div class="nuxt-content">
                <h5> {{ $t("pingo.mall") }}をご利用いただく際の利用規約です。当サイトを楽しんでご利用頂けるよう、予めご利用規約をお読み頂きますようよろしくお願い申し上げます。</h5>
                <h4>第１条（会員）</h4>
                <p align="left">1.WAVUS株式会社（以下、｢当社｣）は、この利用規約を承諾した方のみを当社が運営する{{ $t("pingo.mall") }}（以下、｢当サイト｣）会員（以下、｢会員｣）と認め、サービスを提供いたします。</p>
                <p align="left">2.会員が当社に開示した会員の属性に関する情報および会員の取引に関する履歴等を「会員情報」をいいます。</p>
                <p align="left">
                  3.会員ID・パスワードは会員本人のみが利用できるものとし、他の誰にも譲渡・貸与できないものとします。また、会員ID・パスワードを用いて当社に対して行われた意思表示は、この会員ID・パスワードに該当する会員の有効な意思表示とみなし、これにより生じる支払等はすべて会員の責任となります。
                </p>
                <h4>第２条（会員資格の喪失及び賠償義務）</h4>
                <div align="left">
                  <p>
                    1.会員資格取得申込の際に虚偽の申告をしたとき、通信販売による代金支払債務を怠ったとき、その他当社が会員として不適当と認める事由があるときは、当社は該当する会員の資格を取り消すことができることとします。
                  </p>
                  <p>2.会員は、以下の各号に定める行為をしたことにより会社に損害を生じせしめたときは、これを賠償する責任を負います。</p>
                  <ol class="mt-2 pingo_list">
                    <li>（１）会員ID、パスワードを不正に利用すること</li>
                    <li>（２）当社のホームページにアクセスして情報を改ざんしたり、当社のホームページに有害なコンピュータプログラムを送信したり、当社の営業を妨害すること
                    <li>（３）当社が扱う商品の知的所有権を侵害する行為をすること</li>
                    <li>（４）その他、この利用規約に反する行為をすること</li>

                  </ol>
                </div>
                <h4>第３条（個人情報取り扱いについて）</h4>
                <div align="left">
                  <p>本サービスの利用に関連して当社が知り得た会員の個人情報については、当社が別途定める<a href="/page/Privacy">「プライバシーポリシー」</a>に従い取り扱うものとします。</p>
                </div>
                <h4>第４条（通信時のセキュリティ）</h4>
                <div align="left">
                  <p>
                    個人情報の保護のため、暗号化技術としてＳＳＬを使用し安全性を確保します。ただし、その安全性は当社よって保証されるものではなく、万一当社の過失無くデータ漏洩等の事故が起こった場合は、当社および各クレジットカード会社には責任は及ばないものとします。</p>
                </div>
                <h4>第５条（インターネットシステムの中断）</h4>
                <div align="left">
                  <p>
                    コンピュータトラブル、メンテナンスその他、当社ウェブサイトの運営管理上やむを得ない場合は、会員への事前の通知なく、一時的にシステムの使用を中断する場合があります。これにより会員が損害を被っても、当社は賠償の責任を負わないものとします。
                  </p>
                </div>
                <h4>第６条（コンテンツの変更）</h4>
                <div align="left">
                  <p>
                    当社は、当社ウェブサイトに関して、会員への事前の通知なしに、サービスの変更・停止・中止並びに本規約の変更を行なうことができることとします。
                  </p>
                </div>
                <h4>第７条（注文受付地域）</h4>
                <div align="left">
                  <p>
                    商品のご注文は、原則として日本国内在住の方のみとさせていただきます。 また、配送先も日本国内のみとなります。
                  </p>
                </div>
                <h4>第８条（会員登録資格・基準等）</h4>
                <div align="left">
                  <p>1.「会員」とは、原則として日本在住の方で、本規約に同意の上、入会の申し込みを行う個人をいいます。</p>
                  <p>2.未成年者の方が商品の購入を希望する場合は、保護者の承認を得て、保護者の方より注文を行っていただきます。</p>
                  <p>3.審査等により、商品の発送が遅れることや、申込みをお断りすることがあります。</p>
                  <p>4.過去に会員資格が取り消された方やその他、当社が相応しくないと判断した方からの会員申込はお断りする場合があります。</p>
                </div>
                <h4>第９条（表示価格・税）</h4>
                <div align="left">
                  <p>
                    当サイト上での価格は、送料および消費税を含んで表示しています。
                  </p>
                </div>
                <h4>第１０条（商品の購入）</h4>
                <div align="left">
                  <p>1. 会員は、商品等の購入を希望する場合、当社が指定する下記の方法に従って、商品等の購入又は利用を申込むものとします。</p>
                  <p>
                    2.前項の申込みに伴い、会員が入力・登録した配達先・注文内容等を確認の上、注文が完了した時点で、会員と当社との間に当該商品等に関する売買契約が成立するものとします。その後、当社から注文内容を記載したメールをお送りします。</p>
                  <p>3. 前項の規定に拘わらず、本サービス利用に関して不正行為又は不適当な行為があった場合、当社は売買契約について取消、解除その他の適切な措置を取ることができるものとします。</p>
                  <p>
                    4.インターネット上の障害、その他の当社に帰責事由のない原因により会員の注文が受理されなかった場合、当社はその責任を負いません。また、勤務先等のデバイスをご利用する場合、セキュリティの関係でページが表示できない可能性がございます。</p>
                </div>
                <h4>第１１条（決済方法）支払い方法、支払い時期</h4>
                <div align="left">
                  <p>1.購入された商品等のお支払いは、会員本人名義のクレジットカードでの一括決済を利用するものとします。また、クレジット会社の審査基準等により、契約が成立しないこともありますのでご了承下さい。</p>
                  <p>2.購入代金は、各カード会社の会員規約に基づき、指定口座からの引き落しとなります。利用可能なカードはVISA・マスター・JCB・アメックス・ダイナースとなります。</p>
                  <p>3.利用者の情報に関しては、弊社に適切に管理するための処置を講ずるよう、必要な管理を行います。</p>
                </div>
                <h4>第１２条（商品の発送）</h4>
                <div align="left">
                  <p>1. 在庫がある商品の配送は、以下の場合を除き、注文入力完了から3営業日以内に発送します。但し、共同協入の場合は企画が成立後、適宜発送します。</p>
                  <ul class="pingo_list">
                    <li>・配送事情(中元・歳暮時期等)や、天災・交通事情・天候等が影響した場合</li>
                    <li>・商品の注文発送件数が当初予測を著しく超える件数になった場合</li>
                    <li>・商品の販売ページに特に定めのある場合</li>
                  </ul>
                  <p>2. 商品の引渡しは、ご注文の際に指定されたお届け先に商品が配送されたことをもって完了したものとします。 <br>
                    ただし、会員様の都合で荷物を受け取れなかった場合の再配送費用は、会員様のご負担となります。
                  </p>
                  <p>3. 注文商品のお届け予定が大幅に遅れる場合や、売切れで配送できなくなった場合、Eメール・電話のいずれかでご連絡いたします。</p>
                </div>
                <h4>第１３条（商品の保証）</h4>
                <div align="left">
                  <p>
                    商品の保障は、各商品が規定する保証内容に準じます。
                  </p>
                </div>
                <h4>第１４条（送料）</h4>
                <div align="left">
                  <p>
                    送料は全て無料です。ただし、会員様の都合で荷物を受け取れなかった場合の再配送費用は、会員様のご負担となります。
                  </p>
                </div>
                <h4>第１５条（注文のキャンセル）</h4>
                <div align="left">
                  <p>
                    1. WAVUS株式会社が規定するキャンセル基準に準じます。ご了承ください。
                  </p>
                  <p>
                    2. 商品購入者は、商品の注文確定後、商品等が出荷される前までは、お届け先の変更またはご注文のキャンセルができます。マイページ注文履歴よりキャンセル操作を行うことにより取消が可能です。
                  </p>
                  <p>3. 次の場合は、注文のキャンセルを一切お受けできません。</p>
                  <ul class="pingo_list">
                    <li>・発送済みの商品</li>
                    <li>・利用者が商品等購入時に、キャンセル不可であることが商品ページに明記している商品</li>
                  </ul>
                </div>
                <h4>第１６条（商品等の返品・交換）</h4>
                <div align="left">
                  <p>
                    1. WAVUS株式会社が規定する返品基準に準じます。ご了承ください。
                  </p>
                  <p>■不良品の返品・交換について</p>
                  <ul class="pingo_list">
                    <li>・
                      商品が届きましたら、速やかにご確認をお願いします。商品の品質やお届け方法には万全を期しておりますが、万が一、お申し込み商品と異なっていたり、破損していた場合には受領後7日以内にメールにてお申し出ください。
                    </li>
                    <li>・ 在庫切れ、生産終了等により交換商品の手配が困難な場合はご返金にて対応させていただきます。</li>
                    <li>・ 返品・交換の際は商品到着時(商品のパッケージ、付属品なども含め全てが揃っている)未使用の状態で返品して下さい。</li>
                    <li>・ お客様都合(注文間違い、サイズ・色の交換、イメージと違うなど)による返品・交換につきましてはお承りできません。</li>
                  </ul>
                  <p>■返品をお受けできない商品</p>
                  <ul class="pingo_list">
                    <li>・ お客様都合(注文間違い、イメージと違うなど)による返品</li>
                    <li>・ お客様による損傷・汚損、使用した商品</li>
                    <li>・ 化粧箱の不備によるご返品</li>
                    <li>・ お客様の責任により汚れ・キズ・臭い移り（タバコ・香水）などが生じた商品</li>
                    <li>・ 返品連絡なく返送された商品</li>
                    <li>・ オーダー品や文字入れ・サイズ直し等の加工済みの商品</li>
                    <li>・ 洗濯・クリーニングされた商品</li>
                    <li>・ 限定商品/セール品/福袋/特別キャンペーン・企画の限定品</li>
                    <li>・ 返品不可であることを商品ページに明記している商品</li>
                    <li>・ 食品/書籍/雑誌/衛生商品類/タオル/肌着/寝具/トイレ用品全般/通電後の電化製品</li>
                  </ul>
                </div>
                <h4>第１７条（商品等に関する免責）</h4>
                <div align="left">
                  <p>1.
                    当社は、本サイトを通じて販売される商品等につき、その品質、材質、機能、性能、他の商品との適合性その他の欠陥、又はこれらが原因となり生じた損害、損失、不利益等についてはいかなる保証・負担も負わないものとします。</p>
                  <p>2.
                    当社は、配送先不明等によるトラブルに関しては、会員が登録している連絡先に連絡すること及び商品購入の際に指定された配達先に商品等を配送等することにより、商品等の引渡債務を履行し、当該債務から免責されるものとします。</p>
                  <p>3.
                    当社は、本サイトページ上において、Facebook、Twitter等のSNSサービスの利用会員が投稿した商品等に関するコメントの内容について、当該コメントの内容が事実に反するものであったとしても、これによる商品を購入した会員に生じた損害に対しては、当社に故意又は重過失がある場合を除き、一切の責任を負わないものとします。</p>
                </div>
                <h4>第１８条（著作権・知的財産権）</h4>
                <div align="left">
                  <p>
                    当サイトに掲載されている写真等の著作物・コンテンツの著作権（知的財産権を含む）は、当社または製造会社に帰属します。したがって、会員を含む第三者はこれらの著作物を、当社の事前の承諾なく複製、送信、上映等を行うことはできません。</p>
                </div>
                <h4>第１９条（ポイントサービス）</h4>
                <div align="left">
                  <p>本サイトにおいて商品の購入につき、所定のポイントが還元されるサービスをポイントサービスといいます。またポイントサービスに参加するには当サイトの会員になることが必要です。</p>
                  <ol class="pingo_list">
                    <p>1. 本サイトにおいて商品を購入するごとに、所定のポイントが還元され、次回以降、ポントを利用して商品を購入することができます。</p>
                    <p>2. ポイントは商品の購入以外にキャンペーン等で取得することが出来ますが、キャンペーン参加でポイント取得が保証されるものではありません。</p>
                    <p>3. ポイントの有効期限はポイント取得日から1年間とします。</p>
                    <p>4. ポイントは他人に譲渡することはできません。また退会時に換金・同等の物品による返還請求することはできません。</p>
                    <p>5. ポイントを利用して商品を購入または割引した場合、ポイント付与の対象にはなりません。</p>
                    <p>6. 当サイトではご紹介していただいた会員が商品を購入した場合にもポイントが還元されます。ポイントの還元及び有効期限等についての細則は、<a href="/page/PointPolicy">こちらをご覧ください。</a></p>

                  </ol>
                </div>
                <h4>第２０条（退会手続き）</h4>
                <div align="left">
                  <p>会員は、当社所定の手続を経て、いつでも退会することができるものとします。また、会員は当社が退会申請を受領した時点で会員資格および所有ポイントを喪失するものとします。</p>
                </div>
                <h4>第２１条（その他）</h4>
                <div align="left">
                  <p>
                    天災地変、法令の制定改廃、交通事故、公権力の行使に基づく処分、輸送機関の事故、労働争議、その他やむをえない事情により、商品の引渡しの遅滞または引渡しの不能を生じた場合、当社は何ら賠償の責を負わないものとします。</p>
                </div>
                <h4>第２２条（裁判所）</h4>
                <div align="left">
                  <p>当社と会員の間に、訴訟の必要が生じた場合には、「東京地方裁判所」を第一審の専属的合意管轄裁判所とします。</p>
                </div>
                <h4>第２３条（問い合わせ）</h4>
                <div align="left">
                  <p>本規約に関するお問合せは以下よりお願いいたします。</p>
                  <ul class="pingo_list">
                    <li>メール：{{ company.email }}</li>
                    <li> お電話：{{ company.phone }}（受付時間：土日祝・年末年始を除く、平日10：00～17：00）</li>
                  </ul>
                </div>


                <h4>特定商取引法に基づく表記</h4>
                <div align="left" style="font-size:0.8rem;">
                  <table class="address">
                    <tbody>
                    <tr>
                      <td class="text-right title">販売事業者：</td>
                      <td><p>{{ company.name }}</p></td>
                    </tr>
                    <tr>
                      <td class="text-right title">運営責任者：</td>
                      <td><p>{{ company.CEO }}</p></td>
                    </tr>
                    <tr>
                      <td class="text-right title">所在地：</td>
                      <td>
                        <p>{{ company.postcode }} {{ company.address }}</p>
                      </td>
                    </tr>
                    <tr>
                      <td class="text-right title">連絡電話：</td>
                      <td><p>{{ company.phone }} </p>
                      </td>
                    </tr>
                    <tr>
                      <td class="text-right title">メール：</td>
                      <td>
                        <p>{{ company.email }}</p>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<style>
.pingo_list {
  display: block;
  line-height: 2 !important;
  color: #777777;
  letter-spacing: 0.03rem;
  margin-top: 0.5rem !important;
  margin-bottom: 0.5rem !important;
  padding-left: 1rem !important;
}

table.address tr td.title {
  min-width: 100px !important;
}

.about-page p {
  margin-bottom: 0 !important;
}
</style>
<script>
import Header from '../../components/header/header1'
import Footer from '../../components/footer/footer1'
import Breadcrumbs from '../../components/widgets/breadcrumbs'
import {mapGetters} from 'vuex';

export default {
  name: "spacial_trade",
  components: {
    Header,
    Footer,
    Breadcrumbs
  },
  data() {
    return {
      swiperOption: {
        slidesPerView: 2,
        spaceBetween: 20,
        breakpoints: {
          991: {
            slidesPerView: 1,
            spaceBetween: 20
          }
        }
      },
      swiperOption2: {
        slidesPerView: 4,
        spaceBetween: 20,
        breakpoints: {
          1199: {
            slidesPerView: 3,
            spaceBetween: 20
          },
          991: {
            slidesPerView: 2,
            spaceBetween: 20
          },
          420: {
            slidesPerView: 1,
            spaceBetween: 20
          }
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      },
      items: [
        {
          imagepath: '/images/2.jpg',
          name: 'Mark Jecno',
          role: 'designer',
          decs:
            'you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings.'
        },
        {
          imagepath: '/images/20.jpg',
          name: 'Amy Molive',
          role: 'tester',
          decs:
            'you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings.'
        }
      ],
      teams: [
        {
          imagepath: '/images/team/1.jpg',
          name: 'Hileri Keol',
          post: 'chairman'
        },
        {
          imagepath: '/images/team/2.jpg',
          name: 'Peter Pants',
          post: 'business executive'
        },
        {
          imagepath: '/images/team/3.jpg',
          name: 'john dio',
          post: 'project manager'
        },
        {
          imagepath: '/images/team/4.jpg',
          name: 'Petey Cruiser',
          post: 'web developer'
        }
      ],
      aboutbanner: '/images/about/aj',
      aboutTitle:
        'Sed Ut Perspiciatis Unde Omnis Iste Natus Error Sit Voluptatem Accusantium Doloremque Laudantium',
      aboutText:
        'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium On the other hand.We denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour. when our power of choice is untrammelled and when nothing prevents our being able to do what we like best. every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection he rejects pleasures to secure other greater pleasures or else he endures pains to avoid worse pains.'
    }
  },
  computed: {
    ...mapGetters({
      company: "system/getterCompanyInfo"
    }),
  }
}
</script>
