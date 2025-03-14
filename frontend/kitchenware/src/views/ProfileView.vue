<template>
  <div class="personal-cabinet">
    <div v-if="isAuthenticated" class="cabinet-header">
      <div class="user-info">
        <p class="user-name">
          Добро пожаловать, <strong>{{ userData.name }}</strong
          >!
        </p>
        <div>
          <button v-if="is_admin" class="adm-button" @click="goToAdm">
            Админ-панель
          </button>
          <button class="logout-button" @click="logout">Выйти</button>
        </div>
      </div>
    </div>

    <div v-if="isAuthenticated" class="cabinet-content">
      <div class="orders-section">
        <h2 class="section-title">Ваши заказы</h2>
        <div class="orders-list">
          <Order v-for="order in orders" :key="order.id" :order="order" />
        </div>
      </div>

      <div class="cart-section">
        <h2 class="section-title">Корзина</h2>
        <div class="cart-list">
          <CartItem
            v-for="cartItem in cart"
            :key="cartItem"
            :productId="cartItem"
            @item-removed="handleItemRemoved"
          />
        </div>
        <button
          class="order-button"
          @click="createOrder"
          :disabled="isCartEmpty"
        >
          {{ isCartEmpty ? "Ваша корзина пуста" : "Оформить заказ" }}
        </button>
      </div>
    </div>

    <div v-else class="auth-message">
      <p class="auth-text">Пожалуйста, войдите в систему, чтобы продолжить.</p>
      <button class="auth-button" @click="goToAuth">Войти</button>
    </div>

    <transition name="fade">
      <div v-if="orderPlaced" class="order-confirmation">
        <p>Заказ успешно оформлен!</p>
      </div>
    </transition>
  </div>
</template>

<script>
import Order from "../components/Order.vue";
import CartItem from "@/components/CartItem.vue";
import refreshToken from "../utils/refresh";
import apiClient from "../utils/api";

export default {
  components: { Order, CartItem },

  data() {
    return {
      isAuthenticated: false,
      userData: {},
      orders: [],
      cart: [],
      orderPlaced: false,
      is_admin: false,
    };
  },

  computed: {
    isCartEmpty() {
      return this.cart.length === 0;
    },
  },

  methods: {
    async fetchUserData() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await apiClient.get("/users/me", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        this.userData = response.data;
        if (this.userData.role === "admin") {
          this.is_admin = true;
        }
        this.isAuthenticated = true;
        this.getOrders();
        this.getCart();
      } catch (error) {
        if (error.response && error.response.status === 401) {
          const errorDetail = error.response.data.detail;
          console.error(errorDetail);

          if (
            errorDetail === "Invalid access token" ||
            errorDetail === "Access token has expired"
          ) {
            const refresh = localStorage.getItem("refreshToken");
            if (refresh) {
              const tokenRefreshed = await refreshToken();
              if (tokenRefreshed) {
                await this.fetchUserData();
              } else {
                this.isAuthenticated = false;
                this.$router.push({ name: "auth" });
              }
            }
          }
        } else {
          console.error(error);
        }
      }
    },

    async getOrders() {
      const accessToken = localStorage.getItem("accessToken");
      const response = await apiClient.get("/orders", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      this.orders = response.data.Orders;
      this.orders = this.orders.filter(
        (item) => item.user_id === this.userData.id
      );
    },

    async getCart() {
      let storedData = localStorage.getItem("cart");
      let array = JSON.parse(storedData) || [];
      this.cart = array;
    },

    async logout() {
      try {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        this.isAuthenticated = false;
        this.userData = {};

        this.$router.push({ name: "auth" });
      } catch (error) {
        console.error("Ошибка при выходе из системы:", error);
      }
    },

    goToAuth() {
      this.$router.push({
        name: "auth",
      });
    },

    goToAdm() {
      this.$router.push({
        name: "products",
      });
    },

    async createOrder() {
      let total_price = 0;
      for (let i = 0; i < this.cart.length; i++) {
        let product_id = Number(this.cart[i]);
        const response = await apiClient.get(`/products/${product_id}`);
        let product = response.data;
        let price = product.price;
        total_price += price;
      }
      const response = await apiClient.post("/orders/", {
        user_id: this.userData.id,
        total_price: total_price,
      });
      localStorage.removeItem("cart");
      this.cart = [];

      this.orderPlaced = true;
      setTimeout(() => {
        this.orderPlaced = false;
      }, 5000);

      this.getOrders();
    },

    handleItemRemoved(productId) {
      this.cart = this.cart.filter((id) => id !== productId);
      localStorage.setItem("cart", JSON.stringify(this.cart));
    },
  },

  mounted() {
    this.fetchUserData();
  },
};
</script>

<style scoped>
@import "../../src/assets/profile.css";
</style>
