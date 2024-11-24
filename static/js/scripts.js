function linkify(text) {
    const urlPattern = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlPattern, '<a href="$1" target="_blank">$1</a>');
}


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
        if (data.success) {
            const assignmentElement = document.getElementById(`assignment-${user_id}`);
            if (data.assignment) {
                assignmentElement.innerHTML = `${data.assignment_name || "Unknown Name"} -> Odśwież, aby zobaczyć listę prezentową`;
            } else {
                assignmentElement.textContent = "Nie udało się nikogo znaleźć :c";
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


function resetLottery() {
    
    fetch(`/admin/reset_lottery`, {
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
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while processing the draw request.");
    });
}


function toggleLotteryActive(event) {

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


function reserveItem(event, user_id, item_id, on_dashboard) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/items/reserve/${user_id}/${item_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const wishlistRow = document.querySelector(`#wishlist-${data.owner_id} tr[data-item-id="${item_id}"]`);
                if (wishlistRow) {
                    wishlistRow.remove();
                }

                if (on_dashboard) {
                    const reservedTableBody = document.querySelector(`#reserved-table-${user_id} tbody`);
                    const reservedRow = `
                        <tr class="reserved-item" data-item-id="${item_id}">
                            <td>
                                <span class="item-name">${data.item.item_name}</span>
                                <span class="item-description">${linkify(data.item.item_description)}</span>
                            </td>
                            <td>
                                <span class="remove-icon" onclick="unreserveItem(event, '${item_id}')">×</span>
                            </td>
                            <td>
                                <span class="edit-icon" onclick="toggleBought(event, '${item_id}')">💲</span>
                            </td>
                        </tr>
                    `;
                    console.log("user_id")
                    reservedTableBody.insertAdjacentHTML("beforeend", reservedRow);

                    console.log("user_id")
                    const noReservedItemsMessage = document.getElementById("no-reserved-items");
                    if (noReservedItemsMessage) {
                        noReservedItemsMessage.style.display = "none";
                    }
                }
            } else {
                alert(data.error || "Error reserving item.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while processing the reserve request.");
        });
}







function unreserveItem(event, item_id, on_dashboard) {
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
                const { user_id, item } = data;

                const reservedRow = document.querySelector(`#reserved-table-${user_id} tr[data-item-id="${item_id}"]`);
                if (reservedRow) {
                    reservedRow.remove();
                }

                const reservedTableBody = document.querySelector(`#reserved-table-${user_id} tbody`);
                const noReservedItemsMessage = document.getElementById("no-reserved-items");
                if (!reservedTableBody || !reservedTableBody.querySelector("tr")) {
                    noReservedItemsMessage.style.display = "block";
                } else {
                    noReservedItemsMessage.style.display = "none";
                }
            } else {
                alert(data.message || "Nie można usunąć przedmiotu z listy zarezerwowanych. Może jest oznaczony jako kupiony?");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while processing the unreserve request.");
        });
}




function toggleBought(event, item_id, user_id) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/items/toggle_buy/${item_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                const reservedTable = document.querySelector(`#reserved-table-${user_id}`);
                const reservedRow = document.querySelector(`tr[data-item-id="${item_id}"]`);

                if (reservedRow && reservedTable) {
                    if (data.bought) {
                        reservedRow.classList.add("reserved-green");
                        reservedTable.appendChild(reservedRow);
                    } else {
                        reservedRow.classList.remove("reserved-green");
                        reservedTable.prepend(reservedRow);
                    }
                } else {
                    console.error("Reserved table or row not found.");
                }

                const reservedCell = document.querySelector(`#reserved-table-${item_id}-accept`);
                if (reservedCell) {
                    if (data.bought) {
                        reservedCell.classList.remove("remove-icon");
                        reservedCell.classList.add("edit-icon");
                    } else {
                        reservedCell.classList.remove("edit-icon");
                        reservedCell.classList.add("remove-icon");
                    }
                } else {
                    console.error("Reserved cell not found.");
                }
            } else {
                alert(data.error || "Error toggling bought status.");
            }
        })
        .catch((error) => {
            console.error("Error occurred:", error.message || error);
            alert("An error occurred while processing the request.");
        });
}




