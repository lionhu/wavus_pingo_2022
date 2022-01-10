
export default function ({route, store, redirect}) {
  let isSuperAdmin=store.$auth.$state.user.roles.includes("superadmin")
  return  isSuperAdmin ? redirect() : redirectToLogin()

  function redirectToLogin() {
    redirect('/account/login')
  }

}
