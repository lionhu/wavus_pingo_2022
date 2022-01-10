import {APIServices} from "~/helpers/APIs"
import {swalService} from "~/helpers/swal.service";

export const systemService = {
  system_info,
  get_faqs,
  load_store_system_info,
};
const urls = {
  "list": "/back/store/api/backend_system_info/",
  "faqs": "/back/store/api/sections/",
  "store_system_info": 'store/public/system/store_system_info/'
}

function system_info() {
  return APIServices.get(urls.list)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function load_store_system_info() {
  return APIServices.post(urls.store_system_info)
    .then(response => {
      return response;
    });
}

function get_faqs(options) {
  let url = `${urls.faqs}${options}`
  return APIServices.get(url)
    .then(response => {
      return response;
    });
}


function handleResponse(response) {
  const loggeduser = localStorage.getItem('user');
  // alert("stop system")
  if (response === undefined || response.status === 401) {
    if (!loggeduser) {
      window.location.href = "/account/login"
    } else {
      location.reload(true);
    }
  }
  if (!response.result) {
    const error = response.message || response.statusText;
    swalService.showToast('Error', response.message, 'error')
    return Promise.reject(error);
  }
  return response.data;
}
