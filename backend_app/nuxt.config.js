import * as FontAwesome from './plugins/fontawesome'
import TerserPlugin from 'terser-webpack-plugin';
const environment = process.env.NODE_ENV;
const envSettings = require('./env.pingo.js');

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,
  dev: false,
  server: {
    port: 3000,
    host: '0.0.0.0'
  },
  env: envSettings,
  router: {
    base: '/backend/'
    // base: '/'
  },
  target: 'static',
  loading: './components/Loading.vue',
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'PINGO backend',
    htmlAttrs: { lang: 'en' },
    base: { href: 'router.base' },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    script: [
      // {src: 'https://unpkg.com/element-ui/lib/index.js'},
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/backend/favicon.ico' }]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '~/assets/scss/app.scss'
    // 'https://unpkg.com/element-ui/lib/theme-chalk/index.css'
    // './node_modules/element-ui/packages/theme-chalk/src/base.scss',
  ],

  plugins: [
    '~/plugins/localStorage.js',
    '~/plugins/filters.js',
    '~/plugins/vue_lazyload.js',
    '~/plugins/vue-click-outside.js',
    '~/plugins/vuelidate.js'
  ],

  components: true,

  buildModules: [
    // https://go.nuxtjs.dev/typescript
    // '@nuxt/typescript-build',

    ['@nuxtjs/fontawesome', { component: 'fontAwesome', suffix: true }]
  ],

  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    'nuxt-i18n',
    'bootstrap-vue/nuxt',
    // "nuxt-fontawesome",
    '@nuxt/image'
  ],
  auth: {
    // redirect: {
    //   login: '/login',   // 未ログイン時に認証ルートへアクセスした際のリダイレクトURL
    //   logout: '/login',  // ログアウト時のリダイレクトURL
    //   callback: false,   // Oauth認証等で必要となる コールバックルート
    //   home: '/',         // ログイン後のリダイレクトURL
    // },
    plugins: ['~/plugins/axios.js'],
    strategies: {
      local: {
        scheme: 'refresh',
        endpoints: {
          login: {
            url: 'auth/token/obtain/',
            method: 'post',
            propertyName: 'token'
          },
          refresh: { url: 'auth/token/refresh/', method: 'post' },
          user: { url: 'auth/users/me/', method: 'get', propertyName: false },
          logout: false
        },
        user: {
          property: 'data.user',
          autoFetch: true
        },
        token: {
          property: 'data.access',
          // data: 'access',
          maxAge: 60 * 60 * 24
          // maxAge: 60
        },
        refreshToken: {
          property: 'data.refresh',
          data: 'refresh', // must set if refreshtoken --- commented by lionhu
          maxAge: 60 * 60 * 24 * 30,
          tokenRequired: true
        }
      }
    }
  },
  fontawesome: {
    // component: "fa",
    // imports: [
    //   {
    //     set: "@fortawesome/free-solid-svg-icons",
    //     icons: ["faAdjust", "faHeart", "faUser", "faSpinner"]
    //   }
    // ],
    icons: {
      solid: FontAwesome.solid,
      regular: FontAwesome.regular,
      brands: FontAwesome.brands
    }
  },

  bootstrapVue: {
    components: [
      'BContainer',
      'BRow',
      'BCol',
      'BForm',
      'BFormGroup',
      'BFormInput',
      'BFormRadioGroup',
      'BFormRadio',
      'BFormCheckbox',
      'BFormSelect',
      'BFormSelectOption',
      'BButton',
      'BAlert',
      'BBadge',
      'BTabs',
      'BTab',
      'BModal',
      'BNavItemDropdown',
      'BDropdown',
      'BSpinner',
      'BOverlay',
      'BDropdownItem',
      'BBreadcrumb',
      'BDropdownHeader',
      'BDropdownDivider',
      'BPagination'
    ],
    directives: ['VBModal', 'VBPopover', 'VBTooltip', 'VBScrollspy'],
    componentPlugins: ['ModalPlugin']
  },
  i18n: {
    locales: ['en', 'jp', 'zh'],
    defaultLocale: 'jp',
    vueI18n: {
      fallbackLocale: 'jp',
      messages: {
        en: require('./locales/en.json'),
        jp: require('./locales/jp.json'),
        zh: require('./locales/zh.json')
      }
    }
  },
  axios: {
    https: true,
    baseURL: 'https://www.pingo.jp/daphne/api/'
  },
  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    // analyze: true,
    extractCSS: true,
    babel: {
      compact: true
    },
    transpile: ['vee-validate/dist/rules', '/node_modules/(dom7|swiper)/.*/]'],
    optimization: {
      minimize: true,
      minimizer: [
        new TerserPlugin({
          cache: true,
          parallel: false
        })
      ]
    }
  },

  watchers: {
    chokidar: {
      usePolling: true,
      useFsEvents: false
    },
    webpack: {
      aggregateTimeout: 300,
      poll: true
    }
  }
};
