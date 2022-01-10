<template>
  <div>
    <Header/>
    <Breadcrumbs title="お問合せ" breadcrumb_type="static"/>
    <section class="contact-page section-b-space">
      <div class="container">
        <!--        <div class="row section-b-space">-->
        <!--          <div class="col-lg-7 map">-->
        <!--          <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3241.625243979015!2d139.75464845103573!3d35.661603738557886!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60188bc177dfe2ab%3A0x42a331f0215c57f0!2z44CSMTA1LTAwMjEg5p2x5Lqs6YO95riv5Yy65p2x5paw5qmL77yS5LiB55uu77yX4oiS77yTIOaYreWSjOOCouOCueODhuODg-OCr&#45;&#45;8keWPt-mkqA!5e0!3m2!1sja!2sjp!4v1625232341427!5m2!1sja!2sjp"-->
        <!--                  width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>-->
        <!--          </div>-->
        <!--          <div class="col-lg-5">-->
        <!--            <div class="contact-right">-->
        <!--              <ul>-->
        <!--&lt;!&ndash;                <li>&ndash;&gt;-->
        <!--&lt;!&ndash;                  <div class="contact-icon">&ndash;&gt;-->
        <!--&lt;!&ndash;                    <img :src="phoneimage" alt="Generic placeholder image"/>&ndash;&gt;-->
        <!--&lt;!&ndash;                    <h6>Contact Us</h6>&ndash;&gt;-->
        <!--&lt;!&ndash;                  </div>&ndash;&gt;-->
        <!--&lt;!&ndash;                  <div class="media-body">&ndash;&gt;-->
        <!--&lt;!&ndash;                    <p>{{ company_phone }}</p>&ndash;&gt;-->
        <!--&lt;!&ndash;                  </div>&ndash;&gt;-->
        <!--&lt;!&ndash;                </li>&ndash;&gt;-->
        <!--                <li>-->
        <!--                  <div class="contact-icon">-->
        <!--                    <i class="fa fa-map-marker" aria-hidden="true"></i>-->
        <!--                    <h6>Address</h6>-->
        <!--                  </div>-->
        <!--                  <div class="media-body">-->
        <!--                    <p v-html="company_address"></p>-->
        <!--                  </div>-->
        <!--                </li>-->
        <!--                <li>-->
        <!--                  <div class="contact-icon">-->
        <!--                    <img :src="emailimage" alt="Generic placeholder image"/>-->
        <!--                    <h6>Email</h6>-->
        <!--                  </div>-->
        <!--                  <div class="media-body">-->
        <!--                    <p>{{ company_email }}</p>-->
        <!--                  </div>-->
        <!--                </li>-->
        <!--&lt;!&ndash;                <li>&ndash;&gt;-->
        <!--&lt;!&ndash;                  <div class="contact-icon">&ndash;&gt;-->
        <!--&lt;!&ndash;                    <i class="fa fa-fax" aria-hidden="true"></i>&ndash;&gt;-->
        <!--&lt;!&ndash;                    <h6>Fax</h6>&ndash;&gt;-->
        <!--&lt;!&ndash;                  </div>&ndash;&gt;-->
        <!--&lt;!&ndash;                  <div class="media-body">&ndash;&gt;-->
        <!--&lt;!&ndash;                    <p>{{ company_fax }}</p>&ndash;&gt;-->
        <!--&lt;!&ndash;                  </div>&ndash;&gt;-->
        <!--&lt;!&ndash;                </li>&ndash;&gt;-->
        <!--              </ul>-->
        <!--            </div>-->
        <!--          </div>-->
        <!--        </div>-->
        <div class="row" v-if="!message_sent">
          <div class="col-sm-8 offset-sm-2">
            <form class="theme-form">
              <div v-if="errors.length">
                <ul class="validation-error mb-3">
                  <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                </ul>
              </div>
              <div class="form-row">
                <div class="col-md-6">
                  <label for="username">{{ $t('contact.username') }}</label>
                  <input
                    type="text"
                    class="form-control"
                    id="username"
                    v-model="username"
                    placeholder=" Name"
                    name="username"
                    required
                    :disabled="logged_in"
                  />
                </div>
                <div class="col-md-6">
                  <label for="phone">{{ $t('contact.phone') }}</label>
                  <input
                    type="tel"
                    class="form-control"
                    id="phone"
                    v-model="phone"
                    placeholder="Enter your number"
                    name="phone"
                    required
                    :disabled="logged_in"
                  />
                </div>
                <div class="col-md-6">
                  <label for="email">{{ $t('contact.email') }}</label>
                  <input
                    type="text"
                    class="form-control"
                    id="email"
                    v-model="email"
                    placeholder="Email"
                    name="email"
                    required
                    :disabled="logged_in"
                  />
                </div>
                <div class="col-md-12">
                  <label for="message">{{ $t('contact.message') }}</label>
                  <textarea
                    class="form-control"
                    placeholder="Write Your Message"
                    id="message"
                    v-model="message"
                    name="message"
                    rows="6"
                  ></textarea>
                </div>
                <div class="col-md-12">
                  <b-button class="btn btn-solid" @click="sendMail">{{ $t('contact.btn_send_message') }}</b-button>
                </div>
              </div>
            </form>
          </div>
        </div>
        <div class="row" v-else>
          <div class="col-sm-8 offset-sm-2 text-center">
            <img src='/images/icon/send_mail_02.png' style="max-width:256px;" class="img-fluid" alt="empty cart"/>
              <h3 class="mt-3">
                <strong>ご連絡いただき、誠に有り難うございました。ご確認の上、回答させていただきます。お待ちください。</strong>
              </h3>
          </div>
        </div>
      </div>
    </section>
    <Footer/>
  </div>
