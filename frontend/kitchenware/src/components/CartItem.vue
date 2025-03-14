<template>
  <div class="cart-item" v-if="product">
    <div class="item-image">
      <img :src="imageUrl" :alt="product.name" />
    </div>
    <div class="item-details">
      <h3>{{ product.name }}</h3>
      <p class="price">{{ product.price }} ₽</p>
    </div>
    <div class="remove-button" @click="removeFromCart">
      <span class="remove-icon">×</span>
    </div>
  </div>
</template>

<script>
import apiClient from "@/utils/api";

export default {
  props: {
    productId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      product: null,
    };
  },
  computed: {
    imageUrl() {
      const imageUrl = `${apiClient.defaults.baseURL}/products/image/${
        this.productId
      }?timestamp=${Date.now()}`;
      return imageUrl;
    },
  },
  methods: {
    async fetchProduct() {
      const response = await apiClient.get(`/products/${this.productId}`);
      this.product = response.data;
    },
    removeFromCart() {
      let cart = JSON.parse(localStorage.getItem("cart")) || [];
      this.$emit("item-removed", this.productId);
    },
  },
  mounted() {
    this.fetchProduct();
  },
};
</script>
  
<style scoped>
.cart-item {
  min-width: 130px;
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cart-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.remove-button {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border-radius: 30%;
  cursor: pointer;
  transition: background 0.3s ease;
}

.remove-button:hover {
  background: #ff4757;
}

.remove-icon {
  font-size: 1.5em;
  color: black;
  transition: color 0.3s ease;
}

.remove-button:hover .remove-icon {
  color: white;
}

.item-image img {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
}

.item-details {
  flex: 1;
}

h3 {
  font-size: 1em;
  margin: 0;
  color: #333;
}

.price {
  font-size: 1.1em;
  font-weight: bold;
  color: #696969;
}

@media (max-width: 600px) {
  .item-image img {
    display: none;
  }
}
</style>