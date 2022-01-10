import * as FontAwesome from './plugins/fontawesome'
import Sass from 'sass'
import Fiber from 'fibers'

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',
  server: {
    port: 9000,
    host: '0.0.0.0'
  },
  router: {
    base: '/'
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'PinGo',
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1'},
      {hid: 'description', name: 'description', content: ''},
      {name: 'format-detection', content: 'telephone=no'}
    ],
    link: [
      {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'}
    ],
    script: [
      // { src: 'https://checkout.stripe.com/checkout.js'}
      //production env
      // {src: 'https://js.squareup.com/v2/paymentform'}
      //sandbox env
      // {src: 'https://js.squareupsandbox.com/v2/paymentform', rel: 'preconnect', crossorigin: 'anonymous'},

      {src: 'https://js.squareupsandbox.com/v2/paymentform'},

      // {src: 'https://js.squareupsandbox.com/v2/paymentform', rel: 'dns-prefetch',},
      // {src: 'https://kit.fontawesome.com/19613bff7e.js'},
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/scss/app.scss',
    'element-ui/lib/theme-chalk/index.css'
  ],
  loading: './components/Loading.vue',
  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    // "~/plugins/axios.js"
    '~/plugins/plugins.js',
    '~/plugins/localStorage.js',
    '~/plugins/filters.js',
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    '@nuxtjs/device',
    '@nuxt/image',
    // '@nuxtjs/pwa',
    ['@nuxtjs/fontawesome', {component: 'fontAwesome', suffix: true}]
  ],
  fontawesome: {
    icons: {
      solid: FontAwesome.solid,
      regular: FontAwesome.regular,
      brands: FontAwesome.brands
    }
  },
  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    'nuxt-i18n',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    '@nuxtjs/auth-next',
    'bootstrap-vue/nuxt',
  ],
  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    https: true,
    baseURL: "https://www.pingo.jp/daphne/api",
    // browserBaseURL:"https://www.pingo.jp",
  },
  auth: {
    // redirect: {
    //   login: '/login',   // 未ログイン時に認証ルートへアクセスした際のリダイレクトURL
    //   logout: '/login',  // ログアウト時のリダイレクトURL
    //   callback: false,   // Oauth認証等で必要となる コールバックルート
    //   home: '/',         // ログイン後のリダイレクトURL
    // },
    plugins: [
      "~/plugins/axios.js"
    ],
    strategies: {
      local: {
        scheme: 'refresh',
        endpoints: {
          login: {url: 'auth/token/obtain/', method: 'post', propertyName: 'token'},
          refresh: {url: 'auth/token/refresh/', method: 'post'},
          user: {url: '/auth/users/me/', method: 'get', propertyName: false},
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
          data: 'refresh', //must set if refreshtoken --- commented by lionhu
          maxAge: 60 * 60 * 24 * 30,
          tokenRequired: true
        },
      }
    }
  },
  // PWA module configuration: https://go.nuxtjs.dev/pwa
  i18n: {
    locales: ['jp'],
    // locales: ['jp', 'zh'],
    defaultLocale: 'jp',
    vueI18n: {
      fallbackLocale: 'jp',
      messages: {
        jp: require('./locales/jp.json'),
        // zh: require('./locales/zh.json')
      }
    }
  },

  bootstrapVue: {
    components: ['BContainer', 'BRow', 'BCol', 'BCard', 'BCardHeader', 'BCardBody', 'BCardText', 'BFormGroup', 'BFormInput', 'BFormRadioGroup', 'BFormRadio',
      'BFormCheckbox', 'BFormSelect', 'BButton', 'BButtonGroup', 'BListGroup', 'BListGroupItem', 'BAlert', 'BAvatar', 'BBadge', 'BTabs', 'BTab', 'BModal', 'BNavItemDropdown',
      'BDropdown', 'BSpinner', 'BCollapse', 'BDropdownItem', 'BBreadcrumb', "BPagination", 'BDropdownHeader', 'BDropdownDivider'],
    directives: ['VBModal', 'VBPopover', 'VBTooltip', 'VBScrollspy', "VBToggle"],
    componentPlugins: [
      'ModalPlugin']
  },

  pwa: {
    manifest: {
      name: "PinGo Mall",
      short_name: "Pingo",
      lang: 'ja',
      icon: {
      source: 'SRC_DIR/static/icon.png',
      fileName: 'icon.png'
    }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    // analyze: true,
    vendor: ["axios", "element-ui"],
    extractCSS: true,
    babel: {
      compact: true
    },
    transpile: [
      "vee-validate/dist/rules",
      "/node_modules\/(dom7|swiper)\/.*/]",
    ],
    optimization: {
      splitChunks: {
        cacheGroups: {
          styles: {
            name: 'styles',
            test: /\.(css|vue)$/,
            chunks: 'all',
            enforce: true
          }
        },
        minSize: 10000,
        maxSize: 250000
      }
    },
    terser: {
      // https://github.com/terser/terser#compress-options
      // drop console.lg()
      terserOptions: {
        compress: {
          drop_console: true
        }
      }
    },
    loaders: {
      scss: {
        implementation: Sass,
        sassOptions: {
          fiber: Fiber
        }
      }
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

  // Build Configuration: https://go.nuxtjs.dev/config-build
  // build: {
  //   vendor: ["axios"],
  //   // vendor:["axios","element-ui"],
  //   extractCSS: true,
  //   babel: {
  //     compact: true
  //   },
  // }
}
