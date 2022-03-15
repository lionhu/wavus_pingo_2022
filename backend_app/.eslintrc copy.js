module.exports = {
    env: {
        browser: true,
        es2021: true,
        jquery: true,
    },
    extends: [
        "eslint:recommended",
        "plugin:vue/recommended",
        "plugin:prettier/recommended",
        // "plugin:vue/essential",
    ],
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
    },
    plugins: ["vue", "prettier"],
    rules: {
        // タグの最後で改行しないで
        "vue/html-closing-bracket-newline": [2, { multiline: "never" }],
        "func-call-spacing": [2, "never"],
        "prettier/prettier": "error",
        "no-unused-vars": 1,
        "prettier.singleQuote": true,
        "prettier.semi": false,
        "prettier.eslintIntegration": true,
        "no-unused-vars": "off",
        "@typescript-eslint/no-unused-vars": 1,
        camelcase: "off",
        "@typescript-eslint/camelcase": "off",
        "vue/prop-name-casing": ["error", "camelCase" | "snake_case"]
    },
}
