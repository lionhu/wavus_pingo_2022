import {swalService} from "~/helpers/swal.service";
import {APIServices} from "~/helpers/APIs";

export const clientService = {
  load_superadmin_clients,
  load_client,
  register_clients,
  update_client,
  remove_client
};

const urls = {
  "CRUD": "auth/clients/",
}

function load_superadmin_clients(options) {
  let url=`${urls.CRUD}${options}`
  console.log("load clients",url)
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(res => {
      console.log(res)
      return res;
    }).catch(error => {
      console.log(error)

    });
}

function remove_client(client_id) {
  let url=`${urls.CRUD}${client_id}/`
  console.log("remove_client",url)
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    }).catch(error => {
      console.log(error)
    });
}

function register_clients(info) {
  let url=urls.CRUD
  return APIServices.post(url, info)
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    })
}
function update_client({client_id,info}) {
  let url=`${urls.CRUD}${client_id}/`
  console.log("update info",url, info)
  return APIServices.put(url, info)
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    }).catch(error => {
      console.log(error)
    });
}
function load_client(client_id) {
  let url=`${urls.CRUD}${client_id}/`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    }).catch(error => {
      console.log(error)
    });
}
