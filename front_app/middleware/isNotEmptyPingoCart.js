export default function ({route, store, redirect}) {
    var PINGOCART= store.state.pingoproducts.cart;
    if (PINGOCART!==null && PINGOCART.product.id) {
        return redirect()
    }else{
        return redirect("/pingo")
    }
}
