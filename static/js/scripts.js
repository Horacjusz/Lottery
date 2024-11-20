// Function to submit draw form
function submitDrawForm(user_id) {
    const form = document.getElementById(`draw-form-${user_id}`);
    const url = form.action;

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not OK");
        }
        return response.json();
    })
    .then(data => {
        console.log("Server response:", data);

        if (data.success) {
            const assignmentElement = document.getElementById(`assignment-${user_id}`);
            if (data.assignment) {
                assignmentElement.innerHTML = `${data.assignment} -> ${data.assignment_name || "Unknown Name"}`;
            } else {
                assignmentElement.textContent = "No assignment available.";
            }
        } else {
            alert("Failed to process the draw request.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while processing the draw request.");
    });
}

function toggleLotteryActive(event) {
    console.log("Toggling lottery");

    event.preventDefault();

    const url = "/admin/toggle_lottery"; // This matches the blueprint's URL prefix and route

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to toggle lottery status.");
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const button = document.getElementById("lottery-toggle-btn");
            const statusText = document.getElementById("lottery-status");

            if (data.LOTTERY_ACTIVE) {
                button.classList.remove("lottery-disabled");
                button.classList.add("lottery-enabled");
                button.textContent = "Lottery enabled";
                statusText.textContent = "Current status: Enabled";
            } else {
                button.classList.remove("lottery-enabled");
                button.classList.add("lottery-disabled");
                button.textContent = "Lottery disabled";
                statusText.textContent = "Current status: Disabled";
            }
        } else {
            alert("Failed to toggle lottery status.");
        }
    })
    .catch(error => {
        console.error("Error toggling lottery:", error);
        alert("An error occurred while toggling lottery status.");
    });
}





document.addEventListener("DOMContentLoaded", function() {
    // Toggle for the main user list
    const mainCollapsible = document.querySelector(".main-collapsible");
    const userList = document.querySelector(".users-list");
    mainCollapsible.addEventListener("click", function() {
        this.classList.toggle("active");
        userList.style.display = userList.style.display === "block" ? "none" : "block";
        this.textContent = userList.style.display === "block" ? "Hide" : "Show";
    });

    // Toggle for individual user attributes
    const userCollapsibles = document.querySelectorAll(".user-collapsible");
    userCollapsibles.forEach(button => {
        button.addEventListener("click", function() {
            const userContent = this.parentElement.nextElementSibling; // Correct sibling selection
            userContent.style.display = userContent.style.display === "block" ? "none" : "block";
            this.textContent = userContent.style.display === "block" ? "-" : "+";
        });
    });
});

function unreserveItem(event, item_id) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/items/unreserve/${item_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const reservedRow = document.querySelector(`tr[data-item-id="${item_id}"]`);
                if (reservedRow) {
                    reservedRow.remove();
                }

                const noReservedItemsMessage = document.getElementById("no-reserved-items");
                if (!document.querySelector("#reserved-table tbody tr")) {
                    noReservedItemsMessage.style.display = "block";
                }
            } else {
                alert(data.error || "Error unreserving item.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while processing the unreserve request.");
        });
}



function toggleBought(event, item_id) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/items/toggle_buy/${item_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const reservedRow = document.querySelector(`tr[data-item-id="${item_id}"]`);
                if (reservedRow) {
                    // Toggle the green background based on the new bought status
                    if (data.bought) {
                        reservedRow.classList.add("reserved-green");
                    } else {
                        reservedRow.classList.remove("reserved-green");
                    }
                }
            } else {
                alert(data.error || "Error toggling bought status.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while processing the request.");
        });
}





function editItem(event, item_id, itemName, itemDescription) {
    console.log("Editing item:", item_id);
    event.preventDefault();
    event.stopPropagation();

    const row = event.target.closest("tr");
    const nameCell = row.querySelector(".item-name");
    const descCell = row.querySelector(".item-description");

    // Replace text with input fields for editing
    nameCell.innerHTML = `<input type="text" value="${itemName}" class="edit-name">`;
    descCell.innerHTML = `<input type="text" value="${itemDescription}" class="edit-description">`;

    // Change edit icon to save icon
    const editIconCell = row.querySelector(".edit-icon").parentElement;
    editIconCell.innerHTML = `<span class="save-icon" onclick="saveItem(event, ${item_id})">💾</span>`;
}

