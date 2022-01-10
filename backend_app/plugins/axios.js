export let axios;

export default function ({$axios, store, redirect, $auth, app}, inject) {
  $axios.onRequest(request => {
    let loggedIn = $auth.loggedIn;
    let token_valid = $auth.strategy.token.status().valid()
    let refreshToken_valid = $auth.strategy.refreshToken.status().valid()

    console.log('[ onRequest ]', request)

    if (loggedIn && !token_valid && !refreshToken_valid) {
      $auth.logout()
      redirect("/login")
    } else {
      return request;
    }
  })
  $axios.onResponse(response => {

    console.log('[ RESPONSE ]' + response.request.responseURL, response)
    if (response.status === 204) {
      response.data = {result: true,status:response.status};
    }
    return response
  });

  $axios.onError(error => {
    // console.log("$axios.onError",error.response.status)
    console.log(error.response.data)
    error.response.data.result = false;
    return Promise.reject(error)
  });

  axios = $axios;
  inject("axios", axios)
}
