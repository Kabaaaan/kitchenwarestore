<template>
  <div class="auth-container">
    <div class="auth-form">
      <h2 class="form-title">
        {{ isLoginForm ? "Вход в личный кабинет" : "Регистрация" }}
      </h2>
      <form @submit.prevent="isLoginForm ? login() : register()">
        <div class="form-group">
          <label for="username">Имя пользователя</label>
          <input
            type="text"
            id="username"
            v-model="credentials.name"
            required
            placeholder="Введите имя"
          />
        </div>
        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="credentials.password"
            required
            placeholder="Введите пароль"
          />
        </div>
        <button type="submit" class="submit-button">
          {{ isLoginForm ? "Войти" : "Зарегистрироваться" }}
        </button>
      </form>
      <div class="toggle-form">
        <span>{{ isLoginForm ? "Нет аккаунта?" : "Уже есть аккаунт?" }}</span>
        <button @click="toggleForm" class="toggle-button">
          {{ isLoginForm ? "Зарегистрироваться" : "Войти" }}
        </button>
      </div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import apiClient from "../utils/api";

export default {
  data() {
    return {
      isLoginForm: true,
      credentials: {
        name: "",
        password: "",
      },
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await apiClient.post("/users/login/token", {
          name: this.credentials.name,
          password: this.credentials.password,
        });

        const accessToken = response.data["Authorization"].split(" ")[1];
        const refreshToken = response.data["Refresh-Token"].split(" ")[1];

        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("refreshToken", refreshToken);

        this.$router.push({
          name: "profile",
        })
        
      } catch (error) {
        if (
          error.response &&
          (error.response.status === 403 || error.response.status === 404)
        ) {
          this.errorMessage = "Неверный логин или пароль";
        } else {
          console.error(error);
          this.errorMessage = "Произошла ошибка при входе";
        }
      }
    },
    async register() {
      try {
        const response = await apiClient.post("/users/login/create", {
          name: this.credentials.name,
          password: this.credentials.password,
        });

        if (response.data.success == true) {
          this.login();
        }
      } catch {
        this.errorMessage = "Ошибка при создании пользователя!";
      }
    },
    toggleForm() {
      this.isLoginForm = !this.isLoginForm;
      this.errorMessage = "";
    },
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  margin-top: 100px;
}

.auth-form {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.form-title {
  font-size: 1.8em;
  color: #2c3e50;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  font-size: 0.9em;
  color: #555;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1em;
  box-sizing: border-box;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus {
  border-color: #6a11cb;
  box-shadow: 0 0 8px rgba(106, 17, 203, 0.3);
  outline: none;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #3bb339, #7fdf5f);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.error-message {
  color: #ff4757;
  font-size: 0.9em;
  margin-top: 15px;
}

.toggle-form {
  margin-top: 20px;
  font-size: 0.9em;
  color: #555;
}

.toggle-button {
  background: none;
  border: none;
  color: #6a11cb;
  cursor: pointer;
  font-size: 1em;
  text-decoration: underline;
  transition: color 0.3s ease;
  text-decoration: none;
}

.toggle-button:hover {
  color: #2bac4c;
}
</style>