
document.addEventListener("DOMContentLoaded", function () {
    const addRowBtn = document.getElementById("add-row-btn");
    const formsetTable = document.getElementById("formset-table");
    const totalFormsInput = document.querySelector("#id_assess_target-TOTAL_FORMS");
    const loginAddRowBtn = document.getElementById("add-login-row-btn");
    const loginTable = document.getElementById("login-credentials-table");
    const loginTotalFormsInput = document.querySelector("#id_login_credential-TOTAL_FORMS");

    const modal = document.getElementById("delete-confirm-modal");
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    const cancelDeleteBtn = document.getElementById("cancel-delete-btn");

    if (!modal || !confirmDeleteBtn || !cancelDeleteBtn) {
        console.error("モーダルまたはボタンの要素が見つかりません。HTMLを確認してください。");
        return;
    }

    let rowToDelete = null; // 削除対象の行を一時的に保存

    // 削除ボタンの処理
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-row-btn")) {
            const row = event.target.closest("tr");
            const inputs = row.querySelectorAll("input, select, textarea");
            let hasValue = false;

            // 行内の入力値を確認
            inputs.forEach(input => {
                if (input.name.includes("-DELETE")) return; // 削除フラグは無視
                if (input.value.trim() !== "") {
                    hasValue = true;
                }
            });

            if (hasValue) {
                // 入力値がある場合はモーダルを表示
                rowToDelete = row; // 削除対象の行を保存
                modal.style.display = "flex"; // モーダルを表示
            } else {
                // 入力値がない場合は即削除
                deleteRow(row);
            }
        }
    });

    // モーダルの「削除」ボタンの処理
    confirmDeleteBtn.addEventListener("click", function () {
        if (rowToDelete) {
            deleteRow(rowToDelete); // 行を削除
            rowToDelete = null; // 削除対象をリセット
        }
        modal.style.display = "none"; // モーダルを非表示
    });

    // モーダルの「キャンセル」ボタンの処理
    cancelDeleteBtn.addEventListener("click", function () {
        rowToDelete = null; // 削除対象をリセット
        modal.style.display = "none"; // モーダルを非表示
    });

    // 行を削除する関数
    function deleteRow(row) {
        const deleteInput = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
        if (deleteInput) {
            deleteInput.checked = true; // 削除フラグを設定
        }
        row.style.display = "none"; // 行を非表示にする

        // No列を再計算
        const table = row.closest("table");
        updateAllRowNumbers(table);
    }

    // 特定の行の No列を更新
    function updateRowNumber(row, number) {
        const noCell = row.querySelector("td:first-child");
        if (noCell) {
            noCell.textContent = number;
        }
    }

    // テーブル全体の No列を再計算
    function updateAllRowNumbers(table) {
        const rows = table.querySelectorAll(".form-row:not([style*='display: none'])");
        rows.forEach((row, index) => {
            updateRowNumber(row, index + 1); // 各行の No列を更新
        });
    }

    // Assess Targets の行を追加
    addRowBtn.addEventListener("click", function () {
        const currentFormCount = parseInt(totalFormsInput.value, 10);
        const emptyFormTemplate = formsetTable.dataset.emptyForm.replace(/__prefix__/g, currentFormCount);

        const newRow = document.createElement("tr");
        newRow.classList.add("form-row");

        const columns = [
            "no", // No列を追加
            "url_or_ip_address",
            "host_name",
            "os",
            "web_server",
            "ap_server",
            "framework",
            "db_server",
            "DELETE"
        ];

        columns.forEach(column => {
            const newCell = document.createElement("td");
            if (column === "no") {
                newCell.textContent = currentFormCount + 1;
            } else if (column === "DELETE") {
                const deleteButton = document.createElement("button");
                deleteButton.type = "button";
                deleteButton.classList.add("delete-row-btn");
                deleteButton.textContent = "削除";
                newCell.appendChild(deleteButton);

                const deleteInput = document.createElement("input");
                deleteInput.type = "checkbox";
                deleteInput.name = `form-${currentFormCount}-DELETE`;
                deleteInput.style.display = "none";
                newCell.appendChild(deleteInput);
            } else {
                const parser = new DOMParser();
                const parsedHTML = parser.parseFromString(emptyFormTemplate, "text/html");
                const field = parsedHTML.querySelector(`[name*="${column}"]`);
                if (field) {
                    newCell.appendChild(field);
                }
            }
            newRow.appendChild(newCell);
        });

        formsetTable.querySelector("tbody").appendChild(newRow);
        totalFormsInput.value = currentFormCount + 1;

        // No列を再計算
        updateAllRowNumbers(formsetTable);
    });

    // Assess Login Credentials の行を追加
    loginAddRowBtn.addEventListener("click", function () {
        const currentFormCount = parseInt(loginTotalFormsInput.value, 10);
        const emptyFormTemplate = loginTable.dataset.emptyForm.replace(/__prefix__/g, currentFormCount);

        const newRow = document.createElement("tr");
        newRow.classList.add("form-row");

        const columns = [
            "no", // No列を追加
            "login_id",
            "password",
            "role",
            "DELETE"
        ];

        columns.forEach(column => {
            const newCell = document.createElement("td");
            if (column === "no") {
                newCell.textContent = currentFormCount + 1;
            } else if (column === "DELETE") {
                const deleteButton = document.createElement("button");
                deleteButton.type = "button";
                deleteButton.classList.add("delete-row-btn");
                deleteButton.textContent = "削除";
                newCell.appendChild(deleteButton);

                const deleteInput = document.createElement("input");
                deleteInput.type = "checkbox";
                deleteInput.name = `login_form-${currentFormCount}-DELETE`;
                deleteInput.style.display = "none";
                newCell.appendChild(deleteInput);
            } else {
                const parser = new DOMParser();
                const parsedHTML = parser.parseFromString(emptyFormTemplate, "text/html");
                const field = parsedHTML.querySelector(`[name*="${column}"]`);
                if (field) {
                    newCell.appendChild(field);
                }
            }
            newRow.appendChild(newCell);
        });

        loginTable.querySelector("tbody").appendChild(newRow);
        loginTotalFormsInput.value = currentFormCount + 1;

        // No列を再計算
        updateAllRowNumbers(loginTable);
    });
});



function toggleOtherField() {
    var radios = document.getElementsByName("environment");
    var show = false;
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked && radios[i].value === "other") {
            show = true;
        }
    }
    var otherField = document.getElementById("env_other_field");
    otherField.display = show ? "block" : "none";
    if (otherField) {
        otherField.required = show;
    }
}
window.addEventListener('DOMContentLoaded', function() {
    toggleOtherField();
    var radios = document.getElementsByName("environment");
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
