import {axios} from '@/plugins/axios.js';
// import Swal from "sweetalert2";
import {swalService} from "~/helpers/swal.service";
import {APIServices} from "~/helpers/APIs";

export const userService = {
  login,
  logout,
  register,
  getAll,
  setUserRole,
  validateToken,
  updateUserInfo,
  updateUserProfileInfo,
  query_search_user
};

function query_search_user(field_name,query) {
  let url = `auth/search_users/*${query}*/`
  // let url = `auth/search_users/?${field_name}__startswith=${query}`
  // let url = `auth/users/filter_users?key_str=${query}`
  return APIServices.get(url)
    .then(APIServices.handleResponse)
    .then(response_users => {
      return response_users.map(function (user) {
        return {id: user.id, value: user.username, avatar: user.avatar_url, email: user.email}
      })
    })
}

function validateToken() {
  let user = JSON.parse(localStorage.getItem('user'));
  if (user && user.token) {
    axios.defaults.headers.common['Authorization'] = user.token;
    return axios.$post(`/apiauth/profile/validate_token/`)
      .then(response => {
        return !!(response && response.result);
      })
  }
  return false;
}

function login(email, password, role) {
  return axios.$post(`/apiauth/login/back_login/`, {email, password, role})
    .then(handleResponse)
    .then(user => {
      console.log(user)
      if (user.token) {
        localStorage.setItem('user', JSON.stringify(user));
      }
      return user;
    }).catch(error => {
      console.log(error)
    });
}

function logout() {
  localStorage.removeItem('user');
}

function register(user) {
  const requestOptions = {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(user)
  };
  return fetch(`/users/register`, requestOptions).then(handleResponse);
}

function getAll(url) {
  console.log(url)
  return axios.$get(url)
    .then(response => {
      return response;
    });
}

function setUserRole({user_id, roles}) {
  const url = `/apiauth/users/${user_id}/set_user_role/`
  return axios.$post(url, {user_id, roles})
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function updateUserInfo({user_id, info}) {
  const url = `/apiauth/users/${user_id}/`
  return axios.$put(url, {user_id, info})
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function updateUserProfileInfo({user_id, info}) {
  const url = `/apiauth/profile/${user_id}/`
  return axios.$put(url, {user_id, info})
    .then(handleResponse)
    .then(response => {
      return response;
    });
}

function handleResponse(response) {
  if (response === undefined || response.status === 401) {
    const loggeduser = localStorage.getItem('user');
    if (!loggeduser) {
      window.location.href = "/backend/account/login"
    } else {
      location.reload(true);
    }
  }
  if (!response.result) {
    const error = response.message || response.statusText;
    swalService.showModal('Error', response.message, 'error')
    return Promise.reject(error);
  }
  return response.data;
}

