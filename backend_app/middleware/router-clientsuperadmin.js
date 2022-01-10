export default function ({store, route, redirect}) {
  let isClientSuperAdmin = store.$auth.$state.user.roles.includes("client_superadmin")
  return isClientSuperAdmin ? redirect() : redirectToLogin()

  function redirectToLogin() {
    redirect('/account/login')
  }
}
