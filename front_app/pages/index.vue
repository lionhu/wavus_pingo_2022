<template>
<div class="container-fluid">
    <Header />
    <TopLinks />
    <Slider />
    <div class="layout-8 " style="padding:15px 0;">
        <ProductTab />
    </div>
    <Footer />
</div>
</template>

<script>
import {
    mapState,
    mapGetters
} from 'vuex'

export default {
    name: "shop_top",
    components: {
        Header: () => import('~/components/header/header1'),
        Footer: () => import('~/components/footer/footer1'),
        TopLinks: () => import('~/components/widgets/TopLinks'),
        Slider: () => import("~/components/widgets/slider"),
        Recruting: () => import('./components/recruit/half-parallax-banner'),
        Services: () => import("./components/services"),
        Banner: () => import("./components/banner"),
        ProductTab: () => import("./sharebuy/components/product_tab"),
    },
    head() {
        return {
            link: [{
                rel: "stylesheet",
                href: "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
                // https://animate.style/
            }]
        }
    },
    data() {
        return {}
    },
    computed: {
        ...mapState({
            isLoggedIn: state => state.auth.loggedIn,
        }),
        ...mapGetters({
            back_server: 'system/getterBackServer',
        })
    },
    created() {
        this.$store.dispatch("system/init_shop");
    },
}
</script>
