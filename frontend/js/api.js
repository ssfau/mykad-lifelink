/**
 * js/api.js - The Bridge between Frontend and FastAPI Backend
 * All endpoints match the exact routes defined in backend routers
 */

// Base URL - Auto-detect environment
// In production (Railway), use relative URLs (same domain)
// In local dev, use localhost:8000
const API_BASE_URL = (() => {
    // Check if we're running in production (served from same domain)
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        // Production: use relative URLs (same domain, no port)
        return window.location.origin;
    }
    // Local development: use localhost:8000
    return "http://127.0.0.1:8000";
})();

/**
 * Helper function to get auth headers with Bearer token
 */
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

/**
 * Helper function to handle API errors with proper UI alerts
 */
async function handleApiError(response, context) {
    if (response.status === 401) {
        alert('Unauthorized: Please log in again.');
        // Clear token and redirect to appropriate login
        const role = localStorage.getItem('role');
        localStorage.clear();
        if (role === 'doctor') {
            window.location.href = '../loginPages/doctorLogin.html';
        } else if (role === 'patient') {
            window.location.href = '../loginPages/patientLogin.html';
        } else if (role === 'clinic_admin') {
            window.location.href = '../loginPages/adminLogin.html';
        } else {
            window.location.href = '../index.html';
        }
        return null;
    } else if (response.status === 404) {
        const errorData = await response.json().catch(() => ({ detail: 'Not found' }));
        alert(`Not Found: ${errorData.detail || context}`);
        return null;
    } else if (response.status === 422) {
        // 422 Unprocessable Entity - validation error
        const errorData = await response.json().catch(() => ({ detail: 'Validation error' }));
        const errorMsg = errorData.detail 
            ? (Array.isArray(errorData.detail) 
                ? errorData.detail.map(e => `${e.loc?.join('.')}: ${e.msg}`).join(', ')
                : errorData.detail)
            : 'Validation error';
        console.error('Validation error:', errorData);
        throw new Error(`Validation failed: ${errorMsg}`);
    } else if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(errorData.detail || `${context} failed: ${response.statusText}`);
    }
    return response;
}

