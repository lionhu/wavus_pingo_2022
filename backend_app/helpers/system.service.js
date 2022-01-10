import {APIServices} from "~/helpers/APIs";

export const systemService = {
  system_info,
  section_list,
  section_create,
  section_update,
  section_remove,
  faq_list,
  faq_create,
  faq_update,
  faq_remove

};
const urls = {
  "list": "/back/store/api/backend_system_info/",
  "backend_system_info": "backend/system/backend_system_info/",
  "section_CRUD": "store/public/sections/",
  "faq_CRUD": "store/public/faqs/",
}

function system_info() {
  return APIServices.get(urls.backend_system_info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function section_list(options) {
  let url = `${urls.section_CRUD}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function section_create(info) {
  return APIServices.post(urls.section_CRUD,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function section_update({section_id,info}) {
  let url = `${urls.section_CRUD}${section_id}/`
  console.log(url, info)
  return APIServices.put(url,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function section_remove(section_id) {
  let url = `${urls.section_CRUD}${section_id}/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function faq_list(options) {
  let url = `${urls.faq_CRUD}${options}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function faq_create(info) {
  console.log("faq_create",urls.faq_CRUD,info)
  return APIServices.post(urls.faq_CRUD,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function faq_update({faq_id,info}) {
  let url = `${urls.faq_CRUD}${faq_id}/`
  return APIServices.put(url,info)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function faq_remove(faq_id) {
  let url = `${urls.faq_CRUD}${faq_id}/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
