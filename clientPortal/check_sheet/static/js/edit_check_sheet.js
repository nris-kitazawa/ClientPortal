document.addEventListener("DOMContentLoaded", function () {
    setupFormsetTable({
        tableId: "formset-table",
        addButtonId: "add-row-btn",
        totalFormsSelector: "#id_form-TOTAL_FORMS",
        prefix: "form",
        columns: [
            "url_or_ip_address",
            "host_name",
            "os",
            "web_server",
            "ap_server",
            "framework",
            "db_server"
        ]
    });

    setupFormsetTable({
        tableId: "login-credentials-table",
        addButtonId: "add-login-row-btn",
        totalFormsSelector: "#id_login_form-TOTAL_FORMS",
        prefix: "login_form",
        columns: [
            "login_id",
            "password",
            "role"
        ]
    });

    setupDeleteModal("delete-confirm-modal", "confirm-delete-btn", "cancel-delete-btn");
});

function setupFormsetTable({ tableId, addButtonId, totalFormsSelector, prefix, columns }) {
    const table = document.getElementById(tableId);
    const addButton = document.getElementById(addButtonId);
    const totalFormsInput = document.querySelector(totalFormsSelector);

    // 初期表示後にNo欄を再計算
    updateAllRowNumbers(table);

    // 行を削除する関数
    function deleteRow(row) {
        const deleteInput = row.querySelector(`input[name$="-DELETE"]`);
        if (deleteInput) {
            deleteInput.checked = true; // 削除フラグを設定
        }
        row.style.display = "none"; // 行を非表示にする
        updateAllRowNumbers(table); // No欄を再計算
    }

    // 削除ボタンのイベントリスナーを設定
    table.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-row-btn")) {
            const row = event.target.closest("tr");
            if (row) {
                deleteRow(row);
            }
        }
    });

    // 行を追加する処理
    addButton.addEventListener("click", function () {
        const currentFormCount = parseInt(totalFormsInput.value, 10);
        const newRow = document.createElement("tr");
        newRow.classList.add("form-row");

        columns.forEach(column => {
            const newCell = document.createElement("td");
            const field = document.createElement("input");
            field.name = `${prefix}-${currentFormCount}-${column}`;
            field.type = "text";
            newCell.appendChild(field);
            newRow.appendChild(newCell);
        });

        // 削除ボタンとhidden削除フラグ
        const deleteCell = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.classList.add("delete-row-btn");
        deleteButton.textContent = "削除";
        deleteCell.appendChild(deleteButton);

        const deleteInput = document.createElement("input");
        deleteInput.type = "checkbox";
        deleteInput.name = `${prefix}-${currentFormCount}-DELETE`;
        deleteInput.style.display = "none";
        deleteCell.appendChild(deleteInput);

        newRow.appendChild(deleteCell);

        table.querySelector("tbody").appendChild(newRow);
        totalFormsInput.value = currentFormCount + 1;

        updateAllRowNumbers(table); // No欄を再計算
    });
}

// No欄を再計算する関数
function updateAllRowNumbers(table) {
    const rows = table.querySelectorAll(".form-row:not([style*='display: none'])");
    rows.forEach((row, index) => {
        const noCell = row.querySelector("td:first-child");
        if (noCell) {
            noCell.textContent = index + 1;
        }
    });
}

