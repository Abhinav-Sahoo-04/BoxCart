document.addEventListener("DOMContentLoaded", function () {

  const paypalButtons = window.paypal.Buttons({

    style: {
      shape: "rect",
      layout: "vertical",
      color: "blue",
      label: "paypal",
    },

    createOrder: function (data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: "10.00"
          }
        }]
      });
    },

    onApprove: function (data, actions) {
      return actions.order.capture().then(function (details) {
        alert("Transaction completed by " + details.payer.name.given_name);
      });
    },

    onError: function (err) {
      console.error(err);
    }

  });

  paypalButtons.render("#paypal-button-container");

});








