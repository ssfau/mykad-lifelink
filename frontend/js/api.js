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
     * Fetches the logs for the Admin Dashboard
     */
    async getAdminLogs() {
        try {
            const response = await fetch(`${API_BASE_URL}/admin/logs`);
            return await response.json();
        } catch (error) {
            console.error("API Error (Logs):", error);
            return [];
        }
    }
};