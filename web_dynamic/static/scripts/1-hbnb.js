$(document).ready( function() {
  const dictAmenities = {};

  $('div.amenities li input').change(
    function () {
      if ($(this).is(':checked')) {
        dictAmenities[($(this).attr('data-id'))] = $(this).attr('data-name');
      } else {
        delete dictAmenities[($(this).attr('data-id'))];
      }
      // If there is an amenity, join, otherwise ''.
      $('div.amenities h4').html(Object.values(dictAmenities).join(', ') || '&nbsp;');
    });
});