</template>
<script>

import config from '~/data/config.json'
import {axios} from "~/plugins/axios"
import {swalService} from "~/helpers/swal.service"
import {mapGetters} from "vuex"

export default {
  components: {
    Header: () => import('~/components/header/header1'),
    Footer: () => import('~/components/footer/footer1'),
    Breadcrumbs: () => import('@/components/widgets/breadcrumbs'),
  },
  data() {
    return {
      phoneimage: '/images/icon/phone.png',
      emailimage: '/images/icon/email.png',
      company_phone: "03 6403 5195",
      company_fax: "03 6403 5195",
      company_address: "東京都港区東新橋２丁目７－３昭和アステック１号館",
      company_email: "crs@wavus.jp",
      errors: [],
      username: "",
      // lname: null,
      email: "",
      phone: "",
      message: "",
      message_sent: false,
      logged_in: false
    }
  },
  computed: {
    ...mapGetters({
      ME: "authfack/ME"
    })
  },
  mounted() {
    if (this.ME !== null) {
      this.logged_in = true;
      this.email = this.ME.email;
      this.username = this.ME.username;
      this.phone = "+81-1234-5678"
    }
  },
  methods: {
    checkForm() {
      this.errors = []
      if (!this.username) {
        this.errors.push('username required.')
      }
      if (!this.email) {
        this.errors.push('Email required.')
      } else if (!this.validEmail(this.email)) {
        this.errors.push('Valid email required.')
      }
      if (!this.phone) {
        this.errors.push('Phone Number required.')
      }
      if (!this.message) {
        this.errors.push('Message required.')
      }
      // if (!this.errors.length) return true
      return !this.errors.length;

    },
    sendMail() {
      if (this.checkForm()) {
        let mail_info = {
          username: this.username,
          email: this.email,
          phone: this.phone,
          message: this.message
        }
        axios.$post("/apiauth/login/sendContactMail/", {mail_info: mail_info}).then(response => {
          if (response.result) {
            this.message_sent = true;
            swalService.showToast("success", "ありがとうございました!")
          }
        })
      }
    },
    validEmail: function (email) {
      const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return re.test(email)
    }
  }
}
</script>
