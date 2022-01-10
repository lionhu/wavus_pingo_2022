import {axios} from '@/plugins/axios.js';
import {swalService} from './swal.service'
import {APIServices} from "~/helpers/APIs";

export const productService = {
  getAll,
  getProduct,
  getCategoryProducts,
  getSearchProducts,
  updateInfo,
  admin_create,
  remove,
  remove_batch,

  remove_sliderimage,
  create_variation,
  update_variation,
  delete_variation,

  create_pingoproduct,


  // vendor related
  get_vendor_regularlist,

};
const urls = {
  "admin_CRUD": "store/public/products/",


  "list": "/back/store/api/products/backend_list/",
  "admin_PINGO_CRUD": "/admin_back/api/pingoitems/",
  "admin_search": "/admin_back/api/products/filter_list/",
  "update": "/back/store/api/products/",
  "admin_CRUD_slider_images": "/admin_back/api/itemsliderimages/",
  "admin_CRUD_variations": "store/public/variations/",

  "vendor_CRUD": "/back/vendor/api/products/",
}

function create_pingoproduct(info) {
  return APIServices.post(urls.admin_PINGO_CRUD, info)
    .then(APIServices.handleResponse).then(response => {
      return response;
    });
}


function get_vendor_regularlist(options) {
  let url = `${urls.vendor_CRUD}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse).then(response => {
      return response;
    });
}

function getAll(options) {
  let url = urls.list;
  if (options) {
    url = `${url}${options}`
  }
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getProduct(product_id) {
  let url = `${urls.admin_CRUD}${product_id}/?expand=item_variations,item_sliderimages,supplier,category`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getCategoryProducts(options) {

  let url = `${urls.admin_CRUD}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getSearchProducts(options) {

  let url = urls.admin_search
  console.log(url)
  console.log(options)
  return APIServices.post(url, {filterOptions: options})
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function updateInfo({info, product_id}) {
  if (product_id) {
    let url = `${urls.admin_CRUD}${product_id}/`
    return APIServices.patch(url, info)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
  }
}

function admin_create(info) {
  return APIServices.post(urls.admin_CRUD, info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function remove(product_id) {
  let url = `/admin_back/api/products/${product_id}/remove_product/`
  return APIServices.post(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function remove_batch(ids) {
  let url = `/admin_back/api/products/remove_product_batch/`
  return APIServices.post(url, {ids: ids})
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function remove_sliderimage(sliderimage_id) {
  let url = `/admin_back/api/itemsliderimages/${sliderimage_id}/remove_sliderimage/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function create_variation(info) {
  let url = urls.admin_CRUD_variations
  return APIServices.post(url, info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function update_variation({variation_id, info}) {

  // delete info.id;
  let url = `${urls.admin_CRUD_variations}${variation_id}/`
  return APIServices.put(url, info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function delete_variation(variation_id) {
  let url = `${urls.admin_CRUD_variations}${variation_id}/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse).then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