function saveItem(event, item_id) {
    console.log("Saving item:", item_id);
    event.preventDefault();
    event.stopPropagation();

    const row = event.target.closest("tr");
    const newName = row.querySelector(".edit-name").value;
    const newDescription = row.querySelector(".edit-description").value;

    fetch(`/items/edit/${item_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            new_name: newName,
            new_description: newDescription,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Item saved successfully:", data);

            // Update the row with the new data
            row.querySelector(".item-name").innerText = newName;
            row.querySelector(".item-description").innerText = newDescription;

            // Change save icon back to edit icon
            const saveIconCell = row.querySelector(".save-icon").parentElement;
            saveIconCell.innerHTML = `<span class="edit-icon" onclick="editItem(event, ${item_id}, '${newName}', '${newDescription}')">✎</span>`;
        } else {
            alert(data.error || "Error saving changes.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while saving the item.");
    });
}


function removeItem(event, item_id) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/items/remove/${item_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove the item row
            const row = document.querySelector(`tr[data-item-id="${item_id}"]`);
            if (row) {
                row.remove();
            }

            // Check if the wishlist is now empty
            const tableBody = document.querySelector(".wishlist-table tbody");
            if (tableBody.children.length === 0) {
                document.getElementById("no-items").style.display = "block";
            }
        } else {
            alert(data.message || "Error removing item.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while trying to remove the item.");
    });
}


function addItem(owner_id) {
    console.log("Adding item");
    const itemInput = document.getElementById(`wishlist_item-${owner_id}`);
    const descriptionInput = document.getElementById(`wishlist_description-${owner_id}`);

    // Check if elements exist
    if (!itemInput || !descriptionInput) {
        alert("Error: Missing input fields for adding items.");
        console.error(`Input fields not found for user ID: ${owner_id}`);
        return;
    }

    const itemName = itemInput.value.trim();
    const itemDescription = descriptionInput.value.trim();

    if (!itemName) {
        alert("Nazwa przedmiotu jest wymagana.");
        return;
    }

    fetch(`/items/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            item_name: itemName,
            item_description: itemDescription,
            owner_id: owner_id,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                updateWishlist(owner_id, data.item); // Update wishlist with the new item
                itemInput.value = ""; // Clear the input fields
                descriptionInput.value = "";
            } else {
                alert(data.error || "Nie udało się dodać przedmiotu.");
            }
        })
        .catch((error) => {
            console.error("Error adding item:", error);
            alert("Wystąpił błąd podczas dodawania przedmiotu.");
        });
}


function updateWishlist(owner_id, item) {
    const wishlistTable = document.getElementById("wishlist-table");
    const newRow = document.createElement("tr");
    newRow.setAttribute("data-item-id", item.item_id);

    newRow.innerHTML = `
        <td>
            <span class="item-name">${item.item_name}</span>
            <span class="item-description">${item.item_description}</span>
        </td>
        <td>
            <span class="edit-icon" onclick="editItem(event, '${item.item_id}', '${item.item_name}', '${item.item_description}')">✎</span>
        </td>
        <td>
            <span class="remove-icon" onclick="removeItem(event, ${item.item_id})">×</span>
        </td>
    `;
    wishlistTable.querySelector("tbody").appendChild(newRow);
}


function validatePasswords() {
    const password = document.getElementById("password-new").value;
    const confirmPassword = document.getElementById("confirm_password-new").value;

    if (password && password !== confirmPassword) {
        document.getElementById("error").textContent = "Hasła nie są identyczne. Spróbuj ponownie.";
        return false; // Prevent form submission
    }
    return true;
}

function updateUser(event, user_id = null) {
    event.preventDefault();
    event.stopPropagation();

    const idSuffix = user_id || 'new';
    const name = document.getElementById(`name-${idSuffix}`).value;
    const username = document.getElementById(`username-${idSuffix}`).value;
    const password = document.getElementById(`password-${idSuffix}`).value;
    const choosable = document.getElementById(`choosable-${idSuffix}`)?.checked || false;
    const admin = document.getElementById(`admin-${idSuffix}`)?.checked || false;
    const visible = document.getElementById(`visible-${idSuffix}`)?.checked || true;

    const spouseElement = document.querySelector(`#spouse-${idSuffix}`);
    const spouse = spouseElement ? spouseElement.value : null;

    const payload = {
        new_spouse: spouse,
        new_name: name,
        new_username: username,
        new_password: password,
        new_choosable: choosable,
        new_visible: visible,
        new_admin: admin,
    };

    console.log("Payload being sent:", payload);

    fetch(`/users/update/${user_id || ''}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                const redirectUrl = edit_mode ? "/dashboard" : "/auth/login";
                window.location.href = redirectUrl;
            } else {
                document.getElementById("error").textContent = data.error || "Failed to update user.";
            }
        })
        .catch((error) => {
            console.error("Error updating user:", error);
            document.getElementById("error").textContent = "An error occurred while updating the user.";
        });
}
