$(document).ready(function () {
  jQuery('.btn-delete').click(function () {
    jQuery('.id_to_remove').val(jQuery(this).attr('data-orderid'));
  });
});
