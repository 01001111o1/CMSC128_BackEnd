jQuery(document).ready(function () {
  // click on next button
  jQuery('.form-wizard-next-btn').click(function () {
    var parentFieldset = jQuery(this).parents('.wizard-fieldset');
    var currentActiveStep = jQuery(this)
      .parents('.form-wizard')
      .find('.form-wizard-steps .active');
    var next = jQuery(this);
    var nextWizardStep = true;
    parentFieldset.find('.wizard-required').each(function () {
      var thisValue = jQuery(this).val();
      var idName = jQuery(this).attr('id');
      if (idName == 'snum') {
        jQuery('#' + idName).val().length !== 9 ? (nextWizardStep = false) : '';
      } else if (idName == 'email') {
        !validateEmail(
          jQuery('#' + idName)
            .val()
            .trim()
        )
          ? (nextWizardStep = false)
          : '';
      }
      if (thisValue == '' || thisValue == null) {
        jQuery(this).siblings('.wizard-form-error').slideDown('300');
        nextWizardStep = false;
      } else {
        jQuery(this).siblings('.wizard-form-error').slideUp('300');
      }
    });
    jQuery('quiz_checkbox').click(function () {
      // total_price
      jQuery('#total_price').append('.00');
      console.log('clicked checkbox', 'Price: ', jQuery('#total_price').val());
    });
    // var temp_checked = jQuery('input.quiz_checkbox:checked');
    // var quiz_checked = parentFieldset.find(temp_checked).length;
    // if (quiz_checked <= 0) {
    //   nextWizardStep = false;
    //   alert('Please request at least one form/certificate.');
    // } else {
    //   nextWizardStep = true;
    // }
    if (nextWizardStep) {
      next.parents('.wizard-fieldset').removeClass('show', '400');
      currentActiveStep
        .removeClass('active')
        .addClass('activated')
        .next()
        .addClass('active', '400');
      next
        .parents('.wizard-fieldset')
        .next('.wizard-fieldset')
        .addClass('show', '400');
      jQuery(document)
        .find('.wizard-fieldset')
        .each(function () {
          if (jQuery(this).hasClass('show')) {
            var formAtrr = jQuery(this).attr('data-tab-content');
            jQuery(document)
              .find('.form-wizard-steps .form-wizard-step-item')
              .each(function () {
                if (jQuery(this).attr('data-attr') == formAtrr) {
                  jQuery(this).addClass('active');
                  var innerWidth = jQuery(this).innerWidth();
                  var position = jQuery(this).position();
                  jQuery(document)
                    .find('.form-wizard-step-move')
                    .css({ left: position.left, width: innerWidth });
                } else {
                  jQuery(this).removeClass('active');
                }
              });
          }
        });
    }

    // Function to show the image
    function showImage() {
      // Append the image to the body or any other desired location
      document.body.appendChild(imageElement);
    }

    // Add event listeners to the radio buttons
    onlinePaymentRadio.addEventListener('click', showImageOnClick);
    cashPaymentRadio.addEventListener('click', showImageOnClick);
  });
  //click on previous button
  jQuery('.form-wizard-previous-btn').click(function () {
    var counter = parseInt(jQuery('.wizard-counter').text());
    var prev = jQuery(this);
    var currentActiveStep = jQuery(this)
      .parents('.form-wizard')
      .find('.form-wizard-steps .active');
    prev.parents('.wizard-fieldset').removeClass('show', '400');
    prev
      .parents('.wizard-fieldset')
      .prev('.wizard-fieldset')
      .addClass('show', '400');
    currentActiveStep
      .removeClass('active')
      .prev()
      .removeClass('activated')
      .addClass('active', '400');
    jQuery(document)
      .find('.wizard-fieldset')
      .each(function () {
        if (jQuery(this).hasClass('show')) {
          var formAtrr = jQuery(this).attr('data-tab-content');
          jQuery(document)
            .find('.form-wizard-steps .form-wizard-step-item')
            .each(function () {
              if (jQuery(this).attr('data-attr') == formAtrr) {
                jQuery(this).addClass('active');
                var innerWidth = jQuery(this).innerWidth();
                var position = jQuery(this).position();
                jQuery(document)
                  .find('.form-wizard-step-move')
                  .css({ left: position.left, width: innerWidth });
              } else {
                jQuery(this).removeClass('active');
              }
            });
        }
      });
  });
  //click on form submit button
  jQuery(document).on('click', '.form-wizard .form-wizard-submit', function () {
    var parentFieldset = jQuery(this).parents('.wizard-fieldset');
    var currentActiveStep = jQuery(this)
      .parents('.form-wizard')
      .find('.form-wizard-steps .active');
    parentFieldset.find('.wizard-required').each(function () {
      var thisValue = jQuery(this).val();
      if (thisValue == '' || thisValue == null) {
        jQuery(this).siblings('.wizard-form-error').slideDown('300');
      } else {
        jQuery(this).siblings('.wizard-form-error').slideUp('300');
      }
    });
  });
  // focus on input field check empty or not
  jQuery('.form-control')
    .on('focus', function () {
      var tmpThis = jQuery(this).val();
      if (tmpThis == '' || tmpThis == null) {
        jQuery(this).parent().addClass('focus-input');
      } else if (tmpThis != '') {
        jQuery(this).parent().addClass('focus-input');
      }
    })
    .on('blur', function () {
      var tmpThis = jQuery(this).val();
      if (tmpThis == '' || tmpThis == null) {
        jQuery(this).parent().removeClass('focus-input');
        jQuery(this).siblings('.wizard-form-error').slideDown('3000');
      } else if (tmpThis != '') {
        jQuery(this).parent().addClass('focus-input');
        jQuery(this).siblings('.wizard-form-error').slideUp('3000');
      }
    });
});

