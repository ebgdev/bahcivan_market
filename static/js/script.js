// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if




    
}); 
// jquery end


// Enhanced alert animations
$(document).ready(function() {
    // Check if there are any alerts
    if ($('.alert').length > 0) {
        // Initially hide messages
        $('.alert').hide();

        // Show alerts with slide down animation
        $('.alert').each(function(index) {
            $(this).delay(index * 200).slideDown('slow');
        });

        // Auto fade out after 4 seconds with slide up animation
        setTimeout(function(){
            $('.alert').slideUp('slow', function() {
                $(this).remove();
            });
        }, 4000);
    }

    // Handle manual close button
    $('.alert .close').click(function() {
        $(this).closest('.alert').slideUp('fast', function() {
            $(this).remove();
        });
    });
});

// Cart functionality improvements
$(document).ready(function() {
    // Add loading state for cart quantity buttons
    $('.input-group-prepend form, .input-group-append form').on('submit', function() {
        var $button = $(this).find('button');
        var originalHtml = $button.html();

        $button.prop('disabled', true).html('<i class="fa fa-spinner fa-spin"></i>');

        // Re-enable after 2 seconds (fallback)
        setTimeout(function() {
            $button.prop('disabled', false).html(originalHtml);
        }, 2000);
    });

    // Add loading state for delete buttons
    $('.delete-item-btn').on('click', function(e) {
        var $this = $(this);
        if (confirm('Bu ürünü silmek istediğinize emin misiniz?')) {
            $this.prop('disabled', true).html('<i class="fa fa-spinner fa-spin"></i> Siliniyor...');
            // Allow form submission
            return true;
        } else {
            e.preventDefault();
            return false;
        }
    });

    // Smooth scroll to top for better UX
    $('a[href="#top"]').click(function(e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: 0}, 300);
    });

    // Enhanced button hover effects
    $('.btn').hover(
        function() {
            if (!$(this).is(':disabled')) {
                $(this).addClass('shadow-sm');
            }
        },
        function() {
            $(this).removeClass('shadow-sm');
        }
    );

    // Quantity input protection (prevent manual editing)
    $('.input-group .form-control[readonly]').on('keydown paste', function(e) {
        e.preventDefault();
        return false;
    });
});