document.addEventListener('DOMContentLoaded', () => {
    const cartIcon = document.getElementById('cart-icon');
    const cartDropdown = document.getElementById('cart-dropdown');

    cartIcon.addEventListener('mouseover', () => {
        cartDropdown.style.display = 'block';
    });

    cartIcon.addEventListener('mouseleave', () => {
        cartDropdown.style.display = 'none';
    });
});

function updateCart(items) {
    const cartDropdown = document.getElementById('cart-dropdown');
    const cartCount = document.getElementById('badge');

    if(items.length === 0) {
        cartDropdown.innerHTML = '<p>Shopping cart is empty</p>';
        cartCount.textContent = '0';
    }
    else {
        cartDropdown.innerHTML = items
            .map(
                (item) =>
                    `<div>
                        <p>${item.title} - ${item.quantity}</p>
                        <p>Price: ₱${item.price}</p>
                    </div>`
            )
            .join('');
        cartCount.textContent = items.length.toString();
    }
}

function fetchCart() {
    fetch('/get-cart-data/')
        .then((response) => response.json())
        .then((data) => {
            updateCart(data.cart_items);
        })
        .catch((error) => console.error('Error cart data:', error));
}

fetchCart()


document.addEventListener('DOMContentLoaded', () => {
    const popUp = document.getElementById('pop_up');
    const popClose = document.getElementById('pop_close');
    const body = document.body;

    const popTitle = document.getElementById('pop_title');
    const popPrice = document.getElementById('pop_price');
    const popImage = document.getElementById('pop_image');

document.querySelectorAll('.icon_cart').forEach(button => {
    button.addEventListener('click', (e) => {
        const title = e.target.getAttribute('data-title');
        const price = e.target.getAttribute('data-price');
        const imageSrc = e.target.getAttribute('data-image');

        popTitle.textContent = title;
        popPrice.textContent = `₱${price}`;
        popImage.src = imageSrc;
        popUp.style.display = 'block';
        body.classList.add('overlay-active');
        });
    });

    popClose.addEventListener('click', () => {
        popUp.style.display = 'none';
        body.classList.remove('overlay-active');
    });

    window.addEventListener('click', (e) => {
        if (e.target === popUp) {
            popUp.style.display = 'none';
            body.classList.remove('overlay-active');
        }
    });
});

//CART
document.addEventListener('DOMContentLoaded', () => {
    const cartIcons = document.querySelectorAll('.icon_cart');
    const popup = document.getElementById('pop_up');
    const popupTitle = document.getElementById('.pop_title');
    const popupPrice = document.getElementById('.pop_price');
    const popupImage = document.getElementById('.pop_image');
    const popupClose = document.getElementById('pop_close');

    cartIcons.forEach((icon) => {
        icon.addEventListener('click', (event) => {
            event.preventDefault();
            const title = icon.dataset.title;
            const price = icon.dataset.price;
            const imageUrl = icon.dataset.image;
            popupTitle.textContent = title;
            popupPrice.textContent = `${price}`;
            popupImage.src = imageUrl;
            popup.style.display = 'block';
        });
    });

    popupClose.addEventListener('click', () => {
        popup.style.display = 'none';
    });
});

//STOCK AND QUANTITY
function showPopup(title, price, stock) {
    document.getElementById('pop_title').textContent = title;
    document.getElementById('pop_price').textContent = `${price}`;
    document.getElementById('pop_stock').textContent = stock;

    const quantityInput = document.getElementById('quantity');
    quantityInput.value = 1;
    quantityInput.setAttribute('data-max', stock);

    const popup = document.getElementById('pop_up');
    popup.style.display = 'flex';
}

function updateQuantity(change) {
    const quantityInput = document.getElementById('quantity');
    const currentQuantity = parseInt(quantityInput.value, 10);
    const maxStock = parseInt(quantityInput.getAttribute('data-max'), 10);
    let newQuantity = currentQuantity + change;

    if(newQuantity < 1) {
        newQuantity = 1;
    }
    else if (newQuantity > maxStock){
        newQuantity = maxStock;
    }
    quantityInput.value = newQuantity;
}