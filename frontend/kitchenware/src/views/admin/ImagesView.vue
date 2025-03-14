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
            <th>Фото</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <transition-group name="fade">
            <tr v-for="product in products" :key="product.id">
              <td>{{ product.id }}</td>
              <td>{{ product.name }}</td>
              <td>
                <img
                  v-if="product.imageUrl"
                  :src="product.imageUrl"
                  alt="Product Image"
                  style="width: 50px; height: 50px"
                />
                <span v-else>Нет изображения</span>
              </td>
              <td>
                <button
                  class="admin-table__button admin-table__button--delete"
                  @click="openDeleteImageModal(product.id)"
                >
                  <span class="admin-table__icon">🗑️</span>
                </button>
                <button
                  class="admin-table__button admin-table__button--upload"
                  @click="openUploadImageModal(product.id)"
                >
                  <span class="admin-table__icon">📤</span>
                </button>
              </td>
            </tr>
          </transition-group>
        </tbody>
      </table>
    </div>

    <transition name="fade">
      <div v-if="isDeleteImageModalOpen" class="modal-overlay">
        <div class="modal">
          <h3>Подтверждение удаления</h3>
          <p style="text-align: center">
            Вы уверены, что хотите удалить это изображение?
          </p>
          <div class="modal-actions">
            <button
              class="modal-button modal-button--confirm"
              @click="confirmDeleteImage"
            >
              Удалить
            </button>
            <button
              class="modal-button modal-button--cancel"
              @click="closeDeleteImageModal"
            >
              Отмена
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="isUploadImageModalOpen" class="modal-overlay">
        <div class="modal">
          <h3>Загрузить изображение</h3>
          <form @submit.prevent="uploadImage">
            <div class="form-group">
              <input type="file" @change="onFileChange" required />
            </div>
            <div class="modal-actions">
              <button type="submit" class="modal-button modal-button--confirm">
                Загрузить
              </button>
              <button
                type="button"
                class="modal-button modal-button--cancel"
                @click="closeUploadImageModal"
              >
                Отмена
              </button>
            </div>
          </form>
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
      products: [],
      isDeleteImageModalOpen: false,
      isUploadImageModalOpen: false,
      productIdToDelete: null,
      productIdToUpload: null,
      selectedFile: null,
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
        this.products = response.data.Products.map((product) => ({
          ...product,
          imageUrl: `${apiClient.defaults.baseURL}/products/image/${
            product.id
          }?timestamp=${Date.now()}`,
        }));
      } catch (error) {
        this.handleError(error);
      }
    },
    openDeleteImageModal(productId) {
      this.productIdToDelete = productId;
      this.isDeleteImageModalOpen = true;
    },
    closeDeleteImageModal() {
      this.isDeleteImageModalOpen = false;
      this.productIdToDelete = null;
    },
    async confirmDeleteImage() {
      if (this.productIdToDelete) {
        try {
          const accessToken = localStorage.getItem("accessToken");
          await apiClient.delete(`/products/image/${this.productIdToDelete}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          this.getProducts();
        } catch (error) {
          this.handleError(error);
        } finally {
          this.closeDeleteImageModal();
        }
      }
    },
    openUploadImageModal(productId) {
      this.productIdToUpload = productId;
      this.isUploadImageModalOpen = true;
    },
    closeUploadImageModal() {
      this.isUploadImageModalOpen = false;
      this.productIdToUpload = null;
      this.selectedFile = null;
    },
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadImage() {
      if (!this.selectedFile || !this.productIdToUpload) return;

      try {
        const accessToken = localStorage.getItem("accessToken");
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        try {
          await apiClient.post(
            `/products/image/upload/${this.productIdToUpload}`,
            formData,
            {
              headers: {
                Authorization: `Bearer ${accessToken}`,
                "Content-Type": "multipart/form-data",
              },
            }
          );
        } catch (error) {
          if (error.response && error.response.status === 405) {
            await apiClient.put(
              `/products/image/update/${this.productIdToUpload}`,
              formData,
              {
                headers: {
                  Authorization: `Bearer ${accessToken}`,
                  "Content-Type": "multipart/form-data",
                },
              }
            );
          } else {
            throw error;
          }
        }

        this.closeUploadImageModal();
        this.getProducts();
      } catch (error) {
        this.handleError(error);
      }
    },
    handleError(error) {
      console.error(error);
    },
    goToProfile() {
      this.$router.push({ name: "profile" });
    },
  },
  mounted() {
    this.fetchUserData();
    this.getProducts();
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/admin_panel.scss";
</style>