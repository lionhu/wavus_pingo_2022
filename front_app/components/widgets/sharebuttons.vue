<template>
  <div>
    <input type="hidden" id="testing-code" v-model="share_link">
    <textarea class="form-control" placeholder="Write Your Message"
              id="message" v-model="message" name="message" rows="3"></textarea>
    <!--    <button type="button" class="btn btn-warning text-white my-3" @click="copyTestingCode">Copy Share Link</button>-->

    <div class="mt-3">
      <ul class="list-inline">
        <li class="list-inline-item">
          <ShareNetwork
            network="facebook"
            title="https://www.pingo.jp"
            :url="share_link"
            :quote="`${message} @ ${share_link} `"
            :description="`${message} @ ${share_link} `"
            hashtags="pingo,shopping"
            :media="QRImage"
            :image="QRImage"
            v-inview:animate="'fadeInLeftBig'"
          >
            <i class="fa fa-facebook fa-2x theme-color"></i>
          </ShareNetwork>
        </li>
        <li class="list-inline-item">

          <ShareNetwork
            network="line"
            :url="share_link"
            :title="`${message} @ ${share_link} `"
            :description="message"
            :quote="link_url"
            hashtags="pingo,shopping,point"
            :media="QRImage"
            v-inview:animate="'fadeInUpBig'"
          >
            <font-awesome-icon :icon="['fab', 'line']" class="theme-color fa-2x"/>
          </ShareNetwork>
        </li>
        <li class="list-inline-item">

          <ShareNetwork
            network="twitter"
            :url="share_link"
            :title="`${message} @ ${share_link}`"
            hashtags="pingo,shopping,point"
            v-inview:animate="'fadeInUpBig'"
          >
            <font-awesome-icon :icon="['fab', 'twitter']" class="theme-color fa-2x"/>
          </ShareNetwork>
        </li>
        <li class="list-inline-item">

          <ShareNetwork
            network="email"
            :url="link_url"
            :title="`${message} @ ${QRImage} `"
            :description="message"
            v-inview:animate="'fadeInRightBig'"
          >
            <font-awesome-icon :icon="['fas', 'envelope-open']" class="theme-color fa-2x"/>
          </ShareNetwork>
        </li>

        <li class="list-inline-item">
          <a href="javascript:void(0);" @click="copylink" v-inview:animate="'fadeInRightBig'">
            <font-awesome-icon :icon="['fas', 'link']" class="theme-color fa-2x"/>
          </a>
        </li>
      </ul>
    </div>
    <div class="mt-3">
      <p>{{link_url}}</p>
    </div>
  </div>
</template>
<script>
import {mapGetters, mapState} from "vuex"
import {swalService} from "@/helpers/swal.service"

export default {
  name:"share_buttons",
  props: ["qr_image", "link_url"],
  data() {
    return {
      share_link: "",
      QRImage:"",
      message: `この商品気になる！`,
    };
  },
  watch: {
    link_url(newVal, oldVal) {
      this.share_link = newVal;
    },
    qr_image(newVal, oldVal) {
      this.QRImage = newVal;
    },
  },
  methods:{
    copylink(){
      this.$emit("copylink");
    }
  }

}
</script>
