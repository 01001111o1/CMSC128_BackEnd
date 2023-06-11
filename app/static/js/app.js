const base_values = {
  'Certificate of Enrollment': '50',
  'Certificate of No Disciplinary Action': '20',
  'True Copy of Grades': '50',
  'Certificate of Non-Issuance of ID': '50',
};

const honorable_dismissal_prices = {
  1: '220',
  2: '220',
  3: '290',
  4: '360',
  Alumni: '360',
  'Graduate Student': '430',
};

const course_description_prices = {
  1: '20',
  2: '40',
  3: '60',
  4: '80',
  Alumni: '80',
};

const otr_prices = {
  1: '70',
  2: '70',
  3: '140',
  4: '210',
  Alumni: '210',
  'Graduate Student': '280',
};

const course_description = document.querySelectorAll(
  'input[value= "Course Description"]'
);
const course_description_label = document.querySelectorAll(
  '[data-value="Course Description"]'
);

const honorable_dismissal = document.querySelectorAll(
  'input[value= "Honorable Dismissal"]'
);
const honorable_dismissal_label = document.querySelectorAll(
  '[data-value="Honorable Dismissal"]'
);

const otr = document.querySelectorAll(
  'input[value="Official Transcript of Records"]'
);
const otr_label = document.querySelectorAll(
  '[data-value="Official Transcript of Records"]'
);

const year_level = document.getElementById('YearLevel');
const final_price = document.querySelectorAll('[id=total_price]');
const is_scholarship = document.getElementById('scholarship_toggle');
const is_scholarship_label = document.getElementById(
  'scholarship_toggle_label'
);
const hidden = document.getElementById('hidden');

let updatePrice_scholarship = () => {
  const discounted_documents = document.getElementsByClassName('scholarship');
  const discounted_documents_label =
    document.getElementsByClassName('scholarship_label');
  if (is_scholarship.checked) {
    honorable_dismissal[0].checked = false;
    honorable_dismissal[0].disabled = true;
    jQuery(function () {
      jQuery('[data-value="Honorable Dismissal"]')
        .parent()
        .contents()
        .filter(function () {
          return this.nodeType === Node.TEXT_NODE;
        })
        .remove();
    });
    honorable_dismissal_label[0].innerText = 'Unavailable for Scholarship';
    for (let i = 0; i < discounted_documents.length; i++) {
      discounted_documents[i].dataset.price = '0';
      discounted_documents_label[i].innerText = '0';
    }
  } else {
    honorable_dismissal[0].disabled = false;
    honorable_dismissal_label[0].insertAdjacentText('beforebegin', 'PHP ');
    honorable_dismissal_label[0].innerText =
      honorable_dismissal_prices[year_level.value];
    honorable_dismissal_label[0].insertAdjacentText('afterend', '.00');
    for (let i = 0; i < discounted_documents.length; i++) {
      discounted_documents[i].dataset.price =
        base_values[discounted_documents[i].value];
      discounted_documents_label[i].innerText =
        base_values[discounted_documents[i].value];
    }
  }
  updatePrice();
};

let updatePrice_Yearlevel = () => {
  if (!honorable_dismissal[0].disabled) {
    honorable_dismissal[0].dataset.price =
      honorable_dismissal_prices[event.target.value];
    honorable_dismissal_label[0].innerText =
      honorable_dismissal_prices[event.target.value];
  }
  if (event.target.value == 'Graduate Student') {
    course_description[0].disabled = true;
    course_description[0].checked = false;
    jQuery(function () {
      jQuery('[data-value="Course Description"]')
        .parent()
        .contents()
        .filter(function () {
          return this.nodeType === Node.TEXT_NODE;
        })
        .remove();
    });
    course_description_label[0].innerText =
      'Cannot Apply As A Graduate Student';

    otr[0].dataset.price = otr_prices[event.target.value];
    otr_label[0].innerText = otr_prices[event.target.value];
  } else {
    course_description[0].disabled = false;
    course_description[0].dataset.price =
      course_description_prices[event.target.value];
    jQuery(function () {
      text_length = jQuery('[data-value="Course Description"]')
        .parent()
        .text().length;
      if (text_length <= 2) {
        course_description_label[0].insertAdjacentText('beforebegin', 'PHP ');
        course_description_label[0].insertAdjacentText('afterend', '.00');
      }
    });
    course_description_label[0].innerText =
      course_description_prices[event.target.value];

    otr[0].dataset.price = otr_prices[event.target.value];
    otr_label[0].innerText = otr_prices[event.target.value];
  }
  updatePrice();
};
let updatePrice = () => {
  let price = 0.0;
  const map = new Map();
  const checkboxes = document.getElementsByName('check');
  for (let i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      price += parseInt(checkboxes[i].dataset.price);
      map.set(checkboxes[i].value, checkboxes[i].dataset.price);
    }
  }
  const json = JSON.stringify(Object.fromEntries(map));
  hidden.value = json;
  final_price.forEach((tp) => {
    tp.innerText = price;
  });
};

if (honorable_dismissal[0]) {
  honorable_dismissal[0].addEventListener('click', (event) => {
    if (event.target.checked) {
      is_scholarship.checked = false;
      is_scholarship.disabled = true;
      is_scholarship_label.innerText =
        'Cannot Apply For This With Honorary Dimissal';
    } else {
      is_scholarship.disabled = false;
      is_scholarship_label.innerText = '';
    }
  });
}

document.querySelectorAll('.nav-link').forEach((link) => {
  console.log(link.href);
  if (link.href === window.location.href) {
    link.classList.add('active');
    link.setAttribute('aria-current', 'page');
  }
});

const deleteButtons = document.querySelectorAll('.btn-delete');
const modal = document.querySelector('#modal');

deleteButtons.forEach((deleteButton) => {
  deleteButton.addEventListener('click', function () {
    const orderID = this.getAttribute('data-orderid');
    const name = this.getAttribute('data-name');
    const studentNumber = this.getAttribute('data-studentnumber');

    document.querySelector('#modal-orderid').textContent = orderID;
    document.querySelector('#modal-name').textContent = name;
    document.querySelector('#modal-studentnumber').textContent = studentNumber;
  });
});
/* document.addEventListener('DOMContentLoaded', function() {
    var toastElements = document.querySelectorAll('.toast');

    toastElements.forEach(function(toastEl) {
      var toast = new bootstrap.Toast(toastEl);
      toast.show();

      var closeButton = toastEl.querySelector('.btn-close');
      closeButton.addEventListener('click', function() {
        toast.hide();
      });

      var autohideAttr = toastEl.getAttribute('data-bs-autohide');
      if (autohideAttr === 'true') {
        var autohideDelay = parseInt(toastEl.getAttribute('data-bs-delay')) || 5000;
        setTimeout(function() {
          toast.hide();
        }, autohideDelay);
      }
    });
}} */

// faqs
function expandAll() {
  $('.accordion-collapse').addClass('show');
  $('.accordion-button').addClass('show');
  $('.accordion-button').attr('aria-expanded', 'true');
  $('.accordion-button').removeClass('collapsed');
}

function collapseAll() {
  $('.accordion-collapse').removeClass('show');
  $('.accordion-button').removeClass('show');
  $('.accordion-button').attr('aria-expanded', 'false');
  $('.accordion-button').addClass('collapsed');
}
