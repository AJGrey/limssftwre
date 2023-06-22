(function($) {

	var $window = $(window),
	  $body = $('body');
	
	// Breakpoints.
	breakpoints({
	  default: ['1681px', null],
	  xlarge: ['1281px', '1680px'],
	  large: ['981px', '1280px'],
	  medium: ['737px', '980px'],
	  small: ['481px', '736px'],
	  xsmall: ['361px', '480px'],
	  xxsmall: [null, '360px']
	});
	
	// Play initial animations on page load.
	$window.on('load', function() {
	  window.setTimeout(function() {
		$body.removeClass('is-preload');
	  }, 100);
	});
	
	// Hack: Enable IE workarounds.
	if (browser.name == 'ie')
	  $body.addClass('is-ie');
	
	// Mobile?
	if (browser.mobile)
	  $body.addClass('is-mobile');
	
	// Scrolly.
	$('.scrolly')
	  .scrolly({
		offset: 100
	  });
	
	// Polyfill: Object fit.
	if (!browser.canUse('object-fit')) {
	
	  $('.image[data-position]').each(function() {
	
		var $this = $(this),
		  $img = $this.children('img');
	
		// Apply img as background.
		$this
		  .css('background-image', 'url("' + $img.attr('src') + '")')
		  .css('background-position', $this.data('position'))
		  .css('background-size', 'cover')
		  .css('background-repeat', 'no-repeat');
	
		// Hide img.
		$img
		  .css('opacity', '0');
	
	  });
	
	  $('.gallery > a').each(function() {
	
		var $this = $(this),
		  $img = $this.children('img');
	
		// Apply img as background.
		$this
		  .css('background-image', 'url("' + $img.attr('src') + '")')
		  .css('background-position', 'center')
		  .css('background-size', 'cover')
		  .css('background-repeat', 'no-repeat');
	
		// Hide img.
		$img
		  .css('opacity', '0');
	
	  });
	
	}
	
	// Flash message function.
	function flashMessage(message) {
	  // Create the flash message element.
	  var flashMessage = $('<div>').addClass('flash-message').text(message);
	
	  // Append the flash message to the body.
	  $body.prepend(flashMessage);
	
	  // Scroll to the top of the screen.
	  $('html, body').animate({
		scrollTop: 0
	  }, 'slow');
	
	  // Remove the flash message after 3 seconds.
	  setTimeout(function() {
		flashMessage.fadeOut('slow', function() {
		  $(this).remove();
		});
	  }, 3000);
	}
	
	// Handle make enquiry button click event.
	$('#enquiry-btn').on('click', function() {
	  // Display the flash message.
	  flashMessage('Message Submitted');
	});
	
  })(jQuery);
  