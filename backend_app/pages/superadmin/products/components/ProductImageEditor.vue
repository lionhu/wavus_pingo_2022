<script>
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import {mapGetters} from "vuex";
import {swalService} from "~/helpers/swal.service.js"
import {APIServices} from "@/helpers/APIs";

export default {
  name: "admin_product_image_editor",
  props: ["product"],
  components: {
    "el-upload": () => import("element-ui/lib/upload"),
    "el-dialog": () => import('element-ui/lib/dialog'),
  },
  data() {
    return {
      image: "",
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
    };
  },
  computed: {
    ...mapGetters({
      back_server: "system/getterBackServer",
    }),
    csrftoken() {
      return this.$auth.strategy.token.get();
    },
    sliderlist() {
      if (this.product.item_sliderimages) {
        return this.product.item_sliderimages.map(function (slider) {
          return {url: slider.image, name: slider.http_referer, id: slider.id}
        })
      }

    },
  },
  methods: {
    changeSorted(file){
      console.log(file.id)
    },
    handleSliderRemove(file) {
      let vm = this;
      APIServices.destroy(`store/public/sliderimages/${file.id}/`)
        .then(APIServices.handleResponse)
        .then((res) => {
          console.log(res)
          if (res.result) {
            let index = vm.product.item_sliderimages.findIndex(slider => slider.id === file.id)
            if (index > -1) {
              vm.product.item_sliderimages.splice(index, 1)
            }
          }
        })
    },




    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      // const isJPG = true;
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M || !isJPG) {
        swalService.showModal("check image", 'Upload JPG file under 2M!', "warning");
      }
      // return isLt2M;
      return isJPG && isLt2M;
    },
    handlePostImageAvatarSuccess(res, file) {
      console.log("handlePostImageAvatarSuccess",res, file)
      if (res.result) {
        this.product.image = res.data.image;
        // this.product.thumbimage = res.data.product.thumbimage.replace("http://www.pingo.jp","");
      }
      // this.postimageUrl = URL.createObjectURL(file.raw);
    },
    handleSlideImageSuccess(res, file) {
      console.log("handleSlideImageSuccess",res, file)
      if (res.result) {
        this.product.item_sliderimages.push(res.data.product_slider_image);
        this.imageUrl = URL.createObjectURL(file.raw);
      }
    },
  },
};
</script>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
<template>
  <div class="card">
    <div class="card-body">
      <h4 class="header-title">Product images</h4>
      <p class="sub-header">Upload and change product images</p>

      <div class="row">
        <div class="col-lg-12">
          <el-upload
            class="avatar-uploader"
            :action="'https://www.pingo.jp/daphne/api/store/public/products/'+product.id+'/update_post_image/'"
            :show-file-list="false"
             :name="'image'"
            :headers="{'Authorization':csrftoken}"
            :on-success="handlePostImageAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="product.image" :src="product.image" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>

        </div>
      </div>
      <div class="row">
        <div class="col-lg-12">
          <div class="row justify-content-start">
            <div class="col-xl-8">
              <el-upload
                :action="'https://www.pingo.jp//daphne/api/store/public/sliderimages/'"
                list-type="picture-card"
                ref="upload"
                :show-file-list="true"
                :file-list="sliderlist"
                :before-upload="beforeAvatarUpload"
                :on-success="handleSlideImageSuccess"
                :headers="{'Authorization':csrftoken}"
                :data="{'item':product.id}"
                :name="'image'"
                :auto-upload="true">
                <i slot="default" class="el-icon-plus"></i>
                <div slot="file" slot-scope="{file}">
                  <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
                  <span class="el-upload-list__item-actions">
                          <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                          <i class="el-icon-zoom-in"></i>
                          </span>
                          <span class="el-upload-list__item-delete" @click="changeSorted(file)">
                            <i class="el-icon-download"></i>
                          </span>
                          <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleSliderRemove(file)">
                            <i class="el-icon-delete"></i>
                          </span>
                        </span>
                </div>
              </el-upload>
              <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="">
              </el-dialog>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
