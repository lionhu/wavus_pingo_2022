export default function ({route, store, redirect}) {
    if (store.state.authfack.user.roles.includes("client_admin")) {
        return redirect('/account/dashboard')
    }
    return redirect('/')
}
