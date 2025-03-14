import apiClient from "./api";

export const fetchUserDataMixin = {
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
        if (this.userData.role !== "admin") {
          window.location.href = "/";
        }
      } catch (error) {
        this.goToProfile();
      }
    },
  },
};