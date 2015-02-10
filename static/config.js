System.config({
  "baseURL": "static/",
  "transpiler": "6to5",
  "paths": {
    "*": "*.js",
    "Reach Out Open Data/*": "js/*.js",
    "github:*": "jspm_packages/github/*.js",
    "npm:*": "jspm_packages/npm/*.js"
  }
});

System.config({
  "map": {
    "jquery": "github:components/jquery@2.1.3"
  }
});

