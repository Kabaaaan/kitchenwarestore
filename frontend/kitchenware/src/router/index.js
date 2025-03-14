import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import CatalogView from "../views/CatalogView.vue";
import ProfileView from "../views/ProfileView.vue";
import SignView from "../views/SignView.vue";
import AboutView from "@/views/AboutView.vue";
import ProductsView from "@/views/admin/ProductsView.vue";
import CategoriesView from "@/views/admin/CategoriesView.vue";
import BrandsView from "@/views/admin/BrandsView.vue";
import ImagesView from "@/views/admin/ImagesView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/catalog/product/:id",
      name: "product",
      component: () => import("@/views/ProductView.vue"), // Ленивая загрузка
    },
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/catalog",
      name: "catalog",
      component: CatalogView,
    },
    {
      path: "/auth",
      name: "auth",
      component: SignView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
    },
    {
      path: "/admin/brands",
      name: "brands",
      component: BrandsView,
    },
    {
      path: "/admin/categories",
      name: "categories",
      component: CategoriesView,
    },
    {
      path: "/admin/products",
      name: "products",
      component: ProductsView,
    },
    {
      path: "/admin/images",
      name: "images",
      component: ImagesView,
    },
  ],
});

export default router;
