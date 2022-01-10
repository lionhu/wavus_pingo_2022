<template>
    <div class="nichiei_wrapper">
        <img :src='imagepath(image)' class="thumbnail">
        <span class="number">{{number}}</span>
        <span class="variation_label">{{number}}</span>
    </div>
</template>

<script>
    import {mapGetters} from "vuex"

    export default {
        props: ["image", "number"],
        computed: {
            ...mapGetters({
                back_server: 'system/getterBackServer'
            })
        },
        methods: {
            imagepath: function (value) {
                return this.back_server + value;
            }
        }
    }
</script>
<style>
    .nichiei_wrapper {
        position: relative;
        display: inline-block;
        margin: 10px;
    }

    .thumbnail {
        max-width: 80px;
    }

    .number {
        position: absolute;
        background: var(--theme-deafult);
        width: 20px;
        height: 20px;
        color: white;
        border-radius: 20px;
        text-align: center;
        font-size: 12px;
        line-height: 14px;
        font-weight: 600;
        /*top: 20%;*/
        right: -8px;
        padding: 3px;
    }

    .variation_label {
        position: absolute;
        bottom: 0px;
        left: 0px;
        margin: 0 5px;
        width: 100%;
        background: grey;
        padding: 2px 5px;
        color: white;
        text-align:center;
    }
</style>
