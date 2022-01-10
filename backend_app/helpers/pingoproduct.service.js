import {APIServices} from "~/helpers/APIs";

export const pingoproductService = {
  superadmin_getFilterCategory,
  superadmin_getPingoProductList,
  superadmin_remove,
  superadmin_retrieve,
  superadmin_update,
  superadmin_create,
  superadmin_establish,
  superadmin_release,

  // Pingo Order related functions
  superadmin_related_orderlist,
  superadmin_delete_orders,
  superadmin_batch_update_orders,

  create_variation,
  update_variation,
  delete_variation,


  getCategoryProducts,
  updateInfo,
  insert
};
const urls = {
  "superadmin_list": "store/public/pingo_products/",
  "superadmin_related_orderlist": "store/public/pingo_orders/",
  "superadmin_filter_category": "store/public/pingo_products/?expand=item_pingo_sliderimages/admin_back/api/pingoproducts/?filter{category}={}",
  "admin_CRUD_variations": "/admin_back/api/variations/",
}

function superadmin_establish(product_id) {
  let url = `store/public/pingo_products/${product_id}/establish_pingoitem/`
  return APIServices.post(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function superadmin_release(product_id) {
  let url = `store/public/pingo_products/${product_id}/release_pingoitem/`
  return APIServices.post(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function superadmin_related_orderlist({product_id,options}) {
  let superadmin_related_orderlist = `${urls.superadmin_related_orderlist}?filter{product_id}=${product_id}`
  let url = `${superadmin_related_orderlist}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      console.log(response)
      return response;
    });
}

function superadmin_delete_orders(order_ids) {
  let url = "store/public/pingo_orders/destroy_batch/"
  return APIServices.post(url,{ids:order_ids})
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function superadmin_batch_update_orders(updateinfo) {
  let url = "store/public/pingo_orders/update_batch/"
  return APIServices.post(url,updateinfo)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function superadmin_getPingoProductList(options) {
  let url = `${urls.superadmin_list}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function superadmin_getFilterCategory(options) {
  let url = `${urls.superadmin_list}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function superadmin_remove(product_id) {
  let url = `${urls.superadmin_list}${product_id}/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function superadmin_retrieve(product_id) {
  let url = `${urls.superadmin_list}${product_id}/?expand=item_pingo_sliderimages,supplier`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function superadmin_update(info) {
  let url = `${urls.superadmin_list}${info.id}/`
  console.log("update pingo product",info)
  return APIServices.patch(url, info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function superadmin_create(info) {
  let url = `${urls.superadmin_list}`
  delete info.id;
  console.log("superadmin_create", url, info)
  return APIServices.post(url, info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function create_variation(info) {
  let url = urls.admin_CRUD_variations
  console.log("pingo create variation", info)
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
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}


function getCategoryProducts(options) {
  let url = urls.list;
  return APIServices.post(url, {filterOptions: options})
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function updateInfo(info) {
  console.log("updateInfo", info)
  if (info.id) {
    let url = `${urls.update}${info.id}/`
    return APIServices.put(url, info)
    .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
  }
}

function insert(info) {
  return APIServices.post(urls.list, info)
    .then(APIServices.handleResponse)
    .then(response => {
      console.log(response)
      return response;
    });
}
