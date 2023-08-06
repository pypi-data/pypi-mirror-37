$(function() {
    // Open FAQ Block when location hash is set
    if (window.location.hash)
      jQuery('.ftw-faqblock-faqblock > ' + window.location.hash + ' + div .faqblock > input[type=checkbox]').attr('checked', true)
});
