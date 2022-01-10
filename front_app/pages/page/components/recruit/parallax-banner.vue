<template>
  <div>
    <section class="p-0">
      <div
        class="full-banner parallax text-center p-left"
        v-bind:style="{ 'background-image': `url(${imagepath})` }"
      >
        <div class="container">
          <div class="row">
            <div class="col">
              <div class="banner-contain">
                <h2 style="text-transform:none;" v-bind:class="{'text-white':!$device.isMobile}">{{title}}</h2>
                <h3 style="text-transform:none;"  v-bind:class="{'text-white':!$device.isMobile}">{{subtitle}}</h3>
                <div >
                  <h4 style="text-transform:none;" v-bind:class="{'text-white':!$device.isMobile}">{{text1}}</h4>
                </div>
              </div>
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
      imagepath: require('@/assets/images/parallax/recruit_1.jpg'),
      title: 'PinGo',
      subtitle: 'パートナー募集',
      text1: 'PinGoを一緒に広めてくれる仲間を募集します！'
    }
  }
}
</script>
