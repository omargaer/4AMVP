
document.addEventListener('DOMContentLoaded', function () {
    const companySelect = document.getElementById('id_company');
    const branchOfficeSelect = document.getElementById('id_branch_office');
    const locationSelect = document.getElementById('id_location');

    // Функция для очистки выпадающего списка
    function clearSelect(selectElement) {
        selectElement.innerHTML = '<option value="">---------</option>';
    }

    // Обработчик изменения компании
    companySelect.addEventListener('change', function () {
        const companyId = this.value;
        clearSelect(branchOfficeSelect);
        clearSelect(locationSelect);

        if (!companyId) {
            return;
        }

        fetch(`/admin/load-branch-offices/?company_id=${companyId}`)
            .then(response => response.json())
            .then(data => {
                let options = '<option value="">---------</option>';
                data.forEach(function (branch) {
                    options += `<option value="${branch.id}">${branch.name}</option>`;
                });
                branchOfficeSelect.innerHTML = options;
            })
            .catch(error => {
                console.error('Error fetching branch offices:', error);
            });
    });

    // Обработчик изменения филиала
    branchOfficeSelect.addEventListener('change', function () {
        const branchOfficeId = this.value;
        clearSelect(locationSelect);
        if (!branchOfficeId) {
            return;
        }

        // Обновление списка locations
        fetch(`/admin/load-locations/?branch_office_id=${branchOfficeId}`)
            .then(response => response.json())
            .then(data => {
                let options = '<option value="">---------</option>';
                data.forEach(function (location) {
                    options += `<option value="${location.id}">${location.room} - ${location.room_name}</option>`;
                });
                locationSelect.innerHTML = options;
            })
            .catch(error => {
                console.error('Error fetching locations:', error);
            });
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const branchOfficeSelect = document.getElementById('id_branch_office');
    const applicantSelect = document.getElementById('id_applicant');

    function updateApplicantOptions() {
        const branchOfficeId = branchOfficeSelect.value;
        if (branchOfficeId) {
            fetch(`/admin/get_applicants/?branch_office=${branchOfficeId}`)
                .then(response => response.json())
                .then(data => {
                    // Очистить текущие опции
                    applicantSelect.innerHTML = '';
                    // Добавить пустую опцию
                    const emptyOption = document.createElement('option');
                    emptyOption.value = '';
                    emptyOption.text = '---------';
                    applicantSelect.add(emptyOption);
                    // Добавить новые опции
                    data.applicants.forEach(applicant => {
                        const option = document.createElement('option');
                        option.value = applicant.id;
                        option.text = applicant.full_name;
                        applicantSelect.appendChild(option);
                    });
                    applicantSelect.disabled = false;
                });
        } else {
            applicantSelect.innerHTML = '';
            const emptyOption = document.createElement('option');
            emptyOption.value = '';
            emptyOption.text = '---------';
            applicantSelect.appendChild(emptyOption);
            applicantSelect.disabled = true;
        }
    }

    // Изначально отключить поле applicant если филиал не выбран
    if (!branchOfficeSelect.value) {
        applicantSelect.disabled = true;
    }

    branchOfficeSelect.addEventListener('change', updateApplicantOptions);
});

document.addEventListener('DOMContentLoaded', function () {
    const branchOfficeSelect = document.getElementById('id_branch_office');
    const addApplicantButton = document.querySelector('.add-related.applicant');

    if (addApplicantButton) {
        addApplicantButton.addEventListener('click', function (event) {
            const branchOfficeId = branchOfficeSelect.value;
            const url = addApplicantButton.getAttribute('href') + `&branch_office=${branchOfficeId}`;
            addApplicantButton.setAttribute('href', url);
        });
    }
});