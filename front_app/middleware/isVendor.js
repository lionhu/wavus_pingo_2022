export default function ({route, store, redirect}) {
    if (store.state.authfack.user.roles.includes("vendor")) {
        return redirect('/account/dashboard')
    }
    return redirect('/')
}
