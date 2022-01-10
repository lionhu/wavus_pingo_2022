import {APIServices} from "~/helpers/APIs"

export const pingoproductService = {
  getFilterCategory,
  getProdoctIntroQR,
  getProdoctDetailByID,

};
const urls = {
  "filter_category": "store/public/pingo_products/?filter{}=4",
  "pingo_products": "store/public/pingo_products/",
}

function getProdoctDetailByID(product_id) {
  let url =`store/public/pingo_products/${product_id}/?expand=item_pingo_sliderimages`
  return APIServices.get(url)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function getProdoctIntroQR(product_id) {
  let url = `store/public/pingo_products/${product_id}/get_introduce_qr/`;
  return APIServices.get(url)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function getFilterCategory(options) {
  let url = `store/public/pingo_products/list_recruiting/?${options.page_info}&filter{category_id}=${options.category_id}`
  return APIServices.get(url)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function handleResponse(response) {
  if (response.result){
    return response.data;
  }
  if (response.status === 404) {
    const error = response.message || response.statusText;
    console.log(error)
    return Promise.reject(error);
  }
  return response;
}
