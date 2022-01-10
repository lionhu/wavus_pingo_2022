<template>
  <div>
    <Header/>
    <Breadcrumbs title="PinGoポイントサービス" 　breadcrumb_type="static"/>
    <section class="about-page section-b-space">
      <div class="container">
        <div class="row">
          <div class="col-lg-12 padding-sm-5">
            <h2 class="text-center">「PinGoポイント」サービスに関する細則</h2>
            <div class="nuxt-content-container">
              <textarea class="nuxt-content-editor" style="display: none;"></textarea>
              <div class="nuxt-content">
                <h4 id="（総則）">（総則）：</h4>
                <div align="left">
                  <p>第１条 <br>
                    当細則は、PinGo MALLで付与されるPinGoポイント(以下、ポイント)のサービスについて定めたものです。
                  </p>
                </div>
                <h4 id="（対象者）">（対象者）</h4>
                <div align="left">
                  <p>第２条 <br>
                    このサービスの対象者はPinGo MALLで買い物をする会員（個人または法人）とします。
                  </p>
                </div>
                <h4 id="（PinGoポイントの付与）">（PinGoポイントの付与）</h4>
                <div align="left">
                  <p>第３条</p>
                  <ol class="mt-2 pingo_list">
                    <li>1. ポイントは、PinGo MALLで買い物をする際のお支払い金額に応じて付与される「還元ポイント」と、新規会員登録時や各種企画への参加等に対して付与する「特別ポイント」があります。
                    </li>
                    <li>2. 還元ポイントは、対象となる商品の利用金額(消費税別)ごとに一定のポイントを付与します。</li>
                    <li>3. 還元ポイントの対象となる商品およびポイント数は、サイト内で都度案内します。</li>
                    <li>4. 還元ポイントは、商品の注文が完了した時点で付与されます。付与されたポイントは「マイページ」の「ポイント履歴」でご確認頂けます。<br>
                      ※ ポイントは、請求金額確定までは「承認待ち」と表示されます。請求金額確定後にご自身でポイント確定の処理を行うことによって利用可能なポイントとなります。確定処理を行わない場合は、運営側で翌月末一括処理後、翌々月10日までに利用可能なポイントとなります。
                      <br>
                      　※ ポイントはお支払いをクレジットカードで決済した場合のみに付与されます。また、ご自分のポイントを利用して買い物をした場合、ポイントは付与されません。
                    </li>
                    <li>5. 特別ポイントの対象となる、商品、サービス、キャンペーン等は、その都度ご案内します。</li>
                  </ol>
                </div>
                <h4 id="（還元ポイントの付与）">（還元ポイントの付与）</h4>
                <div align="left">
                  <p>下記の場合に還元ポイントが付与されます。</p>
                  <ol class="mt-2 pingo_list">
                    <li>1. ご自身がPinGo MALLで買い物をした際、購入商品ごとに設定されたポイントが付与されます。
                    </li>
                    <li>2. ご自身の紹介によってPinGoに登録した会員（レベル１）と、そのレベル1会員の紹介によって登録した会員（レベル2）が買い物をした際、購入商品ごとに設定されたポイントが自分に還元されます。
                    </li>
                  </ol>
                </div>
                <h4 id="（特別ポイントの付与）">（特別ポイントの付与）</h4>
                <div align="left">
                  <p>下記の場合に特別ポイントが付与されます。</p>
                  <ol class="mt-2 pingo_list">
                    <li>1. ご自身がPinGoへ会員登録後、初めて買い物をした際に1,000ポイントが付与されます。
                    </li>
                    <li>2. ご自身の紹介によってPinGoに登録した会員（レベル１）が、初めて商品を購入した際、自分に1,000ポイントが付与されます。
                    </li>
                    <li>3. PinGoMALLで実施されるキャンペーン等へのご参加でポイントが付与されます。キャンペーン等を実施する場合は、都度PinGoサイト内にてお知らせします。
                    </li>
                  </ol>
                </div>

                <h4 id="（ポイントの利用)">(ポイントの利用)</h4>
                <div align="left">
                  <p>第４条</p>
                  <ol class="mt-2 pingo_list">
                    <li>1. ご利用可能なポイントは 1 ポイント 1 円として、PinGo MALLで利用することができます。
                    </li>
                    <li>2. ポイントは「マイページ」の「ポイント履歴」に表示する「利用可能なポイント」でご確認ください。</li>
                    <li>3. ポイントを利用する場合は、購入手続き画面で「利用ポイント数」の欄にお使いになるポイント数を入力してください。ポイントは購入代金の全部または一部が利用可能です。</li>
                    <li>4. ポイントを利用して商品を購入または割引した場合、還元ポイント付与の対象にはなりません。
                    </li>
                  </ol>
                </div>
                <h4 id="(ポイントの有効期限)">(ポイントの有効期限)</h4>
                <div align="left">
                  <p>第５条</p>
                  <ol class="mt-2 pingo_list">
                    <li>1. ポイントの有効期限は、利用可能なポイントとして発行された日から1年間となります。
                    </li>
                    <li>2. ポイントの有効期限は、「マイページ」でご確認いただけます。</li>
                  </ol>
                </div>
                <h4 id="(ポイント利用制限)">(ポイント利用制限)</h4>
                <div align="left">
                  <p>第６条</p>
                  <p>付与されたポイントは、第三者への譲渡・共有・合算・貸与等する事はできないものとします。</p>
                </div>
                <h4 id="(退会後のポイント)">(退会後のポイント)</h4>
                <div align="left">
                  <p>第７条</p>
                  <p>PinGoを退会をされる場合は、ポイントは失効となります。</p>
                </div>
                <h4 id="(ポイントの取り消し)">(ポイントの取り消し)</h4>
                <div align="left">
                  <p>第８条</p>
                  <p>当社では次の場合に会員が保有するポイントを取消すことができるものとします。</p>
                  <ol class="mt-2 pingo_list">
                    <li>1. PinGo MALLで購入した商品の代金をお支払いいただけない場合。
                    </li>
                    <li>2. 会員が法令に違反し、また当社が定めた方法以外で不正にポイントを入手した場合。</li>
                    <li>3. 当社がポイントを取消すことが適切であると判断した場合。</li>
                  </ol>
                </div>

                <h4 id="(細則の変更案内)">(細則の変更案内)</h4>
                <div align="left">
                  <p>第９条</p>
                  <p>この細則を変更する場合、当社はPinGoサイトにて変更内容および変更の効力発生日について告知するものとします。</p>
                </div>
                <h4 id="(改廃)">(改廃)</h4>
                <div align="left">
                  <p>第１０条</p>
                  <p>この細則の改廃は当社の取締役会が行います。</p>
                </div>
                <h4 id="(付則)">(付則)</h4>
                <div align="left">
                  <p>この細則は2021年9月1日に制定し、同日より施行します。</p>
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
<script>
export default {
  name: "privacy",
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('@/components/widgets/breadcrumbs'),
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
  }
}
</script>

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
