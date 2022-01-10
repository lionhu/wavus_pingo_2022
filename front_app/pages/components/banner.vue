<template>
  <div>
    <section class="p-0 mt-3">
      <div
        class="full-banner parallax text-center p-left"
        v-bind:style="{ 'background-image': `url(${imagepath})` }">
        <img :src="imagepath" alt class="bg-img d-none" />
        <div class="container">
          <div class="row">
            <div class="col">
              <div class="banner-contain">
                <h2 :class="title_style">{{title}}</h2>
                <h3 :class="subtitle_style">{{subtitle}}</h3>
                <h4 :class="text_style">{{text}}</h4>
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
      imagepath: '/images/banners/happyshare.jpg',
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
