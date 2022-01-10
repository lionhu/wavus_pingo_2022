export let axios;

export default function ({$axios, store, redirect, $auth, app}, inject) {
  $axios.onRequest(request => {
    let loggedIn = $auth.loggedIn;
    let token_valid = $auth.strategy.token.status().valid()
    let refreshToken_valid = $auth.strategy.refreshToken.status().valid()
    if (loggedIn && !token_valid && !refreshToken_valid) {
      $auth.logout()
      redirect("/login")
    } else {
      return request;
    }
  })
  $axios.onResponse(response => {

    console.log('[ RESPONSE ]' + response.request.responseURL, response)
    return response
  });

  $axios.onError(error => {
    console.log(error.response.data)
    // if (error.response && error.response.status === 401) {
    //   error.response.data.result = false;
    //   return Promise.resolve(error.response)
    // }
    error.response.data.result = false;
    return Promise.reject(error)
    // return Promise.reject({result: false, response: error.response});

  });

  axios = $axios;
  inject("axios", axios)
}
