import {APIServices} from "~/helpers/APIs"

export const userService = {
  activate,
  resend_activation,
  send_reset_password,
  reset_password,
  reset_password_confirm,
  validEmailFormat,
  validEmail,
  // validate_verification_status,
  check_activation_status,
};
const urls = {
  "resend_activation": `auth/users/resend_activation/`,
  "activate": `auth/users/activation/`,
  "send_reset_password": `auth/users/reset_password/`,
  "reset_password_confirm": `auth/users/reset_password_confirm/`,
  "reset_password": `auth/users/set_password/`,
  "validate_email": `auth/users/validate_email/`,
  // "validate_verification_status": `auth/users/validate_verification_status/`,
  "activation_status": `auth/users/activation_status/`,
}

function resend_activation(data) {
  return APIServices.post(urls.resend_activation, data)
}

function activate(data) {
 return APIServices.post(urls.activate, data)
}

function send_reset_password(data) {
  console.log(data)
 return APIServices.post(urls.send_reset_password, data)
}
function reset_password_confirm(data) {
  console.log(data)
 return APIServices.post(urls.reset_password_confirm, data)
}

function reset_password(data) {
 return APIServices.post(urls.reset_password, data)
}
function validEmailFormat(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return re.test(email)
}

function validEmail(email) {
  if (validEmailFormat(email)) {
    return APIServices.post(urls.validate_email, {"email": email})
      .then(resp => {
        return Promise.resolve(resp.data)
      })
  }
}

function check_activation_status(email) {
  let url =`${urls.activation_status}?email=${email}`
    return APIServices.get(url)
      .then(resp => {
        // console.log("userService validate_email",resp)
        return Promise.resolve(resp.data)
      })
}
