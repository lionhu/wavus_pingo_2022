export default function ({route, store, redirect}) {
  if (!store.state.authfack.user.roles.includes("superadmin")) {
    return redirect('/')
  }
      console.log("hello superadmin")
}
