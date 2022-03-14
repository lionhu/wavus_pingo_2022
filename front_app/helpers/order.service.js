import {axios} from '@/plugins/axios.js';
import {APIServices} from "~/helpers/APIs"

export const orderService = {
  PlaceOrder,
  PlacePingoOrder,
  loadOrders,
  complete_order_user,
  delete_order_user,


  loadPingoOrders,
  loadPingoOrderDetail,
  loadPingoOrders_ME,
  delete_pingoorder_user,
};
const urls = {
  "order_CRUD": "store/public/orders/",
  "pingo_order_CRUD": "store/public/pingo_orders/",
}

function complete_order_user(order_id) {
  let url = `store/public/orders/${order_id}/set_status_completed/`
  return APIServices.post(url)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}


function delete_pingoorder_user(order_id) {
    let url = urls.pingo_order_CRUD;
    if (order_id) {
      url += `${order_id}/`;
    }
    return APIServices.destroy(url)
    .then(handleResponse)
      .then(response => {
        return response;
      })
}

function delete_order_user(order_id = null, type = "REGULAR") {
  let url = type === "PINGO" ? urls.pingo_order_CRUD : urls.order_CRUD;
  if (order_id) {
    url += `${order_id}/`;
  }
  return APIServices.destroy(url)
    .then(response => {
      return response;
    })
}

function PlaceOrder(order_detail) {
  let url = urls.order_CRUD;
  return APIServices.post(url, order_detail)
    .then(response => {
      return response;
    })
}

function PlacePingoOrder(order_detail) {
  let url = urls.pingo_order_CRUD;
  return APIServices.post(url, order_detail)
    .then(response => {
      return response;
    });
}

function loadOrders(options) {
  let url = `${urls.order_CRUD}${options}`;
  return APIServices.get(url)
    .then(response => {
      return response;
    });
}

function loadPingoOrders(options) {
  let url = `${urls.pingo_order_CRUD}?${options.page_info}`;
  return APIServices.get(url)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}
function loadPingoOrderDetail(order_id) {
  let url = `${urls.pingo_order_CRUD}${order_id}/?expand=product`;
  return APIServices.get(url)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function loadPingoOrders_ME(options) {
  let url = `${urls.pingo_order_CRUD}me/?${options.page_info}`;
  return APIServices.get(url)
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function handleResponse(response) {
  if (response.result){
    if (Object.keys(response.data).includes("links")){
      let meta={
        total: response.data.total,
        links: response.data.links,
        page: response.data.page,
        page_size: response.data.page_size,
      }
      return {
        meta:meta,
        results: response.data.results,
      }
    }
    return response.data;
  }
  if (response.status === 404) {
    const error = response.message || response.statusText;
    return Promise.reject(error);
  }
  return response;
}
