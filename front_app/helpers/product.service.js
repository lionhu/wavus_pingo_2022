// import {axios} from '@/plugins/axios.js';
import {APIServices} from "~/helpers/APIs"
import {swalService} from "~/helpers/swal.service";

export const productService = {
  getCategoryProducts,
  getProductByID,
  getProductDetailByID,
  getProductIntroQR,
  getMyFavorites,
  removeMyFavorites,
  addToMyFavorites,

  getProductComments,
  deleteProductComment,
  createProductComment,
  updateProductComment,
  updateProductCommentThumbs,
};
const urls = {
  "list": "store/public/products/",
  "favorites": "store/public/favorites/",
  "comment_CRUD":"store/api/comments/",
  "comment_filters_url":"store/public/comments"
}
function updateProductCommentThumbs({comment_id,info}) {
  let url=`${urls.comment_CRUD}${comment_id}/thumbs_changed/`
  return APIServices.post(url,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getProductComments(item_id) {
  let url=`${urls.comment_filters_url}/?item=${item_id}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function updateProductComment({comment_id,info}) {
  let url=`${urls.comment_CRUD}${comment_id}/`
  return APIServices.patch(url,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function deleteProductComment(comment_id) {
  let url=`${urls.comment_CRUD}${comment_id}/`
  return APIServices.delete(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function createProductComment(info) {
  return APIServices.post(urls.comment_CRUD,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}


function getMyFavorites(options) {
  let url = options === "" ? urls.favorites : `${urls.favorites}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function removeMyFavorites(wish_id) {
  let url = `${urls.favorites}${wish_id}/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function addToMyFavorites(info) {
  let url = urls.favorites
  return APIServices.post(url,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getCategoryProducts(filter_options) {
  let url = `${filter_options}`;
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getProductByID(product_id) {
  let option = "?expand=item_variations,item_sliderimages"
  let url = product_id ? `${urls.list}${product_id}/${option}` : urls.list;
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getProductDetailByID(options_url) {
  return APIServices.get(options_url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getProductIntroQR(product_id) {
  let url = `store/public/products/${product_id}/get_introduce_qr/`;
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
