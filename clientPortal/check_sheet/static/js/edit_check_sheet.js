document.addEventListener("DOMContentLoaded", function () {
    setupFormsetTable({
        tableId: "formset-table",
        addButtonId: "add-row-btn",
        totalFormsSelector: "#id_assess_target-TOTAL_FORMS",
        prefix: "assess_target",
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
        totalFormsSelector: "#id_login_credential-TOTAL_FORMS",
        prefix: "login_credential",
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

    addButton.addEventListener("click", function () {
        const currentFormCount = parseInt(totalFormsInput.value, 10);
        const emptyFormTemplate = table.dataset.emptyForm.replace(/__prefix__/g, currentFormCount);

        const newRow = document.createElement("tr");
        newRow.classList.add("form-row");

        const noCell = document.createElement("td");
        noCell.textContent = currentFormCount + 1;
        newRow.appendChild(noCell);

        const parser = new DOMParser();
        const parsedHTML = parser.parseFromString(emptyFormTemplate, "text/html");

        columns.forEach(column => {
            const newCell = document.createElement("td");
            const field = parsedHTML.querySelector(`[name*="${column}"]`);
            if (field) {
                newCell.appendChild(field);
            }
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

        updateAllRowNumbers(table);
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

function updateAllRowNumbers(table) {
    const rows = table.querySelectorAll(".form-row:not([style*='display: none'])");
    rows.forEach((row, index) => {
        const noCell = row.querySelector("td:first-child");
        if (noCell) {
            noCell.textContent = index + 1;
        }
    });
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

