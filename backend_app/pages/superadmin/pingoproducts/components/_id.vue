<script>
import {axios} from '@/plugins/axios.js';
import {mapState, mapGetters} from "vuex"
import Switches from 'vue-switches'
import Swal from "sweetalert2";

export default {
  head() {
    return {
      title: `${this.title} | WAVUS EC`,
    };
  },
  components: {
    Switches,
  },
  data() {
    return {
      title: "Product Detail",
      items: [
        {
          text: "WAVUS",
        },
        {
          text: "Ecommerce",
        },
        {
          text: "Product Detail",
          active: true,
        },
      ],
      postimageSelect: true,
      image_id: 0,
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      postimageUrl: "",
      imageUrl: "",
      modeAdd: false,
      edit_variation: {
        price: 0,
        purchase_price: 0,
        name: "",
        description: "",
        point_rule: {
          is_valid: false,
          type: "amount",
          policies: {
            client_admin: 0,
            level_2: 0,
            level_1: 0
          }
        },
      },
      submitted: false

    };
  },
  middleware: ['router-auth', 'router-superadmin'],
  computed: {
    sliderlist() {
      return this.sliderimages.map(function (slider) {
        return {url: slider.image, name: slider.http_referer, id: slider.id}
      })
    },
    csrftoken() {
      return this.$store.state.authfack.user.token;
    },
    ...mapGetters({
      back_server: "system/getterBackServer",
    })
  },
  methods: {
    changeImage(data) {
      this.postimageSelect = data.target.dataset.wavus === "postimage"
      this.image_id = data.target.dataset.image_id
      if (this.postimageSelect) {
        console.log(`image id: ${this.image_id}`)
      } else {
        console.log(`thumbimage id: ${this.image_id}`)
      }
      document.getElementById("myImage").src = data.target.currentSrc
    },
    handleSliderRemove(file) {
      let vm = this;
      console.log(file);
      let url = `/back/store/api/itemsliderimages/${file.id}/`
      axios.$delete(url).then((res) => {
        if (res.result) {
          let removeId = parseInt(res.data.sliderimage_id);
          let index = vm.sliderimages.findIndex(slider => slider.id === removeId)
          if (index > -1) {
            vm.sliderimages.splice(index, 1)
          }
        }
      })

    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    handleDownload(file) {
      console.log(file);
    },
    beforeAvatarUpload(file) {
      console.log("beforeAvatarUpload", file)
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
      }
      return isLt2M;
      // return isJPG && isLt2M;
    },
    handlePostImageAvatarSuccess(res, file) {
      console.log(res)
      if (res.result) {
        this.image = res.data.product.image;
        console.log(this.image)
      }
      // this.postimageUrl = URL.createObjectURL(file.raw);
    },
    handleAvatarSuccess(res, file) {
      console.log(res)
      if (res.result) {
        res.data.sliderimage.image = this.back_server + res.data.sliderimage.image;

        this.sliderimages.push(res.data.sliderimage);
        this.imageUrl = URL.createObjectURL(file.raw);
      }
    },
    editVariation(variation) {
      console.log(variation)
      this.edit_variation = variation;
      this.modeAdd = false;
      this.$bvModal.show("modal_variation")
    },
    switchAddVariationMode() {
      this.modeAdd = true;
      this.$bvModal.show("modal_variation")
    },
    editProduct() {
      this.modeAdd = false;
      console.log("edit product")
      this.$bvModal.show("modal_product")
    },
    update_product_basicinfo() {
      let url = `/back/store/api/products/${this.id}/update_basicinfo/`
      let params = {
        description: this.description,
        series: this.series,
        model: this.model,
        brand: this.brand
      }
      var vm = this;
      this.$axios.post(url, params).then((response) => {
        if (response.data.result) {
          Swal.fire("Success", "Basic Info has been updated successfully updated!", "success")
          vm.$bvModal.hide("modal_product")
        }
      })
    },
    updateProductVariationInformation() {
      if (!this.modeAdd) {
        let url = `/back/store/api/variations/${this.edit_variation.id}/`
        var vm = this;
        this.$axios.put(url, {variation: this.edit_variation}).then((response) => {
          if (response.data.result) {
            let variation_server = response.data.data.variation;
            console.log(variation_server)
            var index = vm.variations_admin.findIndex(variation => variation.id === variation_server.id)
            console.log(index)
            if (index > -1) {
              vm.variations_admin.splice(index, 1, variation_server);
            }
            Swal.fire("Success", "Variation has been updated successfully updated!", "success")
            vm.$bvModal.hide("modal_variation")
          }
        })

      } else {
        let url = `/back/store/api/variations/`
        console.log(this.edit_variation)
        var vm = this;
        this.$axios.post(url, {variation: this.edit_variation, id: this.id}).then((response) => {
          console.log(response)
          if (response.data.result) {
            let variation_server = response.data.data.variation;
            vm.variations_admin.push(variation_server);
            Swal.fire("Success", "Variation has been added successfully updated!", "success")
            vm.$bvModal.hide("modal_variation")
          }
        })

      }

    },
    deleteVariation(variation_id) {
      let url = `/back/store/api/variations/${variation_id}/`
      var vm = this;
      this.$axios.delete(url).then((response) => {
        console.log(response)
        if (response.data.result) {
          var index = vm.variations_admin.findIndex(variation => variation.id === variation_id)
          if (index > -1) {
            vm.variations_admin.splice(index, 1);
          }
          Swal.fire("Success", "Variation has been deleted successfully updated!", "success")
          vm.$bvModal.hide("modal_variation")
        }
      })
    }
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
  <div>
    <PageHeader :title="title" :items="items"/>
    <div class="row">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body">

            <div class="row">
              <div class="col-lg-12">
                <div>
                  <div>
                    <b-badge variant="primary" pill v-if="type==='REGULAR'">REGULAR</b-badge>
                    <b-badge variant="warning" pill v-else>Pingo</b-badge>
                  </div>
                  <div>
                    <a href="javascript:void (0);" class="text-primary">{{ category.title }}</a>
                  </div>
                  <h4 class="mb-1">
                    {{ item_name }}
                    <a href="javascript: void(0);" @click="editProduct" class="text-muted">
                      <i class="mdi mdi-square-edit-outline ml-2"></i>
                    </a>
                  </h4>

                  <p class="text-muted mr-3 font-16">
                    <el-rate
                      v-model="rate"
                      disabled
                      show-score
                      text-color="#ff9900"
                      score-template="{value}">
                    </el-rate>
                  </p>
                  <div class="row">
                    <div class="col-4">
                      <span class="mr-3">Brand:</span>
                      <b-badge variant="primary" pill>{{ brand }}</b-badge>
                    </div>
                    <div class="col-4">
                      <span class="mr-3">Series:</span>
                      <b-badge variant="primary" pill>{{ series }}</b-badge>
                    </div>
                    <div class="col-4"><span class="mr-3">Model:</span>
                      <b-badge variant="primary" pill>{{ model }}</b-badge>
                    </div>
                  </div>
                  <hr/>

                  <div>
                    <p v-html="description"></p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-lg-12">
                <el-upload
                  class="avatar-uploader"
                  :action="'http://localhost:8000/back/store/api/products/'+id+'/update_postimage/'"
                  :show-file-list="false"
                  :headers="{'Authorization':csrftoken}"
                  :on-success="handlePostImageAvatarSuccess"
                  :before-upload="beforeAvatarUpload">
                  <img v-if="image" :src="image" class="avatar">
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>

              </div>
            </div>
            <div class="row">
              <div class="col-lg-12">
                <div class="row justify-content-start">
                  <div class="col-xl-8">
                    <el-upload
                      action="http://localhost:8000/back/store/api/itemsliderimages/"
                      list-type="picture-card"
                      ref="upload"
                      :show-file-list="true"
                      :file-list="sliderlist"
                      :before-upload="beforeAvatarUpload"
                      :on-success="handleAvatarSuccess"
                      :headers="{'Authorization':csrftoken}"
                      :data="{'item_id':id}"
                      :auto-upload="true">
                      <i slot="default" class="el-icon-plus"></i>
                      <div slot="file" slot-scope="{file}">
                        <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
                        <span class="el-upload-list__item-actions">
                          <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                          <i class="el-icon-zoom-in"></i>
                          </span>
                          <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleDownload(file)">
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
        <!-- end card -->
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body">

            <div class="row mb-2">
              <div class="col-sm-6 col-md-offset-6">

              </div>
            </div>
            <div class="row">
              <div class="col-md-6">Available Variations</div>
              <div class="col-md-6">
                <button class="btn btn-danger mb-2 float-right" @click="switchAddVariationMode"><i
                  class="mdi mdi-plus-circle mr-1"></i> Add Variation
                </button>
              </div>
            </div>
            <div class="row">
              <div class="table-responsive">
                <table class="table table-bordered table-centered mb-0">
                  <thead class="thead-light">
                  <tr>
                    <th>name</th>
                    <th>Order</th>
                    <th>price</th>
                    <th>point_rule</th>
                    <th></th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="variation in variations_admin">
                    <td>
                      {{ variation.name }}</td>
                    <td><b-badge variant="danger" pill >{{ variation.sort_by }}</b-badge></td>
                    <td>
                      <span class="d-block">{{ variation.price|currency("¥") }}</span>
                      <span class="d-block">{{ variation.purchase_price|currency("¥") }}</span>
                    </td>
                    <td>
                      <h5>
                        <b-badge variant="success" pill v-if="variation.point_rule.is_valid">on</b-badge>
                        <b-badge variant="danger" pill v-else>off</b-badge>
                      </h5>
                      <ul>
                        <li>
                          <span
                            class="inline-block text-right mr-3">代理店:</span>{{
                            variation.point_rule.policies.client_admin|currency("¥")
                          }}
                        </li>
                        <li>
                          <span
                            class="inline-block text-right mr-3">祖父:</span>{{
                            variation.point_rule.policies.level_2|currency("¥")
                          }}
                        </li>
                        <li>
                          <span
                            class="inline-block text-right mr-3">父親:</span>{{
                            variation.point_rule.policies.level_1|currency("¥")
                          }}
                        </li>
                      </ul>
                    </td>
                    <td class="align-items-center">
                      <a href="javascript:void(0);" @click="editVariation(variation)" class="action-icon">
                        <i class="mdi mdi-square-edit-outline"></i></a>
                      <a href="javascript:void(0);" @click="deleteVariation(variation.id)" class="action-icon">
                        <i class="mdi mdi-delete"></i></a>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <!-- end card -->
        </div>
      </div>
      <!-- end row -->
    </div>
    <b-modal id="modal_product" scrollable title="Edit Variation Information" title-class="font-18"
             body-class="p-4" hide-footer>
      <form @submit.prevent="update_product_basicinfo">
        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label for="field-item_brand" class="control-label">Brand
                <span class="text-danger">*</span>
              </label>
              <input type="text" id="field-item_brand" v-model="brand" class="form-control"
                     :class="{ 'is-invalid': submitted && $v.brand.$error }"
                     :placeholder="brand.name"/>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label for="field-product_description" class="control-label">Description<span class="text-danger">*</span></label>
              <textarea id="field-product_description" v-model="description" class="form-control"
                        :placeholder="description"/>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="field-series" class="control-label">Series
                <span class="text-danger">*</span>
              </label>
              <input type="text" id="field-series" v-model="series" class="form-control"
                     :placeholder="series"/>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
              <label for="field-model" class="control-label">Model
                <span class="text-danger">*</span>
              </label>
              <input type="text" id="field-model" v-model="model"
                     class="form-control"
                     :placeholder="model"/>
            </div>
          </div>
        </div>
        <div class="form-group row">
          <div class="col-8 offset-4">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </form>

    </b-modal>

    <b-modal id="modal_variation" scrollable title="Edit Variation Information" title-class="font-18"
             body-class="p-4" hide-footer>
      <form @submit.prevent="updateProductVariationInformation">
        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label for="field-item_name" class="control-label">Name
                <span class="text-danger">*</span>
              </label>
              <input type="text" id="field-item_name" v-model="edit_variation.name" class="form-control"
                     :class="{ 'is-invalid': submitted && $v.edit_variation.name.$error }"
                     :placeholder="edit_variation.name"/>

              <div v-if="submitted && !$v.edit_variation.name.required" class="invalid-feedback">This value is required.
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label for="field-description" class="control-label">Description<span class="text-danger">*</span></label>
              <textarea id="field-description" v-model="edit_variation.description" class="form-control"
                        :placeholder="edit_variation.description"
                        :class="{ 'is-invalid': submitted && $v.edit_variation.description.$error }"/>

              <div v-if="submitted && !$v.edit_variation.description.required" class="invalid-feedback">This value is
                required.
              </div>
            </div>
          </div>
        </div>
        <div class="row mt-md-2">
          <div class="col-md-6">
            <b-form-group id="field-is_valid" label-cols="4" label-cols-lg="4" label-size="sm" label="Active">
              <switches v-model="edit_variation.point_rule.is_valid" id="field-is_valid" type-bold="false"
                        color="warning"
                        class="ml-1 my-auto"></switches>
            </b-form-group>
          </div>
        </div>

        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="field-price" class="control-label">Price
                <span class="text-danger">*</span>
              </label>
              <input type="number" id="field-price" v-model="edit_variation.price" class="form-control"
                     :class="{ 'is-invalid': submitted && $v.edit_variation.price.$error }"
                     :placeholder="edit_variation.price"/>

              <div v-if="submitted && !$v.edit_variation.price.required" class="invalid-feedback">This value is
                required.
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
              <label for="field-price" class="control-label">Purchase Price
                <span class="text-danger">*</span>
              </label>
              <input type="number" id="field-purchase_price" v-model="edit_variation.purchase_price"
                     class="form-control"
                     :class="{ 'is-invalid': submitted && $v.edit_variation.purchase_price.$error }"
                     :placeholder="edit_variation.purchase_price"/>

              <div v-if="submitted && !$v.edit_variation.purchase_price.required" class="invalid-feedback">This value is
                required.
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4">
            <div class="form-group">
              <label for="field-client_admin"
                     class="control-label">{{ $t("menuitems.organizations.user.client_admin") }}
                <span class="text-danger">*</span>
              </label>
              <input type="number" id="field-client_admin" v-model="edit_variation.point_rule.policies.client_admin"
                     class="form-control"
                     :class="{ 'is-invalid': submitted && $v.edit_variation.point_rule.policies.client_admin.$error }"
                     :placeholder="edit_variation.point_rule.policies.client_admin"/>

              <div v-if="submitted && !$v.edit_variation.point_rule.policies.client_admin.required"
                   class="invalid-feedback">This value is required.
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="field-level_2" class="control-label">{{ $t("menuitems.organizations.user.level_2") }}
                <span class="text-danger">*</span>
              </label>
              <input type="number" id="field-level_2" v-model="edit_variation.point_rule.policies.level_2"
                     class="form-control"
                     :class="{ 'is-invalid': submitted && $v.edit_variation.point_rule.policies.level_2.$error }"
                     :placeholder="edit_variation.point_rule.policies.level_2"/>

              <div v-if="submitted && !$v.edit_variation.point_rule.policies.level_2.required" class="invalid-feedback">
                This value is required.
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="field-level_1" class="control-label">{{ $t("menuitems.organizations.user.level_1") }}
                <span class="text-danger">*</span>
              </label>
              <input type="number" id="field-level_1" v-model="edit_variation.point_rule.policies.level_1"
                     class="form-control"
                     :class="{ 'is-invalid': submitted && $v.edit_variation.point_rule.policies.level_1.$error }"
                     :placeholder="edit_variation.point_rule.policies.level_1"/>

              <div v-if="submitted && !$v.edit_variation.point_rule.policies.level_1.required" class="invalid-feedback">
                This value is required.
              </div>
            </div>
          </div>
        </div>
        <div class="form-group row">
          <div class="col-8 offset-4">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </form>

    </b-modal>


  </div>
</template>
