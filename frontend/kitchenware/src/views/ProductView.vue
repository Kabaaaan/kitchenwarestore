<template>
  <div class="product-detail">
    <div v-if="product" class="product-card">
      <div class="product-image">
        <img :src="imageUrl" :alt="product.name" />
      </div>
      <div class="product-info">
        <h2>{{ product.name }}</h2>
        <p class="brand">Бренд: {{ brand || "Не указано" }}</p>
        <p class="category">Категория: {{ category || "Не указано" }}</p>
        <p class="description">{{ product.description }}</p>
        <p class="price">Цена: {{ product.price }} ₽</p>
        <button
          class="add-to-cart"
          @click="addToCart"
          :class="{ added: isAdded }"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"
            />
          </svg>
          {{ isAdded ? "В корзине" : "В корзину" }}
        </button>
      </div>
    </div>
    <p v-else class="loading">Загрузка данных...</p>
    <div class="similar">
      <h2>Похожие товары ({{ similar_count }}):</h2>
      <div v-if="similar_products.length" class="similar_items">
        <Product
          v-for="product in similar_products"
          :key="product.id"
          :product="product"
        />
      </div>
      <div v-else>
        <p>Нет товаров, соответствующих выбранным фильтрам.</p>
      </div>
    </div>
  </div>
</template>

<script>
import Product from "../components/Product.vue";
import apiClient from "../utils/api";

export default {
  components: { Product },
  data() {
    return {
      product: null,
      category: "",
      brand: "",
      similar_products: [],
      similar_count: 0,
      isAdded: false,
    };
  },
  computed: {
    imageUrl() {
      const imageURL = `${apiClient.defaults.baseURL}/products/image/${
        this.$route.params.id
      }?timestamp=${Date.now()}`;
      return imageURL;
    },
  },
  methods: {
    async fetchProduct() {
      try {
        const response = await apiClient.get(
          `/products/${this.$route.params.id}`
        );
        this.product = response.data;
        this.getCategoryAndBrand();
        this.getSimilarProducts();
        this.checkIfAdded();
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      }
    },
    async getCategoryAndBrand() {
      const response_category = await apiClient.get(
        `/categories/${this.product.category_id}`
      );
      this.category = response_category.data.name;
      const response_brand = await apiClient.get(
        `/brands/${this.product.brand_id}`
      );
      this.brand = response_brand.data.name;
    },
    async getSimilarProducts() {
      const response = await apiClient.get(
        `/products/filter/both/${this.product.category_id}/${this.product.brand_id}`
      );
      this.similar_products = response.data.Products;
      this.similar_products = this.similar_products.filter(
        (item) => item.id !== this.product.id
      );
      this.similar_count = response.data.Count - 1;
    },
    addToCart() {
      let storedData = localStorage.getItem("cart");
      let array = storedData ? JSON.parse(storedData) : [];
      if (!array.includes(this.product.id)) {
        array.push(this.product.id);
        localStorage.setItem("cart", JSON.stringify(array));
        this.isAdded = true;
      }
    },
    checkIfAdded() {
      let storedData = localStorage.getItem("cart");
      let array = storedData ? JSON.parse(storedData) : [];
      this.isAdded = array.includes(this.product.id);
    },
  },
  mounted() {
    this.fetchProduct();
  },
  watch: {
    "$route.params.id": {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchProduct();
        }
      },
    },
  },
};
</script>

<style scoped>
.product-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.product-card {
  display: flex;
  gap: 30px;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.product-image img {
  width: 100%;
  max-width: 300px;
  height: auto;
  border-radius: 10px;
}

.product-info {
  flex: 1;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 32px;
}

h2 {
  font-size: 28px;
  margin-bottom: 15px;
  color: #222;
}

.brand,
.category {
  font-size: 18px;
  color: #555;
  margin-bottom: 10px;
}

.description {
  font-size: 18px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.price {
  font-size: 26px;
  font-weight: bold;
  color: #28a745;
  margin-bottom: 20px;
}

.loading {
  text-align: center;
  font-size: 20px;
  color: #888;
}

.similar .product-card {
  width: 50%;
  background-color: #c8d6c7;
  border: none;
  box-shadow: none;
}

.add-to-cart {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-to-cart:hover {
  background-color: #218838;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.add-to-cart:active {
  transform: scale(0.95);
}

.add-to-cart.added {
  background-color: #6c757d;
  cursor: default;
}

.add-to-cart.added:hover {
  transform: none;
  box-shadow: none;
}

.add-to-cart svg {
  width: 24px;
  height: 24px;
  fill: white;
  transition: transform 0.3s ease;
}

.add-to-cart:hover svg {
  transform: translateX(5px);
}
</style>