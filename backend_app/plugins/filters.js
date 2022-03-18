import Vue from 'vue'

const digitsRE = /(\d{3})(?=\d)/g

Vue.filter('currency', function (value, currency, decimals) {
    value = parseFloat(value)
    if (!isFinite(value) || (!value && value !== 0)) return ''
    currency = currency != null ? currency : ''
    decimals = decimals != null ? decimals : 0
    var stringified = Math.abs(value).toFixed(decimals)
    var _int = decimals ? stringified.slice(0, -1 - decimals) : stringified
    var i = _int.length % 3
    var head = i > 0 ? _int.slice(0, i) + (_int.length > 3 ? ',' : '') : ''
    var _float = decimals ? stringified.slice(-1 - decimals) : ''
    var sign = value < 0 ? '-' : ''
    return sign + currency + head + _int.slice(i).replace(digitsRE, '$1,') + _float
})

Vue.filter('short_date', function (value) {
    if (value) {
        var longstr = value.split('T')[0]
        return longstr.substr(2, 8)
    }
    return ''
})

Vue.filter('short_datetime', function (value) {
    if (value) {
        return value.split('.')[0].replace('T', ' ')
    }
    return ''
})

Vue.filter('short_time', function (value) {
    if (value) {
        return value.split('.')[0].split('T')[1]
    }
    return ''
})

Vue.filter('https_media_prefix', function (value) {
    return process.env.DJANGO_SERVER + '/mediafiles/' + value
})
Vue.filter('https_replace_localhost', function (value) {
    return value.replace('http://localhost:8000', '')
})
Vue.filter('https_replace_http', function (value) {
    return value.replace('http://', 'https://')
})
Vue.filter('order_status_badge_color', function (order_status) {
    let _color = 'success'
    switch (order_status.toLowerCase()) {
        case 'new':
            _color = 'danger'
            break
        case 'processing':
            _color = 'warning'
            break
        case 'delivering':
            _color = 'primary'
            break
        case 'completed':
            _color = 'success'
            break
        default:
            _color = 'secondary'
    }
    return _color
})
Vue.filter('order_payment_methond', function (payment_methond) {
    let _payment_methond = 'fe-credit-card'
    switch (payment_methond.toLowerCase()) {
        case 'card':
            _payment_methond = 'fe-credit-card'
            break
        case 'point':
            _payment_methond = 'fe-database'
            break
        case 'mix':
            _payment_methond = 'fe-command'
            break
        default:
            _payment_methond = 'fe-command'
    }
    return _payment_methond
})
Vue.filter('order_payment_status_color', function (_payment_status) {
    let _payment_status_color = 'btn-secondary'
    switch (_payment_status.toLowerCase()) {
        case 'canceled':
            _payment_status_color = 'btn-danger'
            break
        case 'completed':
            _payment_status_color = 'btn-success'
            break
        case 'approved':
            _payment_status_color = 'btn-warning'
            break
        default:
            _payment_status_color = 'btn-secondary'
    }
    return _payment_status_color
})
