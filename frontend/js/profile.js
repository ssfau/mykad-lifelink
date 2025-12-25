/**
 * profile.js - Loads and displays patient profile data
 * Uses ApiService to fetch data matching PatientDataResponse schema
 */

async function loadPatientProfile() {
    // Get NRIC from localStorage or prompt user
    // In a real system, this would come from the authenticated user's session
    let nric = localStorage.getItem("nric");
    
    // If no NRIC in localStorage, try to get it from URL params or prompt
    if (!nric) {
        const urlParams = new URLSearchParams(window.location.search);
        nric = urlParams.get('nric');
    }
    
    // If still no NRIC, show error
    if (!nric) {
        alert('NRIC not found. Please log in or provide NRIC.');
        return;
    }

    try {
        // Use ApiService to get patient profile (requires auth token)
        const data = await ApiService.getPatientProfile(nric);

        if (!data) {
            alert("Unable to load profile. Please check your authentication.");
            return;
        }

        // Basic fields - matching PatientDataResponse schema
        setText("full_name", data.full_name);
        setText("nric_number", data.nric_number);
        setText("birth_date", formatDate(data.birth_date));
        setText("sex", data.sex);
        setText("blood_type", data.blood_type);

        // Lists → comma-separated strings
        setText("allergies", formatList(data.allergies));
        setText("chronic_conditions", formatList(data.chronic_conditions));
        setText("risk_factors", formatList(data.risk_factors));
        setText("advanced_directives", formatList(data.advanced_directives));

        // Render complex list items
        renderList("major_surgeries", data.major_surgeries, s =>
            `${s.surgery_name} (${formatDate(s.date)}) – ${s.additional_info || ''}`
        );

        renderList("prescriptions", data.prescriptions, p =>
            `${p.prescription_name} | ${p.prescription_dose} (${formatDate(p.date)})${p.additional_info ? ' – ' + p.additional_info : ''}`
        );

        renderList("immunization", data.immunization, i =>
            `${i.immunization_name} (${formatDate(i.date)})${i.additional_info ? ' – ' + i.additional_info : ''}`
        );

        renderList("presenting_complaint", data.presenting_complaint, c =>
            `${c.complaint} (${formatDate(c.date)})${c.additional_info ? ' – ' + c.additional_info : ''}`
        );

        renderList("emergency_contacts", data.emergency_contacts, e =>
            `${e.name} – ${e.contact_number}${e.address ? ' (' + e.address + ')' : ''}${e.additional_info ? ' – ' + e.additional_info : ''}`
        );
    } catch (error) {
        console.error("Error loading patient profile:", error);
        alert("Error loading profile: " + error.message);
    }
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value || "—";
    }
}

function formatList(items) {
    if (!items || !Array.isArray(items) || items.length === 0) {
        return "—";
    }
    return items.join(", ");
}

function formatDate(dateString) {
    if (!dateString) return "—";
    try {
        // Handle both date strings and Date objects
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString; // Return as-is if invalid
        return date.toLocaleDateString(); // Format as local date string
    } catch (e) {
        return dateString; // Return as-is if parsing fails
    }
}

function renderList(id, items, formatter) {
    const ul = document.getElementById(id);
    if (!ul) return;

    ul.innerHTML = "";

    if (!items || !Array.isArray(items) || items.length === 0) {
        ul.innerHTML = "<li>—</li>";
        return;
    }

    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = formatter(item);
        ul.appendChild(li);
    });
}

// Load profile when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadPatientProfile);
} else {
    loadPatientProfile();
}
