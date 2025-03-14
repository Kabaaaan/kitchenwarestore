<template>
  <div>
    <div class="admin-layout">
      <AdminNav />
    </div>
    <div class="admin-table-container">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Описание</th>
            <th>Цена</th>
            <th>Фото</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <transition-group name="fade">
            <tr v-for="product in products.products" :key="product.id">
              <td>{{ product.id }}</td>
              <td>
                <input
                  v-if="product.isEditing"
                  v-model="product.editedName"
                  class="admin-table__input"
                  type="text"
                />
                <span v-else>{{ product.name }}</span>
              </td>
              <td>
                <input
                  v-if="product.isEditing"
                  v-model="product.editedDescription"
                  class="admin-table__input"
                  type="text"
                />
                <span v-else>{{ product.description }}</span>
              </td>
              <td>
                <input
                  v-if="product.isEditing"
                  v-model="product.editedPrice"
                  class="admin-table__input"
                  type="number"
                />
                <span v-else>{{ product.price }}</span>
              </td>
              <td>
                <img
                  v-if="product.imageUrl"
                  :src="product.imageUrl"
                  alt="Product Image"
                  style="width: 50px; height: 50px"
                />
              </td>
              <td>
                <button
                  v-if="product.isEditing"
                  class="admin-table__button admin-table__button--confirm"
                  @click="saveProduct(product)"
                >
                  <span class="admin-table__icon">✔️</span>
                </button>
                <button
                  v-else
                  class="admin-table__button admin-table__button--edit"
                  @click="startEditing(product)"
                >
                  <span class="admin-table__icon">✏️</span>
                </button>
                <button
                  class="admin-table__button admin-table__button--delete"
                  @click="openDeleteModal(product.id)"
                >
                  <span class="admin-table__icon">🗑️</span>
                </button>
              </td>
            </tr>
          </transition-group>
        </tbody>
      </table>
      <button class="admin-table__add-button" @click="openAddProductModal">
        Добавить продукт
      </button>
    </div>

    <transition name="fade">
      <div v-if="isAddProductModalOpen" class="modal-overlay">
        <div class="modal">
          <h3>Добавить новый продукт</h3>
          <form @submit.prevent="saveNewProduct">
            <div class="form-group">
              <label>Название:</label>
              <input v-model="newProductName" type="text" required />
            </div>
            <div class="form-group">
              <label>Описание:</label>
              <input v-model="newProductDescription" type="text" required />
            </div>
            <div class="form-group">
              <label>Цена:</label>
              <input v-model="newProductPrice" type="number" required />
            </div>
            <div class="form-group">
              <label>Категория:</label>
              <select v-model="newProductCategoryId" required>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Бренд:</label>
              <select v-model="newProductBrandId" required>
                <option
                  v-for="brand in brands"
                  :key="brand.id"
                  :value="brand.id"
                >
                  {{ brand.name }}
                </option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="submit" class="modal-button modal-button--confirm">
                Добавить
              </button>
              <button
                type="button"
                class="modal-button modal-button--cancel"
                @click="closeAddProductModal"
              >
                Отмена
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="isDeleteModalOpen" class="modal-overlay">
        <div class="modal">
          <h3>Подтверждение удаления</h3>
          <p style="text-align: center">
            Вы уверены, что хотите удалить этот продукт?
          </p>
          <div class="modal-actions">
            <button
              class="modal-button modal-button--confirm"
              @click="confirmDelete"
            >
              Удалить
            </button>
            <button
              class="modal-button modal-button--cancel"
              @click="closeDeleteModal"
            >
              Отмена
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import apiClient from "@/utils/api";
import AdminNav from "@/components/AdminNav.vue";
import { fetchUserDataMixin } from "@/utils/fetchUserDataMixin";

export default {
  components: {
    AdminNav,
  },
  mixins: [fetchUserDataMixin],
  data() {
    return {
      products: { products: [] },
      isAddProductModalOpen: false,
      newProductName: "",
      newProductDescription: "",
      newProductPrice: 0,
      newProductCategoryId: null,
      newProductBrandId: null,
      categories: [],
      brands: [],
      isDeleteModalOpen: false,
      productToDelete: null,
      userData: null,
    };
  },
  methods: {
    async getProducts() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await apiClient.get("/products", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.products = {
          products: response.data.Products.map((product) => ({
            ...product,
            isEditing: false,
            editedName: product.name,
            editedDescription: product.description,
            editedPrice: product.price,
            imageUrl: `${apiClient.defaults.baseURL}/products/image/${
              product.id
            }?timestamp=${Date.now()}`,
          })),
        };
      } catch (error) {
        this.handleError(error);
      }
    },
    async getCategories() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await apiClient.get("/categories", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.categories = response.data.categories;
      } catch (error) {
        this.handleError(error);
      }
    },
    async getBrands() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await apiClient.get("/brands", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.brands = response.data.brands;
      } catch (error) {
        this.handleError(error);
      }
    },
    openAddProductModal() {
      this.isAddProductModalOpen = true;
    },
    closeAddProductModal() {
      this.isAddProductModalOpen = false;
      this.resetNewProductForm();
    },
    resetNewProductForm() {
      this.newProductName = "";
      this.newProductDescription = "";
      this.newProductPrice = 0;
      this.newProductCategoryId = null;
      this.newProductBrandId = null;
    },
    async saveNewProduct() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await apiClient.post(
          "/products/",
          {
            name: this.newProductName,
            description: this.newProductDescription,
            price: this.newProductPrice,
            category_id: this.newProductCategoryId,
            brand_id: this.newProductBrandId,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.closeAddProductModal();
        this.getProducts();
      } catch (error) {
        this.handleError(error);
      }
    },
    openDeleteModal(id) {
      this.productToDelete = id;
      this.isDeleteModalOpen = true;
    },
    closeDeleteModal() {
      this.isDeleteModalOpen = false;
      this.productToDelete = null;
    },
    async confirmDelete() {
      if (this.productToDelete) {
        try {
          const accessToken = localStorage.getItem("accessToken");
          await apiClient.delete(`/products/${this.productToDelete}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          this.getProducts();
        } catch (error) {
          this.handleError(error);
        } finally {
          this.closeDeleteModal();
        }
      }
    },
    startEditing(product) {
      product.isEditing = true;
    },
    async saveProduct(product) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await apiClient.put(
          `/products/${product.id}`,
          {
            name: product.editedName,
            description: product.editedDescription,
            price: product.editedPrice,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        product.name = product.editedName;
        product.description = product.editedDescription;
        product.price = product.editedPrice;
        product.isEditing = false;
      } catch (error) {
        this.handleError(error);
      }
    },
    handleError(error) {
      console.error(error);
    },
  },
  mounted() {
    this.fetchUserData();
    this.getProducts();
    this.getCategories();
    this.getBrands();
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/admin_panel.scss";
</style>