function editItem(event, item_id, itemName, itemDescription) {
    event.preventDefault();
    event.stopPropagation();

    const row = event.target.closest("tr");
    const nameCell = row.querySelector(".item-name");
    const descCell = row.querySelector(".item-description");

    nameCell.innerHTML = `<input type="text" value="${itemName}" class="edit-name" required>`;
    descCell.innerHTML = `<input type="text" value="${itemDescription}" class="edit-description" required>`;

    const editIconCell = row.querySelector(".edit-icon").parentElement;
    editIconCell.innerHTML = `<span class="save-icon" onclick="saveItem(event, ${item_id})">💾</span>`;
}

function saveItem(event, item_id) {
    event.preventDefault();
    event.stopPropagation();

    const row = event.target.closest("tr");
    const nameInput = row.querySelector(".edit-name");
    const descInput = row.querySelector(".edit-description");

    const newName = nameInput.value.trim();
    const newDescription = descInput.value.trim();

    if (!newName || !newDescription) {
        alert("Nazwa i opis przedmiotu nie mogą być puste.");
        return;
    }

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
            row.querySelector(".item-name").innerText = newName;
            row.querySelector(".item-description").innerText = newDescription;

            const saveIconCell = row.querySelector(".save-icon").parentElement;
            saveIconCell.innerHTML = `<span class="edit-icon" onclick="editItem(event, ${item_id}, '${newName}', '${newDescription}')">✎</span>`;
        } else {
            alert(data.error || "Błąd podczas zapisywania - pamiętaj, że przedmiot musi mieć nazwę i opis");
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


function addItem(event, owner_id) {
    event.preventDefault()
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
                updateWishlist(owner_id, data.item);
                itemInput.value = "";
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
    const wishlistTable = document.getElementById(`own-wishlist-table-${owner_id}`);
    if (!wishlistTable) {
        console.error("Wishlist table not found for owner ID:", owner_id);
        return;
    }

    const newRow = document.createElement("tr");
    newRow.setAttribute("data-item-id", item.item_id);

    newRow.innerHTML = `
        <td>
            <span class="item-name">${item.item_name}</span>
            <span class="item-description">${linkify(item.item_description)}</span>
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
        document.getElementById("error-message-password").textContent = "Hasła nie są identyczne. Spróbuj ponownie.";
        return false;
    }
    return true;
}

function updateUser(event, user_id = null, edit_mode = true) {
    event.preventDefault();
    event.stopPropagation();

    const name = document.getElementById(`name-${user_id}`)?.value || null;
    const username = document.getElementById(`username-${user_id}`)?.value || null;
    const password = document.getElementById(`password-${user_id}`)?.value || null;
    const confirmPassword = document.getElementById(`confirm_password-${user_id}`)?.value || null;
    const choosable = document.getElementById(`choosable-${user_id}`)?.checked || false;
    const admin = document.getElementById(`admin-${user_id}`)?.checked || false;
    const visible = document.getElementById(`visible-${user_id}`)?.checked || true;

    const spouseElement = document.querySelector(`#spouse-${user_id}`);
    const spouse = spouseElement ? spouseElement.value : null;

    console.log(user_id)

    // Check if passwords match
    if (password !== confirmPassword) {
        document.getElementById("error").textContent = "Hasła muszą być identyczne.";
        return;
    }

    // Check if username is free
    fetch(`/users/is_username_free?edit_mode=${edit_mode}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username, user_ID: user_id }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (!data.is_free) {
                document.getElementById("error").textContent = "Nazwa użytkownika jest już zajęta.";
                return;
            }

            // Continue if username is free
            const payload = {
                user_id,
                edit_mode,
                spouse,
                name,
                username,
                password,
                choosable,
                visible,
                admin
            };
            
            fetch(`/users/update`, {
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
                        document.getElementById("error").textContent =
                            data.error || "Nie udało się zaktualizować użytkownika.";
                    }
                })
                .catch((error) => {
                    console.error("Error updating user:", error);
                    document.getElementById("error").textContent =
                        "Wystąpił błąd podczas aktualizacji użytkownika.";
                });
        })
        .catch((error) => {
            console.error("Error checking username:", error);
            document.getElementById("error").textContent = "Nazwa użytkownika jest już zajęta.";
        });
}


async function deleteUser(userId) {
    try {
        const response = await fetch(`/users/delete_user_route`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId }),
        });

        const result = await response.json();

        if (result.success) {
            alert(`User ${userId} has been deleted.`);
            location.reload(); // Refresh the page on success
        } else {
            alert(`Failed to delete user ${userId}: ${result.message}`);
        }
    } catch (error) {
        alert(`Error deleting user ${userId}: ${error.message}`);
    }
}
