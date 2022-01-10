import {APIServices} from "~/helpers/APIs";

export const marginService = {
  load_list,
  update,
  batch_update,
  remove,

  load_list_clientadmin,
};
const urls = {
  "CRUD": "store/public/margins/",
  "batch_update": "store/public/margins/update_batch/",
  "client_admin_CRUD": "/back/clientadmin/api/margins/",
}

function load_list(options) {
    let url = `${urls.CRUD}${options}`;
    return APIServices.get(url)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}

function update({margin_id,info}) {
    let url = `${urls.CRUD}${margin_id}/`;
  console.log(margin_id,info)
    return APIServices.patch(url,info)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}
function remove(margin_id) {
    let url = `${urls.CRUD}${margin_id}/`;
    return APIServices.destroy(url)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}
function batch_update(info) {
    let url = urls.batch_update;
    return APIServices.post(url,info)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}

function load_list_clientadmin(options) {
    let url = `${urls.client_admin_CRUD}${options}`;
    return APIServices.get(url)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}
