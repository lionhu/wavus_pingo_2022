export default function ({store, route, redirect}) {

  let isClient = store.$auth.$state.user.roles.includes("client")
  return isClient ? redirect() : redirectToLogin()

  function redirectToLogin() {
    redirect('/account/login')
  }

}
