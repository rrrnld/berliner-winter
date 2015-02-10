System.config({
  "baseURL": "static/",
  "transpiler": "6to5",
  "paths": {
    "*": "*.js",
    "Reach Out Open Data/*": "js/*.js",
    "github:*": "jspm_packages/github/*.js",
    "npm:*": "jspm_packages/npm/*.js"
  },
  "bundles": {
    "js/bundle": [
      "github:components/jquery@2.1.3/jquery",
      "js/lib/oms.min",
      "js/filter",
      "js/colors",
      "js/popup",
      "github:components/jquery@2.1.3",
      "js/visualization",
      "js/main"
    ]
  }
});

System.config({
  "map": {
    "jquery": "github:components/jquery@2.1.3"
  }
});

