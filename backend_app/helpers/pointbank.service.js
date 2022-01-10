import {APIServices} from '~/helpers/APIs';

export const pointbankService = {
  load_list,
  destroy_list,
};
const urls = {
  "CRUD": "store/public/pointbanks/admin_list/",
  "destroy_list": "/admin_back/api/pointbanks/destroy_list/",
  "batch_update": "/admin_back/api/pointbanks/update_batch/",
}

function load_list(options) {
    let url = `${urls.CRUD}${options}`;
    return APIServices.get(url)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}

function destroy_list(info) {
    let url = urls.destroy_list;
    return APIServices.post(url, info)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}
