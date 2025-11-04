document.addEventListener('DOMContentLoaded', function() {
  function go_back() {
    window.history.back();
  }

  document.querySelectorAll('.cart-item').forEach(itemElem => {
    const itemId = itemElem.getAttribute('data-item-id');
    const qtyMinusBtn = itemElem.querySelector('.qty-minus');
    const qtyPlusBtn = itemElem.querySelector('.qty-plus');
    const qtyDisplay = itemElem.querySelector('.qty-display');
    const itemTotalElem = itemElem.querySelector('.item-total');
    const priceBadge = itemElem.querySelector('.price-badge');

    qtyMinusBtn.addEventListener('click', function () {
      let qty = parseInt(qtyDisplay.textContent);
      if (qty > 1) {
        const newQty = qty - 1;
        updateQuantity(itemId, newQty, qtyDisplay, itemTotalElem, priceBadge);
      }
    });

    qtyPlusBtn.addEventListener('click', function () {
      let qty = parseInt(qtyDisplay.textContent);
      const newQty = qty + 1;
      updateQuantity(itemId, newQty, qtyDisplay, itemTotalElem, priceBadge);
    });
  });

  async function updateQuantity(itemId, newQty, qtyDisplay, itemTotalElem, priceBadge) {
    console.log('item_id=> ' + itemId);

    try {
      const response = await fetch(`/api/product-quantity/update/${itemId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          quantity: newQty,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        qtyDisplay.textContent = data.quantity;
        itemTotalElem.textContent = "Total: ₹" + Number(data.item_total).toFixed(2);
        updateSummaryFields(data.cart_summary, data.final_price);
      } else {
        alert('Could not update quantity.');
      }
    } catch (err) {
      alert('Error updating cart.');
    }
  }

  function updateSummaryFields(summary, final_price) {
    document.getElementById('summary-total-price').textContent = "₹" + Number(summary.total_price).toFixed(2);
    document.getElementById('summary-fee').textContent = "₹" + Number(summary.fee).toFixed(2);
    document.getElementById('summary-discount').textContent = "-₹" + Number(summary.discount).toFixed(2);
    document.getElementById('summary-final-price').textContent = "₹" + Number(final_price).toFixed(2);

    const savingsBadge = document.getElementById('savings');
    if (summary.discount > 0) {
      if (savingsBadge) {
        savingsBadge.style.display = 'block'; // ensure visible
        savingsBadge.innerHTML = `<i class="bi bi-piggy-bank me-2"></i>You're saving ₹${Number(summary.discount).toFixed(2)}!`;
      }
    } else {
      if (savingsBadge) {
        savingsBadge.style.display = 'none'; // hide if no discount
      }
    }
  }

  window.go_back = go_back; // expose globally if used inline
});
