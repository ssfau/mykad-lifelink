/**
 * js/ui.js - Handles all visual updates and button clicks
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log("MyKad-LifeLink UI Initialized");
    
    // --- GLOBAL: Live Clock for Dashboards ---
    const clockEl = document.getElementById('systemClock');
    if (clockEl) {
        setInterval(() => {
            clockEl.innerText = new Date().toLocaleTimeString();
        }, 1000);
    }

    // --- 1. DOCTOR/PARAMEDIC PAGE LOGIC ---
    const scanBtn = document.getElementById('scanBtn');
    const scanInterface = document.getElementById('scanInterface');
    const resultInterface = document.getElementById('resultInterface');
    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');

    // Create hidden file input for MyKad image upload
    let fileInput = null;
    if (scanBtn && scanInterface) {
        fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';
        scanInterface.appendChild(fileInput);

        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            // Visual feedback: Start scanning
            btnText.innerText = "PROCESSING MYKAD...";
            scanBtn.classList.add('pulse-btn');
            loader.classList.remove('hidden');

            try {
                // Step 1: Scan MyKad to get OCR data (nric, name, raw_ocr)
                const ocrData = await ApiService.doctorScanMyKad(file);
                
                if (!ocrData || !ocrData.nric) {
                    throw new Error('Could not extract NRIC from MyKad image');
                }

                // Step 2: Use the extracted NRIC to fetch patient profile
                const patientData = await ApiService.doctorGetPatientProfile(ocrData.nric);

                if (patientData) {
                    // Success: Populate the UI with patient data
                    // Note: doctor.html doesn't have patientNameDisplay/patientICDisplay, using the available IDs
                    const patientAllergies = patientData.allergies && patientData.allergies.length > 0 
                        ? patientData.allergies.join(', ') 
                        : "NONE";
                    const patientChronic = patientData.chronic_conditions && patientData.chronic_conditions.length > 0
                        ? patientData.chronic_conditions.join(', ')
                        : "None Reported";

                    document.getElementById('patientAllergies').innerText = patientAllergies;
                    document.getElementById('patientBlood').innerText = patientData.blood_type || "--";
                    document.getElementById('patientChronic').innerText = patientChronic;

                    // Additional notes could include other critical info
                    let additionalNotes = [];
                    if (patientData.risk_factors && patientData.risk_factors.length > 0) {
                        additionalNotes.push(`Risk Factors: ${patientData.risk_factors.join(', ')}`);
                    }
                    if (patientData.advanced_directives && patientData.advanced_directives.length > 0) {
                        additionalNotes.push(`Directives: ${patientData.advanced_directives.join(', ')}`);
                    }
                    document.getElementById('additionalNotes').innerText = additionalNotes.length > 0 
                        ? additionalNotes.join(' | ') 
                        : "No critical alerts.";

                    // Switch Views
                    scanInterface.classList.add('hidden');
                    resultInterface.classList.remove('hidden');
                } else {
                    // Patient not found in database - show OCR data only
                    alert(`Patient with NRIC ${ocrData.nric} not found in database.`);
                    btnText.innerText = "RETRY SCAN";
                    loader.classList.add('hidden');
                }
            } catch (error) {
                // Error handling
                alert(`MyKad Scan Error: ${error.message}`);
                btnText.innerText = "RETRY SCAN";
                loader.classList.add('hidden');
            } finally {
                // Reset file input
                fileInput.value = '';
            }
        });

        // When scan button is clicked, trigger file input
        scanBtn.addEventListener('click', () => {
            fileInput.click();
        });
    }

    // --- 2. PATIENT REGISTRATION LOGIC ---
    const patientForm = document.getElementById('patientForm');
    if (patientForm) {
        patientForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Stop page from refreshing
            
            const submitBtn = patientForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = "UPLOADING TO SECURE SERVER...";
            submitBtn.disabled = true;

            try {
                // Collect data from the form matching PatientRegistrationConfirm schema
                const allergiesText = document.getElementById('allergies')?.value.trim() || '';
                const chronicConditionsText = document.getElementById('chronic_conditions')?.value.trim() || '';
                const riskFactorsText = document.getElementById('risk_factors')?.value.trim() || '';

                // Convert comma-separated strings to arrays, filtering out empty values
                const allergies = allergiesText ? allergiesText.split(',').map(s => s.trim()).filter(s => s) : null;
                const chronicConditions = chronicConditionsText ? chronicConditionsText.split(',').map(s => s.trim()).filter(s => s) : null;
                const riskFactors = riskFactorsText ? riskFactorsText.split(',').map(s => s.trim()).filter(s => s) : null;

                const registrationData = {
                    full_name: document.getElementById('full_name').value.trim(),
                    nric_number: document.getElementById('nric_number').value.trim(),
                    birth_date: document.getElementById('birth_date').value, // YYYY-MM-DD format
                    sex: document.getElementById('sex').value,
                    blood_type: document.getElementById('blood_type').value,
                    allergies: allergies && allergies.length > 0 ? allergies : null,
                    chronic_conditions: chronicConditions && chronicConditions.length > 0 ? chronicConditions : null,
                    risk_factors: riskFactors && riskFactors.length > 0 ? riskFactors : null,
                    emergency_contacts: null // Not collected in initial registration form
                };

                // Check consent
                if (!document.getElementById('consent').checked) {
                    alert("Please agree to the consent form to proceed.");
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                    return;
                }

                const result = await ApiService.patientConfirmRegistration(registrationData);

                if (result && (result.status === 'created' || result.status === 'exists')) {
                    alert(`Registration ${result.status === 'created' ? 'Successful' : 'Info'}: ${result.message}`);
                    if (result.status === 'created') {
                        window.location.href = "../index.html"; // Redirect home
                    } else {
                        submitBtn.innerText = originalText;
                        submitBtn.disabled = false;
                    }
                } else {
                    alert("Error: " + (result?.message || "Registration failed"));
                    submitBtn.innerText = originalText;
                    submitBtn.disabled = false;
                }
            } catch (error) {
                alert("Error: " + error.message);
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        });
    }

    // --- 2b. LOAD EXISTING PATIENT PROFILE ---
    const loadBtn = document.getElementById('loadProfileBtn');
    const profileSummary = document.getElementById('profileSummary');

    if (loadBtn) {
        loadBtn.addEventListener('click', async () => {
            const ic = document.getElementById('icNumber').value.trim();
            if (!ic) { alert('Please enter your NRIC to load the profile.'); return; }

            loadBtn.disabled = true;
            loadBtn.innerText = 'LOADING...';

            const data = await ApiService.getPatientProfile(ic);

            loadBtn.disabled = false;
            loadBtn.innerText = 'LOAD PROFILE';

            if (!data) {
                alert('Profile not found or server error.');
                return;
            }

            // Show summary at top
            if (profileSummary) profileSummary.style.display = 'block';
            document.getElementById('patientNameDisplay').innerText = data.full_name || 'N/A';
            document.getElementById('patientICDisplay').innerText = data.nric_number || 'N/A';
            document.getElementById('patientBlood').innerText = data.blood_type || '--';
            document.getElementById('patientAllergies').innerText = (data.allergies && data.allergies.length) ? data.allergies.join(', ') : 'NONE';
            document.getElementById('patientChronic').innerText = (data.chronic_conditions && data.chronic_conditions.length) ? data.chronic_conditions.join(', ') : 'None Reported';

            // Populate form fields for editing convenience
            document.getElementById('fullName').value = data.full_name || '';
            document.getElementById('dob').value = data.birth_date || '';
            document.getElementById('gender').value = data.sex || '';
            document.getElementById('bloodType').value = data.blood_type || '';
            document.getElementById('allergies').value = (data.allergies || []).join(', ');
            document.getElementById('chronic').value = (data.chronic_conditions || []).join(', ');

            document.getElementById('surgeries').value = (data.major_surgeries || []).map(s => `${s.surgery_name} (${s.date})`).join('; ');
            document.getElementById('medications').value = (data.prescriptions || []).map(p => `${p.prescription_name} ${p.prescription_dose}`).join('; ');
            document.getElementById('immunizations').value = (data.immunization || []).map(i => `${i.immunization_name} (${i.date})`).join('; ');
            document.getElementById('presenting').value = (data.presenting_complaint || []).map(p => `${p.complaint}`).join('; ');

            document.getElementById('riskFactors').value = (data.risk_factors || []).join(', ');
            document.getElementById('emergencyNotes').value = (data.advanced_directives || []).join(', ');

            if (data.emergency_contacts && data.emergency_contacts.length > 0) {
                const e = data.emergency_contacts[0];
                document.getElementById('nokName').value = e.name || '';
                document.getElementById('nokRelation').value = e.additional_info || '';
                document.getElementById('nokPhone').value = e.contact_number || '';
            }
        });
    }

    // --- 3. ADMIN LOGS LOGIC ---
    const logTable = document.getElementById('logTable');
    if (logTable) {
        const loadLogs = async () => {
            const logs = await ApiService.getAdminLogs();
            if (logs.length > 0) {
                logTable.innerHTML = ""; // Clear placeholders
                logs.forEach(log => {
                    const row = `<tr>
                        <td>${log.timestamp}</td>
                        <td>${log.patient_ic}</td>
                        <td>${log.action}</td>
                        <td>${log.staff_name}</td>
                    </tr>`;
                    logTable.innerHTML += row;
                });
            }
        };
        loadLogs();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('dark-mode-toggle');
    const body = document.body;

    // 1. Check for saved user preference on load
    const darkMode = localStorage.getItem('dark-mode');

    if (darkMode === 'enabled') {
        body.classList.add('dark-mode');
        if (toggleBtn) toggleBtn.textContent = '🌙'; // Change icon to sun
    }

    // 2. Add event listener to the button
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('dark-mode', 'enabled');
                toggleBtn.textContent = '🌙';
            } else {
                localStorage.setItem('dark-mode', 'disabled');
                toggleBtn.textContent = '☀️';
            }
        });
    }
});

