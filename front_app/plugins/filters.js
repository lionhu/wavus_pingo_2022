import Vue from 'vue'

const digitsRE = /(\d{3})(?=\d)/g;

Vue.filter('currency', function (value,currency,decimals) {

    value = parseFloat(value);
    if (!isFinite(value) || (!value && value !== 0)) return '';
    currency = currency != null ? currency : '';
    decimals = decimals != null ? decimals : 0;
    var stringified = Math.abs(value).toFixed(decimals);
    var _int = decimals ? stringified.slice(0, -1 - decimals) : stringified;
    var i = _int.length % 3;
    var head = i > 0? (_int.slice(0, i) + (_int.length > 3 ? ',' : '')): '';
    var _float = decimals? stringified.slice(-1 - decimals): '';
    var sign = value < 0 ? '-' : '';
    return sign + currency + head +_int.slice(i).replace(digitsRE, '$1,') +_float
});


Vue.filter('short_date', function (value) {
    var longstr=value.split("T")[0]

    return  longstr.substr(2,8)
});

Vue.filter('https_media_prefix', function (value) {

      return value!==""||value!==null? process.env.DJANGO_SERVER+"/mediafiles/"+value:"";
});
Vue.filter('https_pingo_prefix', function (value) {
      return value!==""||value!==null? process.env.DJANGO_SERVER+value:"";
});
Vue.filter('https_replace_localhost', function (value) {
      return value!==""||value!==null? value.replace("http://localhost:8000",process.env.DJANGO_SERVER):"";
});
Vue.filter('https_replace_http', function (value) {
      return value!==""||value!==null? value.replace("http://","https://"):"";
});
