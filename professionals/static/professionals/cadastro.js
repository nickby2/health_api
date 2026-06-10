const tokenKey = "health_api_access_token";

const statusContainer = document.getElementById("status");
const authForm = document.getElementById("auth-form");
const professionalForm = document.getElementById("professional-form");
const appointmentForm = document.getElementById("appointment-form");
const appointmentProfessionalSelect = document.getElementById("appointment-professional");
const appointmentsSummary = document.getElementById("appointments-summary");
const refreshDataButton = document.getElementById("refresh-data");
const logoutButton = document.getElementById("logout-button");
const tokenState = document.getElementById("token-state");

function showStatus(message, type = "success") {
    if (!statusContainer) {
        return;
    }

    statusContainer.innerHTML = `<div class="alert ${type}">${message}</div>`;
}

function showApiError(error) {
    const message = error instanceof Error ? error.message : "Falha na requisição.";
    showStatus(message, "error");
}

function clearStatus() {
    if (statusContainer) {
        statusContainer.innerHTML = "";
    }
}

function updateTokenState() {
    if (!tokenState) {
        return;
    }

    tokenState.textContent = getToken()
        ? "Token JWT salvo. Você já pode carregar e cadastrar dados."
        : "Nenhum token salvo no navegador.";
}

function getToken() {
    return localStorage.getItem(tokenKey) || "";
}

function setToken(token) {
    localStorage.setItem(tokenKey, token);
}

function clearToken() {
    localStorage.removeItem(tokenKey);
}

function formatAppointmentDate(value) {
    const date = new Date(value);
    return date.toISOString();
}

async function requestJson(url, options = {}) {
    const { headers: customHeaders, ...requestOptions } = options;

    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(customHeaders || {}),
        },
        ...requestOptions,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        if (data.detail) {
            throw new Error(data.detail);
        }

        const fieldErrors = Object.entries(data)
            .map(([field, value]) => {
                const text = Array.isArray(value) ? value.join(" ") : String(value);
                return `${field}: ${text}`;
            })
            .filter(Boolean);

        if (fieldErrors.length) {
            throw new Error(fieldErrors.join(" | "));
        }

        throw new Error("Falha na requisição.");
    }

    return data;
}

function authHeaders() {
    const token = getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
}

function renderProfessionals(professionals) {
    if (!appointmentProfessionalSelect) {
        return;
    }

    const currentValue = appointmentProfessionalSelect.value;
    appointmentProfessionalSelect.innerHTML = '<option value="">Selecione um profissional</option>';

    professionals.forEach((professional) => {
        const option = document.createElement("option");
        option.value = professional.id;
        option.textContent = `${professional.social_name} - ${professional.profession}`;
        appointmentProfessionalSelect.appendChild(option);
    });

    appointmentProfessionalSelect.value = currentValue;
}

function renderAppointments(appointments) {
    if (!appointmentsSummary) {
        return;
    }

    if (!appointments.length) {
        appointmentsSummary.innerHTML = '<p class="empty-state">Ainda não há consultas cadastradas.</p>';
        return;
    }

    appointmentsSummary.innerHTML = appointments
        .map((appointment) => {
            const professional = appointment.professional || {};
            const date = new Date(appointment.appointment_date);

            return `
                <article class="summary-item">
                    <strong>${professional.social_name || "Profissional"}</strong>
                    <span>${professional.profession || ""}</span>
                    <time>${date.toLocaleString("pt-BR")}</time>
                </article>
            `;
        })
        .join("");
}

async function refreshLists() {
    const headers = authHeaders();

    if (!headers.Authorization) {
        updateTokenState();
        return;
    }

    const professionals = await requestJson("/api/professionals/", { headers });
    renderProfessionals(Array.isArray(professionals) ? professionals : professionals.results || []);

    const appointments = await requestJson("/api/appointments/", { headers });
    renderAppointments(Array.isArray(appointments) ? appointments : appointments.results || []);
    updateTokenState();
}

if (refreshDataButton) {
    refreshDataButton.addEventListener("click", async () => {
        clearStatus();

        if (!getToken()) {
            showStatus("Faça login com JWT antes de carregar os dados.", "error");
            return;
        }

        try {
            await refreshLists();
            showStatus("Dados recarregados com sucesso.", "success");
        } catch (error) {
            showApiError(error);
        }
    });
}

if (logoutButton) {
    logoutButton.addEventListener("click", () => {
        clearToken();
        clearStatus();
        updateTokenState();

        if (appointmentProfessionalSelect) {
            appointmentProfessionalSelect.innerHTML = '<option value="">Selecione um profissional</option>';
        }

        if (appointmentsSummary) {
            appointmentsSummary.innerHTML = '<p class="empty-state">Ainda não há consultas cadastradas.</p>';
        }

        if (authForm) {
            authForm.reset();
        }

        showStatus("Sessão encerrada. Faça login novamente para usar a API.", "success");
    });
}

if (authForm) {
    authForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearStatus();

        const formData = new FormData(authForm);
        const username = formData.get("username");
        const password = formData.get("password");

        try {
            const tokenData = await requestJson("/api/token/", {
                method: "POST",
                body: JSON.stringify({ username, password }),
            });

            setToken(tokenData.access);
            updateTokenState();
            showStatus("Autenticação realizada com sucesso.", "success");
            await refreshLists();
        } catch (error) {
            showApiError(error);
        }
    });
}

if (professionalForm) {
    professionalForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearStatus();

        const token = getToken();
        if (!token) {
            showStatus("Faça login com JWT antes de cadastrar.", "error");
            return;
        }

        const formData = new FormData(professionalForm);
        const payload = {
            social_name: formData.get("social_name"),
            profession: formData.get("profession"),
            address: formData.get("address"),
            contact: formData.get("contact"),
        };

        try {
            await requestJson("/api/professionals/", {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify(payload),
            });

            professionalForm.reset();
            showStatus("Profissional cadastrado com sucesso.", "success");
            await refreshLists();
        } catch (error) {
            showApiError(error);
        }
    });
}

if (appointmentForm) {
    appointmentForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearStatus();

        const token = getToken();
        if (!token) {
            showStatus("Faça login com JWT antes de cadastrar.", "error");
            return;
        }

        const formData = new FormData(appointmentForm);
        const appointmentDate = formData.get("appointment_date");

        try {
            await requestJson("/api/appointments/", {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify({
                    professional: Number(formData.get("professional")),
                    appointment_date: formatAppointmentDate(appointmentDate),
                }),
            });

            appointmentForm.reset();
            showStatus("Consulta cadastrada com sucesso.", "success");
            await refreshLists();
        } catch (error) {
            showApiError(error);
        }
    });
}

refreshLists().catch(() => {
    // Login may not exist yet; ignore until the user authenticates.
});

updateTokenState();