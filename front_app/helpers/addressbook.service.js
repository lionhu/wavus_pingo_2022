import {axios} from '@/plugins/axios.js';

export const addressbookService = {
  getUserAddressList,
  deleteAddress,
  addAddress,
};
const urls = {
  "CRUD": "store/public/addressbooks/",
}
function getUserAddressList(options){
  let url = urls.CRUD
  return axios.$get(url)
    .then(response => {
      return response;
    });
}

function addAddress(address){
  let url = urls.CRUD
  return axios.$post(url,address)
    .then(response => {
      return response;
    });
}

function deleteAddress(address_id){
  let url = `${urls.CRUD}${address_id}/`
  return axios.$delete(url)
    .then(response => {
      return response;
    });
}

function handleResponse(response) {
  if (response === undefined || response.status === 401) {
    const loggeduser = localStorage.getItem('user');
    if (!loggeduser) {
      window.location.href = "/account/login"
    } else {
      location.reload(true);
    }
  }
  if (!response.result) {
    const error = response.message || response.statusText;
    // Swal.fire('Error', response.message,'error')
    console.log(error)
    return Promise.reject(error);
  }
  return response.data;
}
