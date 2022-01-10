export default function ({route, store, redirect}) {
    var hasItem= store.state.cart.cart.length;
    if (hasItem===0) {
        return redirect('/')
    }
}
