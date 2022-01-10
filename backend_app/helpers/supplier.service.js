import {APIServices} from "~/helpers/APIs";
import Swal from 'sweetalert2'

export const supplierService = {
  getAll,
  getOne,
  updateInfo,
  insert,
  remove,

  // vendor related APIs
  vendor_updateInfo,
};

const urls = {
  "url_CRUD": "store/public/suppliers/",
  "url_CRUD_vendor": "/back/vendor/api/vendors/",
}

function getOne(vendor_id) {
  let url = `${urls.url_CRUD}${pk}/`
  console.log(url)
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getAll(options) {
  let url = `${urls.url_CRUD}${options}`
  console.log(url)
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function updateInfo({supplier_id, info}) {
  let url = `${urls.url_CRUD}${supplier_id}/`
  return APIServices.put(url, info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}


function insert(info) {
  info.admin = info.admin_id;
  delete info.admin_id;
  console.log("insert", info)
  return APIServices.post(urls.url_CRUD, info)
    .then(APIServices.handleResponse)
    .then(response => {
      console.log(response)
      return response;
    });
}

function remove(vendor_id) {
  let url = `${urls.url_CRUD}${vendor_id}/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(response => {
      console.log(response)
      return response;
    });
}

function vendor_updateInfo({vendor_id, info}) {
  let url = `${urls.url_CRUD_vendor}${vendor_id}/`
  console.log(url,info)
  return APIServices.put(url, info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
