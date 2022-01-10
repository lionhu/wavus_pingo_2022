<script>

export default {
  name: "admin_product_detail_card",
  props: ["product"],
};
</script>

<template>
  <div class="card">
    <div class="card-body">
      <div class="row">
        <div class="col-lg-5">
          <div class="row justify-content-center">
            <div class="col-xl-8">
              <div id="product-carousel" class="carousel slide product-detail-carousel" data-ride="carousel">
                <div class="carousel-inner">
                  <div class="carousel-item active">
                    <div>
                      <img :src="product.thumbimage_url" alt="product-img" id="myImage"
                           class="img-fluid"/>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-7">
          <div>
            <div>
              <a href="#" class="text-primary">{{ product.category.title }}</a>
              <a href="javascript:void(0);" class="ml-3 btn btn-sm waves-effect waves-light"
                  :class="{'btn-success':product.is_valid,'btn-warning':!product.is_valid}">
                    {{product.is_valid?"公開":"未公開"}}
                  </a>
            </div>
            <h4 class="my-2">
              {{ product.item_name }}
              <a href="javascript: void(0);" class="text-muted">
                <i class="mdi mdi-square-edit-outline ml-2"></i>
              </a>
            </h4>
            <hr/>
            <div>
              <p v-html="`${product.description.substring(0,100)}...`">
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
