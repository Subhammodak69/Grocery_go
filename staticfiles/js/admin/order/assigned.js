document.addEventListener('DOMContentLoaded', function() {
    // Function for Order assignment
    function handleOrderAssignment(selectElem) {
        const orderId = selectElem.getAttribute('data-order-id');
        const selectedDboyId = selectElem.value;

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({order_id: orderId, assigned_to: selectedDboyId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                window.location.reload();
            } else {
                console.log('error' , data.message);
                window.location.reload();
            }
        })
        .catch(error => {
            console.log('error',error.message);
            window.location.reload();
        });
    }

    // Function for Exchange assignment  
    function handleExchangeAssignment(selectElem) {
        const exchangeId = selectElem.getAttribute('data-exchange-id');
        const selectedDboyId = selectElem.value;

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({exchange_id: exchangeId, assigned_to: selectedDboyId})
        })
        .then(response => response.json())
        .then(data => {
            console.log(JSON.stringify(data));
            if (data.success){
                window.location.reload();
            } else {
                console.log('error' , data.message);
                window.location.reload();
            }
        })
        .catch(error => {
            console.log('error',error.message);
            window.location.reload();
        });
    }

    // Attach event listeners to all selects
    document.querySelectorAll('.assigned-to-select').forEach(function(selectElem) {
        // Check which type of select it is and attach appropriate handler
        if (selectElem.hasAttribute('data-order-id')) {
            selectElem.addEventListener('change', function() {
                handleOrderAssignment(this);
            });
        } else if (selectElem.hasAttribute('data-exchange-id')) {
            selectElem.addEventListener('change', function() {
                // console.log("called !");
                handleExchangeAssignment(this);
            });
        }
    });
});
