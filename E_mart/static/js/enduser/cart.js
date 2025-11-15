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
        // Debug
        console.log("API Response:", data);

        if (qtyDisplay) qtyDisplay.textContent = data.quantity;
        if (itemTotalElem) itemTotalElem.textContent = "Total: ₹" + Number(data.item_total).toFixed(2);

        updateSummaryFields(data.cart_summary, data.final_price, data.in_stock);
        toggleQuantityButtons(data.in_stock, itemId);

      } else {
        alert('Could not update quantity.');
      }
    } catch (err) {
      alert('Error updating cart.');
      console.error(err);
    }
  }


  function updateSummaryFields(summary, final_price, in_stock) {
    if (!summary) return;

    const totalPriceElem = document.getElementById('summary-total-price');
    const feeElem = document.getElementById('summary-fee');
    const discountElem = document.getElementById('summary-discount');
    const finalPriceElem = document.getElementById('summary-final-price');
    const outOfStockElem = document.getElementById('outofstock');
    const savingsBadge = document.getElementById('savings');

    if (totalPriceElem) totalPriceElem.textContent = "₹" + Number(summary.list_price).toFixed(2);
    if (feeElem) feeElem.textContent = "₹" + Number(summary.fee).toFixed(2);
    if (discountElem) discountElem.textContent = "-₹" + Number(summary.discount).toFixed(2);
    if (finalPriceElem) finalPriceElem.textContent = "₹" + Number(summary.total_price).toFixed(2);

    if (outOfStockElem) {
      outOfStockElem.style.display = in_stock ? 'none' : 'block';
    }

    if (savingsBadge) {
      if (summary.discount > 0) {
        savingsBadge.style.display = 'block';
        savingsBadge.innerHTML = `<i class="bi bi-piggy-bank me-2"></i>You're saving ₹${Number(summary.discount).toFixed(2)}!`;
      } else {
        savingsBadge.style.display = 'none';
      }
    }
  }

  function toggleQuantityButtons(in_stock, itemId) {
    console.log("in stock => "+in_stock);
    const itemElem = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
    if (!itemElem) return;

    const qtyPlusBtn = itemElem.querySelector('.qty-plus');

    if (qtyPlusBtn) qtyPlusBtn.disabled = !in_stock;
  }

  window.go_back = go_back; // global exposure if used inline
});
