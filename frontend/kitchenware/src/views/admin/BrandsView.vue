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
            <tr v-for="brand in brands.brands" :key="brand.id">
              <td>{{ brand.id }}</td>
              <td>
                <input
                  v-if="brand.isEditing"
                  v-model="brand.editedName"
                  class="admin-table__input"
                  type="text"
                />
                <span v-else>{{ brand.name }}</span>
              </td>
              <td>
                <button
                  v-if="brand.isEditing"
                  class="admin-table__button admin-table__button--confirm"
                  @click="saveBrand(brand)"
                >
                  <span class="admin-table__icon">✔️</span>
                </button>
                <button
                  v-else
                  class="admin-table__button admin-table__button--edit"
                  @click="startEditing(brand)"
                >
                  <span class="admin-table__icon">✏️</span>
                </button>
                <button
                  class="admin-table__button admin-table__button--delete"
                  @click="openDeleteModal(brand.id)"
                >
                  <span class="admin-table__icon">🗑️</span>
                </button>
              </td>
            </tr>
          </transition-group>
          <tr v-if="isAddingNewBrand">
            <td>Новый</td>
            <td>
              <input
                v-model="newBrandName"
                class="admin-table__input"
                type="text"
                placeholder="Введите название"
              />
            </td>
            <td>
              <button
                class="admin-table__button admin-table__button--confirm"
                @click="saveNewBrand"
              >
                <span class="admin-table__icon">✔️</span>
              </button>
              <button
                class="admin-table__button admin-table__button--cancel"
                @click="cancelAddingNewBrand"
              >
                <span class="admin-table__icon">❌</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="admin-table__add-button" @click="addNewBrand">
        Добавить бренд
      </button>
    </div>

    <transition name="fade">
      <div v-if="isDeleteModalOpen" class="modal-overlay">
        <div class="modal">
          <h3>Подтверждение удаления</h3>
          <p>Вы уверены, что хотите удалить этот бренд?</p>
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
      brands: { brands: [] },
      isAddingNewBrand: false,
      newBrandName: "",
      isDeleteModalOpen: false,
      brandToDelete: null,
      userData: null,
    };
  },
  methods: {
    async getBrands() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await apiClient.get("/brands", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.brands = {
          brands: response.data.brands.map((brand) => ({
            ...brand,
            isEditing: false,
            editedName: brand.name,
          })),
        };
      } catch (error) {
        this.handleError(error);
      }
    },
    openDeleteModal(id) {
      this.brandToDelete = id;
      this.isDeleteModalOpen = true;
    },
    closeDeleteModal() {
      this.isDeleteModalOpen = false;
      this.brandToDelete = null;
    },
    async confirmDelete() {
      if (this.brandToDelete) {
        try {
          const accessToken = localStorage.getItem("accessToken");
          await apiClient.delete(`/brands/${this.brandToDelete}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          this.getBrands();
        } catch (error) {
          this.handleError(error);
        } finally {
          this.closeDeleteModal();
        }
      }
    },
    startEditing(brand) {
      brand.isEditing = true;
    },
    async saveBrand(brand) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await apiClient.put(
          `/brands/${brand.id}`,
          {
            name: brand.editedName,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        brand.name = brand.editedName;
        brand.isEditing = false;
      } catch (error) {
        this.handleError(error);
      }
    },
    addNewBrand() {
      this.isAddingNewBrand = true;
    },
    async saveNewBrand() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await apiClient.post(
          "/brands",
          {
            name: this.newBrandName,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.isAddingNewBrand = false;
        this.newBrandName = "";
        this.getBrands();
      } catch (error) {
        this.handleError(error);
      }
    },
    cancelAddingNewBrand() {
      this.isAddingNewBrand = false;
      this.newBrandName = "";
    },
    goToProfile() {
      this.$router.push({
        name: "profile",
      });
    }
  },
  mounted() {
    this.fetchUserData();
    this.getBrands();
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/admin_panel.scss";
</style>