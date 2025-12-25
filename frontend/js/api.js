/**
 * js/api.js - The Bridge between Nabil's Frontend and ssfau's Python Backend
 */

// 1. Set the Base URL (Update this to your teammate's local IP or Vercel URL)
const API_BASE_URL = "http://127.0.0.1:8000"; 

const ApiService = {
    
    /**
     * Simulates or triggers a MyKad hardware scan via the Python Backend
     */
    async scanMyKad() {
        try {
            // Your teammate's route: /routers/doctor.py -> @router.get("/scan")
            const response = await fetch(`${API_BASE_URL}/patient/scan`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                throw new Error(`Scan Failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error("API Error (Scan):", error);
            return null;
        }
    },

    /**
     * Sends new patient registration data to the Python Backend
     */
    async registerPatient(patientData) {
        try {
            // Your teammate's route: /routers/patient.py -> @router.post("/register")
            const response = await fetch(`${API_BASE_URL}/patient/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(patientData)
            });

            return await response.json();
        } catch (error) {
            console.error("API Error (Register):", error);
            return { success: false, message: "Server connection failed" };
        }
    },

    /**
     * Perform a mock login (backend expects only a role)
     */
    async login(role) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ role })
            });

            if (!response.ok) {
                throw new Error(`Login Failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error("API Error (Login):", error);
            return { success: false, message: "Server connection failed" };
        }
    },

    /**
     * Fetches the logs for the Admin Dashboard
     */
    async getAdminLogs() {
        try {
            const token = localStorage.getItem('access_token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
            const response = await fetch(`${API_BASE_URL}/admin/logs`, { headers });
            return await response.json();
        } catch (error) {
            console.error("API Error (Logs):", error);
            return [];
        }
    },

    /**
     * Fetches a patient profile by NRIC number
     */
    async getPatientProfile(nric) {
        try {
            const response = await fetch(`${API_BASE_URL}/patient/profile?nric=${encodeURIComponent(nric)}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                throw new Error(`Profile fetch failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error("API Error (GetProfile):", error);
            return null;
        }
    }
};