function onKeyDown(evt) {
  if (['e', 'E', '+', '-', '.', '='].includes(evt.key)) {
    evt.preventDefault();
  }
}
function maxLengthCheck(object) {
  const requiredLength = 9;
  if (object.value.length > requiredLength) {
    object.value = object.value.slice(0, requiredLength);
  }

  if (object.value.length !== requiredLength) {
    object.classList.add('error'); // Add a CSS class to highlight the input
    const errorElement = document.querySelector('.wizard-form-error-msg');
    errorElement.innerText = `Input must be exactly ${requiredLength} characters long.`;
  } else {
    object.classList.remove('error'); // Remove the CSS class
    const errorElement = document.querySelector('.wizard-form-error-msg');
    errorElement.innerText = '';
  }
}

function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validateEmailInput() {
  const emailElement = document.getElementById('email');
  const emailErrorElement = emailElement.nextElementSibling;

  if (!validateEmail(emailElement.value.trim())) {
    emailElement.classList.add('error');
    emailErrorElement.innerText =
      emailElement.value.trim() === ''
        ? 'Email'
        : 'Email should contain at least "@" and "."';
  } else {
    emailElement.classList.remove('error');
    emailErrorElement.innerText = 'Email';
  }
}

function validateForm() {
  const emailElement = document.getElementById('email');
  const emailErrorElement = emailElement.nextElementSibling;

  if (!validateEmail(emailElement.value.trim())) {
    emailElement.classList.add('error');
    emailErrorElement.innerText =
      emailElement.value.trim() === ''
        ? 'Email'
        : 'Email should contain at least "@" and "."';
    return false;
  } else {
    emailElement.classList.remove('error');
    emailErrorElement.innerText = 'Email';
  }
  return true;
}

/* function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validateForm() {
  const emailElement = document.getElementById('email');
  const emailValue = emailElement.value.trim();

  if (!validateEmail(emailValue)) {
    emailElement.classList.add('error'); // Add a CSS class to highlight the input
    const errorElement = document.querySelector('.wizard-form-error-msg');
    errorElement.innerText = 'Please enter a valid email address.';
    return false; // Prevent form submission
  } else {
    emailElement.classList.remove('error'); // Remove the CSS class
    const errorElement = document.querySelector('.wizard-form-error-msg');
    errorElement.innerText = '';
    return true; // Allow form submission
  }
}
 */
// Get the total amount from the query parameters
/* const urlParams = new URLSearchParams(window.location.search);

const totalAmount = urlParams.get('total_amount');

const totalAmount = urlParams.get('total_amount');

// Update the amount payable in the HTML
const totalPriceElement = document.getElementById('total_price');
if (totalPriceElement) {
  totalPriceElement.textContent = totalAmount || '0.00';
}
 */

// ../imgs/icons/payment1.jpg

/* // Get the radio buttons
const onlinePaymentRadio = document.getElementById('online_paymode');
const cashPaymentRadio = document.getElementById('cash_paymode');

// Function to handle the click event
function showImageOnClick(event) {
  const imageContainer = document.getElementById('image_container');
  
  // Check which radio button was clicked
  if (event.target === onlinePaymentRadio) {
    // Show the image for online payment
    imageContainer.innerHTML = '<img src="../imgs/icons/payment1.jpg" alt="Online Payment" />';
  } else if (event.target === cashPaymentRadio) {
    // Show the image for cash payment
    imageContainer.innerHTML = '<img src="path/to/payment1.jpg" alt="Cash Payment" />';
  }
}

// Add event listeners to the radio buttons
onlinePaymentRadio.addEventListener('click', showImageOnClick);
cashPaymentRadio.addEventListener('click', showImageOnClick); */

/* $(document).ready(function() {
  // Event handler for radio button change
  $('input[name="payment_method"]').change(function() {
    var selectedPayment = $(this).attr('id');
    var imageToShow = '';

    if (selectedPayment === 'online_paymode') {
      imageToShow = '{{ url_for("static", filename="payment1.jpg") }}'; // Image for Online Payment
    } else if (selectedPayment === 'cash_paymode') {
      imageToShow = '{{ url_for("static", filename="imgs/icons/payment2.jpg") }}'; // Image for Cash Payment
    }

    // Update the image container with the new image
    $('#image_container').html('<img src="' + imageToShow + '">');
  });
}); */
$(document).ready(function () {
  // Event handler for radio button change
  $('input[name="payment_method"]').change(function () {
    var selectedPayment = $(this).attr('id');
    var imageToShow = '';

    if (selectedPayment === 'online_paymode') {
      imageToShow = 'static/imgs/icons/payment1.png'; // Image for Online Payment
    } else if (selectedPayment === 'cash_paymode') {
      imageToShow = 'static/imgs/icons/payment2.png'; // Image for Cash Payment
    }

    // Update the image container with the new image
    $('#image_container').html(
      '<img src="' + imageToShow + '" style="height: 3in; width: 5in;">'
    );
  });
});

// // Update the amount payable in the HTML
// const totalPriceElement = document.getElementById('total_price');
// if (totalPriceElement) {
//   totalPriceElement.textContent = totalAmount || '0.00';
// }

// // Get the price value
// var price = base_prices[list2[i]];

// // Update the span element with the price value
// document.getElementById('priceValue').textContent = price;
