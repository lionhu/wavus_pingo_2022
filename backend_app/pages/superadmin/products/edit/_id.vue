/* eslint-disable no-console */
<script>
import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from '@ckeditor/ckeditor5-build-classic'
import { mapGetters } from 'vuex'
import { APIServices } from '@/helpers/APIs'
import { swalService } from '~/helpers/swal.service'

export default {
  name: 'EditProduct',
  components: {
    'el-select': () => import('element-ui/lib/select'),
    'el-rate': () => import('element-ui/lib/rate'),
    'el-option': () => import('element-ui/lib/option'),
    'el-cascader': () => import('element-ui/lib/cascader'),
    Switches: () => import('vue-switches'),
    VariationTable: () => import('../components/VariationTable'),
    ProductImageEditor: () => import('../components/ProductImageEditor'),
    ckeditor: CKEditor.component
  },
  middleware: ['router-auth', 'router-superadmin'],
  data () {
    return {
      title: '商品情報',
      items: [
        { text: 'PINGO' },
        { text: 'eCommerce' },
        { text: '商品情報', active: true }
      ],
      editor: ClassicEditor,
      // editorData: "<p>Content of the editor.</p>",
      labels: [
        { value: 'NW', label: 'New' },
        { value: 'BS', label: 'Best Seller' }
      ],
      image: '',
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      imageUrl: '',
      submitted: false,
      product: {}
    }
  },
  head () {
    return {
      title: `${this.title} | Pingo Admin`,
      script: [{ src: 'https://unpkg.com/element-ui/lib/index.js' }],
      link: [
        {
          rel: 'stylesheet',
          href: 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'
        }
      ]
    }
  },
  computed: {
    ...mapGetters({
      back_server: 'system/getterBackServer',
      suppliers: 'suppliers/getterSupplierList',
      categories: 'categories/getProductCategories',
      _product_id: 'products/getterProductID'
    }),
    supplierSelectionList () {
      return this.suppliers.map((supplier) => {
        return { value: supplier.id, label: supplier.name }
      })
    },
    supplier_id () {
      if (
        typeof this.product.supplier === 'object' &&
        Object.keys(this.product.supplier).includes('id')
      ) {
        return this.product.supplier.id
      }
      return this.product.supplier
    }
  },
  mounted () {
    if (this._product_id > 0) {
      this.load_product(this._product_id)
    } else {
      window.location.href = '/backend/superadmin/products'
    }
  },
  methods: {
    load_product (product_id) {
      const vm = this
      this.$store
        .dispatch('products/load_product', product_id)
        .then((response) => {
          vm.product = response.item
          vm.product.supplier = response.item.supplier.id
        })
    },
    handleCategoryChange (val) {
      const index = val.length - 1
      this.product.category = val[index]
    },
    update_product () {
      const product_id = this.product.id
      this.product.supplier = this.supplier_id
      delete this.product.id
      delete this.product.image
      delete this.product.item_sliderimages
      delete this.product.item_variations
      delete this.product.created_at

      const vm = this

      vm.$nuxt.$loading.start()
      this.$store
        .dispatch('products/update_product', {
          product_id,
          info: this.product
        })
        .then((item) => {
          vm.load_product(product_id)
          swalService.showModal('Success', 'Product was updated!', 'success')
        })

      vm.$nuxt.$loading.finish()
    },
    operateVariationTable (result) {
      switch (result.command) {
        case 'addVariation':
          this.AddVariation(result.variation)
          break
        case 'editVariation':
          this.ReplaceVariation(result.variation)
          break
        case 'replaceVariation':
          this.ReplaceVariation(result.variation)
          break
        case 'deleteVariation':
          this.deleteVariation(result.variation)
          break
      }
    },
    AddVariation (_variation) {
      this.product.item_variations.unshift(_variation)
      swalService.showModal(
        'Success',
        'Variation has been successfully added!',
        'success'
      )
    },
    ReplaceVariation (_variation) {
      const vm = this
      if (vm.product.item_variations.length === 0) {
        vm.product.item_variations.push(_variation)
      } else {
        const index = vm.product.item_variations.findIndex(
          variation => variation.id === _variation.id
        )
        if (index > -1) {
          vm.product.item_variations.splice(index, 1, _variation)
          swalService.showModal(
            'Success',
            'Variation has been successfully updated!',
            'success'
          )
        }
      }
    },
    deleteVariation (variation_id) {
      const url = `store/public/variations/${variation_id}/`
      const vm = this
      APIServices.destroy(url)
        .then(APIServices.handleResponse)
        .then((response) => {
          if (response.result) {
            const index = vm.product.item_variations.findIndex(
              variation => variation.id === variation_id
            )
            if (index > -1) {
              vm.product.item_variations.splice(index, 1)
            }
            swalService.showModal(
              'Success',
              'Variation has been deleted successfully updated!',
              'success'
            )
            vm.$bvModal.hide('modal_variation')
          }
        })
    },
    CreateProductResult (info) {
      if (info.result) {
        this.product = info.product
      }
    }
  }
}
</script>

