async function loadPatientProfile() {
    const nric = localStorage.getItem("nric"); // or from token later
    if (!nric) return;

    const res = await fetch(`/profile?nric=${nric}`);
    if (!res.ok) {
        alert("Unable to load profile");
        return;
    }

    const data = await res.json();

    // Basic fields
    setText("full_name", data.full_name);
    setText("nric_number", data.nric_number);
    setText("birth_date", data.birth_date);
    setText("sex", data.sex);
    setText("blood_type", data.blood_type);

    // Lists → comma-separated
    setText("allergies", data.allergies?.join(", "));
    setText("chronic_conditions", data.chronic_conditions?.join(", "));
    setText("risk_factors", data.risk_factors?.join(", "));
    setText("advanced_directives", data.advanced_directives?.join(", "));

    renderList("major_surgeries", data.major_surgeries, s =>
        `${s.surgery_name} (${s.date}) – ${s.additional_info}`
    );

    renderList("prescriptions", data.prescriptions, p =>
        `${p.prescription_name} | ${p.prescription_dose} (${p.date})`
    );

    renderList("immunization", data.immunization, i =>
        `${i.immunization_name} (${i.date})`
    );

    renderList("presenting_complaint", data.presenting_complaint, c =>
        `${c.complaint} (${c.date})`
    );

    renderList("emergency_contacts", data.emergency_contacts, e =>
        `${e.name} – ${e.contact_number} (${e.additional_info})`
    );
}

function setText(id, value) {
    document.getElementById(id).textContent = value || "—";
}

function renderList(id, items, formatter) {
    const ul = document.getElementById(id);
    ul.innerHTML = "";

    if (!items || items.length === 0) {
        ul.innerHTML = "<li>—</li>";
        return;
    }

    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = formatter(item);
        ul.appendChild(li);
    });
}

loadPatientProfile();
