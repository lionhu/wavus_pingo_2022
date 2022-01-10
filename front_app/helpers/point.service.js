import {APIServices} from "~/helpers/APIs";

export const pointService = {
  getUserPointlist,
  getUseablePoint,
  getPointHistorySummary
};
const urls = {
  "user_list": "store/public/margins/",
  "history_summary":"store/public/pointbanks/summary/"
}

function getPointHistorySummary() {
  let url = urls.history_summary
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getUserPointlist(options) {
  let url = options !== "" ? `${urls.user_list}${options}` : urls.user_list
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function getUseablePoint() {
  let url = "/back/store/api/pointbank/retrieve_usable_point/"
  return APIServices.post(url)
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
