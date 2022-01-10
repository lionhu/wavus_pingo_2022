export default function ({store, route, redirect}) {

  let isSupplier = store.$auth.$state.user.roles.includes("supplier")
  return isSupplier ? redirect() : redirectToLogin()

  function redirectToLogin() {
    redirect('/account/login')
  }


}
