<template>
<div>
    <Header />
    <Calendar :attributes="attributes">
        <div slot="day-popover" slot-scope="{ day, dayTitle, attributes }">
            <div class="text-xs text-gray-300 font-semibold text-center">
                {{ dayTitle }}
            </div>
            <popover-row v-for="attr in attributes" :key="attr.key" :attribute="attr">
                {{ attr.customData.description }}
            </popover-row>
        </div>
    </Calendar>
    <Slider />
    <About />
    <!-- <ProductSlider :products="products" :category="category" @openQuickview="showQuickview" @openCompare="showCoampre" @openCart="showCart" /> -->
    <VideoTutorial />
    <!-- <TopProductslider :products="products" @openQuickview="showQuickview" @openCompare="showCoampre" @openCart="showCart" /> -->
    <Blog />
    <!-- <Instagram /> -->
    <Footer />
    <!-- <cartRightModel :openCart="showcartmodal" @closeCart="closeCart" /> -->
</div>
</template>

<script>
import Calendar from 'v-calendar/lib/components/calendar.umd'
import DatePicker from 'v-calendar/lib/components/date-picker.umd'
import PopoverRow from 'v-calendar/lib/components/popover-row.umd.min'
import {
    mapState
} from 'vuex'
// import cartRightModel from '../../../components/cart-model/cart-right-model'
import Slider from './components/slider'
import About from './components/about'
// import ProductSlider from './components/product-slider'
import VideoTutorial from './components/video-tutorial'
// import TopProductslider from './components/top-product-slider'
import Blog from './components/blog'
// import Instagram from './components/instagram'
export default {
    components: {

        Header: () => import('~/components/header/header1'),
        Footer: () => import('~/components/footer/footer1'),
        Slider,
        About,
        // ProductSlider,
        VideoTutorial,
        // TopProductslider,
        Blog,
        // Instagram,
        // cartRightModel,
        Calendar,
        DatePicker,
        PopoverRow
    },
    data() {
        return {
            products: [],
            category: [],
            calendar_attrs: [{
                key: 'today',
                highlight: true,
                dates: new Date(),
            }, ],
            todos: [{
                description: 'Take Noah to basketball practice.',
                isComplete: false,
                dates: {
                    weekdays: 6
                }, // Every Friday
                color: 'red',
            }, ]
            // showquickviewmodel: false,
            // showcomparemodal: false,
            // showcartmodal: false,
            // quickviewproduct: {},
            // comapreproduct: {}
        }
    },
    computed: {
        attributes() {
            return [
                // Attributes for todos
                ...this.todos.map(todo => ({
                    dates: todo.dates,
                    dot: {
                        color: todo.color,
                        class: todo.isComplete ? 'opacity-75' : '',
                    },
                    popover: {
                        label: todo.description,
                    },
                    customData: todo,
                })),
            ];
        }
    },
    mounted() {
        // this.productsArray()
    },
    methods: {
        // productsArray: function () {
        //     this.productslist.map((item) => {
        //         if (item.type === 'beauty') {
        //             this.products.push(item)
        //             item.collection.map((i) => {
        //                 const index = this.category.indexOf(i)
        //                 if (index === -1) this.category.push(i)
        //             })
        //         }
        //     })
        // },
        // showQuickview(item, productData) {
        //     this.showquickviewmodel = item
        //     this.quickviewproduct = productData
        // },
        // showCoampre(item, productData) {
        //     this.showcomparemodal = item
        //     this.comapreproduct = productData
        // },
        // closeCompareModal(item) {
        //     this.showcomparemodal = item
        // },
        // showCart(item) {
        //     this.showcartmodal = item
        // },
        // closeCart(item) {
        //     this.showcartmodal = item
        // }
    }
}
</script>
