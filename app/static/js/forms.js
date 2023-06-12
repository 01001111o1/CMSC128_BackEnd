let summaryDetails = { scholarship_toggle: false };

jQuery(document).ready(function () {
  // Event handler for radio button change
  jQuery('input[name="payment_method"]').change(function () {
    var selectedPayment = jQuery(this).attr('id');
    var imageToShow = '';

    if (selectedPayment === 'online_paymode') {
      imageToShow = 'static/imgs/icons/payment1.png'; // Image for Online Payment
    } else if (selectedPayment === 'cash_paymode') {
      imageToShow = 'static/imgs/icons/payment2.png'; // Image for Cash Payment
    }

    // Update the image container with the new image
    jQuery('#img_source').removeAttr('hidden');
    jQuery('#img_source').attr('src', imageToShow);
  });
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
    // checks if atleast 1 form is checked
    var forms_section = parentFieldset.find('input[name="check"]').length !== 0;
    var atLeastOneIsChecked =
      parentFieldset.find('input[name="check"]:checked').length > 0;

    if (!atLeastOneIsChecked && forms_section) {
      nextWizardStep = false;
    }

    // checks if they chose a payment method
    var payment_section =
      parentFieldset.find('input[name="payment_method"]').length !== 0;
    atLeastOneIsChecked =
      parentFieldset.find('input[name="payment_method"]:checked').length > 0;

    if (!atLeastOneIsChecked && payment_section) {
      nextWizardStep = false;
    } else {
      for (const key of Object.keys(summaryDetails)) {
        jQuery('.summary-details').append(
          '<p>' + key + ':' + summaryDetails[key] + '</p>'
        );
      }
    }

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
      summaryDetails[jQuery(this).attr('id')] = tmpThis;
      if (tmpThis == '' || tmpThis == null) {
        jQuery(this).parent().removeClass('focus-input');
        jQuery(this).siblings('.wizard-form-error').slideDown('3000');
      } else if (tmpThis != '') {
        jQuery(this).parent().addClass('focus-input');
        jQuery(this).siblings('.wizard-form-error').slideUp('3000');
      }
    });
  // checks if scholarship is on or off
  jQuery('.scholarship-checkbox').click(function () {
    var tmpThis = jQuery('#scholarship_toggle').is(':checked');
    summaryDetails[jQuery(this).attr('id')] = tmpThis;
  });
  // checks the payment method
  jQuery('.payment-radio').click(function () {
    var tmpThis = jQuery(this).val();
    summaryDetails[jQuery(this).attr('name')] = tmpThis;
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
