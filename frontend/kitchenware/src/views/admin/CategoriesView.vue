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
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <transition-group name="fade">
            <tr v-for="category in categories.categories" :key="category.id">
              <td>{{ category.id }}</td>
              <td>
                <input
                  v-if="category.isEditing"
                  v-model="category.editedName"
                  class="admin-table__input"
                  type="text"
                />
                <span v-else>{{ category.name }}</span>
              </td>
              <td>
                <button
                  v-if="category.isEditing"
                  class="admin-table__button admin-table__button--confirm"
                  @click="saveCategory(category)"
                >
                  <span class="admin-table__icon">✔️</span>
                </button>
                <button
                  v-else
                  class="admin-table__button admin-table__button--edit"
                  @click="startEditing(category)"
                >
                  <span class="admin-table__icon">✏️</span>
                </button>
                <button
                  class="admin-table__button admin-table__button--delete"
                  @click="openDeleteModal(category.id)"
                >
                  <span class="admin-table__icon">🗑️</span>
                </button>
              </td>
            </tr>
          </transition-group>
          <tr v-if="isAddingNewCategory">
            <td>Новый</td>
            <td>
              <input
                v-model="newCategoryName"
                class="admin-table__input"
                type="text"
                placeholder="Введите название"
              />
            </td>
            <td>
              <button
                class="admin-table__button admin-table__button--confirm"
                @click="saveNewCategory"
              >
                <span class="admin-table__icon">✔️</span>
              </button>
              <button
                class="admin-table__button admin-table__button--cancel"
                @click="cancelAddingNewCategory"
              >
                <span class="admin-table__icon">❌</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="admin-table__add-button" @click="addNewCategory">
        Добавить категорию
      </button>
    </div>

    <transition name="fade">
      <div v-if="isDeleteModalOpen" class="modal-overlay">
        <div class="modal">
          <h3>Подтверждение удаления</h3>
          <p>Вы уверены, что хотите удалить эту категорию?</p>
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
      categories: { categories: [] },
      isAddingNewCategory: false,
      newCategoryName: "",
      isDeleteModalOpen: false,
      categoryToDelete: null,
      userData: null,
    };
  },
  methods: {
    async getCategories() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await apiClient.get("/categories", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.categories = {
          categories: response.data.categories.map((category) => ({
            ...category,
            isEditing: false,
            editedName: category.name,
          })),
        };
      } catch (error) {
        this.handleError(error);
      }
    },
    openDeleteModal(id) {
      this.categoryToDelete = id;
      this.isDeleteModalOpen = true;
    },
    closeDeleteModal() {
      this.isDeleteModalOpen = false;
      this.categoryToDelete = null;
    },
    async confirmDelete() {
      if (this.categoryToDelete) {
        try {
          const accessToken = localStorage.getItem("accessToken");
          await apiClient.delete(`/categories/${this.categoryToDelete}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          this.getCategories();
        } catch (error) {
          this.handleError(error);
        } finally {
          this.closeDeleteModal();
        }
      }
    },
    startEditing(category) {
      category.isEditing = true;
    },
    async saveCategory(category) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await apiClient.put(
          `/categories/${category.id}`,
          {
            name: category.editedName,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        category.name = category.editedName;
        category.isEditing = false;
      } catch (error) {
        this.handleError(error);
      }
    },
    addNewCategory() {
      this.isAddingNewCategory = true;
    },
    async saveNewCategory() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await apiClient.post(
          "/categories",
          {
            name: this.newCategoryName,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.isAddingNewCategory = false;
        this.newCategoryName = "";
        this.getCategories();
      } catch (error) {
        this.handleError(error);
      }
    },
    cancelAddingNewCategory() {
      this.isAddingNewCategory = false;
      this.newCategoryName = "";
    },
    goToProfile() {
      this.$router.push({
        name: "profile",
      });
    },
  },
  mounted() {
    this.fetchUserData();
    this.getCategories();
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/admin_panel.scss";
</style>