document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('adminOrderUpdateForm');
    const messageDiv = document.getElementById('message');
    
    let currentItems = new Map();
    let newItems = new Map();
    
    // Initialize current items SAFELY
    document.querySelectorAll('.current-item').forEach(item => {
        const productId = item.dataset.productId;
        const qtyInput = item.querySelector('.current-quantity');
        
        if (productId && qtyInput) {
            const price = parseFloat(qtyInput.dataset.productSalePrice) || 0;
            currentItems.set(productId, {
                element: item,
                quantity: parseInt(qtyInput.value) || 0,
                price: price
            });
        }
    });
    
    // Current quantity change handlers
    document.querySelectorAll('.current-quantity').forEach(input => {
        input.addEventListener('input', function() {
            const productId = this.dataset.productId;
            const qty = parseInt(this.value) || 0;
            const item = currentItems.get(productId);
            if (item) {
                item.quantity = qty;
                updateSummary();  // Call updateSummary instead
            }
        });
    });
    
    // FIXED Remove button handler
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', function() {
            // Get productId from closest parent .current-item
            const itemRow = this.closest('.current-item');
            const productId = itemRow.dataset.productId;
            
            if (productId && currentItems.has(productId)) {
                const item = currentItems.get(productId);
                if (item && item.element) {
                    item.element.remove();
                    item.quantity = 0;
                    currentItems.delete(productId);
                    updateSummary();
                }
            }
        });
    });
    
    // New product checkbox handlers
    document.querySelectorAll('.product-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const productRow = this.closest('.new-product-row');
            const productId = productRow.dataset.productId;
            const qtyInput = productRow.querySelector('.product-quantity');
            
            if (!productId || !qtyInput) return;
            
            if (this.checked) {
                const price = parseFloat(qtyInput.dataset.productSalePrice) || 0;
                newItems.set(productId, {
                    product_id: productId,
                    quantity: parseInt(qtyInput.value) || 1,
                    price: price,
                    element: productRow
                });
            } else {
                newItems.delete(productId);
            }
            updateSummary();
        });
    });
    
    // New quantity change handlers
    document.querySelectorAll('.product-quantity').forEach(input => {
        input.addEventListener('input', function() {
            const productId = this.dataset.productId;
            const qty = parseInt(this.value) || 0;
            const item = newItems.get(productId);
            if (item) {
                item.quantity = qty;
                updateSummary();
            }
        });
    });
    
    function updateSummary() {
        let total = 0;
        let listingTotal = 0;
        
        // Current items
        currentItems.forEach(item => {
            if (item.quantity > 0) {
                total += item.quantity * item.price;
                listingTotal += item.quantity * item.price;
            }
        });
        
        // New items
        newItems.forEach(item => {
            if (item.quantity > 0) {
                total += item.quantity * item.price;
                listingTotal += item.quantity * item.price;
            }
        });
        
        // UPDATE ALL FIELDS CORRECTLY
        document.getElementById('total_price').value = total.toFixed(2);
        document.getElementById('listing_price').value = listingTotal.toFixed(2);
        
        // Calculate discount (10% of total for demo)
        const discountValue = total * 0.05;  // 5% discount
        document.getElementById('discount').value = discountValue.toFixed(2);
        
        // Recalculate total_price after discount
        const finalTotal = total - discountValue;
        document.getElementById('total_price').value = finalTotal.toFixed(2);
    }
    
    // Form submission
    window.order_update = async function(orderId) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = '';
        messageEl.className = '';
        
        const formData = {
            user: document.getElementById('user').value,
            status: document.getElementById('status').value,
            total_price: document.getElementById('total_price').value,
            discount: document.getElementById('discount').value,
            delivery_fee: document.getElementById('delivery_fee').value,
            listing_price: document.getElementById('listing_price').value,
            delivery_address: document.getElementById('delivery_address').value,
            is_active: document.getElementById('is_active').checked,
            order_id: orderId,
            current_items: Array.from(currentItems.entries())
                .map(([id, item]) => ({ product_id: id, quantity: item.quantity }))
                .filter(item => item.quantity > 0),
            new_items: Array.from(newItems.entries())
                .map(([id, item]) => ({ product_id: id, quantity: item.quantity }))
                .filter(item => item.quantity > 0)
        };
        
        if (!formData.user || !formData.status || 
            (formData.current_items.length === 0 && formData.new_items.length === 0)) {
            showMessage('Please fill required fields and add items', 'error');
            return false;
        }
        
        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            if (response.ok) {
                showMessage(result.message || 'Order updated successfully!', 'success');
                setTimeout(() => window.location.href = '/admin/orders/', 1500);
            } else {
                showMessage(result.error || 'Update failed', 'error');
            }
        } catch (err) {
            showMessage('Network error. Please try again.', 'error');
        }
    };
    
    function showMessage(text, type) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = text;
        messageEl.className = type;
    }
    
    // Initial summary calculation
    updateSummary();
});
