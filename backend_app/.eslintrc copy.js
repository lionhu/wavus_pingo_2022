module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  parser: "@babel/eslint-parser",
  parserOptions: {
    requireConfigFile: false,
  },
  extends: [
    "@nuxtjs",
    "plugin:nuxt/recommended",
    "plugin:vue/vue3-essential",
    "prettier",
  ],
  plugins: [],
  rules: {
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": 1,
    camelcase: "off",
    "@typescript-eslint/camelcase": "off",
    "vue/prop-name-casing": ["error", "camelCase" | "snake_case"],
  },
};