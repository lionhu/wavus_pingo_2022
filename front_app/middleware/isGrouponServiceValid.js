export default function ({route, store, redirect}) {
  let service_status=store.state.system.services.groupon_buy;
    if (!service_status) {
        return redirect('/')
    }
}
