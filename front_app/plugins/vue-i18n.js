import Vue from 'vue';
import VueI18n from 'vue-i18n';


Vue.use(VueI18n);

export default ({app}) => {
    const locale = app.$cookies.get('locale') || 'jp';
    app.i18n = new VueI18n({
        locale,
        fallbackLocale: 'jp',
        messages: {
            jp: require('~/locales/jp.json'),
            zh: require('~/locales/zh.json'),
        }
    });
};
