export default function ({route, store, redirect}) {
  return store.$auth.$state.loggedIn ? redirect() : redirectToLogin()
  function redirectToLogin() {
    redirect('/account/login')
  }
}
