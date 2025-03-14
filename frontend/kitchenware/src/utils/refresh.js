import axios from "axios";
import apiClient from "./api";

export default async function refreshToken() {
  const userConfirmed = await showSessionExpiredModal();
  if (userConfirmed) {
    const Token = localStorage.getItem("refreshToken");

    try {
      const response = await apiClient.post(
        "/users/login/refresh",
        {},
        {
          headers: {
            RefreshToken: `Bearer ${Token}`,
          },
        }
      );

      const newAccessToken = response.data["Authorization"].split(" ")[1];
      localStorage.setItem("accessToken", newAccessToken);

      return true;
    } catch (error) {
      console.error("Ошибка при обновлении токена:", error);
    }
  } else {
    window.location.href = "/auth";
  }
}

function showSessionExpiredModal() {
  return new Promise((resolve) => {
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";

    const modal = document.createElement("div");
    modal.className = "modal";

    const message = document.createElement("p");
    message.textContent = "Ваша сессия истекла. Хотите продлить сессию?";

    const yesButton = document.createElement("button");
    yesButton.textContent = "Да";
    yesButton.addEventListener("click", () => {
      document.body.removeChild(overlay);
      resolve(true);
    });

    const noButton = document.createElement("button");
    noButton.textContent = "Нет";
    noButton.addEventListener("click", () => {
      document.body.removeChild(overlay);
      localStorage.removeItem("refreshToken");
      resolve(false);
    });

    overlay.addEventListener("click", () => {
      document.body.removeChild(overlay);
      localStorage.removeItem("refreshToken");
      resolve(false);
    });

    modal.appendChild(message);
    modal.appendChild(yesButton);
    modal.appendChild(noButton);
    overlay.appendChild(modal);

    document.body.appendChild(overlay);
  });
}
