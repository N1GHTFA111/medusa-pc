function change_sidebar_color() {
    let element = document.getElementById("page-header");
    if (element.innerText == "Transactions"){
        let sidebar_element_to_change = document.getElementById("home");
        sidebar_element_to_change.classList.add("current");
    }
    else if (element.innerText == "All Users"){
        let sidebar_element_to_change = document.getElementById("all_users");
        sidebar_element_to_change.classList.add("current");
    }
    else if (element.innerText == "All Shipments"){
        let sidebar_element_to_change = document.getElementById("shipments");
        sidebar_element_to_change.classList.add("current");
    }
    else if (element.innerText == "Inventory"){
        let sidebar_element_to_change = document.getElementById("inventory");
        sidebar_element_to_change.classList.add("current");
    }
    else if (element.innerText == "Upload New Price List"){
        let sidebar_element_to_change = document.getElementById("price_list");
        sidebar_element_to_change.classList.add("current");
    }
    else{
        return true;
    }

    return true;
}

window.onload = function() {
    change_sidebar_color();
};