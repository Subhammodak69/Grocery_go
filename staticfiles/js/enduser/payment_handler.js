// Payment Handler JavaScript for GroceryGo Order Summary
// Handles payment method selection, form display, and payment creation API call

document.addEventListener('DOMContentLoaded', function() {
    // ==================== ELEMENTS ====================
    const paymentMethodSelect = document.getElementById('payment-method');
    const allMethodForms = document.querySelectorAll('.method-form');
    
    // Form elements for each payment method
    const upiForm = document.getElementById('UPI-form');
    const creditCardForm = document.getElementById('CREDITCARD-form');
    const debitCardForm = document.getElementById('DEBITCARD-form');
    const netBankingForm = document.getElementById('NETBANKING-form');
    const codForm = document.getElementById('COD-form');

    // ==================== PAYMENT METHOD SELECTION ====================
    if (paymentMethodSelect) {
        paymentMethodSelect.addEventListener('change', function() {
            const selectedMethod = this.value;
            
            // Hide all payment method forms
            allMethodForms.forEach(form => {
                form.style.display = 'none';
            });
            
            // Show the selected payment method form
            if (selectedMethod) {
                const selectedForm = document.getElementById(`${selectedMethod}-form`);
                if (selectedForm) {
                    selectedForm.style.display = 'block';
                }
            }
        });
    }

    // ==================== UPI PAYMENT SUBMISSION ====================
    if (upiForm) {
        const upiBtn = upiForm.querySelector('button');
        const upiInput = upiForm.querySelector('input[type="text"]');
        
        upiBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const upiId = upiInput.value.trim();
            
            if (!upiId) {
                showNotification('Please enter a valid UPI ID', 'error');
                return;
            }
            
            if (!validateUPI(upiId)) {
                showNotification('Invalid UPI ID format', 'error');
                return;
            }
            
            createPayment('UPI', { upi_id: upiId });
        });
    }

    // ==================== CREDIT CARD PAYMENT SUBMISSION ====================
    if (creditCardForm) {
        const ccBtn = creditCardForm.querySelector('button');
        const ccNumber = creditCardForm.querySelector('input[placeholder*="XXXX"]');
        const ccExpiry = creditCardForm.querySelector('input[placeholder*="MM/YY"]');
        const ccCVV = creditCardForm.querySelector('input[type="password"]');
        ccBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const cardNumber = ccNumber.value.trim().replace(/-/g, '');
            console.log(cardNumber);

            const expiry = ccExpiry.value.trim();
            const cvv = ccCVV.value.trim();
            
            if (!cardNumber || !expiry || !cvv) {
                showNotification('Please fill all credit card details', 'error');
                return;
            }
            
            if (!validateCardNumber(cardNumber)) {
                showNotification('Invalid card number', 'error');
                return;
            }
            
            if (!validateExpiry(expiry)) {
                showNotification('Invalid expiry date', 'error');
                return;
            }
            
            if (!validateCVV(cvv)) {
                showNotification('Invalid CVV', 'error');
                return;
            }
            
            createPayment('CREDITCARD', {
                card_number: maskCardNumber(cardNumber),
                expiry: expiry,
                cvv: cvv 
            });
        });
    }

    // ==================== DEBIT CARD PAYMENT SUBMISSION ====================
    if (debitCardForm) {
        const dcBtn = debitCardForm.querySelector('button');
        const dcNumber = debitCardForm.querySelector('input[placeholder*="XXXX"]');
        const dcExpiry = debitCardForm.querySelector('input[placeholder*="MM/YY"]');
        const dcCVV = debitCardForm.querySelector('input[type="password"]');
        
        dcBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const cardNumber = dcNumber.value.trim().replace(/\s+/g, '');
            const expiry = dcExpiry.value.trim();
            const cvv = dcCVV.value.trim();
            
            if (!cardNumber || !expiry || !cvv) {
                showNotification('Please fill all debit card details', 'error');
                return;
            }
            
            if (!validateCardNumber(cardNumber)) {
                showNotification('Invalid card number', 'error');
                return;
            }
            
            if (!validateExpiry(expiry)) {
                showNotification('Invalid expiry date', 'error');
                return;
            }
            
            if (!validateCVV(cvv)) {
                showNotification('Invalid CVV', 'error');
                return;
            }
            
            createPayment('DEBITCARD', {
                card_number: maskCardNumber(cardNumber),
                expiry: expiry,
                cvv: cvv
            });
        });
    }

    // ==================== NET BANKING SUBMISSION ====================
    if (netBankingForm) {
        const nbBtn = netBankingForm.querySelector('button');
        const bankSelect = netBankingForm.querySelector('select');
        
        nbBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const selectedBank = bankSelect.value;
            
            if (!selectedBank) {
                showNotification('Please select a bank', 'error');
                return;
            }
            
            createPayment('NETBANKING', { bank: selectedBank });
        });
    }

    // ==================== COD SUBMISSION ====================
    if (codForm) {
        const codBtn = codForm.querySelector('button');
        
        codBtn.addEventListener('click', function(e) {
            e.preventDefault();
            createPayment('COD', {});
        });
    }

    // ==================== PAYMENT CREATION API CALL ====================
    function createPayment(paymentMethod, paymentDetails) {
        // Get order details
        const cartId = document.getElementById('cartId')?.value;
        const deliveryAddress = document.getElementById('delivery-address')?.value.trim();
        const finalPrice = document.getElementById('final_price')?.value;
        const deliveryFee = document.getElementById('delivery_fee')?.value;
        const discount = document.getElementById('discount')?.value;
        
        // Validate delivery address
        if (!deliveryAddress) {
            showNotification('Please enter delivery address', 'error');
            document.getElementById('delivery-address').focus();
            return;
        }
        
        // Collect product IDs
        const productIds = Array.from(document.querySelectorAll('input[name="product_ids"]'))
            .map(input => input.value);
        
        if (productIds.length === 0) {
            showNotification('No products found in cart', 'error');
            return;
        }
        
        // Prepare payment data
        const paymentData = {
            cart_id: cartId,
            product_ids: productIds,
            delivery_address: deliveryAddress,
            method: paymentMethod,
            payment_details: paymentDetails,
            amount: parseFloat(finalPrice),
            delivery_fee: parseFloat(deliveryFee),
            discount: parseFloat(discount)
        };
        
        // Show loading state
        showLoading(true);
        
        const loader = document.getElementById('loaderdiv');
        loader.style.display = 'block';
        setTimeout(()=>{
            // Make API call
            fetch('/api/payment/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(paymentData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(err.message || 'Payment creation failed');
                    });
                }
                return response.json();
            })
            .then(data => {
                showLoading(false);
                
                if (data.success) {
                    showNotification('Payment created successfully!', 'success');
                    loader.style.display = 'none';

                    setTimeout(()=>{
                        create_order();
                    },1000);
                    
                } else {
                    showNotification(data.message || 'Payment creation failed', 'error');
                    loader.style.display = 'none';

                }
            })
            .catch(error => {
                showLoading(false);
                loader.style.display = 'none';

                console.error('Payment Error:', error);
                showNotification(error.message || 'An error occurred during payment', 'error');
            });
        },3000);
    }

    // ==================== VALIDATION FUNCTIONS ====================
    function validateUPI(upiId) {
        // UPI format: username@bankname
        const upiRegex = /^[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}$/;
        return upiRegex.test(upiId);
    }

    function validateCardNumber(cardNumber) {
        // Basic Luhn algorithm for card validation
        if (cardNumber.length < 13 || cardNumber.length > 19) {
            return false;
        }
        
        let sum = 0;
        let isEven = false;
        
        for (let i = cardNumber.length - 1; i >= 0; i--) {
            let digit = parseInt(cardNumber.charAt(i));
            
            if (isEven) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            
            sum += digit;
            isEven = !isEven;
        }
        
        return (sum % 10) === 0;
    }

    function validateExpiry(expiry) {
        // Format: MM/YY
        const expiryRegex = /^(0[1-9]|1[0-2])\/\d{2}$/;
        
        if (!expiryRegex.test(expiry)) {
            return false;
        }
        
        const [month, year] = expiry.split('/');
        const currentDate = new Date();
        const currentYear = currentDate.getFullYear() % 100;
        const currentMonth = currentDate.getMonth() + 1;
        
        const expYear = parseInt(year);
        const expMonth = parseInt(month);
        
        if (expYear < currentYear || (expYear === currentYear && expMonth < currentMonth)) {
            return false;
        }
        
        return true;
    }

    function validateCVV(cvv) {
        return /^\d{3,4}$/.test(cvv);
    }

    function maskCardNumber(cardNumber) {
        // Mask all but last 4 digits
        return cardNumber.slice(0, -4).replace(/\d/g, '*') + cardNumber.slice(-4);
    }

    // ==================== UTILITY FUNCTIONS ====================
    function showLoading(show) {
        const allButtons = document.querySelectorAll('.method-form button');
        allButtons.forEach(btn => {
            btn.disabled = show;
            if (show) {
                btn.innerHTML = '<i class="bi bi-arrow-repeat spin"></i> Processing...';
            }
        });
    }

    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} notification-toast`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            animation: slideIn 0.3s ease-out;
        `;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }


    // ==================== AUTO-FORMAT CARD INPUTS ====================
    // Auto-format card number input
    document.querySelectorAll('input[placeholder*="XXXX-XXXX-XXXX-XXXX"]').forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = value.match(/.{1,4}/g)?.join('-') || value;
            e.target.value = formattedValue;
        });
    });

    // Auto-format expiry date
    document.querySelectorAll('input[placeholder*="MM/YY"]').forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2, 4);
            }
            e.target.value = value;
        });
    });

    // Restrict CVV to numbers only
    document.querySelectorAll('input[placeholder*="***"]').forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '').slice(0, 4);
        });
    });
});

// ==================== CSS ANIMATIONS ====================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .spin {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
`;
document.head.appendChild(style);
