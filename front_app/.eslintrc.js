module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  parserOptions: {
    parser: "@babel/eslint-parser",
    requireConfigFile: false,
  },
  extends: ["@nuxtjs", "plugin:nuxt/recommended"],
  plugins: [],
  // add your custom rules here
  rules: {
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": 1,
    camelcase: "off",
    "@typescript-eslint/camelcase": "off",
    "vue/prop-name-casing": ["error", "camelCase" | "snake_case"],
  },
};
