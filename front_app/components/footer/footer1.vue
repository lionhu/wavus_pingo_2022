<template>
  <div>
    <footer class="footer-light">
      <section class="section-b-space light-layout">
        <div class="container">
          <div class="row footer-theme partition-f">
            <div class="col-lg-4 col-md-6">
              <div class="footer-content">
                <div class="footer-logo">
                  <img :src="logo_image" alt="logo" style="max-height: 50px" />
                </div>
                <div class="footer-social">
                  <ul>
                    <li>
                      <a
                        href="https://www.facebook.com/profile.php?id=100068895348154"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <i class="fa fa-facebook" aria-hidden="true"></i>
                      </a>
                    </li>
                    <li>
                      <a
                        href="https://www.youtube.com/channel/UCpwc5X5pcmjtyAGsxdbRiHg"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <i class="fa fa-youtube" aria-hidden="true"></i>
                      </a>
                    </li>
                    <li>
                      <a
                        href="https://twitter.com/pingo48245583"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <i class="fa fa-twitter" aria-hidden="true"></i>
                      </a>
                    </li>
                    <li>
                      <a
                        href="https://www.instagram.com/pingomall/"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <i class="fa fa-instagram" aria-hidden="true"></i>
                      </a>
                    </li>
                    <li>
                      <a
                        href="https://vt.tiktok.com/ZSeeu9fuy/"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <img
                          src="images/icon/tiktok.svg"
                          style="width: 14px; padding-bottom: 5px"
                        />
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="col offset-xl-1">
              <div class="sub-title">
                <div class="footer-title">
                  <h4 style="text-transform: inherit">
                    {{ $t("pingo.footer_about") }}
                  </h4>
                </div>
                <div class="footer-contant">
                  <ul>
                    <li>
                      <a href="/page/aboutPingo">{{ $t("pingo.about") }}</a>
                    </li>
                    <li>
                      <a href="/page/ECommerce">{{ $t("pingo.ecommerce") }}</a>
                    </li>
                    <li>
                      <a href="/page/Privacy">{{ $t("pingo.privacy") }}</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="sub-title">
                <div class="footer-title">
                  <h4 v-bind:class="{ 'pt-2': $device.isMobile }">
                    サイト運営
                  </h4>
                </div>
                <div class="footer-content">
                  <ul class="contact-list">
                    <li>
                      <i class="fa fa-building"></i>
                      {{ config.company_info.name }}
                    </li>
                    <li>
                      <i class="fa fa-map-marker"></i>
                      <span v-html="config.company_info.postcode"></span> <br />
                      <span v-html="config.company_info.address"></span>
                    </li>
                    <li>
                      <i class="fa fa-envelope-o"></i>メール:
                      <a
                        :href="`mailto:${config.company_info.email}`"
                        style="text-transform: none"
                        >{{ config.company_info.email }}</a
                      >
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <div class="sub-footer">
        <div class="container">
          <div class="row">
            <div class="col-xl-6 col-md-6 col-sm-12">
              <div class="footer-end">
                <p>
                  <i class="fa fa-copyright" aria-hidden="true"></i>
                  {{ config.company_info.copyright }}
                </p>
              </div>
            </div>
            <div class="col-xl-6 col-md-6 col-sm-12">
              <div class="payment-card-bottom">
                <img src="/images/logo/credit_card_logo.png" alt="" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import Config from "~/data/config.json";

export default {
  name: "pingo_footer",
  data() {
    return {
      logo_image: "/images/logo/pingo_dark.svg",
      config: Config,
    };
  },
  computed: {
    ...mapGetters({
      company: "system/getterCompanyInfo",
      layout: "layout/getterLayout",
    }),
  },
  watch: {
    layout(newVal, oldVal) {
      if (newVal === "dark") {
        this.logo_image = "/images/logo/pingo_white.svg";
      } else {
        this.logo_image = "/images/logo/pingo_dark.svg";
      }
    },
  },
};
</script>

<style>
.footer-logo img {
  max-height: 120px;
}

.payment-card-bottom img {
  max-height: 32px;
}
</style>