const ApiService = {
    
    /**
     * Mock Login - sends user_id and role to /auth/login
     * Returns: { access_token, token_type, role }
     */
    async login(userId, role) {
        try {
            // Validate inputs
            if (userId === undefined || userId === null) {
                throw new Error('user_id is required');
            }
            if (!role || typeof role !== 'string') {
                throw new Error('role is required and must be a string');
            }

            const requestBody = { user_id: userId, role: role };
            console.log('Login request:', requestBody);

            const requestUrl = `${API_BASE_URL}/auth/login`;
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(requestBody)
            };
            console.log('Login URL:', requestUrl);
            console.log('Login options:', requestOptions);
            
            const response = await fetch(requestUrl, requestOptions);
            console.log('Login response status:', response.status);

            const handledResponse = await handleApiError(response, 'Login');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Login):", error);
            alert(`Login failed: ${error.message}`);
            return null;
        }
    },

    /**
     * DOCTOR ENDPOINTS
     */

    /**
     * Doctor: Scan MyKad and get OCR data
     * POST /doctor/viewpatientdata/mykadscan
     * Requires: Bearer token (doctor role)
     * Body: FormData with file
     * Returns: { nric, name, raw_ocr }
     */
    async doctorScanMyKad(file) {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                throw new Error('No authentication token found');
            }

            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE_URL}/doctor/viewpatientdata/mykadscan`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                    // Don't set Content-Type - browser will set it with boundary for FormData
                },
                body: formData
            });

            const handledResponse = await handleApiError(response, 'MyKad Scan');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Doctor Scan):", error);
            alert(`Scan failed: ${error.message}`);
            return null;
        }
    },

    /**
     * Doctor: Get patient profile by NRIC
     * GET /doctor/viewpatientdata/profile?nric=...
     * Requires: Bearer token (doctor role)
     * Returns: PatientDataResponse schema
     */
    async doctorGetPatientProfile(nric) {
        try {
            const response = await fetch(`${API_BASE_URL}/doctor/viewpatientdata/profile?nric=${encodeURIComponent(nric)}`, {
                method: 'GET',
                headers: getAuthHeaders()
            });

            const handledResponse = await handleApiError(response, 'Get Patient Profile');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Doctor Get Profile):", error);
            alert(`Failed to get patient profile: ${error.message}`);
            return null;
        }
    },

    /**
     * PATIENT ENDPOINTS
     */

    /**
     * Patient: Initial MyKad scan (OCR only, no auth required)
     * POST /patient/mykadscan/initial
     * Body: FormData with file
     * Returns: { nric, name, raw_ocr }
     */
    async patientInitialScan(file) {
        try {
            // Validate file
            if (!file) {
                throw new Error('No file selected');
            }

            // Check file type
            if (!file.type || !file.type.startsWith('image/')) {
                throw new Error('Please select an image file');
            }

            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE_URL}/patient/mykadscan/initial`, {
                method: 'POST',
                body: formData
            });

            const handledResponse = await handleApiError(response, 'Initial MyKad Scan');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Patient Initial Scan):", error);
            
            // Provide more helpful error messages for network/connection errors
            let errorMessage = error.message || 'Unknown error occurred';
            const errorType = error.constructor.name;
            const errorString = String(error);
            
            // Check for network/connection errors
            // fetch() throws TypeError with "Failed to fetch" when connection is refused
            if (errorType === 'TypeError' && 
                (errorMessage.includes('fetch') || errorString.includes('Failed to fetch'))) {
                errorMessage = 'Cannot connect to the server. Please make sure the backend server is running on http://127.0.0.1:8000. Start it using: python start_server.py';
            } else if (errorMessage.includes('ERR_CONNECTION_REFUSED') || 
                       errorMessage.includes('NetworkError') ||
                       errorMessage.includes('Failed to fetch') ||
                       errorString.includes('ERR_CONNECTION_REFUSED')) {
                errorMessage = 'Cannot connect to the server. Please make sure the backend server is running on http://127.0.0.1:8000. Start it using: python start_server.py';
            }
            
            throw new Error(errorMessage);
        }
    },

    /**
     * Patient: Confirm registration with patient data
     * POST /patient/mykadscan/confirmation
     * Requires: Bearer token (patient role)
     * Body: PatientRegistrationConfirm schema
     * Returns: { status, patient_id, message }
     */
    async patientConfirmRegistration(patientData) {
        try {
            const response = await fetch(`${API_BASE_URL}/patient/mykadscan/confirmation`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(patientData)
            });

            const handledResponse = await handleApiError(response, 'Patient Registration');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Patient Registration):", error);
            alert(`Registration failed: ${error.message}`);
            return null;
        }
    },

    /**
     * Patient: Get own profile by NRIC
     * GET /patient/profile?nric=...
     * Requires: Bearer token (patient role)
     * Returns: PatientDataResponse schema
     */
    async getPatientProfile(nric) {
        try {
            const response = await fetch(`${API_BASE_URL}/patient/profile?nric=${encodeURIComponent(nric)}`, {
                method: 'GET',
                headers: getAuthHeaders()
            });

            const handledResponse = await handleApiError(response, 'Get Patient Profile');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Get Patient Profile):", error);
            alert(`Failed to get profile: ${error.message}`);
            return null;
        }
    },

    /**
     * CLINIC ADMIN ENDPOINTS
     */

    /**
     * Clinic Admin: Scan MyKad and get OCR data
     * POST /clinicadmin/viewpatientdata/mykadscan
     * Requires: Bearer token (clinic_admin role)
     * Body: FormData with file
     * Returns: { nric, name, raw_ocr }
     */
    async clinicAdminScanMyKad(file) {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                throw new Error('No authentication token found');
            }

            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE_URL}/clinicadmin/viewpatientdata/mykadscan`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            const handledResponse = await handleApiError(response, 'MyKad Scan');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Clinic Admin Scan):", error);
            alert(`Scan failed: ${error.message}`);
            return null;
        }
    },

    /**
     * Clinic Admin: Get patient profile (limited view)
     * GET /clinic/viewpatientdata/profile?nric=...
     * Requires: Bearer token (clinic_admin role)
     * Returns: ClinicPatientViewResponse schema
     */
    async clinicAdminGetPatientProfile(nric) {
        try {
            const response = await fetch(`${API_BASE_URL}/clinic/viewpatientdata/profile?nric=${encodeURIComponent(nric)}`, {
                method: 'GET',
                headers: getAuthHeaders()
            });

            const handledResponse = await handleApiError(response, 'Get Patient Profile');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Clinic Admin Get Profile):", error);
            alert(`Failed to get patient profile: ${error.message}`);
            return null;
        }
    },

    /**
     * Clinic Admin: Update patient records (prescriptions, complaints)
     * POST /clinic/viewpatientdata/update?nric=...
     * Requires: Bearer token (clinic_admin role)
     * Body: ClinicPatientUpdateRequest schema
     * Returns: { status, message }
     */
    async clinicAdminUpdatePatient(nric, updateData) {
        try {
            const response = await fetch(`${API_BASE_URL}/clinic/viewpatientdata/update?nric=${encodeURIComponent(nric)}`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(updateData)
            });

            const handledResponse = await handleApiError(response, 'Update Patient Records');
            if (!handledResponse) return null;

            return await handledResponse.json();
        } catch (error) {
            console.error("API Error (Clinic Admin Update):", error);
            alert(`Update failed: ${error.message}`);
            return null;
        }
    },

    /**
     * LEGACY/COMPATIBILITY METHODS
     * These are kept for backward compatibility but redirect to new methods
     */

    /**
     * @deprecated Use doctorScanMyKad or patientInitialScan instead
     */
    async scanMyKad() {
        console.warn('scanMyKad() is deprecated. Use doctorScanMyKad() or patientInitialScan() instead.');
        // For doctor context, use doctorScanMyKad
        const role = localStorage.getItem('role');
        if (role === 'doctor') {
            // This requires a file, so return error
            throw new Error('Please use doctorScanMyKad(file) instead');
        }
        throw new Error('Please use patientInitialScan(file) or doctorScanMyKad(file) instead');
    },

    /**
     * @deprecated Use patientConfirmRegistration instead
     */
    async registerPatient(patientData) {
        console.warn('registerPatient() is deprecated. Use patientConfirmRegistration() instead.');
        return await this.patientConfirmRegistration(patientData);
    },

    /**
     * Admin: Get admin logs (stub - endpoint not implemented in backend yet)
     * Returns: Empty array for now
     */
    async getAdminLogs() {
        try {
            // TODO: Implement when backend adds admin logs endpoint
            // For now, return empty array
            console.warn('getAdminLogs() is not yet implemented in the backend');
            return [];
        } catch (error) {
            console.error("API Error (Admin Logs):", error);
            return [];
        }
    }
};
