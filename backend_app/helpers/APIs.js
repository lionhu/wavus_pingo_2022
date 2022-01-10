import {axios} from '@/plugins/axios.js';

export const APIServices = {
  get,
  post,
  put,
  patch,
  destroy,
  handleResponse
};

function post(url, data) {
  return axios.$post(url, data)
    .then(response => {
      return Promise.resolve(response)
    }).catch(error => {
      return Promise.reject(error.response)
    });
}

function get(url) {
  return axios.$get(url)
    .then(response => {
      return Promise.resolve(response)
    })
}

function destroy(url) {
  return axios.$delete(url)
    .then(response => {
      return Promise.resolve(response)
    }).catch(error => {
      return Promise.reject(error.response)
    });
}

function put(url, data) {
  return axios.$put(url, data)
    .then(response => {
      return Promise.resolve(response)
    })
}

function patch(url, data) {
  return axios.$patch(url, data)
    .then(response => {
      return Promise.resolve(response)
    })
}

function handleResponse(response) {
  if (response.result) {
    // console.log("handleResponse",response)
    // console.log("response.status",response.status)
    if (response.status===204){
      return response;
    }
    if (Object.keys(response.data).length>0 && Object.keys(response.data).includes("links")) {
      let meta = {
        total: response.data.total,
        links: response.data.links,
        page: response.data.page,
        page_size: response.data.page_size,
      }
      return {
        meta: meta,
        results: response.data.results,
      }
    }
    return response.data;
  }
  if (response.status === 404) {
    const error = response.message || response.statusText;
    // console.log(error)
    return Promise.reject(error);
  }
  return response;
}
