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

    if (scanBtn) {
        scanBtn.addEventListener('click', async () => {
            // Visual feedback: Start scanning
            btnText.innerText = "COMMUNICATING WITH CHIP...";
            scanBtn.classList.add('pulse-btn');
            loader.classList.remove('hidden');

            // Call the Python Backend (api.js)
            const data = await ApiService.scanMyKad();

            if (data) {
                // Success: Populate the UI
                document.getElementById('patientNameDisplay').innerText = data.name || "N/A";
                document.getElementById('patientICDisplay').innerText = data.ic || "N/A";
                document.getElementById('patientBlood').innerText = data.blood_group || "--";
                document.getElementById('patientAllergies').innerText = data.allergies || "NONE";
                document.getElementById('patientChronic').innerText = data.chronic_diseases || "None Reported";

                // Switch Views
                scanInterface.classList.add('hidden');
                resultInterface.classList.remove('hidden');
            } else {
                // Error handling
                alert("MyKad Connection Error. Please re-insert card.");
                btnText.innerText = "RETRY SCAN";
                loader.classList.add('hidden');
            }
        });
    }

    // --- 2. PATIENT REGISTRATION LOGIC ---
    const patientForm = document.getElementById('patientForm');
    if (patientForm) {
        patientForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Stop page from refreshing
            
            const submitBtn = patientForm.querySelector('button');
            submitBtn.innerText = "UPLOADING TO SECURE SERVER...";
            submitBtn.disabled = true;

            // Collect data from the form
            const formData = {
                name: patientForm.querySelector('input[type="text"]').value,
                ic: patientForm.querySelectorAll('input[type="text"]')[1].value,
                blood_group: patientForm.querySelector('select').value,
                allergies: patientForm.querySelector('textarea').value,
                consent: document.getElementById('consent').checked
            };

            const result = await ApiService.registerPatient(formData);

            if (result.success) {
                alert("Registration Successful! Your MyKad is now linked.");
                window.location.href = "../index.html"; // Redirect home
            } else {
                alert("Error: " + result.message);
                submitBtn.innerText = "SAVE PROFILE";
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
        if (toggleBtn) toggleBtn.textContent = '☀️'; // Change icon to sun
    }

    // 2. Add event listener to the button
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('dark-mode', 'enabled');
                toggleBtn.textContent = '☀️';
            } else {
                localStorage.setItem('dark-mode', 'disabled');
                toggleBtn.textContent = '🌙';
            }
        });
    }
});

