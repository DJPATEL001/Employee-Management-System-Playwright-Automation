// WorkForce HR Client JavaScript

document.addEventListener("DOMContentLoaded", () => {
    // 1. Client side employee table search and filtering
    const searchInput = document.querySelector('[data-testid="employee-search"]');
    const deptFilter = document.querySelector('[data-testid="department-filter"]');
    const statusFilter = document.querySelector('[data-testid="status-filter"]');
    const posFilter = document.querySelector('[data-testid="position-filter"]');
    const employeeRows = document.querySelectorAll('[data-testid^="employee-row"]');

    function filterEmployees() {
        if (!employeeRows.length) return;

        const searchVal = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const deptVal = deptFilter ? deptFilter.value.toLowerCase() : '';
        const statusVal = statusFilter ? statusFilter.value.toLowerCase() : '';
        const posVal = posFilter ? posFilter.value.toLowerCase() : '';

        employeeRows.forEach(row => {
            const code = row.getAttribute('data-code')?.toLowerCase() || '';
            const name = row.getAttribute('data-name')?.toLowerCase() || '';
            const email = row.getAttribute('data-email')?.toLowerCase() || '';
            const dept = row.getAttribute('data-department')?.toLowerCase() || '';
            const status = row.getAttribute('data-status')?.toLowerCase() || '';
            const position = row.getAttribute('data-position')?.toLowerCase() || '';

            const matchesSearch = !searchVal || code.includes(searchVal) || name.includes(searchVal) || email.includes(searchVal);
            const matchesDept = !deptVal || deptVal === 'all' || dept === deptVal;
            const matchesStatus = !statusVal || statusVal === 'all' || status === statusVal;
            const matchesPos = !posVal || posVal === 'all' || position.includes(posVal);

            if (matchesSearch && matchesDept && matchesStatus && matchesPos) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    if (searchInput) searchInput.addEventListener("input", filterEmployees);
    if (deptFilter) deptFilter.addEventListener("change", filterEmployees);
    if (statusFilter) statusFilter.addEventListener("change", filterEmployees);
    if (posFilter) posFilter.addEventListener("input", filterEmployees);

    // 2. Delete Confirmation Modal Handler
    const modal = document.getElementById("delete-modal");
    const confirmBtn = document.querySelector('[data-testid="confirm-delete"]');
    const cancelBtn = document.querySelector('[data-testid="cancel-delete"]');
    let targetDeleteUrl = "";

    document.querySelectorAll('[data-testid^="delete-employee"]').forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const employeeId = button.getAttribute("data-id");
            targetDeleteUrl = `/employees/${employeeId}/delete`;
            if (modal) {
                modal.classList.add("active");
            }
        });
    });

    if (cancelBtn) {
        cancelBtn.addEventListener("click", () => {
            if (modal) modal.classList.remove("active");
        });
    }

    if (confirmBtn) {
        confirmBtn.addEventListener("click", () => {
            if (targetDeleteUrl) {
                // Submit POST or DELETE request to target URL
                const form = document.createElement("form");
                form.method = "POST";
                form.action = targetDeleteUrl;
                document.body.appendChild(form);
                form.submit();
            }
        });
    }
});
