import { createRouter, createWebHashHistory } from "vue-router";
import Storefront from '../views/Storefront.vue';

const routes = [
  {
    path: "/",
    name: "Store",
    component: Storefront
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
