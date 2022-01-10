import {APIServices} from "~/helpers/APIs";

export const logisticService = {
  list_logistic,
  create_logistic,
  update_logistic,
  remove_logistic
};

const urls = {
  "CRUD": "store/public/logistics/",
}

function list_logistic() {
  let url=`${urls.CRUD}?per_page=20`;
  return APIServices.get(url, )
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    })
}
function create_logistic(info) {
  let url=urls.CRUD;
  return APIServices.put(url, info)
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    })
}
function update_logistic({logistic_id,info}) {
  console.log(logistic_id,info)
  let url=`${urls.CRUD}${logistic_id}/`
  return APIServices.put(url, info)
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    })
}

function remove_logistic(logistic_id) {
  let url=`${urls.CRUD}/${logistic_id}/`
  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(res => {
      return res;
    })
}

