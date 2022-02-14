<template>
  <div>
    <section class="section-b-space beauty-about">
      <div class="container">
        <div class="row">
          <div class="col-xl-5 col-lg-6 col-md-12 offset-xl-1 text-center">
            <img :src="imagepath" alt class="img-fluid" />
          </div>
          <div class="col-xl-5 col-lg-6 col-md-12">
            <div class="about-section">
              <div>
                <h2>{{title}}</h2>
                <div class="about-text">
                  <p>{{desc}}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
export default {
  data() {
    return {
      imagepath: 'https://vue.pixelstrap.com/multikart/_nuxt/img/about-us.d1c37c5.jpg',
      title: 'about us',
      desc:
        'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam.sit voluptatem accusantium doloremque laudantium,totam rem aperiam.',
      service_1: 'free shipping',
      service_2: '24 X 7 service',
      service_3: 'festival offer'
    }
  }
}
</script>
