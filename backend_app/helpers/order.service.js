import { APIServices } from '~/helpers/APIs'

export const orderService = {
    // admin: related API
    get_list,
    update_batch,
    ordercompleted_batch,
    updateOrderItem_superadmin,
    getVendorOrderitemList,
    updateOrderItemStatus,

    // vendor related api
    get_vendor_orderitemlist,
    updateOrderItemStatus_vendor,

    get_FilteredList_superadmin,
    updateOrder_superadmin,
    updateOrder_BATCH_superadmin,
    completeOrder_BATCH_superadmin,
    removeOrder_superadmin,
    batch_removeOrders_superadmin,

    updateOrderItem_BATCH_superadmin,
    getFilteredOrderItems_superadmin,

    getSuperadminFilteredOrderitemList,
    // getVendorFilteredOrderitemList,
}
const urls = {
    list: 'store/public/orders/',
    update_batch: 'store/public/orders/update_batch/',
    ordercompleted_batch: '/admin_back/api/orders/set_status_completed_batch/',
    removeorders_batch: '/admin_back/api/orders/destory_list/',
    superadmin_orderitem_update_batch: 'store/public/orderitems/update_batch/',
    superadmin_orderitem: '/admin_back/api/orderitems/',

    // vendor related urls
    vendor_orderitemlist: '/back/vendor/api/orderitems/',

    // superadmin_list: '/daphne/api/store/public/orders/',
    superadmin_filtered_list: '/admin_back/api/orders/filtered_list/',
    superadmin_orderupdate_batch: '/admin_back/api/orders/update_batch/',
    superadmin_ordercompleted_batch: '/admin_back/api/orders/set_status_completed_batch/',
    // "removeorders_batch": "/back/store/api/orders_superadmin/destory_list/",
    superadmin_filter_orderitemlist: 'store/public/orderitems/filtered_list/',
    vendor_filter_orderitemlist: '/back/store/api/orderitems_vendor/list_filter/',
    // "superadmin_orderitem_update_batch": "/back/store/api/orderitems_superadmin/update_batch/",
}

function get_list(options) {
    let url = `${urls.list}${options}`
    return APIServices.get(url)
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function update_batch(updateinfo) {
    let url = urls.update_batch
    return APIServices.post(url, updateinfo)
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function ordercompleted_batch(updateinfo) {
    let url = urls.ordercompleted_batch
    return APIServices.post(url, updateinfo)
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function batch_removeOrders_superadmin(order_ids) {
    if (order_ids && order_ids.length) {
        let url = urls.removeorders_batch
        return APIServices.post(url, {
            order_ids: order_ids,
        }).then(APIServices.handleResponse)
            .then((response) => {
                // return response;
                if (response.data.result) {
                    return response.data.data
                }
                return Promise.reject(error)
            })
    }
}

function updateOrderItemStatus({ orderitem_id: orderitem_id, status: status }) {
    let url = `${urls.superadmin_orderitem}${orderitem_id}/update_status/`
    return APIServices.post(url, { status: status })
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function updateOrderItemStatus_vendor({ orderitem_id: orderitem_id, status: status }) {
    let url = `${urls.vendor_orderitemlist}${orderitem_id}/update_status/`
    return APIServices.post(url, { status: status })
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function updateOrderItem_BATCH_superadmin(info) {
    console.log(info)
    let url = urls.superadmin_orderitem_update_batch
    return APIServices.post(url, info)
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function getVendorOrderitemList(options) {
    let url = `${urls.superadmin_orderitem}${options}`
    return APIServices.get(url)
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

// vendor related functions
function get_vendor_orderitemlist(options) {
    let url = `${urls.vendor_orderitemlist}${options}`
    return APIServices.get(url)
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function completeOrder_BATCH_superadmin({ order_ids, status }) {
    let url = urls.superadmin_ordercompleted_batch
    return APIServices.post(url, { order_ids: order_ids, status: status })
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function getSuperadminFilteredOrderitemList({ options, data }) {
    let url = `${urls.superadmin_filter_orderitemlist}${options}`
    console.log(url)
    return APIServices.post(url, { filters: data })
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function get_FilteredList_superadmin(orderfilter) {
    let url = urls.superadmin_filtered_list
    console.log(orderfilter)
    return APIServices.post(url, { filters: orderfilter })
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function updateOrder_superadmin(info) {
    if (info.id) {
        let url = `${urls.list}${info.id}/`
        delete info.id
        console.log('info', info)
        return APIServices.put(url, info)
            .then(APIServices.handleResponse)
            .then((response) => {
                return response
            })
    }
}

function updateOrder_BATCH_superadmin(info) {
    if (info.ids && info.ids.length) {
        let url = urls.update_batch
        return APIServices.post(url, info)
            .then(APIServices.handleResponse)
            .then((response) => {
                return Promise.resolve(response)
            })
            .catch((error) => {
                return Promise.reject(error)
            })
    }
}

function removeOrder_superadmin(order_id) {
    let url = `${urls.list}${order_id}/`
    console.log(url)
    return APIServices.destroy(url)
        .then(APIServices.handleResponse)
        .then((response) => {
            return response
        })
}

function getFilteredOrderItems_superadmin(filter_options) {
    console.log(filter_options)
    let url = `${urls.superadmin_orderitem}filtered_list/`
    return axios
        .post(url, { filters: filter_options })
        .then(APIServices.handleResponse)
        .then((response) => {
            // return response;
            if (response.data.result) {
                return response.data.data
            }
            return Promise.reject(error)
        })
}

function insert(info) {
    return APIServices.post(urls.list, info)
        .then(APIServices.handleResponse)
        .then((response) => {
            console.log(response)
            return response
        })
}

function remove(product_id) {
    let url = `${urls.update}product_id`
    return APIServices.destroy(url)
        .then(APIServices.handleResponse)
        .then((response) => {
            console.log(response)
            return response
        })
}

// OrderItem related
function updateOrderItem_superadmin(info) {
    if (info.id) {
        let url = `${urls.superadmin_orderitem}${info.id}/`
        return APIServices.put(url, { update_info: info })
            .then(APIServices.handleResponse)
            .then((response) => {
                return response
            })
    }
}