function setupDeleteModal(modalId, confirmBtnId, cancelBtnId) {
    const modal = document.getElementById(modalId);
    const confirmDeleteBtn = document.getElementById(confirmBtnId);
    const cancelDeleteBtn = document.getElementById(cancelBtnId);

    if (!modal || !confirmDeleteBtn || !cancelDeleteBtn) {
        console.error("モーダルまたはボタンの要素が見つかりません。HTMLを確認してください。");
        return;
    }

    let rowToDelete = null;

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-row-btn")) {
            const row = event.target.closest("tr");
            const inputs = row.querySelectorAll("input, select, textarea");
            const hasValue = [...inputs].some(input =>
                !input.name.includes("-DELETE") && input.value.trim() !== ""
            );

            if (hasValue) {
                rowToDelete = row;
                modal.style.display = "flex";
            } else {
                deleteRow(row);
            }
        }
    });

    confirmDeleteBtn.addEventListener("click", function () {
        if (rowToDelete) {
            deleteRow(rowToDelete);
            rowToDelete = null;
        }
        modal.style.display = "none";
    });

    cancelDeleteBtn.addEventListener("click", function () {
        rowToDelete = null;
        modal.style.display = "none";
    });
}

function deleteRow(row) {
    const deleteInput = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
    if (deleteInput) {
        deleteInput.checked = true;
    }
    row.style.display = "none";

    const table = row.closest("table");
    updateAllRowNumbers(table);
}

function toggleOtherField() {
    var radios = document.getElementsByName("environment");
    var otherContainer = document.getElementById("env-other-container");
    var show = false;

    // ラジオボタンの選択状態を確認
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked && radios[i].value === "other") {
            show = true;
            break;
        }
    }

    // 「その他」の入力フィールドの表示/非表示を切り替え
    if (otherContainer) {
        otherContainer.style.display = show ? "inline-block" : "none";
        var inputField = otherContainer.querySelector("input");
        if (inputField) {
            inputField.required = show; // 必須属性を切り替え
        }
    }
}

// DOMContentLoaded イベントで初期化
window.addEventListener('DOMContentLoaded', function () {
    toggleOtherField(); // 初期状態を設定
    var radios = document.getElementsByName("environment");

    // ラジオボタンの変更イベントを監視
    for (var i = 0; i < radios.length; i++) {
        radios[i].addEventListener('change', toggleOtherField);
    }
});

// 自動で高さを調整するテキストエリアの処理
document.addEventListener("input", function (e) {
    if (e.target.classList.contains("auto-resize-textarea")) {
        e.target.style.height = "auto";
        e.target.style.height = e.target.scrollHeight + "px";
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const ipAddressManagementField = document.querySelectorAll('input[name="ip_address_management"]');
    const outsourcingInfoRow = document.getElementById('outsourcing-info-row');
    const preApplicationRequiredRow = document.getElementById('pre-application-required-row');
    const preApplicationStatusRow = document.getElementById('pre-application-status-row');
    const preApplicationRequiredField = document.querySelectorAll('input[name="pre_application_required"]'); // 修正ポイント

    function getSelectedValue(radioButtons) {
        for (const radio of radioButtons) {
            if (radio.checked) {
                return radio.value;
            }
        }
        return null;
    }

    function toggleFields() {
        const selectedValue = getSelectedValue(ipAddressManagementField);
        console.log('Selected value (ip_address_management):', selectedValue); // デバッグ用

        if (selectedValue !== '自社管理') {
            outsourcingInfoRow.style.display = '';
            preApplicationRequiredRow.style.display = '';

            const preApplicationRequiredValue = getSelectedValue(preApplicationRequiredField); // 修正ポイント
            console.log('Selected value (pre_application_required):', preApplicationRequiredValue); // デバッグ用

            if (preApplicationRequiredValue === 'True') {
                preApplicationStatusRow.style.display = '';
            } else {
                preApplicationStatusRow.style.display = 'none';
            }
        } else {
            outsourcingInfoRow.style.display = 'none';
            preApplicationRequiredRow.style.display = 'none';
            preApplicationStatusRow.style.display = 'none';
        }
    }

    // ラジオボタンの変更イベントを監視
    ipAddressManagementField.forEach(radio => {
        radio.addEventListener('change', toggleFields);
    });

    preApplicationRequiredField.forEach(radio => { // 修正ポイント
        radio.addEventListener('change', toggleFields);
    });

    toggleFields(); // 初期状態を設定
});