<template>
  <div>
    <PageHeader :title="title" :items="items" />
    <div class="row">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-6">
                <h4 class="header-title">
                  基本情報(商品ID #{{ product.id }})
                </h4>
                <p class="sub-header">
                  下記の基本情報を入力してください。
                </p>
              </div>
              <div class="col-6 text-right">
                <b-button
                  variant="warning"
                  @click="$router.push('/superadmin/products/comments')"
                >
                  コメント管理
                </b-button>
              </div>
            </div>
            <div>
              <div class="row">
                <div class="col-md-4">
                  <div class="form-group mb-3">
                    <label
                      for="product-active"
                    >有効<span class="text-danger">*</span></label>
                    <br>
                    <switches
                      id="product-active"
                      v-model="product.is_valid"
                      type-bold="false"
                      color="warning"
                      class="ml-1 my-auto"
                    />
                  </div>
                </div>
                <div class="col-md-2">
                  <div class="form-group mb-3">
                    <label for="product-sort">
                      カテゴリー内の並び順番:
                      <span class="text-danger">*</span>
                    </label>
                    <input
                      id="product-sort"
                      v-model="product.sort_by"
                      type="number"
                      class="form-control"
                      :placeholder="product.sort_by"
                    >
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4">
                  <div class="form-group mb-3">
                    <label for="product-rate">
                      評価
                      <span class="text-danger">*</span>
                    </label>
                    <el-rate id="product-rate" v-model="product.rate" />
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group mb-3">
                    <label
                      for="product-label"
                    >ラベル<span class="text-danger">*</span></label>
                    <br>
                    <el-select
                      id="product-label"
                      v-model="product.labels"
                      multiple
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="item in labels"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                      />
                    </el-select>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group mb-3">
                    <label for="product-category">
                      カテゴリー
                      <span class="text-danger">*</span>
                    </label>
                    <el-cascader
                      id="product-category"
                      v-model="product.category"
                      :options="categories"
                      size="medium"
                      :props="{
                        expandTrigger: 'hover',
                        multiple: false,
                        label: 'title',
                        value: 'id',
                      }"
                      @change="handleCategoryChange"
                    />
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label
                      class="control-label"
                    >サプライヤー<span class="text-danger">*</span></label>
                    <el-select v-model="product.supplier" placeholder="请选择">
                      <el-option
                        v-for="supplier in supplierSelectionList"
                        :key="supplier.value"
                        :label="supplier.label"
                        :value="supplier.value"
                      />
                    </el-select>
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-4">
                  <label for="product-brand">
                    ブランド
                    <span class="text-danger">*</span>
                  </label>
                  <input
                    id="product-brand"
                    v-model="product.brand"
                    type="text"
                    class="form-control"
                    :placeholder="product.brand"
                  >
                </div>
                <div class="col-md-4">
                  <label for="product-Series">
                    シリーズ
                    <span class="text-danger">*</span>
                  </label>
                  <input
                    id="product-Series"
                    v-model="product.series"
                    type="text"
                    class="form-control"
                    :placeholder="product.series"
                  >
                </div>
                <div class="col-md-4">
                  <label for="product-model">
                    モデル
                    <span class="text-danger">*</span>
                  </label>
                  <input
                    id="product-model"
                    v-model="product.model"
                    type="text"
                    class="form-control"
                    :placeholder="product.model"
                  >
                </div>
              </div>

              <div class="form-group mb-3">
                <label for="product-name">
                  商品名
                  <span class="text-danger">*</span>
                </label>
                <input
                  id="product-name"
                  v-model="product.item_name"
                  type="text"
                  class="form-control"
                  placeholder="e.g : Apple iMac"
                >
              </div>
              <div class="form-group mb-3">
                <label for="product-video_url">
                  ビデオURL
                  <span class="text-danger">*</span>
                </label>
                <input
                  id="product-video_url"
                  v-model="product.video_url"
                  type="text"
                  class="form-control"
                  placeholder="e.g : Apple iMac"
                >
              </div>
              <div class="form-group mb-3">
                <label for="product-description">
                  商品紹介
                  <span class="text-danger">*</span>
                </label>
                <ckeditor
                  id="product-description"
                  v-model="product.description"
                  :editor="editor"
                />
              </div>

              <div class="form-group mb-3">
                <label>商品仕様</label>

                <ckeditor
                  id="product-package"
                  v-model="product.package"
                  :editor="editor"
                />
              </div>
              <div class="form-group mt-3 float-right">
                <b-button
                  class="btn-rounded"
                  variant="danger"
                  @click="update_product"
                >
                  更新
                </b-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <ProductImageEditor :product="product" />
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <VariationTable
          :variations="product.item_variations"
          :product_id="product.id"
          @operateTable="operateVariationTable"
        />
      </div>
    </div>
  </div>
</template>
